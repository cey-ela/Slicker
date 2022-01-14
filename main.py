"""
                     ______     __         __     ______     __  __     ______     ______
                    /\  ___\   /\ \       /\ \   /\  ___\   /\ \/ /    /\  ___\   /\  == \
                    \ \___  \  \ \ \____  \ \ \  \ \ \____  \ \  _"-.  \ \  __\   \ \  __<
                     \/\_____\  \ \_____\  \ \_\  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\
                      \/_____/   \/_____/   \/_/   \/_____/   \/_/\/_/   \/_____/   \/_/ /_/

                     # ## ### #### ##### ##### # THE SLICKER TICKER # ##### ##### #### ### ## #
                    # ## ### #### ##### ###### #######  v1.0  ####### ###### ##### #### ### ## #
                     # ## ### #### # Built by Joe Edwards for ITV Daytime - 2020 # ### ### ## #



This program has been built using Kivy. Kivy is an open-source Python library for rapid development of applications. It
comes loaded with plenty of useful modules and pre-defined UI styles that take some of the labour out of app
development.

When writing this code I tried to follow the MVC method which separates an application into 3 components:
Model, View & Controller - this should aid readability and development speed.

Model: The external modules I've created to reduce bloating in the main App Class, such as popups.py and
sql_connection.py

View: All .kv files pertain to the front-end/UI side of things. It's written in Kivy Lang which is similar to HTML in
the way that you create widgets trees in a declarative way and bind properties to them in a readable manner.

Controller: The main App class, SlickerApp. This is the core of the application speaking to modules and the UI, the
first and last thing to run, all inherited from the kivy.app module.

For more info on Kivy visit: https://kivy.org/doc/stable/
"""

import os
import sys
import enchant
from kivy.app import App
from kivy import properties as kp
from settings.misc import void_chars
from datetime import datetime
from rows.rows import Row
from popups.popups import Popups
from database import update_databases
from database.sql_connection import retrieve_sql_data
from settings.settings_json import gen_settings_json, custom_cats_json, contact_json, help_json, about_json
from kivy.config import Config
from kivy.uix.settings import SettingsWithSidebar
from settings.settings_customisation import MySettings


