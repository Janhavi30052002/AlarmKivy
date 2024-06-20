from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.pickers import MDTimePicker
from kivy.clock import Clock
import datetime
import pygame
import os

Window.size = (350, 600)

KV = '''
MDFloatLayout:
    md_bg_color: 1, 1, 1, 1
    MDLabel:
        text: "ALARM"
        font_size: "30sp"
        pos_hint: {"center_y": .935}
        halign: "center"
        bold: True
    MDIconButton:
        icon: "plus"
        pos_hint: {"center_x": .87, "center_y": .94}
        md_bg_color: 0, 0, 0, 1
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        on_release: app.time_picker()
    MDLabel:
        id: alarm_time
        text: ""
        pos_hint: {"center_y": .5}
        halign: "center"
        font_size: "30sp"
        bold: True
    MDRectangleFlatButton:
        text: "Stop"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_release: app.stop()
'''


class AlarmApp(MDApp):
    pygame.init()
    sound_file = "alarm_sound.mp3"

    if os.path.exists(sound_file):
        sound = pygame.mixer.Sound(sound_file)
    else:
        print(f"Error: Sound file '{sound_file}' not found.")
        sound = None

    volume = 0

    def build(self):
        return Builder.load_string(KV)

    def time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.schedule)
        time_dialog.open()

    def schedule(self, *args):
        Clock.schedule_interval(self.check_alarm, 1)

    def check_alarm(self, *args):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if self.root.ids.alarm_time.text == current_time:
            self.start()

    def set_volume(self, *args):
        self.volume += 0.05
        if self.volume < 1.0:
            self.sound.set_volume(self.volume)
            print(self.volume)
        else:
            self.sound.set_volume(1)
            Clock.unschedule(self.set_volume)
            print("Reached Maximum volume!")

    def start(self, *args):
        if self.sound:
            self.sound.play(-1)
            Clock.schedule_interval(self.set_volume, 10)
        else:
            print("Error: No sound to play.")

    def stop(self, *args):
        if self.sound:
            self.sound.stop()
            Clock.unschedule(self.set_volume)
            self.volume = 0

    def get_time(self, instance, time):
        self.root.ids.alarm_time.text = str(time)


AlarmApp().run()
