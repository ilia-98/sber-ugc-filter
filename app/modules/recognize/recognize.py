import os
from moviepy.editor import VideoFileClip, AudioFileClip

from app.modules.recognize.vosk_transcriber import VOSKTranscriber
from app.modules.recognize.audio_recognizer import AudioRecognizer
from ..file_manager import FileManger
from typing import Dict, List, Tuple
import numpy as np
from ..model import ModelRecognize, AreaCoordinates
from PIL import Image, ImageFilter


SAVING_FRAMES_PER_SECOND = 2


class ContentRecognize:

    def __init__(self) -> None:
        self.file_service = FileManger()
        self.vosk_transcriber = VOSKTranscriber()
        self.find_celebritis_service = ModelRecognize()
        self.audio_recognizer = AudioRecognizer()
        self.height_of_video = 0

    def recognize_ugc(self, source: str, prefix: str):
        path_to_file = self.file_service.get_videofile_from_url_source(source)

        clip = VideoFileClip(path_to_file)
        self.height_of_video = clip.h

        # Отсечение аудио от видео и отправка на проверку
        audio = clip.audio
        audio, audio_dict = self.recognize_audio(audio)
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
        audio_file_path = self.file_service.save_audio_file_clip(audio_clip, 'audio.wav')
        transcribed_text = self.vosk_transcriber.transcribe(audio_file_path)
        result = self.audio_recognizer.recognize(transcribed_text)
        return audio_clip, result

    def recognize_video_without_audio(self, video_clip: VideoFileClip) -> Tuple[VideoFileClip, Dict]:
        found_celebrities = {}
        temp_image_file, ext = os.path.splitext(video_clip.filename)
        saving_frames_per_second = min(
            video_clip.fps, SAVING_FRAMES_PER_SECOND)
        step = 1 / saving_frames_per_second
        for current_duration in np.arange(0, video_clip.duration, step):

            frame_filename = f'{temp_image_file}.jpg'
            video_clip.save_frame(frame_filename, current_duration)
            areas_for_blur = self.check_for_celebrities(frame_filename)

            if not areas_for_blur:
                continue

            self.area_blur(areas_for_blur, frame_filename)

    def check_for_celebrities(self, img):
        recognized_faces = self.find_celebritis_service.find_celebrities(img)
        areas_for_blur = []
        for face in recognized_faces:
            if face[0] != 'unknow':
                areas_for_blur.append(
                    self.find_celebritis_service.get_coordinates(face[1]))

        return areas_for_blur

    def area_blur(self, areas: List[AreaCoordinates], path_to_image):
        image = Image.open(path_to_image)
        for area in areas:
            croped_image = image.crop(area.coordinates_to_blur)
            blured_image = croped_image.filter(
                ImageFilter.GaussianBlur(radius=20))
            image.paste(
                blured_image, area.left_upper)
            image.save(path_to_image)
