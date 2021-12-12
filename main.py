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



class ListOfTasks(FloatLayout):
    name = ObjectProperty()
    comment = ObjectProperty()
    date_end = ObjectProperty()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''


class Harakiri(MDApp, Screen):
    until_midnight_time = ObjectProperty()

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
                title="Create Task",
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
        self.theme_cls.primary_palette = "DeepOrange"

        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('history.kv'))

        return screen_manager

    def add_to_db(self, name, comment, date_end):
        screen_manager.get_screen('main').taskList.add_widget(
            ListOfTasks(name=name, comment=comment, date_end=date_end))

        status = False
        now = strftime('%Y-%m-%d %H:%M:%S')
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
        cur.execute("""SELECT names, comment, time_end FROM harakiri """)
        for x in cur:
            name = x[0]
            comment = x[1]
            date_end = x[2]

            date = [int(word) for word in date_end.split() if word.isdigit()]
            deadline = datetime.datetime(int(date[0]),int(date[1]),int(date[2])) - datetime.datetime.now()
            # hours = str(deadline.seconds // 3600)
            # minutes = str((deadline.seconds % 3600) // 60)
            # seconds = str((deadline.seconds % 3600) % 60)

            date_cooldown = (f'Days: {deadline.days}')#, {hours}:{minutes}:{seconds}

            screen_manager.get_screen('main').taskList.add_widget(
                ListOfTasks(name=name, comment=comment, date_end=date_cooldown))

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