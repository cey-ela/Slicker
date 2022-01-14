"""
Does what it says on the tin. Everything pertaining to Popups is handled here and even more so in the corresponding
.kv file
This .py is just a set of links really
"""

from kivy.uix.popup import Popup


class ObitConfirmation(Popup):
    def do_obit(self):
        print("THEY DEAD")
        self.dismiss()

    def dont_obit(self):
        print("THEY ALIVE")
        self.dismiss()


class UnQueueGeneric(Popup):
    def do_unqueue(self):
        print("UNQUEUE GENERIC")
        self.dismiss()

    def dont_unqueue(self):
        print("DON'T UNQUEUE GENERIC")
        self.dismiss()


class CategoryAdded(Popup):
    pass


class CategoryDeleted(Popup):
    pass


class ClearAllConfirmation(Popup):
    pass


class DelRowConfirmation(Popup):
    index = None


class MaestroReminder(Popup):
    pass


class SQLWarning(Popup):
    pass


class WallWarning(Popup):
    pass


class BackupWarning(Popup):
    pass


class Popups:

    def obit_confirmation(self, state):
        if state == 'down':
            ObitConfirmation().open()

    def unqueue_generic_ticker(self, state):
        if state == 'normal':
            UnQueueGeneric().open()

    def category_added(self):
        CategoryAdded().open()

    def category_deleted(self, target_cat):
        if target_cat:
            CategoryDeleted().open()

    def clear_all_confirmation(self):
        ClearAllConfirmation().open()

    def delete_row_confirmation(self, index=None):
        DelRowConfirmation().open()
        DelRowConfirmation.index = index

    def maestro_reminder(self, data_set):
        if 'generic' in data_set:
            MaestroReminder().open()

    def sql_warning(self):
        SQLWarning().open()

    def wall_warning(self):
        WallWarning().open()

    def backup_warning(self):
        BackupWarning().open()
