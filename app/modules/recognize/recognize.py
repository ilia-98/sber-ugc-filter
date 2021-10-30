import os
from moviepy.editor import VideoFileClip, AudioFileClip
from ..file_manager import FileManger
from typing import Dict, Tuple
from datetime import timedelta
import numpy as np
SAVING_FRAMES_PER_SECOND = 25


class ContentRecognize:

    def __init__(self) -> None:
        self.file_service = FileManger()

    def recognize_ugc(self, source: str, prefix: str):
        path_to_file = self.file_service.get_videofile_from_url_source(source)
        filename, ext = os.path.splitext(path_to_file)

        clip = VideoFileClip(path_to_file)

        # Отсечение аудио от видео и отправка на проверку
        audio = clip.audio
        audio, audio_dict = result_of_recognize_audio = self.recognize_audio(
            audio)

        # Отсечение видео от аудио и отправка на проверку
        video_without_audio: VideoFileClip = clip.without_audio()
        video_without_audio, video_dict = self.recognize_video_without_audio(
            video_without_audio)

        resulting_video = video_without_audio
        resulting_video.audio = audio

        self.file_service.put_files_to_s3_bucket(
            audio_dict, video_dict, resulting_video, prefix)

        if audio_dict or video_dict:
            mes = 'Мentions of celebrities found'
        else:
            mes = 'Мentions of celebrities not found'
        return mes

    def recognize_audio(self, audio_clip: AudioFileClip) -> Tuple[AudioFileClip, Dict]:
        pass

    def recognize_video_without_audio(self, video_clip: VideoFileClip) -> Tuple[VideoFileClip, Dict]:
        for frame in video_clip.iter_frames():
            res = self.check_for_celebrities(frame)
            blur_frame = self.area_blur()

    def check_for_celebrities(self, frame):
        recognized_faces = []
        areas_for_blur = []
        for face in recognized_faces:
            if face[0] != 'unknow':
                areas_for_blur.append(face)

        return areas_for_blur

    def area_blur(self):
        pass
