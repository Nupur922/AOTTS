# 🎯 AOTTS: Always-On Target Tracking System

> **A Next-Generation Active Surveillance Solution**  
> *Turning passive monitoring into active engagement with Edge AI and Raspberry Pi 5.*

---

## 1. 🚨 Problem Statement & Real-World Need

**The Problem:**  
Traditional surveillance systems are **passive**. They record crimes but do not intervene. Existing automated tracking solutions are often bulky, expensive, or suffer from high latency, making them ineffective for real-time response.

**The Solution (AOTTS):**  
AOTTS transforms surveillance from passive recording to **active engagement**. By combining **Edge AI (TensorFlow.js)** with high-speed hardware actuation (**Raspberry Pi 5**), we provide a low-latency, "always-on" system.

> **Why this matters:** In high-security zones, industrial safety (geofencing), or automated wildlife monitoring, a system must not only "see" but "point" and "alert" instantly. AOTTS fulfills this by using a laser-guided pan-tilt mechanism that follows targets with **sub-100ms latency**.

---

## 2. ⚡ Selection of Microboard: Raspberry Pi 5 vs. ESP32

While many hobbyist projects use the ESP32, AOTS utilizes the **Raspberry Pi 5** for distinct strategic advantages:

| Feature | Raspberry Pi 5 🏆 | ESP32 |
| :--- | :--- | :--- |
| **Computational Power** | Runs full WebRTC & Async Python Server | Struggles with high-bitrate video |
| **PWM Precision** | **Stable Hardware PWM** (RP1 Chip) | Software Emulated (Jittery) |
| **Multi-Tasking** | Handles AI, Web Server, Database, & Servos | Limited concurrency |
| **Scalability** | Support for Local LLMs & OpenCV | Very limited expansion |

---

## 3. 🛠️ Proposed Solution: The Phased Approach

We executed the implementation in five distinct phases:

*   **Phase I: The Perception Layer** 👁️  
    Implementing `TensorFlow.js COCO-SSD` for real-time browser-based object detection.
*   **Phase II: The Communication Bridge** 📡  
    Establishing a **WebRTC Data Channel** to send coordinates from browser to Pi with **zero lag**.
*   **Phase III: Actuation & Control** 🦾  
    Converting normalized coordinates (`-1.0` to `1.0`) into PWM duty cycles to drive the Pan-Tilt mechanism.
*   **Phase IV: Intelligence & Automation** 🧠  
    Implementing **Path Recording**, **Replay Loops**, and **Sticky-Target Locking**.
*   **Phase V: Security Logic** 🛡️  
    Developing advanced "Virtual Fence" capabilities including **Deviation Monitoring** (Safety Corridors) and **No-Go Zones**.

---

## 4. 🏗️ IoT Architecture (Level 4/5)

According to standard IoT benchmarks, AOTS operates at **IoT Level 4**, moving toward Level 5.

1.  **Perception Layer**: Camera sensor & AI model (TensorFlow.js).
2.  **Network Layer**: WebRTC (P2P Media/Data) & HTTP (API Alerts).
3.  **Middleware Layer**: Raspberry Pi 5 acting as Edge Gateway (Python/Asyncio).
4.  **Application Layer**: Interactive Web Dashboard.

---

## 5. 🎨 Design System Flow

### A. Logical Design (Backend - Python/Pi 5)
*   **Asyncio**: Non-blocking web server.
*   **VideoReceiver**: Processes WebRTC data channels.
*   **Smoothing Algorithm**: applied `SMOOTHING (0.20)` and `DEADZONE (0.04)` to prevent servo jitter.

### B. Hardware Setup
*   **Pan-Tilt Shield**: GPIO 12 & 13 (High-Torque Servos).
*   **Visual Indicator**: GPIO 17 (Laser Diode).
*   **Power Isolation**: Dedicated rail for servos to prevent brownouts.

### C. Control Logic (Frontend - HTML5/JS)
The frontend is the "Brain" of the operation:
*   **🤖 Auto Mode**: Calculates bounding box centers.
*   **🕹️ Manual Mode**: D-Pad control.
*   **🔒 Locked Mode**: "Sticks" to a specific target using Euclidean distance.
*   **🛡️ Deviation Monitor**: Alerts if a target strays from a pre-recorded path.
*   **⛔ No-Go Zones**: Virtual tripwires that trigger immediate alerts upon entry.

---

## 6. 🎬 Implementation & Demo Sequence

1.  **Initialization**: Powering up & WebRTC Handshake.
2.  **Target Acquisition**: AI detects "Person/Cell Phone" -> Laser snaps to target.
3.  **Path Recording**: Record movement -> Save to `paths.json` -> Replay Loop.
4.  **Deviation Monitoring**: Walk "off-path" -> System draws **Red Correction Vector**.
5.  **No-Go Zones**: Breach a restricted zone -> **"BREACH"** Alert.
6.  **Remote Alert**: System sends **Email Notification**.

---

## 7. 🌍 Applications & Research

**Research Foundation:** Inspired by *"Edge Inference in Low-Power Robotics"*. Offloading AI to the client browser achieves high FPS that Pi-only CV cannot match.

**Real-World Use Cases:**
*   🪖 **Military/Defense**: Autonomous Sentry Gun simulation.
*   🛍️ **Retail**: Heat-mapping customer movement.
*   🏭 **Industrial Safety**: Hazardous zone monitoring.
*   🌾 **Agriculture**: Automated pest deterrence.

---

## 8. 🚀 Future Enhancements

*   [ ] **LiDAR Integration**: Depth-aware tracking.
*   [ ] **Night Vision**: IR-Cut camera for 24/7 operation.
*   [ ] **Swarm Coordination**: Multiple AOTS units linked to one dashboard.
