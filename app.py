#!/usr/bin/python3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

import logging
import config
import utils
import os
import sys
import display

led = "off"
logger = logging.getLogger("MAIN")
utils.setup_coin_acceptor()

## checks if a screen is set in config

## start Kivy version
if config.display == 'touchscreen':


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

## start papyrus version
elif config.display == 'papirus':

    def main():
        utils.check_epd_size()
        logger.info("Application started")

        # Display startup startup_screen
        display.update_startup_screen()

        utils.setup_coin_acceptor()

        while True:
            utils.monitor_coins_and_button()

    while True:
        try:
            main()
        except KeyboardInterrupt:
            display.update_shutdown_screen()
            utils.GPIO.cleanup()
            logger.info("Application finished (Keyboard Interrupt)")
            sys.exit("Manually Interrupted")
        except Exception:
            logger.exception("Oh no, something bad happened! Restarting...")
            utils.GPIO.cleanup()
            os.execv("/home/pi/LightningATM/app.py", [""])

else:
    Print('no screen chosen')
