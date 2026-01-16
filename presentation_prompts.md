# 🎙️ AOTS Technical Presentation Prompts

Use these prompts to generate slides or as speaker notes. Each section focuses on a specific code module within the `aotts/` directory.

---

## 1. 🕹️ Control Logic: Smoothing & Deadzone
**Prompt for AI/Slide Generation:**
> "Create a technical slide explaining the 'Control Logic' for a laser tracking system. Focus on how it solves servo jitter using an Exponential Moving Average (EMA) and a Deadzone threshold. Show the formula: NewPos = (Smoothing * Target) + ((1-Smoothing) * Current)."

**Key Code Reference (`main.py`):**
*   **Constants:** `SMOOTHING = 0.20`, `DEADZONE = 0.04`.
*   **Why?** Raw AI coordinates fluctuate rapidly. Without smoothing, the servos would vibrate violently.
*   **The Logic:**
    1.  Calculates difference (`abs(target - current)`).
    2.  If diff > `DEADZONE`, apply **EMA** (Exponential Moving Average).
    3.  Result: Smooth, organic movement like a human camera operator.

---

## 2. 🛡️ Security Feature: No-Go Zones
**Prompt for AI/Slide Generation:**
> "Design a slide about 'No-Go Zone Logic' in a surveillance interface. Explain how a user draws a rectangle (x, y, w, h) on a video feed. Describe the collision detection algorithm: checking if the target's center point (Cx, Cy) lies within the rectangle coordinates. Visual: A red semi-transparent box overlay."

**Key Code Reference (`main.html`):**
*   **State:** `zones = []` array storing `{x,y,w,h}`.
*   **User Input:** 2-Click system (Top-Left -> Bottom-Right) to define area.
*   **Detection Loop:**
    ```javascript
    const inZone = activePoint.x >= z.x && activePoint.x <= z.x + z.w && ...
    ```
*   **Action:** If `inZone == true` -> Trigger Alert & Draw "BREACH" text.

---

## 3. 📉 Security Feature: Deviation Monitoring
**Prompt for AI/Slide Generation:**
> "Create a diagram slide for 'Path Deviation Monitoring'. Visual: A green path line and a target object slightly away from it. Show a 'Distance Vector' (d) between the object and the closest point on the path. If d > Tolerance, trigger an alarm. Concept: Virtual Corridor / Geofencing."

**Key Code Reference (`main.html`):**
*   **Algorithm:** Iterate through every point in `recordedPath`.
*   **Math:** `Math.hypot(p.x - current.x, p.y - current.y)` to find the *Minimum Distance*.
*   **Visual Feedback:**
    *   **Green Tube:** Safe Zone (`ctx.lineWidth = threshold * 2`).
    *   **Red Dashed Line:** Drawn from Taget -> Path when limit exceeded.
    *   **Alert:** "⚠️ OFF PATH".

---

## 4. 💌 Alerts & Communication: SMTP Integration
**Prompt for AI/Slide Generation:**
> "Explain the 'Remote Alert Architecture' using Python AsyncIO. Show a flow diagram: Browser Detects Threat -> WebRTC -> Pi Server -> Async SMTP Task -> Gmail Servers -> User's Inbox. Highlight security practices like using App Passwords."

**Key Code Reference (`main.py`):**
*   **Libraries:** `smtplib`, `ssl`, `email.mime`.
*   **Async Handling:** The server does *not* pause while sending email. It continues tracking frames.
*   **Payload:** HTML formatted email with clear Red Header "🚨 ALERT".

---

## 5. 💾 Database: Path Persistence
**Prompt for AI/Slide Generation:**
> "Describe the 'Path Replay System'. How does a robotic system remember a route? Explain the JSON storage structure: numeric arrays of X/Y coordinates coupled with Timestamps. Show the flow: Record -> Save to JSON -> Load -> Loop Playback."

**Key Code Reference (`main.py` & `paths.json`):**
*   **Storage:** Simple JSON file database (`paths.json`).
*   **Endpoints:** `/save_path` (POST) and `/get_paths` (GET).
*   **Replay Logic:** When looping, the frontend ignores AI inputs and instead iterates through the `recordedPath` array index by index.

---

## 6. 🧠 The "Brain": WebRTC & AsyncIO
**Prompt for AI/Slide Generation:**
> "Technical Architecture Slide: Explain how 'aiohttp' and 'aiortc' enable real-time tracking. Center concept: The Browser does the heavy lifting (Vision AI), and the Pi does the actuation (Servos), connected by a WebRTC Data Channel for millisecond latency."

**Key Code Reference (`main.py`):**
*   `RTCPeerConnection`: Establishes the P2P link.
*   `DataChannel`: Sends tiny JSON packets (`{x: 320, y: 240}`) instead of heavy video.
*   **Benefit:** Extremely low latency control compared to standard HTTP polling.
