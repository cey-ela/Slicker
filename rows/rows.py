"""
Whenever a row is created it is done so by utilising Kivy's RecycleView Class:
https://kivy.org/doc/stable/api-kivy.uix.recycleview.html

Instead of creating each row individually a template for a row is taken from the Row class and handled efficiently by
RecyclView
"""

import kivy.properties as kp
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.config import Config

config = Config
config.read("C:\\Program Files\\Slicker\\slicker.ini")


class LimitedTextInput(TextInput):
    """A custom text input class is created so that we can limit the character amount per box and do some formatting.
    The formatting in this instance replaces any '\n' (newlines) with a space, to workaround an error seen when
    copying text in from Avid iNews"""

    char_count = kp.NumericProperty()
    at_limit = kp.BooleanProperty()

    limit = config.getint('main', 'char_limit')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ' '  # Tackles a minor bug that expands the rows buttons on init

    def insert_text(self, substring, from_undo=False):
        if not from_undo and len(self.text) >= self.limit:
            s = substring.replace("\r\n", " ")
            return s

        s = substring.replace("\r\n", " ")
        return super().insert_text(s, from_undo=from_undo)

    def caps(self, substring):
        s = substring.upper()
        self.text = s


class Row(RecycleDataViewBehavior, BoxLayout):
    """The main template row. A small but very important part of the process"""
    index = kp.NumericProperty()
    index_text = kp.StringProperty()
    category = kp.StringProperty()
    text = kp.StringProperty()
    options_shown = False

    def show_options(self, widget):
        """These 3 option functions are used to control the visibility of the navigation properties in each row"""
        widget.parent.width = 70
        widget.children[1].width = 50
        widget.children[0].width = 20
        self.options_shown = True

    def close_options(self, widget):
        widget.parent.width = 52
        widget.children[1].width = - 1
        widget.children[0].width = 52
        self.options_shown = False

    def row_options(self, widget):
        if not self.options_shown:
            self.show_options(widget)
        elif self.options_shown:
            self.close_options(widget)

    def refresh_view_attrs(self, view, index, data):
        """Inherited from RecycleDataViewBehavior. Called whenever a change is made in the UI.
         Utilised in this case to keep the index/row numbers up to date"""
        self.index = index

        return super(Row, self).refresh_view_attrs(view, index, data)

    def on_parent(self, instance, parent):
        """  Another class inherited from RecycleDataViewBehavior, called in a similar way, basically any update in the
        UI. We need to manually update these properties since the widget instances are changed by the (RV) recycleview.
        Without this running to keep everything synced with the data_set things get very disorganised"""
        if parent:
            new_cat = self.category.replace(".", "")
            new_cat = new_cat.replace("Breaking News", "Breaking")  # Some formatting of the category before it's sent
            # to the UI

            self.ids.spinner.text = new_cat  # Now sending to the UI
            self.ids.text_input.text = self.text



class RowTicker(Row):
    """The main row class isn't directly used by RV. Each on is taken individually form it's own new subclass"""
    class Category:
        """This subclass is different because it retrieves the current category options stored in slicker.ini"""
        choices = []

        for (each_key, each_value) in config.items('cats'):
            if each_value:
                choices.append(each_value)


class RowBreaking(Row):
    """Breaking and Obit could just use Row directly but this provides more definition on the .kv side"""
    pass


class RowObit(Row):
    pass
