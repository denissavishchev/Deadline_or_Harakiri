from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

Window.size = (360, 770)  # (1080, 2340)

class CreateTask(MDBoxLayout):
    pass

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when useer first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))


    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk


    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
        else:
            # we shall add code to remove the strikethrough later
            pass

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)



class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''


class Harakiri(MDApp, Screen):

    def createTask(self):
        screen_manager.get_screen('main').taskList.add_widget(CreateTask())

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

    def add_task(self, task, task_date):
        '''Add task to the list of tasks'''

        print(task.text, task_date)
        screen_manager.get_screen('main').taskList.add_widget(ListItemWithCheckbox(text='[b]' + task.text + '[/b]', secondary_text=task_date))
        # self.root.ids['container'].add_widget(
        #     ListItemWithCheckbox(text='[b]' + task.text + '[/b]', secondary_text=task_date))
        task.text = ''  # set the dialog entry to an empty string(clear the text entry)


    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"

        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('history.kv'))

        return screen_manager








if __name__ == '__main__':
    Harakiri().run()