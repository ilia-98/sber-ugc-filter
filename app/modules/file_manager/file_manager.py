import urllib.request
from datetime import datetime
from settings import UCGFilterSettings
import os


DT_FORMAT = "%d%m%Y%H%M%S"


class FileManger:

    def __init__(self) -> None:
        self.file_manager_settings = UCGFilterSettings().file_manager_settings
        self.media_folder = self.file_manager_settings['media_folder']

    def get_videofile_from_url_source(self, url: str):

        path_to_file = f'{self.media_folder}{datetime.now().strftime(DT_FORMAT)}.mp4'
        path_to_folder, file_name = os.path.split(path_to_file)
        urllib.request.urlretrieve(
            url, path_to_file)
        return file_name
