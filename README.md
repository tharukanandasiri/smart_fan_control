# Smart Fan Control Using Image Processing

> Academic project: Contactless fan control using hand gestures, computer vision, and Arduino-based motor control.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Hardware Requirements](#hardware-requirements)
5. [Software Requirements](#software-requirements)
6. [Installation & Setup](#installation--setup)
7. [Usage](#usage)
8. [Gesture Mapping](#gesture-mapping)
9. [Wiring & Pinout](#wiring--pinout)
10. [Repository Structure](#repository-structure)
11. [Testing & Calibration](#testing--calibration)
12. [Limitations & Future Work](#limitations--future-work)
13. [Acknowledgements & Contact](#acknowledgements--contact)
14. [References](#references)

---

## Overview

This project enables contactless control of a DC fan using hand gestures detected via a webcam. The system uses computer vision (OpenCV + MediaPipe) to interpret hand poses and sends commands to an Arduino, which controls the fan speed using PWM. The project is intended for academic demonstration and is not licensed for commercial use.

---

## Features

- Real-time hand gesture recognition using webcam
- Three fan speed levels and ON/OFF control
- Visual feedback of detected gesture and fan state
- Modular Python code for gesture detection and hardware control

---

## System Architecture

1. **Webcam Capture**: OpenCV captures video frames from the user's camera.
2. **Hand Detection**: MediaPipe detects hands and extracts finger landmarks.
3. **Gesture Interpretation**: The number of extended fingers is mapped to a control action (OFF, ON, Speed 1/2/3).
4. **Arduino Interface**: PyFirmata sends PWM values to the Arduino (pin D10) to control the fan speed.
5. **Motor Driver**: Arduino drives the motor driver to set the DC fan speed.

---

## Hardware Requirements

- Arduino Uno (or compatible)
- DC Motor (fan)
- Motor driver (e.g., L298N) supporting PWM
- Laptop/PC with webcam
- Jumper wires, external power supply for the motor

---

## Software Requirements

- OS: Windows / macOS / Linux
- Python 3.8+
- Arduino IDE (to upload Firmata)
- Python packages:
  - opencv-python
  - mediapipe
  - pyfirmata
  - numpy

Install dependencies:

```bash
pip install opencv-python mediapipe pyfirmata numpy
```

Upload the **StandardFirmata** sketch to your Arduino using the Arduino IDE.

---

## Installation & Setup

1. **Prepare Arduino**
   - Upload `StandardFirmata` to your Arduino Uno.
   - Connect Arduino to your computer and note the serial port (e.g., `COM3`).
2. **Python Environment**
   - Create and activate a virtual environment (optional but recommended).
   - Install required packages.
3. **Run the App**
   - Place camera and fan in desired positions.
   - Run:
     ```bash
     python main.py
     ```
   - The serial port is set in `controller.py` (`COM3` by default). Change it if needed.

---

## Usage

- On launch, the program opens a webcam window and starts detecting hands.
- The number of fingers detected determines the fan state:
  - 0 fingers: OFF
  - 1, 2, or 3 fingers: Speed 1, 2, or 3
  - 5 fingers: ON (restores last speed)
- The current gesture and fan speed are displayed on-screen.
- Press 'q' to exit the application.

---

## Gesture Mapping

- **0 fingers (fist)**: Fan OFF
- **1 finger**: Speed 1 (Low, ~30% PWM)
- **2 fingers**: Speed 2 (Medium, ~60% PWM)
- **3 fingers**: Speed 3 (High, ~100% PWM)
- **5 fingers (open palm)**: ON (restores last speed)

---

## Wiring & Pinout

- Arduino D10 (PWM) → Motor driver PWM input
- Motor driver outputs → DC motor terminals
- Motor driver powered by external supply
- Common ground between Arduino and motor driver

---

## Repository Structure

```
├── README.md
├── main.py              # Main application (OpenCV + MediaPipe + PyFirmata)
├── controller.py        # Fan control logic
├── pyvenv.cfg           # Python virtual environment config
├── Scripts/             # Python venv scripts
├── __pycache__/         # Python cache
└── share/               # Documentation/man pages
```

---

## Testing & Calibration

- Test under different lighting conditions.
- Calibrate hand position and distance for reliable detection.
- Adjust speed thresholds in `controller.py` if needed.

---

## Limitations & Future Work

**Limitations**

- Performance may degrade in poor lighting.
- Single-hand gestures only.
- Motor driver and motor selection may limit power.

**Future Improvements**

- Multi-hand gesture support.
- Integration with smart home systems.
- Improved robustness for varied environments.
- Add voice control.

---

## Acknowledgements & Contact

Developed for CCS3360 - Technology Challenge Competition 2.

Group members:

- W. M. H. E. K. Wickramasinghe — 22UG1-0789
- T. D. Nandasiri — 22UG1-0788
- D. M. S. B. Dissanayake — 22UG1-0783
- W. M. T. R. Wijekoon — 22UG1-0844
- P. M. V. M. Didulani — 22UG1-0487

Contact: [tharukanandasiri123@gmail.com](mailto:tharukanandasiri123@gmail.com) ·

---

## References

- Arduino Documentation: https://www.arduino.cc/en/guide
- MediaPipe: https://google.github.io/mediapipe/
- OpenCV: https://opencv.org/
- PyFirmata: https://github.com/tino/pyFirmata
