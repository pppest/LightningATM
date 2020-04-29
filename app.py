#!/usr/bin/python3


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

import logging
import os
import sys
import time
import math
from PIL import Image, ImageDraw

import config
import lndrest
import lntxbot
import qr
import utils
import importlib

led = "off"
logger = logging.getLogger("MAIN")

utils.setup_coin_acceptor()


class StartPage(Screen):
    pass


class SelectionPage(Screen):
    pass


class PaymentPage(Screen):
    pass


class Latm(ScreenManager):
    pass


class LatmApp(App):
    def build(self):
        return Latm()


if __name__ == "__main__":
    LatmApp().run()
