from moviepy.video.io.VideoFileClip import VideoFileClip

from ..file_manager import FileManger


class ContentRecognize:

    def __init__(self) -> None:
        self.file_service = FileManger()

    def recognize_video(self, source: str, prefix: str):

        audio_dict = {
           "result": [
               {
                   "time_start":1.23456,
                   "time_end":2.3456
               },
               {
                   "time_start":3.23456,
                   "time_end":4.3456
               }
           ]
        }
        video_dict = {
           "result": [
               {
                   "time_start": 1.23456,
                   "time_end": 2.3456,
                   "corner_1": [123, 456],
                   "corner_2": [321, 654]
               },
               {
                   "time_start": 3.23456,
                   "time_end": 4.3456,
                   "corner_1": [213, 546],
                   "corner_2":[312, 654]
               }
           ]
        }
        path_to_file = self.file_service.get_videofile_from_url_source(source)
        self.file_service.put_files_to_s3_bucket(audio_dict, video_dict, VideoFileClip(path_to_file), prefix)
        return 'ok'
