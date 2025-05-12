import cv2
import mediapipe as mp
import numpy as np
import time
import os
import pygame  # For sound playback

# Initialize MediaPipe Pose and webcam
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Feature Flag Configuration
class FeatureFlags:
    def __init__(self):
        # Core features
        self.enable_pose_detection = True
        self.enable_calibration = True
        
        # Visual feedback features
        self.show_skeleton = True
        self.show_angles = True
        self.show_posture_status = True
        
        # Alert features
        self.enable_sound_alerts = True
        self.enable_visual_alerts = True
        
        # Advanced features
        self.mirror_view = True
        self.record_session = False
        self.display_stats = True
        
        # Alert configuration
        self.alert_cooldown = 3  # seconds
        self.sound_file = "alert.mp3"  # Change to your sound file path

# Create feature flags instance
flags = FeatureFlags()

# Initialize pygame for sound playback if enabled
if flags.enable_sound_alerts:
    pygame.mixer.init()
    if os.path.exists(flags.sound_file):
        alert_sound = pygame.mixer.Sound(flags.sound_file)
    else:
        print(f"Warning: Sound file '{flags.sound_file}' not found. Sound alerts disabled.")
        flags.enable_sound_alerts = False

# Initialize variables
is_calibrated = False
calibration_frames = 0
calibration_shoulder_angles = []
calibration_neck_angles = []
shoulder_threshold = None
neck_threshold = None
last_alert_time = time.time()
stats = {"good_posture_time": 0, "poor_posture_time": 0, "last_check": time.time()}
session_start_time = time.time()

