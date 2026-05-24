# ClearTide
ClearTide replaces mechanical nets with smart, low-power electrostatic tech. An autonomous surface sweeper designed to target ocean microplastics.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Industry 4.0](https://img.shields.io/badge/Industry%204.0-Control%20Systems-blue?style=for-the-badge)

##  Overview
An AI-driven marine robotics system engineered for autonomous environmental remediation. This project transitions traditional marine surface-sweeping from purely mechanical filtration to software-centric intelligence. By integrating real-time computer vision with autonomous navigational control, the **Autonomous Sea-Sweeper (ASS)** intelligently identifies, tracks, and intercepts surface debris and pervasive microplastics (<5mm). 

Replacing energy-intensive trawling nets with an intelligent **Electrostatic Filtration Array (EFA)**, this Unmanned Surface Vehicle (USV) demonstrates how advanced kinematic control and edge computing can achieve highly efficient, low-power ecological restoration.

---

##  The Problem: Microplastic Ubiquity
The primary challenge in ocean cleanup is the invisible threat: microplastics. 
* **Inefficiency of Existing Solutions:** Conventional skimmers and nets are inadequate. The extremely fine mesh required to capture microplastics creates excessive water drag, rapidly draining power and requiring massive, complex infrastructure.
* **Ecological Hazard:** These particles transfer toxins through the aquatic food web, posing a direct threat to marine life and human health. A selective, low-power, and highly mobile autonomous system is required to address this at scale.

---

##  Core Architecture & Industry 4.0 Integration

The system architecture prioritizes software logic and smart actuation over mechanical brute force.

### 1. Dual-Processing Edge Compute
* **High-Level Intelligence (Raspberry Pi / Jetson Nano):** Handles computationally intensive, non-real-time operations including YOLOv8 visual perception, Boustrophedon (Lawnmower) path planning, and data logging.
* **Real-Time Kinematics (STM32 / Arduino Mega):** A dedicated microcontroller managing high-speed, time-critical tasks like generating exact PWM signals for the Electronic Speed Controllers (ESCs) and maintaining the continuous PID stabilization loop.

### 2. Visual Perception & AI (YOLOv8)
* Utilizes a custom-trained YOLOv8 object detection model using OpenCV to process live video feeds.
* Dynamically segments and classifies marine debris against complex, reflective water surface backgrounds.
* Lays the groundwork for predictive heat-mapping of pollution accumulation zones by logging the spatial distribution of detected waste.

### 3. Navigation & Sensor Fusion
* **Extended Kalman Filter (EKF):** Mathematically combines data from a fast, drift-prone 9-DOF IMU (Accelerometer, Gyroscope, Magnetometer) with a slower, noisy GPS receiver.
* **Result:** Provides a highly accurate, continuous estimate of the vessel’s instantaneous position, velocity, and attitude (Process Variable) for precise path adherence despite wind and current disturbances.

### 4. Smart Actuation: Electrostatic Filtration Array (EFA)
* Moving away from passive nets, the system deploys a submerged EFA commanded by the control unit. 
* It generates a low-voltage electric field to actively induce a charge on non-polar plastic particles, causing them to clump (flocculate) for highly efficient, low-drag recovery.

---

##  Kinematic Control Loop & Methodology

The Sea-Sweeper operates in a continuous autonomous cycle driven by a strict mathematical feedback loop:

1. **Mission Planning:** The microprocessor generates an optimized Boustrophedon Path Plan, minimizing transit time and guaranteeing 100% target area coverage. 
2. **Translating Vision to Vectors:** Bounding box coordinates from the YOLOv8 model are translated into spatial vectors, dynamically updating the immediate target heading.
3. **PID Stabilization:** The microcontroller continuously compares the desired target heading (**Set Point**) against the EKF-smoothed IMU data (**Process Variable**). 
4. **Differential Thrust:** The PID controller calculates the error and outputs a **Manipulated Variable**—adjusting the counter-rotating DC thrusters to intercept the debris or maintain the planned course.

---

##  Tech Stack

| Category | Technologies Used |
| :--- | :--- |
| **Language** | Python, C++ |
| **Computer Vision** | OpenCV, Ultralytics (YOLOv8 Nano) |
| **Control Logic** | PID Control, Matrix Transformations, Extended Kalman Filter |
| **Hardware** | Raspberry Pi / Jetson Nano, STM32 MCU, 9-DOF IMU, GPS Module |
| **Actuation** | Differential DC Thrusters, Electrostatic Filtration Array |

---

##  Future Scope

* **Adaptive Path Planning:** Upgrading the algorithm to incorporate real-time current sensor data, executing "Current-Aware" pathing to maximize coverage efficiency while minimizing power expenditure against strong tides.
* **Energy Augmentation:** Integrating flexible photovoltaic solar panels across the catamaran hull to achieve near-perpetual operation for long-duration remediation missions.
* **Advanced Material Classification:** Expanding the machine learning model to distinguish between complex macro-debris and biological matter (e.g., kelp vs. plastic) to prevent unnecessary biological bycatch.
