# Real-Time Bad Posture Detection System



A lightweight, real-time posture monitoring system that helps prevent neck strain, back pain, and spinal misalignment caused by prolonged computer usage. Using computer vision and pose estimation, this system provides immediate feedback when poor posture is detected.

![Demo](demo.gif)

## 🌟 Features

- **Real-time Posture Monitoring**: Continuous analysis of sitting posture using webcam
- **Non-intrusive Detection**: No wearable devices or special hardware required
- **Immediate Feedback**: Desktop notifications and audio alerts for poor posture
- **Configurable Thresholds**: Customizable sensitivity and alert timing
- **Cross-platform Support**: Works on Windows, macOS, and Linux
- **Lightweight**: Minimal system resource usage
- **Privacy-focused**: All processing done locally, no data transmission

## 🎯 Health Benefits

- Reduces neck strain and cervical spine issues
- Prevents chronic back pain from slouching
- Improves spinal alignment awareness
- Encourages healthy work habits
- Promotes ergonomic consciousness

## 🛠️ Technology Stack

- **Computer Vision**: OpenCV for video processing
- **Pose Estimation**: MediaPipe for body landmark detection
- **Notifications**: Cross-platform desktop alerts
- **Audio Alerts**: Sound cues for immediate attention


## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Webcam (built-in or external)
- Minimum 4GB RAM
- Windows 10/macOS 10.14/Ubuntu 18.04 or later

### Python Dependencies
```
opencv-python>=4.5.0
mediapipe>=0.8.0
numpy>=1.21.0
plyer>=2.0.0
pygame>=2.0.0
```

## 🚀 Installation

### Option 1: Clone Repository
```bash
git clone https://github.com/yourusername/posture-detection-system.git
cd posture-detection-system
pip install -r requirements.txt
```

### Option 2: Direct Download
1. Download the latest release from [Releases](https://github.com/yourusername/posture-detection-system/releases)
2. Extract the archive
3. Install dependencies: `pip install -r requirements.txt`

## 🎮 Usage

### Quick Start
```bash
python main.py
```



## 📊 How It Works

1. **Pose Detection**: MediaPipe identifies key body landmarks
2. **Angle Calculation**: Computes neck, shoulder, and spine angles
3. **Posture Analysis**: Compares angles against healthy posture thresholds
4. **Alert System**: Triggers notifications when poor posture is sustained
5. **Feedback Loop**: Provides real-time visual and audio feedback

### Key Measurements
- **Neck Angle**: Forward head posture detection
- **Shoulder Alignment**: Slouching and uneven shoulder detection  
- **Spine Curvature**: Overall posture quality assessment

## 🎨 Screenshots

| Main Interface | Alert Notification | Posture Visualization |
|:--------------:|:-----------------:|:--------------------:|
| ![Interface](screenshots/interface.png) | ![Alert](screenshots/alert.png) | ![Visualization](screenshots/visualization.png) |



## 🤝 Contributing

We welcome contributions! 
### Development Setup
```bash
git clone https://github.com/yourusername/posture-detection-system.git
cd posture-detection-system
pip install -r requirements-dev.txt
pre-commit install
```



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



**⭐ If this project helped improve your posture and health, please give it a star!**

*Built with ❤️ for healthier computing habits*