def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    # Calculate angle
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def draw_angle(frame, p1, p2, p3, angle, color):
    """Draw the angle on the frame."""
    if flags.show_angles:
        cv2.putText(frame, str(int(angle)), 
                    (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

def format_time(seconds):
    """Format seconds into minutes and seconds."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize video recording if enabled
if flags.record_session:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('posture_session.avi', fourcc, 20.0, 
                         (int(cap.get(3)), int(cap.get(4))))

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Apply mirror view if enabled
        if flags.mirror_view:
            frame = cv2.flip(frame, 1)

        if flags.enable_pose_detection:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Extract key landmarks
                left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * frame.shape[1]),
                                int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * frame.shape[0]))
                right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame.shape[1]),
                                int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame.shape[0]))
                left_ear = (int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x * frame.shape[1]),
                            int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y * frame.shape[0]))
                right_ear = (int(landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x * frame.shape[1]),
                            int(landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y * frame.shape[0]))

                # Calculate angles
                shoulder_angle = calculate_angle(left_shoulder, right_shoulder, (right_shoulder[0], 0))
                neck_angle = calculate_angle(left_ear, left_shoulder, (left_shoulder[0], 0))

                # Handle calibration if enabled
                if flags.enable_calibration and not is_calibrated and calibration_frames < 30:
                    calibration_shoulder_angles.append(shoulder_angle)
                    calibration_neck_angles.append(neck_angle)
                    calibration_frames += 1
                    cv2.putText(frame, f"Calibrating... {calibration_frames}/30", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                elif flags.enable_calibration and not is_calibrated:
                    shoulder_threshold = np.mean(calibration_shoulder_angles) - 10
                    neck_threshold = np.mean(calibration_neck_angles) - 10
                    is_calibrated = True
                    print(f"Calibration complete. Shoulder threshold: {shoulder_threshold:.1f}, Neck threshold: {neck_threshold:.1f}")

                # Draw skeleton if enabled
                if flags.show_skeleton:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                # Draw angles if enabled
                midpoint = ((left_shoulder[0] + right_shoulder[0]) // 2, (left_shoulder[1] + right_shoulder[1]) // 2)
                draw_angle(frame, left_shoulder, midpoint, (midpoint[0], 0), shoulder_angle, (255, 0, 0))
                draw_angle(frame, left_ear, left_shoulder, (left_shoulder[0], 0), neck_angle, (0, 255, 0))

                # Provide feedback if calibrated
                if is_calibrated:
                    current_time = time.time()
                    
                    # Update stats
                    time_since_last_check = current_time - stats["last_check"]
                    stats["last_check"] = current_time
                    
                    if shoulder_angle < shoulder_threshold or neck_angle < neck_threshold:
                        status = "Poor Posture"
                        color = (0, 0, 255)  # Red
                        stats["poor_posture_time"] += time_since_last_check
                        
                        # Trigger alerts if cooldown has passed
                        if current_time - last_alert_time > flags.alert_cooldown:
                            print("Poor posture detected! Please sit up straight.")
                            
                            # Sound alert
                            if flags.enable_sound_alerts:
                                try:
                                    alert_sound.play()
                                except:
                                    pass
                                
                            # Visual alert (flashing border)
                            if flags.enable_visual_alerts:
                                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 10)
                                
                            last_alert_time = current_time
                    else:
                        status = "Good Posture"
                        color = (0, 255, 0)  # Green
                        stats["good_posture_time"] += time_since_last_check

                    # Display posture status if enabled
                    if flags.show_posture_status:
                        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                        cv2.putText(frame, f"Shoulder Angle: {shoulder_angle:.1f}/{shoulder_threshold:.1f}", (10, 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.putText(frame, f"Neck Angle: {neck_angle:.1f}/{neck_threshold:.1f}", (10, 90), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Display statistics if enabled
        if flags.display_stats and is_calibrated:
            total_session_time = time.time() - session_start_time
            cv2.putText(frame, f"Session: {format_time(total_session_time)}", (frame.shape[1] - 200, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Good posture: {format_time(stats['good_posture_time'])}", (frame.shape[1] - 200, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Poor posture: {format_time(stats['poor_posture_time'])}", (frame.shape[1] - 200, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
        
        # Record frame if enabled
        if flags.record_session:
            out.write(frame)
            
        # Display the frame
        cv2.imshow('Posture Corrector', frame)
        
        # Check for keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break
        elif key == ord('s'):  # Toggle sound alerts
            flags.enable_sound_alerts = not flags.enable_sound_alerts
            print(f"Sound alerts: {'ON' if flags.enable_sound_alerts else 'OFF'}")
        elif key == ord('v'):  # Toggle visual alerts
            flags.enable_visual_alerts = not flags.enable_visual_alerts
            print(f"Visual alerts: {'ON' if flags.enable_visual_alerts else 'OFF'}")
        elif key == ord('k'):  # Toggle skeleton
            flags.show_skeleton = not flags.show_skeleton
            print(f"Skeleton: {'ON' if flags.show_skeleton else 'OFF'}")
        elif key == ord('a'):  # Toggle angle display
            flags.show_angles = not flags.show_angles
            print(f"Angle display: {'ON' if flags.show_angles else 'OFF'}")
        elif key == ord('m'):  # Toggle mirror view
            flags.mirror_view = not flags.mirror_view
            print(f"Mirror view: {'ON' if flags.mirror_view else 'OFF'}")
        elif key == ord('d'):  # Toggle stats display
            flags.display_stats = not flags.display_stats
            print(f"Stats display: {'ON' if flags.display_stats else 'OFF'}")
        elif key == ord('r'):  # Start/stop recording
            if not flags.record_session:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('posture_session.avi', fourcc, 20.0, 
                                    (int(cap.get(3)), int(cap.get(4))))
                flags.record_session = True
                print("Recording started")
            else:
                flags.record_session = False
                out.release()
                print("Recording stopped and saved")

# Clean up
if flags.record_session:
    out.release()
cap.release()
cv2.destroyAllWindows()

if flags.enable_sound_alerts:
    pygame.mixer.quit()

# Print session summary
print("\n=== Session Summary ===")
print(f"Total session time: {format_time(time.time() - session_start_time)}")
print(f"Time with good posture: {format_time(stats['good_posture_time'])}")
print(f"Time with poor posture: {format_time(stats['poor_posture_time'])}")
if stats['good_posture_time'] + stats['poor_posture_time'] > 0:
    good_percentage = (stats['good_posture_time'] / (stats['good_posture_time'] + stats['poor_posture_time'])) * 100
    print(f"Good posture percentage: {good_percentage:.1f}%")