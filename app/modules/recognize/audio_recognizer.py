import datetime
import json
from typing import List, Dict

WORDS_PER_LINE = 3
CELEB_FILENAME = "modules/recognize/celeb_names.txt"

class AudioRecognizer:

    def __init__(self):
        with open(CELEB_FILENAME, "r", encoding="utf_8_sig") as file:
            content = file.read()
        self.celeb_names = content.split("\n")

    def recognize(self, transcribed_text: List[Dict]):
        timecodes = []
        for i, res in enumerate(transcribed_text):
            jres = json.loads(res)
            if not 'result' in jres:
                continue
            words = jres['result']
            for j in range(0, len(words), WORDS_PER_LINE):
                line = words[j: j + WORDS_PER_LINE]
                list_of_words = [l['word'] for l in line]
                founded = False
                for celeb_name in self.celeb_names:
                    count_of_founds = 0
                    splited_name = celeb_name.split(' ')
                    for search_word in celeb_name.split(' '):
                        if len(search_word) > 3:
                            founded_words = [x for x in list_of_words if search_word.lower() in x.lower()]
                            if founded_words:
                                count_of_founds += 1
                    if len(splited_name[0]) < 5 and count_of_founds < 2:
                        continue
                    if len(splited_name) > 1 and len(splited_name[1]) < 5 and count_of_founds < 2:
                        continue
                    if len(splited_name) > 2 and len(splited_name[2]) < 5 and count_of_founds < 2:
                        continue
                    if count_of_founds > 0:
                        founded = True
                        break
                if founded:
                    timecode = {
                        'start': datetime.timedelta(seconds=line[0]['start']).total_seconds(),
                        'end': datetime.timedelta(seconds=line[-1]['end']).total_seconds()
                    }
                    timecodes.append(timecode)
        return timecodes