from kivy.core.window import Window
import sqlite3 as sql
from time import strftime
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.properties import ObjectProperty
import time
import threading
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.boxlayout import BoxLayout

Window.size = (360, 770)  # (1080, 2340)

class CreateTask(MDBoxLayout):
    pass

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when useer first opens dialog box
        self.ids.date_end.text = str(datetime.datetime.now().strftime('%A %d %B %Y'))


    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime('%Y %m %d')
        self.ids.date_end.text = str(date)



class ListOfTasks(FloatLayout, FakeRectangularElevationBehavior, TouchBehavior):
    name = ObjectProperty()
    comment = ObjectProperty()
    date_end = ObjectProperty()
    progress = ObjectProperty()

    def on_long_touch(self, *args):
        layout = BoxLayout(orientation='vertical')
        layout1 = FloatLayout()

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .18, 'center_y': .6},
                                                size_hint=(.3, .3),
                                                theme_text_color='Custom',
                                                text_color=(1, 1, 1, 1),
                                                on_release=self.edit_button)
        layout1.add_widget(self.editButton)
        self.deleteButton = MDFillRoundFlatButton(text='Delete', pos_hint={'center_x': .55, 'center_y': .6},
                                                  size_hint=(.3, .3),
                                                  theme_text_color='Custom',
                                                  text_color=(1, 1, 1, 1),
                                                  on_release=self.delete_button)
        layout1.add_widget(self.deleteButton)
        self.closeButton = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .85, 'center_y': .6},
                                                 size_hint=(.1, .3),
                                                 theme_text_color='Custom',
                                                 text_color=(1, 1, 1, 1),
                                                 on_release=self.closeWindow)
        layout1.add_widget(self.closeButton)
        layout.add_widget(layout1)

        self.pop = Popup(title=self.name, background_color='white', #title_font='KaushanScript-Regular.ttf',
                          content=layout,
                          size_hint=(None, None), size=(600, 300), pos_hint={'center_x': .5, 'center_y': .5})
        self.pop.open()
        return layout

    def edit_button(self, obj):
        print('Edit')

    def delete_button(self, obj):
        print('Delete')

    def closeWindow(self, obj):
        self.pop.dismiss()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''


class Harakiri(MDApp, Screen):
    until_midnight_time = ObjectProperty()

    def show_comment(self, comment):
        self.comment = comment
        self.dialog = MDDialog(
            title=str(comment), on_touch_down=MDDialog.dismiss, md_bg_color=(173/255, 255/255, 125/255, .4),
            radius=[20])
        self.dialog.open()


    def time_until_end_of_day(self, dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        time_until = ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)

        future_date = datetime.datetime.now() + datetime.timedelta(seconds=time_until)

        while True:
            curr_date = datetime.datetime.now()
            rem_time = future_date - curr_date
            total_seconds = int(rem_time.total_seconds())

            if total_seconds > 0:
                days, h_remainder = divmod(total_seconds, 86400)
                hours, remainder = divmod(h_remainder, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.until_midnight_time = (f"Time Left: {hours} hours, {minutes} minutes, {seconds} seconds")

                time.sleep(1)
                break
            else:
                break

        # hours = str(time_until // 3600)
        # minutes = str((time_until % 3600) // 60)
        # seconds = str((time_until % 3600) % 60)
        # print(hours+' '+minutes+' '+seconds)
        # time.sleep(1)

    # def createTask(self):
    #     screen_manager.get_screen('main').taskList.add_widget(CreateTask())

    task_list_dialog = None

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="[color=008F11]Create Task[/color]",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    # def add_task(self, name, comment, date_end):
    #     '''Add task to the list of tasks'''
    #
    #     print(name, comment)
    #     screen_manager.get_screen('main').taskList.add_widget(ListOfTasks(name=name, comment=comment, date_end=date_end))
        # self.root.ids['container'].add_widget(
        #     ListItemWithCheckbox(text='[b]' + task.text + '[/b]', secondary_text=task_date))
        name = ''  # set the dialog entry to an empty string(clear the text entry)


    def build(self):
        colors = {
            "Teal": {
                "50": "e4f8f9",
                "100": "bdedf0",
                "200": "97e2e8",
                "300": "79d5de",
                "400": "6dcbd6",
                "500": "008F11",#reference
                "600": "63b2bc",
                "700": "5b9ca3",
                "800": "54888c",
                "900": "486363",
                "A100": "bdedf0",
                "A200": "97e2e8",
                "A400": "6dcbd6",
                "A700": "5b9ca3",
            },
            "Blue": {
                "50": "e3f3f8",
                "100": "b9e1ee",
                "200": "91cee3",
                "300": "72bad6",
                "400": "62acce",
                "500": "589fc6",
                "600": "5191b8",
                "700": "487fa5",
                "800": "426f91",
                "900": "35506d",
                "A100": "b9e1ee",
                "A200": "91cee3",
                "A400": "62acce",
                "A700": "487fa5",
            },
            "Red": {
                "50": "ff6600",
                "100": "ff6600",
                "200": "EF9A9A",
                "300": "E57373",
                "400": "EF5350",
                "500": "ff6600",
                "600": "E53935",
                "700": "D32F2F",
                "800": "C62828",
                "900": "B71C1C",
                "A100": "FF8A80",
                "A200": "FF5252",
                "A400": "FF1744",
                "A700": "D50000",
            },
            "Light": {
                "StatusBar": "E0E0E0",
                "AppBar": "F5F5F5",
                "Background": "FAFAFA",
                "CardsDialogs": "FFFFFF",
                "FlatButtonDown": "cccccc",
            },
            "Dark": {
                "StatusBar": "000000",
                "AppBar": "212121",
                "Background": "303030",
                "CardsDialogs": "424242",
                "FlatButtonDown": "999999",
            }
        }

        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Green" #Teal, LightGreen, Lime

        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('history.kv'))

        return screen_manager

    def add_to_db(self, name, comment, date_end):
        screen_manager.get_screen('main').taskList.add_widget(
            ListOfTasks(name=name, comment=comment, date_end=date_end))

        status = False
        now = strftime('%Y %m %d')
        con = sql.connect('death.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO harakiri (names, comment, status, time_end, time_start) VALUES (?,?,?,?,?)""",
                    (name, comment, status, date_end, now))
        con.commit()
        con.close()

        screen_manager.get_screen('main').taskList.clear_widgets()
