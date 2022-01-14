"""
The inbuilt Settings function for kivy is very clean but limited so a bit of gymnastics are needed to provide things
like a list of options and customised buttons
"""
from kivy.uix.settings import SettingsWithSidebar, SettingOptions, SettingItem
from kivy.uix.button import Button
from configparser import ConfigParser

config = ConfigParser()
config.read("C:\\Program Files\\Slicker\\slicker.ini")


category_list = []

for (each_key, each_value) in config.items('cats'):
    if each_value:
        category_list.append(each_value)


class SettingDynamicOptions(SettingOptions):
    """Called when pulling up the list of options and choosing one to delete.
    """

    def _create_popup(self, instance):
        # Update the options
        self.options = category_list
        # Call the parent __init__
        super(SettingDynamicOptions, self)._create_popup(instance)

    def _set_option(self, instance):
        self.value = instance.text
        self.popup.dismiss()


class SettingButtons(SettingItem):
    """Called to be able to have multiple buttons on one row """

    def __init__(self, **kwargs):
        self.register_event_type('on_release')

        kw = kwargs.copy()
        kw.pop('buttons', None)
        super(SettingItem, self).__init__(**kw)
        for aButton in kwargs["buttons"]:
            oButton = Button(text=aButton['title'], font_size='15sp')
            oButton.ID = aButton['id']
            self.add_widget(oButton)
            oButton.bind(on_release=self.On_ButtonPressed)

    def set_value(self, section, key, value):
        pass

    def On_ButtonPressed(self, instance):
        self.panel.settings.dispatch('on_config_change', self.panel.config, self.section, self.key, instance.ID)


class MySettings(SettingsWithSidebar):
    """ Customised settings panel."""

    def __init__(self, *args, **kargs):
        super(MySettings, self).__init__(*args, **kargs)
        self.register_type('dynamic_options', SettingDynamicOptions)
        self.register_type('buttons', SettingButtons)
