from display import Display
from settings import Settings


class Manager:
    _title = 'MineSweeper'
    _background = (100, 100, 255)
    _instance = None

    def __new__(cls):
        if Manager._instance is not None:
            return Manager._instance

    def __init__(self):
        self.settings = Settings()
        self.display = Display(self.settings, self._title, self._background)
        Manager.__update_singleton(self)

    @staticmethod
    def get_setting(name):
        self = Manager.get_singleton()
        return self.settings(name)

    @staticmethod
    def get_display():
        self = Manager.get_singleton()
        return self.display

    @staticmethod
    def get_title():
        return Manager._title

    @staticmethod
    def get_background():
        return Manager._background

    @staticmethod
    def get_singleton():
        return Manager._instance if Manager._instance is not None else Manager()

    @staticmethod
    def __update_singleton(this):
        Manager._instance = this
