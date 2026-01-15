import asyncio

import cv2

import json

import sys

import time

from aiortc import RTCPeerConnection, RTCSessionDescription

import aiohttp

from aiohttp import web

from rpi_hardware_pwm import HardwarePWM

from gpiozero import LED

import smtplib

import ssl

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart



# ==========================================

# --- CONFIGURATION ---

# ==========================================

SMOOTHING = 0.20

DEADZONE = 0.04



# 0.0 is the logical center (maps to 7.5% duty cycle)

curr_pan = 0.0

curr_tilt = 0.0



# ==========================================

# --- HARDWARE INITIALIZATION ---

# ==========================================

class MockPWM:

    def start(self, dc): print(f"[MOCK] PWM Start at Center: {dc}")

    def change_duty_cycle(self, dc): pass 

    def stop(self): print("[MOCK] PWM Stop")



class MockLED:

    def on(self): print("[MOCK] Laser ON")

    def off(self): print("[MOCK] Laser OFF")



try:

    # PWM 0 -> GPIO 12, PWM 1 -> GPIO 13

    pwm_pan = HardwarePWM(pwm_channel=0, hz=50)

    pwm_tilt = HardwarePWM(pwm_channel=1, hz=50)

    

    # Start at 7.5 (Neutral/Center)

    pwm_pan.start(5.9) 

    pwm_tilt.start(5.9)

    

    laser = LED(17)

    laser.on()

    print("✓ Hardware PWM & Laser initialized to CENTER.")

except Exception as e:

    print(f"⚠️ Hardware Error: {e}")

    print("⚠️ Running in SIMULATION MODE")

    pwm_pan = MockPWM()

    pwm_tilt = MockPWM()

    laser = MockLED()



def servo_map(val):

    """

    Maps normalized value (-1.0 to 1.0) to Duty Cycle (5.0 to 10.0)

    0.0 becomes 7.5 (Center)

    """

    val = max(min(val, 1.0), -1.0) 

    return 5.9 + (val * 2.5)



# 



class VideoReceiver:

    def __init__(self):

        self.pc = RTCPeerConnection()



        @self.pc.on("datachannel")

        def on_datachannel(channel):

            @channel.on("message")

            def on_message(message):

                global curr_pan, curr_tilt

                try:

                    data = json.loads(message)

                    

                    # 1. Convert pixel coords to normalized -1.0 to 1.0

                    # data['x'] / data['w'] gives 0 to 1. 

                    # Multiplying by 2 and subtracting 1 gives -1 to 1.

                    target_x = -((data['x'] / data['w']) * 2 - 1.0)

                    target_y = (data['y'] / data['h']) * 2 - 1.0



                    # 2. Smoothing & Deadzone Logic

                    if abs(target_x - curr_pan) > DEADZONE:

                        curr_pan = (SMOOTHING * target_x) + ((1 - SMOOTHING) * curr_pan)

                    

                    if abs(target_y - curr_tilt) > DEADZONE:

                        curr_tilt = (SMOOTHING * target_y) + ((1 - SMOOTHING) * curr_tilt)



                    # 3. Move Servos

                    pwm_pan.change_duty_cycle(servo_map(curr_pan))

                    pwm_tilt.change_duty_cycle(servo_map(curr_tilt))

                    

                    print(f"Tracking {data.get('label', 'object')} | Pan: {curr_pan:+.2f} Tilt: {curr_tilt:+.2f}", end='\r')

                except Exception as e:

                    print(f"Data Error: {e}")



    async def start_stream(self, offer):

        @self.pc.on("track")

        def on_track(track):

            if track.kind == "video":

                asyncio.ensure_future(self.process_frames(track))

        await self.pc.setRemoteDescription(offer)

        answer = await self.pc.createAnswer()

        await self.pc.setLocalDescription(answer)

        return self.pc.localDescription



    async def process_frames(self, track):

        while True:

            try:

                frame = await track.recv()

            except Exception:

                break



# --- WEB SERVER ROUTES ---

async def index(request):

    try:

        with open('main.html', 'r', encoding='utf-8') as f:

            return web.Response(text=f.read(), content_type='text/html')

    except FileNotFoundError:

        return web.Response(text="main.html not found", status=404)



async def offer(request):

    params = await request.json()

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    receiver = VideoReceiver()

    answer = await receiver.start_stream(offer)

    return web.Response(

        content_type="application/json", 

        text=json.dumps({"sdp": answer.sdp, "type": answer.type})

    )



async def save_path(request):

    try:

        data = await request.json()

        entry = {

            "name": data.get("name", "Untitled Path"),

            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

            "points": data.get("path", [])

        }

        try:

            with open('paths.json', 'r') as f: db = json.load(f)

        except: db = []

        db.append(entry)

        with open('paths.json', 'w') as f: json.dump(db, f, indent=2)

        return web.Response(text=json.dumps({"status": "ok"}), content_type="application/json")

    except Exception as e:

        return web.Response(text=json.dumps({"error": str(e)}), status=500)



async def get_paths(request):

    try:

        with open('paths.json', 'r') as f: db = json.load(f)

    except: db = []

    return web.Response(text=json.dumps(db), content_type="application/json")



async def send_alert(request):
    try:
        data = await request.json()
        obj_name = data.get("object", "Unknown Object")
        recipient = data.get("email", "") 

        # EMAIL SETTINGS
        SENDER_EMAIL = "vedantkhot112@gmail.com"
        APP_PASSWORD = "wwxz xout qszt hnru" # WARNING: Change this password!
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🚨 ALERT: {obj_name} Detected!"
        message["From"] = SENDER_EMAIL
        message["To"] = recipient
        
        html = f"<html><body><h2 style='color:red;'>🚨 Alert</h2><p>{obj_name} detected.</p></body></html>"
        message.attach(MIMEText(html, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, message.as_string())
        
        return web.Response(text=json.dumps({"status": "ok"}), content_type="application/json")


    except Exception as e:

        return web.Response(text=json.dumps({"error": str(e)}), status=500)



app = web.Application()

app.router.add_get("/", index)

app.router.add_post("/offer", offer)

app.router.add_post("/save_path", save_path)

app.router.add_get("/get_paths", get_paths)

app.router.add_post("/send_alert", send_alert)



if __name__ == "__main__":

    try:

        web.run_app(app, host="0.0.0.0", port=7080)

    finally:

        laser.off()

        pwm_pan.stop()

        pwm_tilt.stop()