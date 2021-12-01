from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout

Window.size = (360, 770)  # (1080, 2340)

class CreateTask(FloatLayout):
    pass

class Harakiri(MDApp, Screen):

    def createTask(self):
        screen_manager.get_screen('main').taskList.add_widget(CreateTask())


    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('createTask.kv'))
        screen_manager.add_widget(Builder.load_file('history.kv'))

        return screen_manager








if __name__ == '__main__':
    Harakiri().run()