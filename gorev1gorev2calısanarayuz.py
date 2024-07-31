import sys
import subprocess
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import threading
import tkinter as tk
from tkinter import simpledialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(914, 665)
        MainWindow.setStyleSheet("background-color: rgb(230, 237, 244);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        
        self.GOREV1 = QtWidgets.QGroupBox(self.centralwidget)
        self.GOREV1.setGeometry(QtCore.QRect(0, 440, 251, 191))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setBold(True)
        font.setWeight(75)
        self.GOREV1.setFont(font)
        self.GOREV1.setStyleSheet("background-color: rgb(255, 225, 205);")
        self.GOREV1.setFlat(False)
        self.GOREV1.setCheckable(False)
        self.GOREV1.setChecked(False)
        self.GOREV1.setObjectName("GOREV1")

        self.g1baslat = QtWidgets.QPushButton(self.GOREV1)
        self.g1baslat.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.g1baslat.setStyleSheet("background-color: rgb(205, 255, 205);")
        self.g1baslat.setObjectName("g1baslat")

        self.g1durdur = QtWidgets.QPushButton(self.GOREV1)
        self.g1durdur.setGeometry(QtCore.QRect(50, 20, 41, 16))
        self.g1durdur.setStyleSheet("background-color: rgb(255, 255, 187);")
        self.g1durdur.setObjectName("g1durdur")

        
        self.GOREV2 = QtWidgets.QGroupBox(self.centralwidget)
        self.GOREV2.setGeometry(QtCore.QRect(260, 440, 251, 191))
        font.setBold(True)
        font.setWeight(75)
        self.GOREV2.setFont(font)
        self.GOREV2.setStyleSheet("background-color: rgb(255, 225, 205);")
        self.GOREV2.setFlat(False)
        self.GOREV2.setCheckable(False)
        self.GOREV2.setChecked(False)
        self.GOREV2.setObjectName("GOREV2")

        self.g2baslat = QtWidgets.QPushButton(self.GOREV2)
        self.g2baslat.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.g2baslat.setStyleSheet("background-color: rgb(205, 255, 205);")
        self.g2baslat.setObjectName("g2baslat")

        self.g2durdur = QtWidgets.QPushButton(self.GOREV2)
        self.g2durdur.setGeometry(QtCore.QRect(50, 20, 41, 16))
        self.g2durdur.setStyleSheet("background-color: rgb(255, 255, 187);")
        self.g2durdur.setObjectName("g2durdur")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ana Sayfa"))
        self.GOREV1.setTitle(_translate("MainWindow", "Görev 1"))
        self.g1baslat.setText(_translate("MainWindow", "Başlat"))
        self.g1durdur.setText(_translate("MainWindow", "Durdur"))
        self.GOREV2.setTitle(_translate("MainWindow", "Görev 2"))
        self.g2baslat.setText(_translate("MainWindow", "Başlat"))
        self.g2durdur.setText(_translate("MainWindow", "Durdur"))

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.capture_thread_event = threading.Event()
        self.is_capturing = False
        self.process1 = None
        self.process2 = None

        self.g1baslat.clicked.connect(self.start_task1)
        self.g1durdur.clicked.connect(self.stop_task1)
        self.g2baslat.clicked.connect(self.start_task2)
        self.g2durdur.clicked.connect(self.stop_task2)

    def capture_frame(self):
        video_capture = cv2.VideoCapture(0)
        while self.is_capturing:
            ret, frame = video_capture.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = frame_rgb.shape
                q_img = QtGui.QImage(frame_rgb.data, width, height, 3 * width, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(q_img)
                scaled_pixmap = pixmap.scaled(self.label_3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.label_3.setPixmap(scaled_pixmap)
                
            self.capture_thread_event.wait(0.1)
        video_capture.release()

    def start_task1(self):
        if self.process1 is None or self.process1.poll() is not None:
            script_path = os.path.join(os.path.expanduser("~"), "Desktop", "gorev1", "CircleDetector.py")
            if os.path.exists(script_path):
                self.process1 = subprocess.Popen(["python", script_path])
            else:
                print("Script bulunamadı: ", script_path)

    def stop_task1(self):
        if self.process1 and self.process1.poll() is None:
            self.process1.terminate()
            self.process1 = None

    def start_task2(self):
        if self.process2 is None or self.process2.poll() is not None:
            script_path = os.path.join(os.path.expanduser("~"), "Desktop", "gorev2", "line_detection.py")
            if os.path.exists(script_path):
                self.process2 = subprocess.Popen(["python", script_path])
            else:
                print("Script bulunamadı: ", script_path)

    def stop_task2(self):
        if self.process2 and self.process2.poll() is None:
            self.process2.terminate()
            self.process2 = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
