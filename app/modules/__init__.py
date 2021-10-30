from .recognize import ContentRecognize
from .file_manager import FileManger


class ContainerService:

    _recongize_service: ContentRecognize
    _file_service: FileManger

    def __init__(self) -> None:
        self._file_service = FileManger()
        self._recongize_service = ContentRecognize()


container_service = ContainerService()