################
        con = sql.connect('death.db')
        cur = con.cursor()
        cur.execute("""SELECT names, comment, time_end FROM harakiri """)
        for x in cur:
            name = x[0]
            comment = x[1]
            date_end = x[2]

            date = [int(word) for word in date_end.split() if word.isdigit()]
            deadline = datetime.datetime(int(date[0]), int(date[1]), int(date[2])) - datetime.datetime.now()
            # hours = str(deadline.seconds // 3600)
            # minutes = str((deadline.seconds % 3600) // 60)
            # seconds = str((deadline.seconds % 3600) % 60)

            date_cooldown = (f'Days: {deadline.days}')  # , {hours}:{minutes}:{seconds}

            screen_manager.get_screen('main').taskList.add_widget(
                ListOfTasks(name=name, comment=comment, date_end=date_cooldown))

        con.commit()
        con.close()


    def on_start(self, dt=None):
        con = sql.connect('death.db')
        cur = con.cursor()
        cur.execute("""SELECT names, comment, time_end, time_start FROM harakiri """)
        for x in cur:
            name = x[0]
            comment = x[1]
            date_end = x[2]
            date_start = x[3]

            time_end = [int(word) for word in date_end.split() if word.isdigit()]
            deadline = datetime.datetime(int(time_end[0]),int(time_end[1]),int(time_end[2])) - datetime.datetime.now()

            time_start = [int(word) for word in date_start.split() if word.isdigit()]
            full_days = datetime.datetime(int(time_end[0]),int(time_end[1]),int(time_end[2])) - datetime.datetime(int(time_start[0]),int(time_start[1]),int(time_start[2]))
            # hours = str(deadline.seconds // 3600)
            # minutes = str((deadline.seconds % 3600) // 60)
            # seconds = str((deadline.seconds % 3600) % 60)

            date_cooldown = (f'Days: {deadline.days}[color=#3d3d3d][size=24]({full_days.days})[/size][/color]')#, {hours}:{minutes}:{seconds}

            progress = (deadline.days / full_days.days) * 100

            screen_manager.get_screen('main').taskList.add_widget(
                ListOfTasks(name=name, comment=comment, date_end=date_cooldown, progress=progress))


        con.commit()
        con.close()

#########time############
        def cooldown(dt=None):
            if dt is None:
                dt = datetime.datetime.now()
            time_until = ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)

            future_date = datetime.datetime.now() + datetime.timedelta(seconds=time_until)

            while True:
                curr_date = datetime.datetime.now()
                rem_time = future_date - curr_date
                total_seconds = int(rem_time.total_seconds())

                if total_seconds > 0:
                    days, h_remainder = divmod(total_seconds, 86400)
                    hours, remainder = divmod(h_remainder, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    self.until_midnight_time = (f"Time Left: {hours} hours, {minutes} minutes, {seconds} seconds")

                    time.sleep(1)

                else:
                    break
        t = threading.Thread(target=cooldown, name='time', args=(), daemon=True)
        t.start()
        # t.join()

    con = sql.connect('death.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE  IF NOT EXISTS  harakiri(
            UserID integer PRIMARY KEY AUTOINCREMENT,
            names text,
            comment text,
            status text,
            time_end text,
            time_start timestamp)
            """)
    con.commit()
    con.close()






if __name__ == '__main__':
    Harakiri().run()