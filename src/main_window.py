from settings.settings_window import SettingsWindow
from screenshot.screenshot import get_screenshot
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt
from settings.settings import current_settings
import time


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.settings_updated()
        self.setMouseTracking(True)

        self.imageLabel = QLabel(self)
        self.error_label = QLabel(self)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self._event_loop()

    
    def _event_loop(self):
        if self.isVisible():
            tic = time.perf_counter()
            self.set_image()
            toc = time.perf_counter()
            # print(f"Fetched image in {(toc - tic) * 1000:0.5f} milliseconds")

        QTimer.singleShot(1000, self._event_loop)


    def settings_updated(self):
        self.opacity = current_settings.get_opacity()
        
        pos = current_settings.get_frame_pos()
        self.move(pos[0], pos[1])


    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.black)) 
        painter.drawRoundedRect(self.rect(), 10, 10)  
        # painter.drawRect(self.rect())


    def set_image(self):
        self.error_label.hide()
        self.imageLabel.show()
        image, err = get_screenshot()
        if err != None:
            return self._show_error_message(err)

        qim = ImageQt(image)
        pix = QPixmap.fromImage(qim)
        self.imageLabel.setPixmap(pix)
        self.imageLabel.move(0, 0)
        self.imageLabel.resize(pix.width(),pix.height())
         
        self.resize(pix.width(),pix.height())


    def show_settings(self):
        self.settings = SettingsWindow(self)


    def _show_error_message(self, error):
        print("Show error: ", error)
        self.resize(220, 80)
        self.error_label.resize(220, 80)
        self.imageLabel.hide()
        self.error_label.setFont(QFont('Arial', 10))
        self.error_label.setText(error)
        self.error_label.setStyleSheet("color: white;")
        self.error_label.setWordWrap(True)
        self.error_label.move(0, 0)
        self.error_label.show()