class SlickerApp(App):
    """# ### INITIALISING THE MAIN APP CLASS ### ## #
    # ## ### INITIALISING THE MAIN APP CLASS ### ## #
    # ## ### INITIALISING THE MAIN APP CLASS ### ## #
    """

    kvconfg = Config
    kvconfg.read("slicker.ini")  # Import the settings ini

    contact_active = kvconfg.get('main', 'contact_bool')
    weather_active = kvconfg.get('main', 'weather_bool')

    kvconfg.set('main', 'add_new_cat', '')
    kvconfg.set('main', 'category_list', '')
    with open('slicker.ini', 'w'):
        kvconfg.write()  # Clear some parameters in the settings ini

    settings_cls = SettingsWithSidebar
    use_kivy_settings = False  # Some settings config

    popups = Popups()  # Create an instance of the popup class
    show_maestro_reminder = True

    # Create local datasets for each tab by retrieving the data from the relevant SQL data table
    data_generic = kp.ListProperty(retrieve_sql_data('data_generic'))
    data_breaking = kp.ListProperty(retrieve_sql_data('data_breaking'))
    data_obit = kp.ListProperty(retrieve_sql_data('data_obit'))

    current_data_set = "self.data_generic"  # Set which data_set the functions will focus on. This is changed when
    # a new tab is selected in the GUI

    placeholder = Row.options_shown  # Fairly useless but essential placeholder. If a Row item isn't imported the App

    # doesn't run

    def build(self):
        """A useful function belonging to the kivy.App class which is called upon initialisation of the App.
        Used in this instance to establish some custom settings
        """
        self.settings_cls = MySettings

        if self.contact_active == '1':
            self.root.ids.contact_indicator.state = 'down'
        else:
            self.root.ids.contact_indicator.state = 'normal'

        if self.weather_active == '1':
            self.root.ids.weather_indicator.state = 'down'
        else:
            self.root.ids.weather_indicator.state = 'normal'


    """# ### INTERACTIVITY ### ## #
    # ## ### INTERACTIVITY ### ## #
    # ## ### INTERACTIVITY ### ## #
    """

    deleted_rows = []  # used by the undo func

    def default_row(self, data_set):
        """Called when adding a row, returning the default cat and blank text
        """

        if data_set == self.data_breaking:
            category = "BREAKING"
        elif data_set == self.data_obit:
            category = "OBIT"
        else:
            category = "NEWS"

        return {"category": category, "text": ""}

    def add_row(self, index=None):
        """Add a new row, called by the bottom bar '+' button or the individual row's '+'
        The bulk of this is a novelty feature that can be removed if needed, it provides an automatic 'GOOD MORNING
        BRITAIN (+ date) etc as the first row of the Generic dataset
        """
        data_set = eval(self.current_data_set)  # Determining which dataset is to have rows added to it. eval() converts
        # current_data_set from a string into a format that can be used. You'll see this in most functions
        if index is not None:  # insert the default_row at the index position
            if len(data_set) < 10:
                return data_set.insert(index, self.default_row(data_set))

        elif "generic" in self.current_data_set:  # If we're on the generic dataset and it holds no data, then the
            # first row will auto-populate with 'GOOD MORNING BRITAIN, ITS (DATE)...'
            if not data_set:
                # Retrieving the date and storing each element as a variable:
                weekday = datetime.today().strftime('%A').upper() + " "
                date = int((datetime.today().strftime('%d')))
                month = datetime.today().strftime('%B').upper() + " "
                year = str(datetime.today().year)

                if 4 <= date <= 20 or 24 <= date <= 30:  # Determining which numerical date gets the appropriate date
                    # suffix. First statement selects numbers between 4 - 20 and(or) 24 - 30
                    suffix = "th "
                else:
                    # Else (remainder of date / 10) - 1
                    # e.g. remainder of 3 / 10 = 3, 3 - 1 = 2. Indicating we want to use index 2 in the suffix list
                    suffix = ["st ", "nd ", "rd "][date % 10 - 1]

                return data_set.append({"category": "NEWS", "text": "GOOD MORNING BRITAIN IT'S " + weekday + str(date)
                                                                    + suffix + month + year})
        if len(data_set) < 10:
            return data_set.append(self.default_row(data_set))  # Append a default row if no index provided

    def remove_row(self, row_index=None):
        """Opposite of add row. Pops row from dataset at index position. Also appends deleted item to a list to be
        recalled by the undo function
        """
        data_set = eval(self.current_data_set)
        if data_set:
            self.deleted_rows.append([row_index, self.data_generic[row_index]])
            return data_set.pop(row_index)

    def move_row_up(self, index):
        """Rows are moved by storing the row contents in a temp var (moving row), deleting it and then inserting it
        back into the dataset + or - an index position.
        """
        data_set = eval(self.current_data_set)

        if index > 0:
            moving_row = data_set[index]
            data_set.pop(index)
            return data_set.insert(index - 1, moving_row)

    def move_row_down(self, index):
        data_set = eval(self.current_data_set)
        moving_row = data_set[index]
        data_set.pop(index)
        return data_set.insert(index + 1, moving_row)

    def clear_each_row(self):
        """This function clears all rows by clearing the entire data_set list of dicts to []
        A popup will confirm the change"""
        data_set = eval(self.current_data_set)
        if 'generic' in self.current_data_set:
            self.data_generic.clear()
        elif 'break' in self.current_data_set:
            self.data_breaking.clear()
        else:
            self.data_obit.clear()
        return data_set.reverse(), data_set.reverse()

    def toggle_contact(self, state):
        """Turn the contact button on/off, store it's state in the slicker.ini so that it remains unchanged through
        application exit. Also sends a command to the 'UPDATE TICKER' button to prompt user for update"""
        kvconfg = Config
        kvconfg.read("slicker.ini")
        if state == 'normal':
            kvconfg.set('main', 'contact_bool', '0')
        else:
            kvconfg.set('main', 'contact_bool', '1')
        with open('slicker.ini', 'w'):
            kvconfg.write()
        self.update_btn_status('not_updated')

    def toggle_weather(self, state):
        """Same as above but for the weather button"""
        kvconfg = Config
        kvconfg.read("slicker.ini")
        if state == 'normal':
            kvconfg.set('main', 'weather_bool', '0')
        else:
            kvconfg.set('main', 'weather_bool', '1')
        with open('slicker.ini', 'w'):
            kvconfg.write()
        self.update_btn_status('not_updated')

    def show_contact_weather_btns(self, tab):
        """Remove the contact and weather buttons from the breaking and obit tabs.
        Replace them in the correct state when returning back to the generic tab"""
        kvconfg = Config
        kvconfg.read("slicker.ini")
        contact_active = int(kvconfg.get('main', 'contact_bool'))
        weather_active = int(kvconfg.get('main', 'weather_bool'))

        if tab == 'generic':
            self.root.ids.contact_indicator.text = 'CONTACT'
            if contact_active == 1:
                print('cont down')
                self.root.ids.contact_indicator.state = 'down'
            else:
                print('cont normal')
                self.root.ids.contact_indicator.state = 'normal'

            self.root.ids.weather_indicator.text = 'WEATHER'
            if weather_active == 1:
                print('weather down')
                self.root.ids.weather_indicator.state = 'down'
            else:
                print('weather normal')
                self.root.ids.weather_indicator.state = 'normal'
        else:
            self.root.ids.contact_indicator.text = ''
            self.root.ids.weather_indicator.text = ''
            self.root.ids.contact_indicator.state = 'normal'
            self.root.ids.weather_indicator.state = 'normal'

    def maestro_popup(self):
        if self.show_maestro_reminder:
            Popups.maestro_reminder(self.current_data_set, self.current_data_set)

    def do_not_show_maestro_reminder(self):
        self.show_maestro_reminder = False

    """# ### DATA RELATED FUNCTIONS ### ## #
    # ## ### DATA RELATED FUNCTIONS ### ## #
    # ## ### DATA RELATED FUNCTIONS ### ## #
    """

    def set_data_set(self, data_set_title):
        """When the user moves to a different tab this function is run and the variable 'current_data_set' is changed.
        """
        self.current_data_set = data_set_title

    def update_data(self, index, prop, value, data_set):
        """Called on every key stroke, category change or adjustment to the row positions/quantities.
        """
        eval(data_set)[index][prop] = value
        self.placeholder = ""

    def update_dbs(self):
        """Called when the cursor moves to any alternate row.
        This func was being triggered twice on every call, so a switch for send_data is set to only call
        update_databases on every other pass through"""

        data_set = eval(self.current_data_set)

        update_databases.prepare_data_for_sql(self.current_data_set, data_set)
        update_databases.update_excel_wall(self.current_data_set, data_set)
        # update_databases.update_excel_backup(self.current_data_set, data_set)

    def update_btn_status(self, status):

        if status == 'updated':
            self.root.ids.update_btn_ticker.color = (1, 1, 1, 1)
            self.root.ids.update_btn_ticker.text = 'TICKER UPDATED'
        else:
            self.root.ids.update_btn_ticker.color = (0.992, 0.407, 0.407, 1)
            self.root.ids.update_btn_ticker.text = 'UPDATE TICKER'

    """# ### SPELL CHECK FUNCTIONS ### ## #
    # ## ### SPELL CHECK FUNCTIONS ### ## #
    # ## ### SPELL CHECK FUNCTIONS ### ## #
    """

    personal_dict = "C:\\Program Files\\Slicker\\settings\\personal_dictionary.txt"  # Location of custom person dictionary
    spellcheck = enchant.DictWithPWL("en_GB", personal_dict)  # Sets the dictionaries for which all spelling checks
    # will be referenced against
    spellcheck_bool = kvconfg.getint('main', 'spellcheck_bool')  # Check if spellcheck is on/off from the last session
    flagged_word_and_suggestions = []  # List of recommended words fetched using spellcheck.suggest()

    def spell_check(self, index):
        """The initial spell_check function that paves the way for the following related funcs
        """
        try:
            if self.spellcheck_bool:  # IF spellcheck is set to True in settings
                text = eval(self.current_data_set)[index]['text']  # Pull the item text from the current row
                clean_text = text.translate(str.maketrans(void_chars))  # Strip it of all non-alphabet characters
                sentence = clean_text.split()  # Add each word to a list as a new element

                if not all(self.spellcheck.check(word) for word in sentence):  # Iterate through sentence, if the word
                    for word_bad in sentence:  # Iterate through sentence
                        if len(word_bad) > 2:  # If the word more 3+ characters
                            if not self.spellcheck.check(word_bad):  # If word fails spellcheck
                                self.root.ids.spell_check_spinner.text = 'RUN SPELLCHECK'  # Adjust spellcheck bar
                                self.root.ids.spell_check_spinner.color = 0.992, 0.407, 0.407
        except IndexError:
            print('OUT OF RANGE')

    def run_spell_check_on_all_text(self):
        """Spinner is Kivy's term for a button, that when clicked produces a dropdown menu with variable options.
        This function sets the values of the spinner in the bottom left hand corner of the GUI.
         """
        try:
            if self.spellcheck_bool:  # if spellch on
                for index, each_row in enumerate(eval(self.current_data_set)):  # loop through each row, adding index
                    # store list of words with row index
                    each_organised_row = (index, (each_row['text']).translate(str.maketrans(void_chars)).split())
                    # go through each word
                    for word in each_organised_row[1]:
                        # if word is spelt incorrectly
                        if not self.spellcheck.check(word):
                            # self.FWS = row index, bad words and list of suggestions
                            self.flagged_word_and_suggestions = (index, word, self.spellcheck.suggest(word)[:3])
                            # add top spinner value
                            self.flagged_word_and_suggestions[2].insert(0, 'FLAGGED WORD: ' +
                                                                        '[color=#fd6868]' + word + '[/color]')
                            # add bottom spinner value
                            self.flagged_word_and_suggestions[2].insert(1, 'ADD TO DICTIONARY')

                            self.flagged_word_and_suggestions[2].append('IGNORE')
                            # update spinner values
                            self.root.ids.spell_check_spinner.values = self.flagged_word_and_suggestions[2]
                            # close loop
                            return self.flagged_word_and_suggestions

                # This section of code cycles through every word and if no spelling errors are flagged the spellcheck
                # bar is updated with 'spellcheck complete!'
                new_list = []
                for row in eval(self.current_data_set):
                    for word in (row['text']).translate(str.maketrans(void_chars)).split():
                        new_list.append(word)

                if all(self.spellcheck.check(word) for word in new_list):
                    self.flagged_word_and_suggestions = []
                    self.root.ids.spell_check_spinner.values = []
                    self.root.ids.spell_check_spinner.color = 1, 1, 1
                    self.root.ids.spell_check_spinner.text = 'SPELLCHECK COMPLETE!'
        except:
            'brokeh'

    def spinner_choice(self, btn_text):
        """If 'add to dictionary'  selected fromm the spinner then the flagged word is added to
         the personal word list and not flagged again.
         """

        try:

            if self.flagged_word_and_suggestions:  # if a word is flagged
                if btn_text == 'ADD TO DICTIONARY' or btn_text == 'IGNORE':  # if dict button is pressed
                    self.spellcheck.add_to_pwl(self.flagged_word_and_suggestions[1])  # add new word to personal dict

                    self.root.ids.spell_check_spinner.trigger_action(0.3)  # trigger the spellcheck button again so it
                    # continues looping through all text looking for spelling errors
                    self.root.ids.spell_check_spinner.text = 'SPELLCHECK COMPLETE!'

                elif 'WORD:' in btn_text:
                    self.root.ids.spell_check_spinner.text = 'RUN SPELLCHECK'

                elif btn_text in self.flagged_word_and_suggestions[2]:
                    # if new word is selected send to func below
                    self.replace_word(btn_text)

        except:
            print('brokeh')

    def replace_word(self, btn_text):
        """This function replaces the incorrect, flagged word and replaces it with the selected suggested word.
        """
        try:
            data_set = eval(self.current_data_set)  # What data set are we working with.

            # replace the old bad word with the new choice and save it as a new_line of text
            new_line = data_set[self.flagged_word_and_suggestions[0]]['text'].replace \
                (self.flagged_word_and_suggestions[1], btn_text)

            # Replace the whole body of text from the relevant dict
            data_set[self.flagged_word_and_suggestions[0]]['text'] = new_line

            # trigger the spellcheck button again so it continues looping through all text looking for spelling errors
            self.root.ids.spell_check_spinner.trigger_action(0.3)

            # quickly reverse the data twice to refresh the widgets (couldn't fund a better way to do this)
            return data_set.reverse(), data_set.reverse()
        except:
            print('brokeh')

    """  SETTINGS PAGE CONFIG & FUNCTIONS ## #
    # ## SETTINGS PAGE CONFIG & FUNCTIONS ## #
    # ## SETTINGS PAGE CONFIG & FUNCTIONS ## #
    
    Kivy comes with a pre-defined settings module that let's the user change parameters of graphics, logging etc
    I've disabled the default settings page (all can also be adjust manually in slicker.ini) and entered some custom
    settings pages specific to the ticker app.
    """

    # todo: Give bool value to each category in the settings page so the on/off switches have a function

    def build_settings(self, settings):
        """The settings module pulls it's functionality and layout info from a local JSON file, settings_json.py
        I pick the order in which to add them:
        """
        settings.add_json_panel('General',
                                self.kvconfg,
                                data=gen_settings_json)

        settings.add_json_panel('Categories',
                                self.kvconfg,
                                data=custom_cats_json)

        settings.add_json_panel('Contact Information',
                                self.kvconfg,
                                data=contact_json)

        settings.add_json_panel('Help & Tips',
                                self.kvconfg,
                                data=help_json)

        settings.add_json_panel('About',
                                self.kvconfg,
                                data=about_json)

    # Variables used by the func below:
    new_cat = ""
    target_cat = ""

    def on_config_change(self, config, section, key, value):
        """When any change is made within the settings page this function is fired, passing with it 4 arguments:
        config = slicker.ini, section = which [section] of the .ini, key = white .ini text, value = green text"""

        """GENERAL PAGE
        """

        if key == 'contact_bool' and value == '1':
            self.root.ids.contact_indicator.text = 'C ON'
        elif key == 'contact_bool' and value == '0':
            self.root.ids.contact_indicator.text = 'C OFF'

        if key == 'weather_bool' and value == '1':
            self.root.ids.weather_indicator.text = 'W ON'
        elif key == 'weather_bool' and value == '0':
            self.root.ids.weather_indicator.text = 'W OFF'

        # When the spellcheck switch is toggled in the settings its value within slicker.ini changes between 0 & 1 and
        # and a local reference is also stored in a class var to keep track within the session
        if key == 'spellcheck_bool' and value == '1':
            self.spellcheck_bool = True
        elif key == 'spellcheck_bool' and value == '0':
            self.spellcheck_bool = False


        """CATEGORY PAGE
        """
        # When a new category is entered into the settings it's stored in a class var to be used by other functions
        if key == 'add_new_cat':
            self.new_cat = value

        # Triggered by the add button
        if value == 'add_cat':
            self.popups.category_added()  # Displays a message confirming the new addition
            for (each_key, each_value) in self.kvconfg.items('cats'):  # Using the kivy configparser to read the .ini
                # loop through each item in the [cats] section

                if not each_value:  # Until it hits a key without a value
                    self.kvconfg.set('cats', each_key, self.new_cat)  # At that point set the new category as its value
                    with open('slicker.ini', 'w'):
                        return self.kvconfg.write()  # write to .ini and return to break the loop

        # Sets the selection from the drop down list of cats as a variable to be used in the del statement below
        if key == 'category_list':
            self.target_cat = value

        # Triggered by the delete button
        if value == 'del_cat':
            self.popups.category_deleted(self.target_cat)  # Displays a message confirming the deletion
            for (each_key, each_value) in self.kvconfg.items('cats'):  # Using the kivy configparser to read the .ini
                # loop through each item in the [cats] section

                if each_value == self.target_cat:  # When loop reaches the target_cat set previously, it replaces the
                    # key's value with an empty string
                    self.kvconfg.set('cats', each_key, "")
                    with open('slicker.ini', 'w'):
                        return self.kvconfg.write()  # write to .ini and return to break the loop

        # I'm yet to work out how to 'refresh' the settings, or the entire App without restarting the whole application
        # For now this is the best solution. All data is quickly pulled from the SQL on load anyway, so it's just a few
        # seconds downtime for a task that will very rarely be used.
        if value == 'refresh_cats':
            os.execvp(sys.executable, ['python'] + sys.argv)  # execvp func replaces the running process image with a
            # new process, sys.executable to get the Python path. This may only work running the app from cmd, once
            # compiled it may need adjusting

    """# ### MISC FUNCTIONS ### ## #
    # ## ### MISC FUNCTIONS ### ## #
    # ## ### MISC FUNCTIONS ### ## #
    """

    def not_conf(self):
        """Popup function"""
        self.root.ids.obit_queue_btn.state = 'normal'

    def unqueue_generic(self):
        """Popup function"""
        self.root.ids.generic_queue_btn.state = 'down'


SlickerApp().run()  # RUN!!
