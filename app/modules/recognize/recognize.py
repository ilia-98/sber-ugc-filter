import os
from moviepy.editor import VideoFileClip, AudioFileClip

from app.modules.recognize.vosk_transcriber import VOSKTranscriber
from app.modules.recognize.audio_recognizer import AudioRecognizer
from ..file_manager import FileManger
from typing import Dict, List, Tuple
import numpy as np
from ..model import ModelRecognize, AreaCoordinates
from PIL import Image, ImageFilter
from collections import defaultdict


SAVING_FRAMES_PER_SECOND = 2
LABEL_TIME_END = 'time_end'
LABEL_TIME_START = "time_start"
LABEL_CORNER_1 = "corner_1"
LABEL_CORNER_2 = "corner_2"
UNKNOWN = 'unknown'


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
        audio_file_path = self.file_service.save_audio_file_clip(
            audio_clip, 'audio.wav')
        transcribed_text = self.vosk_transcriber.transcribe(audio_file_path)
        result = self.audio_recognizer.recognize(transcribed_text)
        return audio_clip, result

    def recognize_video_without_audio(self, video_clip: VideoFileClip) -> Tuple[VideoFileClip, Dict]:
        found_celebrities = defaultdict(list)
        temp_image_file, ext = os.path.splitext(video_clip.filename)

        saving_frames_per_second = min(
            video_clip.fps, SAVING_FRAMES_PER_SECOND)
        step = 1 / saving_frames_per_second
        previous_rec = None

        for current_duration in np.arange(0, video_clip.duration, step):
            if current_duration > 30:
                break
            frame_filename = f'{temp_image_file}.jpg'
            video_clip.save_frame(frame_filename, current_duration)
            areas_for_blur = self.check_for_celebrities(frame_filename)
            if not areas_for_blur:
                previous_rec = None
                continue
            if previous_rec:
                current_names_celebrities = [
                    ar.celebrity for ar in areas_for_blur]
                previous_names_celebrities = [
                    ar.celebrity for ar in previous_rec]
                for name in current_names_celebrities:
                    if name in previous_names_celebrities:
                        found_celebrities[name][-1][LABEL_TIME_END] = current_duration
            for area in areas_for_blur:
                area_in_dict = found_celebrities[area.celebrity]
                if not area_in_dict or area_in_dict[-1][LABEL_TIME_END] != current_duration:
                    found_celebrities[area.celebrity].append(
                        {
                            LABEL_TIME_START: current_duration,
                            LABEL_TIME_END: current_duration,
                            LABEL_CORNER_1: [
                                area.coordinates_to_ret[0],
                                self.height_of_video -
                                area.coordinates_to_ret[1]
                            ],
                            LABEL_CORNER_2: [
                                area.coordinates_to_ret[2],
                                self.height_of_video -
                                area.coordinates_to_ret[3]
                            ],
                        }
                    )

            previous_rec = areas_for_blur
        to_ret = []
        for name, stamps in found_celebrities.items():
            for stamp in stamps:
                to_ret.append(stamp)
        return video_clip, to_ret

    def check_for_celebrities(self, img) -> List[AreaCoordinates]:
        recognized_faces = self.find_celebritis_service.find_celebrities(img)
        areas_for_blur = []
        for face in recognized_faces:
            if face[0] != UNKNOWN:
                areas_for_blur.append(
                    self.find_celebritis_service.get_coordinates(face[0], face[1]))

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
