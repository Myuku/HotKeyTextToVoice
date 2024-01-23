import os, sys, time
from pygame import mixer
from PyQt5.QtWidgets import QErrorMessage

APPLICATION_PATH = os.path.dirname(sys.executable)
# APPLICATION_PATH = os.getcwd()

class AudioToMic():
    def __init__(self):
        # Initialize it with the correct device
        mixer.init(devicename = 'CABLE Input (VB-Audio Virtual Cable)')
        if mixer.get_init() is None:
            print("hi")
            errorDialog = QErrorMessage()
            errorDialog.showMessage('Virtual Cable not initialized! \nPlease follow the instructions on GitHub.')
            errorDialog.setWindowTitle("Error!")
            errorDialog.exec_()
        
    def play(self, pos):
        if pos == 1:
            mixer.music.load(f'{APPLICATION_PATH}/speech.wav')
        else:   
            mixer.music.load(f'{APPLICATION_PATH}/speech2.wav')
        mixer.music.play()
        
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
