from __future__ import annotations
from typing import Optional
from threading import Lock
from os.path import dirname, realpath
from yaml import safe_load


class SingletonMeta(type):

    _instance: Optional[UGCFilterSettings] = None

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    def reset(cls):
        cls._instance = None


class UGCFilterSettings(metaclass=SingletonMeta):
    SETTINGS_FILENAME = "settings.yaml"
    APP_NAME = "ucg_filter"

    def __init__(self, settings_path=None) -> None:

        if not settings_path:
            path = dirname(realpath(__file__))
            settings_path = "{}/{}".format(path,
                                           UGCFilterSettings.SETTINGS_FILENAME)

        with open(settings_path, "r", encoding="utf-8") as ymlfile:
            self._config = safe_load(ymlfile)

    @property
    def app_settings(self):
        return self._config['app']

    @property
    def file_manager_settings(self):
        return self._config['file_manager']
