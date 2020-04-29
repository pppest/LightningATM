#!/usr/bin/python3


from kivy.app import App

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


class AtmApp(App):
    def build(self):
        return AtmApp()

    # utils.check_epd_size()

    logger.info("Application started")
    # display.update_startup_screen()
    utils.setup_coin_acceptor()

    # while True:
    #     monitor_coins_and_button()

if __name__ == "__main__":
    AtmApp().run()
