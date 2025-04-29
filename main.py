from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.button import MDFloatingActionButton
import cv2
import time
from ultralytics import YOLO
from kivy.core.window import Window

KV = '''
ScreenManager:
    SetupScreen:
    StreamScreen:

<SetupScreen>:
    name: 'setup'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(15)
        padding: dp(20)
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            adaptive_height: True
            spacing: dp(10)
            pos_hint: {"center_x": 0.5}

            Image:
                source: "kt_favicon.png"  # <-- your logo file here
                size_hint: None, None
                size: dp(150), dp(150)
                pos_hint: {"center_x": 0.5}

            MDLabel:
                text: "ESP_Vision_Pro by Krishtec"
                halign: "center"
                font_style: "H4"
                size_hint_y: None
                adaptive_height: True

            MDLabel:
                text: "Experience the Future of Vision"
                halign: "center"
                font_style: "Subtitle2"
                size_hint_y: None
                adaptive_height: True

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            adaptive_height: True
            spacing: dp(20)
            pos_hint: {"center_x": 0.5}

            MDTextField:
                id: ip_input
                hint_text: "Enter ESP32-CAM IP Address"
                text: ""
                size_hint_x: None
                width: dp(300)
                pos_hint: {"center_x": 0.5}
                mode: "rectangle"

            MDBoxLayout:
                size_hint_y: None
                height: dp(60)
                spacing: dp(20)
                padding: dp(10)
                pos_hint: {"center_x": 0.5}
                size_hint_x: None
                width: dp(350)

                MDFillRoundFlatButton:
                    text: "View Live Stream"
                    on_release: app.start_live_stream()

                MDFillRoundFlatButton:
                    text: "AI Processed Stream"
                    on_release: app.start_ai_stream()


<StreamScreen>:
    name: 'stream'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDLabel:
            id: stream_label
            text: "Streaming..."
            halign: "center"
            font_style: "H6"
            size_hint_y: None
            height: dp(40)

        Image:
            id: stream_image
            allow_stretch: True
            keep_ratio: True

        MDBoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: dp(20)
            padding: dp(20)

            MDFillRoundFlatButton:
                text: "Back"
                on_release: app.go_back()

    MyFloatingButton:
        icon: "camera"
        md_bg_color: 1, 0, 0, 1
        pos_hint: {"right": 0.95, "y": 0.05}
        tooltip_text: "Take Screenshot"
        on_release: app.take_picture()

'''

class SetupScreen(MDScreen):
    pass

class StreamScreen(MDScreen):
    pass

class MyFloatingButton(MDFloatingActionButton, MDTooltip):
    '''Custom Floating Button with Tooltip'''
    pass

    

class ESP32CamApp(MDApp):

    def build(self):
        self.model = YOLO("yolov8s.pt")  # Load YOLO model
        Window.icon = 'kt_favicon.png'
        self.ip_address = ""
        self.selected_mode = ""
        self.streaming = False
        self.capture = None
        return Builder.load_string(KV)

    def start_live_stream(self):
        self.selected_mode = "live"
        self.start_stream()

    def start_ai_stream(self):
        self.selected_mode = "ai"
        self.start_stream()

    def start_stream(self):
        self.ip_address = self.root.get_screen('setup').ids.ip_input.text
        self.root.current = 'stream'
        self.streaming = True
        self.capture = cv2.VideoCapture(f"http://{self.ip_address}/stream")
        Clock.schedule_interval(self.update_frame, 1.0 / 20.0)  # 20 FPS

    def update_frame(self, dt):
        if self.streaming and self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                if self.selected_mode == "ai":
                    results = self.model(frame, verbose=False)[0]
                    frame = results.plot()

                self.last_frame = frame.copy()

                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.root.get_screen('stream').ids.stream_image.texture = texture
            else:
                print("⚠️ Failed to grab frame.")
        else:
            if self.capture:
                self.capture.release()
                self.capture = None
            return False

    def go_back(self):
        self.streaming = False
        if self.capture:
            self.capture.release()
            self.capture = None
        self.root.current = 'setup'

    def take_picture(self):
        if hasattr(self, 'last_frame'):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"esp32cam_capture_{timestamp}.png"
            cv2.imwrite(filename, self.last_frame)
            print(f"✅ Picture saved as {filename}")
        else:
            print("⚠️ No frame available to capture.")

if __name__ == "__main__":
    ESP32CamApp().run()
