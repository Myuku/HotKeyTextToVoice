import os, sys
from pynput import keyboard

from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QSystemTrayIcon, QMenu, QAction, QErrorMessage, QStyle, QLineEdit
from PyQt5.QtCore import Qt, QSize, QObject, pyqtSignal, QEvent
from PyQt5.QtGui import QIcon

import SpeechSynth as ss

APPLICATION_PATH = os.path.dirname(sys.executable)
# APPLICATION_PATH = os.getcwd()

class Forwarder(QObject):
    signal = pyqtSignal()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self._init_boundary()
        self._init_message()
        self._init_systray()
        self.update()
        
    def _init_boundary(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.FramelessWindowHint
        )
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight, Qt.AlignCenter,
                QSize(440, 64),
                qApp.desktop().availableGeometry()
            )
        )
        
    def _init_message(self):
        self.message = QLineEdit()
        self.tts = ss.SpeechSynth()
        
        font = self.message.font()
        font.setPointSize(27)
        
        self.message.setFont(font)
        self.message.setPlaceholderText("Your Message...")
        self.message.installEventFilter(self)
        self.setCentralWidget(self.message)
        
    def _init_systray(self):
        def openDict():
            os.startfile(f'{APPLICATION_PATH}/userDict.txt')
            
        def errorPrompt():
            errorDialog = QErrorMessage()
            errorDialog.showMessage('Oh no!')
            errorDialog.setWindowTitle("Error")
            errorDialog.exec_()
            
        icon = QIcon(f'{APPLICATION_PATH}/icon.ico')  
        self.tray = QSystemTrayIcon(self) 
        self.tray.setIcon(icon) 
        self.tray.setVisible(True) 
        
        # Creating the options 
        showAction = QAction("Show", self) 
        hideAction = QAction("Hide", self)
        quitAction = QAction("Quit", self)
        settingsAction = QAction("Settings", self) 
        dictAction = QAction("Edit Dictionary", self)
        showAction.triggered.connect(self.show)
        hideAction.triggered.connect(self.hide)
        quitAction.triggered.connect(app.quit)
        settingsAction.triggered.connect(errorPrompt)
        dictAction.triggered.connect(openDict)
        
        menu = QMenu() 
        menu.addAction(showAction) 
        menu.addAction(hideAction)
        menu.addAction(quitAction) 
        menu.addAction(settingsAction) 
        menu.addAction(dictAction)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
    def hotkey(self):
        forwarder = Forwarder(parent=self)
        forwarder.signal.connect(self.wakeUp)

        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<alt>+x'), forwarder.signal.emit)
        listener = keyboard.Listener(
                on_press=for_canonical(hotkey.press),
                on_release=for_canonical(hotkey.release)
        )
        listener.start()
        
    def wakeUp(self):
        self.show()
        self.setFocus()
        self.raise_()
        self.activateWindow()
        self.message.setFocus()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.message:
            if event.key() == Qt.Key_Return:
                if len(self.message.text()) == 0:
                    self.hide()
                else: 
                    self.tts.read(self.message.text())
                    self.message.clear()
                    self.hide()
        return super().eventFilter(obj, event)    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    myWindow = MainWindow()
    myWindow.show()
    myWindow.hotkey()
    sys.exit(app.exec_())