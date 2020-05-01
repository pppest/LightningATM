

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import StringProperty
import config

def run():


    class StartPage(Screen):
        pass


    class SelectionPage(Screen):
        pass


    class PaymentPage(Screen):
        pass


    class Latm(ScreenManager):
        pass


    class LatmApp(App):
        coins = StringProperty()
        sats = StringProperty()

        def update(self, *args):
            # all update stuff here
            self.coins = str(config.FIAT)
            self.sats = str(config.SATS)
            pass

        def build(self):
            Clock.schedule_interval(self.update, 0.1)
            return Latm()

    LatmApp().run()
