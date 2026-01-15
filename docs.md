________________________________________
Project Report: AOTS (Always-On Target Tracking System)
1. Problem Statement & Real-World Need
The Problem: Traditional surveillance systems are passive. They record crimes but do not intervene. Existing automated tracking solutions are often bulky, expensive, or suffer from high latency, making them ineffective for real-time response.
The Solution (AOTS): AOTS transforms surveillance from passive recording to active engagement. By combining Edge AI (TensorFlow.js) with high-speed hardware actuation (Raspberry Pi 5), we provide a low-latency, "always-on" system.
•	Backtracking the Need: In scenarios like high-security zones, industrial safety (geofencing), or automated wildlife monitoring, a system must not only "see" but "point" and "alert" instantly. AOTS fulfills this by using a laser-guided pan-tilt mechanism that follows targets with sub-100ms latency.
2. Selection of Microboard: Raspberry Pi 5 vs. ESP32
While many hobbyist projects use the ESP32, AOTS utilizes the Raspberry Pi 5 for the following strategic reasons:
•	Computational Overhead: Our system runs a full WebRTC stack and an asynchronous Python web server (aiohttp). The ESP32 struggles with high-bitrate video concurrent with complex WebRTC handshaking.
•	Hardware PWM Precision: The Pi 5’s new RP1 I/O controller provides exceptionally stable Hardware PWM. Unlike the ESP32’s software-emulated PWM, the Pi 5 ensures the servos move smoothly without "jitter" during AI inference.
•	Multi-Tasking: The Pi 5 handles the laser, two high-torque servos, a web server, and a database (paths.json) simultaneously without thermal throttling.
•	Scalability: The Pi 5 allows for future integration of local LLMs or more complex OpenCV processing that the ESP32 simply cannot support.
3. Proposed Solution: The Phased Approach
We divided the implementation into five distinct phases:
•	Phase I: The Perception Layer: Implementing TensorFlow.js COCO-SSD for real-time browser-based object detection.
•	Phase II: The Communication Bridge: Establishing a WebRTC Data Channel. This is critical for sending coordinates from the browser to the Pi with zero lag.
•	Phase III: Actuation & Control: Converting normalized coordinates (-1.0 to 1.0) into PWM duty cycles (5% to 10%) to drive the Pan-Tilt mechanism.
•	Phase IV: Intelligence & Automation: Implementing Path Recording, Replay Loops, and Sticky-Target Locking.
•	Phase V: Security Logic: Developing advanced "Virtual Fence" capabilities including Deviation Monitoring (Safety Corridors) and No-Go Zones (Restricted Areas).
________________________________________
4. IoT Architecture (Level 4/5 Implementation)
According to standard IoT benchmarks, AOTS operates at IoT Level 4, moving toward Level 5:
1.	Perception Layer: Camera sensor and AI model (TensorFlow.js).
2.	Network Layer: WebRTC for peer-to-peer media/data transfer and HTTP for API alerts.
3.	Middleware/Support Layer: Raspberry Pi 5 acting as an Edge Gateway, processing coordinates and managing the paths.json database.
4.	Application Layer: The Interactive Web Dashboard (UI) featuring:
    - Manual/Auto Control Modes
    - Path Recorder & Playback
    - Security Zone Drawing & Monitoring
________________________________________
5. Design System Flow
Our system logic is bifurcated into three core segments:
A. Logical Design (Backend - Python/Pi 5)
The backend uses Asynchronous I/O (asyncio).
•	It listens for WebRTC offers to start the stream.
•	The VideoReceiver class processes the data channel messages.
•	Smoothing Algorithm: We implemented a SMOOTHING constant (0.20) and a DEADZONE (0.04) to prevent jerky servo movements, ensuring the laser stays steady on the target.
B. Actual System (Hardware)
•	Pan-Tilt Shield: Two servos connected to GPIO 12 and 13.
•	Visual Indicator: A laser diode on GPIO 17.
•	Isolation: The Pi 5 manages logic, while the servos are powered via a dedicated rail to prevent "brownouts" during high-speed tracking.
C. Control Logic (Frontend - HTML5/JS)
The frontend is the "Brain" of the operation:
•	Auto Mode: Bounding box center points are calculated.
•	Manual Mode: A D-Pad or Arrow Keys send direct coordinate offsets.
•	Locked Mode: Uses Euclidean distance to "stick" to a specific target.
•	Deviation Monitor: Mathematically calculates perpendicular distance from a recorded path. If a target exceeds the tolerance threshold, a vector is drawn to guide them back.
•	No-Go Zones: User-drawn rectangles that act as virtual tripwires. Entry triggers immediate audio-visual and API alerts.
________________________________________
6. Implementation & Demo Sequence
During the demo, each team member will showcase a specific capability:
1.	Initialization: Powering the Pi and establishing the WebRTC handshake.
2.	Target Acquisition: Showing the AI detect "person" or "cell phone" and the laser instantly snapping to the target.
3.	Path Recording: Recording a movement pattern, saving it to paths.json, and replaying it (The "Loop" function).
4.	Deviation Monitoring: Walking "off-path" to demonstrate the dynamic red vector and correction arrow.
5.	No-Go Zones: Drawing a restricted box on live video and physically breaching it to trigger the "BREACH" alert.
6.	Remote Alerting: Confirming receipt of the WhatsApp/Email notification.
________________________________________
7. Application & Research Integration
Research Foundation: Our project is inspired by research into "Edge Inference in Low-Power Robotics." By offloading the AI inference to the client browser (using the user's phone/PC GPU) and using the Pi 5 solely for actuation, we achieve a high FPS (Frames Per Second) that traditional Pi-only CV projects cannot match.
Real-World Applications:
•	Military/Defense: Autonomous sentry gun simulation with defined rules of engagement (Zones).
•	Retail: Heat-mapping customer movement via the "Path History" feature.
•	Industrial Safety: Ensuring workers stay on safe walkways (Deviation Monitor) and out of hazardous machinery areas (No-Go Zones).
•	Agriculture: Automated laser-scaring for crop-destroying pests.
________________________________________
8. Future Enhancements
•	LiDAR Integration: To add "Depth" to the tracking, allowing the laser to adjust for distance.
•	Night Vision: Upgrading to an IR-Cut camera for 24/7 "Always-On" capability.
•	Swarm Coordination: Connecting multiple AOTS units to a single C2 (Command & Control) dashboard to cover blind spots.
________________________________________
