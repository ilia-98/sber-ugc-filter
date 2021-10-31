import json
import urllib.request
import boto3
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip
from settings import UGCFilterSettings
import os
import sys

from modules.file_manager import utils

FILE_NAME = 'video_file'
AWS_ACCESS_KEY_ID = 'CMG2SNAMOCRNGALFWXER'
AWS_SECRET_ACCESS_KEY = 'cCI4rfySaaInz6jfqy6KFftxC0LevVrnIvvxf5GV'
BUCKET_NAME = 'hackathon-ecs-11'
S3_HOST = "https://obs.ru-moscow-1.hc.sbercloud.ru"


class FileManger:

    def __init__(self) -> None:
        self.file_manager_settings = UGCFilterSettings().file_manager_settings
        self.media_folder = self.file_manager_settings['media_folder']

    # http://hackaton.sber-zvuk.com/hackathon_part_1.mp4
    def get_videofile_from_url_source(self, url: str) -> str:
        path_to_file = f'{self.media_folder}{FILE_NAME}.mp4'
        utils.remove_exists_file(path_to_file)
        # path_to_folder, file_name = os.path.split(path_to_file)
        print('Start downloading video')
        urllib.request.urlretrieve(url, path_to_file)
        return path_to_file

    def put_files_to_s3_bucket(self, audio_dict: dict, video_dict: dict,
                               video_result: VideoFileClip, prefix: str) -> None:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=S3_HOST,
            use_ssl=False,
            verify=False)

        audio_json_file_name = f'{prefix}_audio.json'
        video_json_file_name = f'{prefix}_video.json'
        video_result_file_name = f'{prefix}_result.mp4'

        audio_json_file_path = f'{self.media_folder}{audio_json_file_name}'
        video_json_file_path = f'{self.media_folder}{video_json_file_name}'
        video_result_file_path = f'{self.media_folder}{video_result_file_name}'

        utils.remove_exists_file(audio_json_file_path)
        utils.remove_exists_file(video_json_file_path)
        utils.remove_exists_file(video_result_file_path)

        utils.dict_to_json_file(audio_dict, audio_json_file_path)
        utils.dict_to_json_file(video_dict, video_json_file_path)

        video_result.write_videofile(video_result_file_path)
        video_result.close()

        s3_client.upload_file(
            audio_json_file_path,
            BUCKET_NAME,
            audio_json_file_name)
        s3_client.upload_file(
            video_json_file_path,
            BUCKET_NAME,
            video_json_file_name)
        s3_client.upload_file(
            video_result_file_name,
            BUCKET_NAME,
            video_result_file_name)

    def save_audio_file_clip(self, audio_file_clip: AudioFileClip, filename: str) -> str:
        audio_file_path = f'{self.media_folder}{filename}'
        audio_file_clip.write_audiofile(audio_file_path)
        return audio_file_path

