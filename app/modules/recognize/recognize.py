from ..file_manager import FileManger


class ContentRecognize:

    def __init__(self) -> None:
        self.file_service = FileManger()

    def recognize_video(self, source: str, prefix: str):
        file_name = self.file_service.get_videofile_from_url_source(source)
        result = f'{prefix}_{file_name}'
        return result
