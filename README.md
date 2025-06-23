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
- **GUI**: Simple interface for configuration

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

### Configuration Options
```bash
# Run with custom settings
python main.py --threshold 15 --alert-delay 30 --sensitivity medium

# Show help
python main.py --help
```

### Command Line Arguments
- `--threshold`: Posture angle threshold (degrees, default: 20)
- `--alert-delay`: Time before alert triggers (seconds, default: 10)
- `--sensitivity`: Detection sensitivity (low/medium/high, default: medium)
- `--sound`: Enable/disable sound alerts (default: enabled)
- `--notifications`: Enable/disable desktop notifications (default: enabled)

## ⚙️ Configuration

Edit `config.json` to customize settings:

```json
{
  "posture_threshold": 20,
  "alert_delay_seconds": 10,
  "sensitivity": "medium",
  "enable_sound": true,
  "enable_notifications": true,
  "webcam_index": 0,
  "detection_frequency": 30
}
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

## 🔧 Troubleshooting

### Common Issues

**Webcam not detected:**
```bash
# Check available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).read()[0]])"
```

**Poor detection accuracy:**
- Ensure good lighting conditions
- Position camera at eye level
- Maintain 2-3 feet distance from camera
- Avoid cluttered backgrounds

**High CPU usage:**
- Reduce detection frequency in config
- Lower webcam resolution
- Close unnecessary applications

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/posture-detection-system.git
cd posture-detection-system
pip install -r requirements-dev.txt
pre-commit install
```

### Running Tests
```bash
pytest tests/
python -m coverage run -m pytest
python -m coverage report
```

## 📈 Roadmap

- [ ] Machine learning model improvements
- [ ] Mobile app companion
- [ ] Exercise recommendations
- [ ] Posture history tracking
- [ ] Team/office dashboard
- [ ] Integration with fitness trackers
- [ ] Custom alert sounds
- [ ] Multiple user profiles

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for pose estimation technology
- [OpenCV](https://opencv.org/) for computer vision capabilities
- Healthcare professionals who provided posture guidelines
- Beta testers and contributors

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/posture-detection-system/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/posture-detection-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/posture-detection-system/discussions)
- **Email**: support@posturedetection.com

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/posture-detection-system?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/posture-detection-system?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/posture-detection-system)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/posture-detection-system)

---

**⭐ If this project helped improve your posture and health, please give it a star!**

*Built with ❤️ for healthier computing habits*
