import urllib
from typing import Dict, List
from vosk import Model, KaldiRecognizer, SetLogLevel
import subprocess
import platform

SAMPLE_RATE = 16000
MODEL_PATH = "modules/recognize/vosk_model"


class VOSKTranscriber:

    def __init__(self):
        SetLogLevel(-1)
        self.rec = KaldiRecognizer(Model(MODEL_PATH), SAMPLE_RATE)
        self.rec.SetWords(True)

    def transcribe(self, audio_file_path: str) -> List[Dict]:
        results = []
        plt = platform.system()
        shell = False
        if plt == "Windows":
           shell = True
        process = subprocess.Popen(['ffmpeg',
                                    '-loglevel', 'quiet',
                                    '-i', audio_file_path,
                                    '-ar', str(SAMPLE_RATE),
                                    '-ac', '1',
                                    '-f', 's16le',
                                    '-'],
                                   stdout=subprocess.PIPE,
                                   shell=shell)
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                results.append(self.rec.Result())
        results.append(self.rec.FinalResult())
        return results
