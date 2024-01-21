import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

import SpeechSynth as ss


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self._init_boundary()
        self._init_message()
        self._init_systray()
        
    def _init_boundary(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            qtw.QStyle.alignedRect(
                Qt.LeftToRight, Qt.AlignCenter,
                QSize(440, 64),
                qApp.desktop().availableGeometry()
            )
        )
        
    def _init_message(self):
        self.message = qtw.QLineEdit()
        self.tts = ss.SpeechSynth()
        
        font = self.message.font()
        font.setPointSize(27)
        
        self.message.setFont(font)
        self.message.installEventFilter(self)
        self.setCentralWidget(self.message)
        
    def _init_systray(self):
        
        def openDict():
            import subprocess as sp
            
            programName = "notepad.exe"
            fileName = "userDict.txt"
            editing = sp.Popen([programName, fileName])
            editing.wait()

        # Adding an icon 
        icon = QIcon("icon.ico") 
        
        # Adding item on the menu bar 
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
        # TODO: Settings Action
        dictAction.triggered.connect(openDict)
        
        menu = QMenu() 
        menu.addAction(showAction) 
        menu.addAction(hideAction)
        menu.addAction(quitAction) 
        menu.addAction(settingsAction) 
        menu.addAction(dictAction)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
    
    def eventFilter(self, obj, event):
        if event.type() == qtc.QEvent.KeyPress and obj is self.message:
            if event.key() == Qt.Key_Return and self.message.hasFocus():
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
    app.exec_()