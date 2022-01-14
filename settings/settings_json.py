"""
The inbuilt Settings function of Kivy has been built to use a JSON file as it's constructor.
Each settings page is it's own JSON.dumps item, and within there each item is defined in its own dict.
"""

import json
from kivy.config import Config

kvconfg = Config
kvconfg.read("slicker.ini")


gen_settings_json = json.dumps([


    {'type': 'bool',
     'title': 'Spellcheck',
     'desc': 'Turn the spellcheck function on/off',
     'section': 'main',
     'key': 'spellcheck_bool'},

    {'type': 'title',
     'title': ''},

    {'type': 'numeric',
     'title': 'Character Limit',
     'desc': 'Set the character limit for the text input box. \n'
             'Restart the software to initialise rows with new limit',
     'section': 'main',
     'key': 'char_limit'}, ])


kustom_kats_json = [

    {'type': 'title',
     'title': ''},

    {"type": "string",
     "title": "Add a category",
     "desc": 'Click here to enter a new category, followed by add',
     "section": "main",
     "key": "add_new_cat"},

    {"type": "buttons",
     "title": " ",
     "section": "$var(InterfaceConfigSection)",
     "key": "config_change_buttons",
     "buttons": [{"title": "Add", "id": "add_cat"}]},

    {'type': 'title',
     'title': ''},

    {"type": "dynamic_options",
     "title": "Delete a Category",
     "desc": 'Select a category from the list, followed by delete',
     "section": "main",
     "key": "category_list"},

    {"type": "buttons",
     "title": " ",
     "section": "$var(InterfaceConfigSection)",
     "key": "config_change_buttons",
     "buttons": [{"title": "Delete", "id": "del_cat"}]},

    {"type": "buttons",
     "title": " ",
     "section": "$var(InterfaceConfigSection)",
     "key": "config_change_buttons",
     "buttons": [{"title": "Refresh", "id": "refresh_cats"}]},

    {'type': 'title',
     'title': ''},

    {'type': 'title',
     'title': 'Use with care. If you edit or delete a category which impacts the GUI negatively please manually'
              ' remove all categories then re-add them. The default, case sensitive categories are: NEWS, BREAKING,'
              ' ENTS, SPORT, WEATHER, CONTACT US'},

    {'type': 'title',
     'title': ''}
 ]

for (each_key, each_value) in kvconfg.items('cats'):
    if each_value:
        kustom_kats_json.append({'type': 'bool',
                                 'title': each_value,
                                 'section': 'cats_bool',
                                 'key': each_key})

custom_cats_json = json.dumps(kustom_kats_json)


contact_json = json.dumps([

    {'type': 'title',
     'title': ''},

    {'type': 'string',
     'title': 'Email',
     'section': 'main',
     'key': 'contact_email'},

    {'type': 'string',
     'title': 'Web',
     'section': 'main',
     'key': 'contact_web'},

    {'type': 'string',
     'title': 'Twitter',
     'section': 'main',
     'key': 'contact_twitter'},

    {'type': 'string',
     'title': 'Facebook',
     'section': 'main',
     'key': 'contact_fb'},

    {'type': 'title',
     'title': ''}])


help_json = json.dumps([

    {'type': 'title',
     'title': ''},

    {'type': 'title',
     'title': 'Add/remove rows to/from end of the list using the + / - in the bottom bar'
     },
    {'type': 'title',
     'title': 'Insert/delete rows from anywhere in the list by using that rows own - / + button'
     },
    {'type': 'title',
     'title': 'Use ctrl + a on the keyboard or triple click to select the whole contents of a text box'
     }
])

about_json = json.dumps([

    {'type': 'title',
     'title': ''},

    {'type': 'title',
     'title': 'Joe Edwards. ITV Daytime 2020...\n\n\n'
              'Contact: joeedwards88@gmail.com'
     }])

