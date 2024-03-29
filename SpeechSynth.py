import os, sys, json
from txtai.pipeline import TextToSpeech
import soundfile as sf
import AudioToMic as am

APPLICATION_PATH = os.path.dirname(sys.executable)
# APPLICATION_PATH = os.getcwd()

def applyUserDict(text: str):

    with open(f'{APPLICATION_PATH}/userDict.txt') as file:
        userDict = json.load(file)
    file.close()
    userDict["type"] = "dictionary"
    
    words = text.split()
    for i, word in enumerate(words):
        if word in userDict.keys():
            words[i] = userDict.get(word)
    return " ".join(words)

class SpeechSynth():
    def __init__(self):
        self.mic = am.AudioToMic()
        self.tts = TextToSpeech()
        
    def read(self, text: str):
        message = applyUserDict(text);  
        print(message)      
        speech, rate = self.tts(message), 22050
        try:
            sf.write(f'{APPLICATION_PATH}/speech.wav', speech, rate)
            self.mic.play(1)
        except:
            sf.write(f'{APPLICATION_PATH}/speech2.wav', speech, rate)
            self.mic.play(2)
        
    
