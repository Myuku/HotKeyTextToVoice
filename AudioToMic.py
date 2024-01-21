import time
from pygame import mixer


class AudioToMic():
    def __init__(self):
        # Initialize it with the correct device
        self.player = mixer.init(devicename = 'CABLE Input (VB-Audio Virtual Cable)')
        
    def play(self, pos):
        # mixer.music.stop()
        # mixer.music.unload()
        if pos == 1:
            mixer.music.load("speech.wav")
        else:   
            mixer.music.load("speech2.wav")
        mixer.music.play()
        
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
