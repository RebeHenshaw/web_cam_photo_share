import time
import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from filesharer import FileSharer
from kivy.core.clipboard import Clipboard

Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    def start(self):
        """Start webcam."""
        self.ids.camera.play = True
        self.ids.button1.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera.opacity = 1

    def stop(self):
        """Stop webcam."""
        self.ids.camera.play = False
        self.ids.button1.text = 'Start Camera'
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        """Take a photo, save it, and switch to image screen."""
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filename = "photos/" + current_time + '.png'
        self.ids.camera.export_to_png(self.filename)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filename


class ImageScreen(Screen):
    def create_link(self):
        """Upload image to filestack and create a link."""
        filepath = App.get_running_app().root.ids.camera_screen.filename
        fileshare = FileSharer(filepath=filepath)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy(self):
        """Copy URL to Clipboard."""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = 'Create a link first!'

    def open(self):
        """Open URL in new window."""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = 'Create a link first!'


# go back button

class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
