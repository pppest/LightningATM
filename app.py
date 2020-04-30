#!/usr/bin/python3


from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.button import Button
# from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

import logging

import config
import utils


led = "off"
logger = logging.getLogger("MAIN")
utils.setup_coin_acceptor()

## start Kivy version
if config.kivy:


    class StartPage(Screen):
        pass


    class Latm(ScreenManager):
        pass


    class LatmApp(App):
        def build(self):
            return Latm()

    if __name__ == "__main__":
        LatmApp().run()

## start papyrus version
elif config.papyrus:

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
