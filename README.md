# Smart Fan Control Using Image Processing

> Contactless fan control using hand gestures — a smart, hygienic way to operate household fans using computer vision and Arduino-based motor control.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Hardware Requirements](#hardware-requirements)
4. [Software Requirements](#software-requirements)
5. [System Architecture](#system-architecture)
6. [Installation & Quick Start](#installation--quick-start)
7. [Usage](#usage)
8. [Gesture Mapping (Suggested)](#gesture-mapping-suggested)
9. [Wiring / Pinout (Suggested)](#wiring--pinout-suggested)
10. [Repository Structure](#repository-structure)
11. [Testing & Calibration](#testing--calibration)
12. [Limitations & Future Work](#limitations--future-work)
13. [Acknowledgements & Contact](#acknowledgements--contact)
14. [License](#license)

---

## Project Overview

This project implements a contactless fan control system that uses a laptop webcam for hand gesture recognition and an Arduino + motor driver to control a DC fan’s power and speed. The aim is to improve convenience and hygiene by removing the need for physical switches or remotes. The system uses **MediaPipe** and **OpenCV** for hand detection and **PyFirmata** to interface with the Arduino motor driver.&#x20;

---

## Key Features

* Real-time hand gesture detection using webcam.
* Multiple fan speed levels controlled by mapped gestures.
* Arduino + L298N motor driver for PWM-based speed control.
* Configurable gesture-to-speed mapping.
* Designed to integrate into a smart home environment.&#x20;

---

## Hardware Requirements

* Arduino Uno (or compatible microcontroller)
* L298N motor driver (or compatible motor driver supporting PWM)
* DC Motor (fan) suitable for L298N and Arduino power/current constraints
* Laptop or PC with an integrated or external webcam
* Jumper wires, external power supply for the motor (recommended)
* (Optional) Breadboard, connectors, and mounting hardware.&#x20;

---

## Software Requirements

* OS: Windows / macOS / Linux
* Python 3.8+
* Arduino IDE (to flash Firmata if using PyFirmata)
* Python packages (recommended):

```bash
pip install opencv-python mediapipe pyfirmata numpy argparse
```

* (Optional) `pyserial` if directly communicating with Arduino via serial.
* Upload **StandardFirmata** (or custom Firmata) sketch to the Arduino when using PyFirmata (instructions below).&#x20;

---

## System Architecture

1. **Webcam Capture (Laptop)**

   * Capture video frames with OpenCV.
2. **Hand Detection & Landmark Extraction**

   * Use MediaPipe to detect hands and extract finger landmarks.
3. **Gesture Interpretation**

   * Convert landmark positions into a gesture label or numeric control signal (speed level).
4. **Arduino Interface (PyFirmata / Serial)**

   * Send PWM values or speed commands to Arduino.
5. **Motor Driver (L298N)**

   * Arduino drives L298N inputs (and enable/PWM) to control the DC motor (fan).&#x20;

---

## Installation & Quick Start

### 1. Prepare Arduino

* Open Arduino IDE → Examples → Firmata → `StandardFirmata` → upload to your Arduino Uno.
* Connect Arduino to your computer and note the serial port (e.g., `COM3` on Windows, `/dev/ttyACM0` on Linux).

### 2. Python environment

```bash
# create virtual environment (recommended)
python -m venv venv
# activate it (windows)
venv\Scripts\activate
# or (mac/linux)
source venv/bin/activate

# install dependencies
pip install opencv-python mediapipe pyfirmata numpy argparse
```

### 3. Run the app

Place camera and fan in desired positions, then run:

```bash
python gesture_fan_control.py --port COM3
# or on Linux:
python gesture_fan_control.py --port /dev/ttyACM0
```

(Replace `COM3` / `/dev/ttyACM0` with your actual Arduino port.)

---

## Usage

* On launch the program opens a webcam window and starts detecting hands.
* The current detected gesture and corresponding fan speed are shown on-screen.
* The mapped PWM value is sent to the Arduino to set motor speed.
* Use the on-screen instructions (or console output) to calibrate thresholds as needed.

---

## Gesture Mapping (Suggested)

The project documents gesture → speed mapping conceptually; below is a suggested, configurable mapping you can implement in `gesture_fan_control.py`:

* **Fist (no fingers open)** → Fan **OFF** (0% PWM)
* **One finger (index)** → **Low** speed (\~30% PWM)
* **Two fingers (index + middle)** → **Medium** speed (\~60% PWM)
* **Open palm (all fingers extended)** → **High** speed (\~100% PWM)

> Note: These mappings are suggested defaults — make them configurable via a JSON / YAML settings file or CLI flags for easier experimentation.

---

## Wiring / Pinout (Suggested)

**Example wiring when using Arduino Uno + L298N** (adjust pins as needed):

* Arduino PWM pin (e.g., D9 / PWM) → L298N `ENA` (enable, for speed control).
* Arduino D8 → L298N `IN1`
* Arduino D7 → L298N `IN2`
* Motor connected to L298N output terminals.
* L298N `Vcc` connected to motor power supply (match motor voltage), L298N `5V` jumper and GND common with Arduino.

> **Important:** Use an appropriate external power supply for the motor (do not drive motor directly from Arduino 5V). Include flyback diodes or rely on L298N internal protections. Always follow motor and driver current ratings.

---

## Repository Structure (Recommended)

```
├── README.md
├── gesture_fan_control.py        # main Python app (OpenCV + MediaPipe + PyFirmata)
├── requirements.txt              # pinned Python deps
├── arduino/
│   └── StandardFirmata.ino      # or instructions to upload via Arduino IDE
├── hardware_diagram.png          # wiring diagram image
├── docs/
│   ├── flowchart.png
│   └── software_architecture.md
├── LICENSE
└── .gitignore
```

---

## Testing & Calibration

* Test under multiple lighting conditions — MediaPipe performance can vary.
* Calibrate hand-to-speed thresholds while standing at the expected distance from the camera.
* Add debouncing or smoothing (rolling average) to avoid frequent speed jitter when detection is noisy.&#x20;

---

## Limitations & Future Work

**Limitations**

* Performance may degrade in poor lighting or with occlusions.
* Single-hand gestures only (unless multi-hand implementation is added).
* Motor driver and motor selection impose limits on power and noise.

**Future Improvements** (aligns with project recommendations)

* Multi-hand gesture detection and expanded gesture vocabulary.
* Integration into a broader smart home ecosystem (e.g., MQTT, Home Assistant).
* Robustness improvements for varied lighting and backgrounds.
* Add voice control as an alternative modality.&#x20;

---

## Acknowledgements & Contact

Project developed as part of CCS3360 - Technology Challenge Competition 2. Group members:

* W. M. H. E. K. Wickramasinghe — 22UG1-0789
* T. D. Nandasiri — 22UG1-0788
* D. M. S. B. Dissanayake — 22UG1-0783
* W. M. T. R. Wijekoon — 22UG1-0844
* P. M. V. M. Didulani — 22UG1-0487

For questions or collaboration: [tharukanandasiri123@gmail.com](mailto:tharukanandasiri123@gmail.com) · +94 767 405599.&#x20;

---

## License

This repository is distributed under the **MIT License** — feel free to reuse and adapt for academic and non-commercial purposes. Add `LICENSE` file in the repo with full MIT text.

---

## References

Arduino. (2021). Arduino Documentation: 
https://www.arduino.cc/en/guide 
Oliveira, L. A., & Ribeiro, P. F. (2017). Speed Control of an Induction Motor by 
Arduino. International Journal of Electrical and Computer Engineering, 7(4), 2303
2311: 
https://ijisrt.com/wp-content/uploads/2017/09/Speed-Control-of-Induction-Motor-Using
Arduino.pdf 
Géron, A. (2017). Hands-On Machine Learning with Scikit-Learn and TensorFlow: 
Concepts, Tools, and Techniques to Build Intelligent Systems (1st ed.). O'Reilly Media: 
https://powerunit-ju.com/wp-content/uploads/2021/04/Aurelien-Geron-Hands-On
Machine-Learning-with-Scikit-Learn-Keras-and-Tensorflow_-Concepts-Tools-and
Techniques-to-Build-Intelligent-Systems-OReilly-Media-2019.pdf 

---

### Final notes

This README is a complete, ready-to-copy `README.md` for your repository. You can further adapt the example gesture mappings, wiring pins, and commands to match the exact implementation and file names in your codebase. If you want, I can also:

* generate a `requirements.txt`,
* create an example `gesture_fan_control.py` skeleton, or
* draft the Arduino wiring diagram as an image file — tell me which one and I’ll add it into the repository content.
