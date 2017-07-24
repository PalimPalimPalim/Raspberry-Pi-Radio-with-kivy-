""" GUI for PalimRadio"""

from __future__ import print_function

import subprocess
import csv
import time

import radiocontrols as rdc

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.uix.modalview import ModalView
from kivy.uix.slider import Slider
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget

from kivy.vector import Vector


class StationLbl(Label):
    """Label displaying Radio Station info"""

    def __init__(self, **kwargs):
        """init Label and call update to get station info"""
        super(StationLbl, self).__init__(**kwargs)
        self.text = 'retrieving Info'
        self.update()
        Clock.schedule_interval(self.update, 2)

    def update(self, *args):
        """get Info about Song and Radio Station"""
        info = subprocess.check_output('mpc current', shell=True)
        self.text = info

class VolumeBtn(Button):
    def open_vlm_slider(self):
        view = VolumeMdlVw(size=(self.width, self.height*4))
        view.open()


class VolumeMdlVw(ModalView):
    volume = NumericProperty()
    def __init__(self, **kwargs):
        """init Label and call update to get station info"""
        self.volume = rdc.get_volume_num()
        super(VolumeMdlVw, self).__init__(**kwargs)

    def mute(self):
        self.ids.slider.value = 0
        rdc.set_volume(0)




class ChannelGrid(GridLayout):
    """ChannelGrid holds all ChannelBtn"""
    def __init__(self, **kwargs):
        super(ChannelGrid, self).__init__(**kwargs)

        # read stations.csv and add ChannelBtn for each
        rdc.clear_stations()

        with open('stations.csv', 'rb') as f:
            reader = csv.reader(f)
            chnl_list = list(reader)


        for index, chnl in enumerate(chnl_list):
            rdc.add_station(chnl[2])
            img_file_location = "ButtonImages/" + chnl[1]
            channel_btn = ChannelBtn(background_normal=img_file_location, chnl_num=(index + 1))
            self.add_widget(channel_btn)



class ChannelBtn(Button):
    """Btn for each channel to switch to channel"""
    chnl_num = NumericProperty()

    def play_channel(self):
        """change to channel self"""
        subprocess.call('mpc play ' + str(self.chnl_num), shell=True)


class PlayPauseBtn(ButtonBehavior, Widget):
    img_source = StringProperty("ButtonControls/play.png")

    def __init__(self, **kwargs):
        """init Label and call update to get station info"""
        super(PlayPauseBtn, self).__init__(**kwargs)
        Clock.schedule_interval(self.check_playing, 1)

    def collide_point(self, x, y):
        return Vector(x, y).distance(self.center) <= self.width / 2

    def toggle_play_pause(self):
        status = rdc.toggle()
        print(status)
        if status:
            self.img_source = "ButtonControls/pause.png"
        else:
            self.img_source = "ButtonControls/play.png"

    def check_playing(self, *args):
        if rdc.get_playing():
            self.img_source = "ButtonControls/pause.png"
        else:
            self.img_source = "ButtonControls/play.png"

class ClockLbl(Label):
    def __init__(self, **kwargs):
        """init Label and call update to get station info"""
        super(ClockLbl, self).__init__(**kwargs)
        self.text = time.asctime()
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.asctime()

class VolumeLbl(Label):
    def __init__(self, **kwargs):
        """init Label and call update to get volume info"""
        super(VolumeLbl, self).__init__(**kwargs)
        self.text = rdc.get_volume()
        #Clock.schedule_interval(self.update, 2)

    def update(self, *args):
        self.text = rdc.get_volume()


class RadioApp(App):
    """RadioApp"""
    pass

RadioApp().run()
