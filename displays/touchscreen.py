

    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen


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
        def build(self):
            return Latm()

    LatmApp().run()
