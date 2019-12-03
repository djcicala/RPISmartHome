#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: gui.py                                                           *
* Purpose:   Methods and functions pertaining to the GUI module.              *
* Date:      11/26/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "0.1.1"

# imports
import configs
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
  QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
  QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
  QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
  QVBoxLayout, QWidget, QMessageBox)
import sys
import time
import urllib.request
import json
import functools
import datetime

class WidgetGallery(QDialog):

  def __init__(self, parent=None):
    super(WidgetGallery, self).__init__(parent)
    self.setWindowTitle("Raspberry Pi Smarthome")
    self.setFixedSize(1300,700)
    
    mainLayout = QGridLayout()
    self.createMenu()
    self.createSysInfo()
    self.closeEvent = self.closeWindow
    mainLayout.addWidget(self.menu,   0,0,4,12)
    mainLayout.addWidget(self.sysinfo,5,0,3,3)
    self.setLayout(mainLayout)

  def closeWindow(self, event):
    global run_log_csv_writer_thread
    print("close?")
    box = QMessageBox()
    box.setIcon(QMessageBox.Question)
    box.setWindowTitle('Please confirm!')
    box.setText('Really Exit?')
    box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
    box.setFixedSize(600,250)
    buttonY = box.button(QMessageBox.Yes)
    buttonY.setText('YES')
    buttonY.setFixedSize(200,100)
    buttonY.setStyleSheet('QPushButton {font: bold;color: gray;font-size:30px;border-style: outset; border-width: 2px; border-color: black;border-radius: 10px;}')
    buttonN = box.button(QMessageBox.No)
    buttonN.setText('NO')
    buttonN.setFixedSize(200,100)
    buttonN.setStyleSheet('QPushButton {font: bold;font-size:30px;border-style: outset; border-width: 2px; border-color: black;border-radius: 10px;}')
    box.exec_()
    if box.clickedButton() == buttonY:
      event.accept()
      print('closing!')
      run_log_csv_writer_thread = False
    elif box.clickedButton() == buttonN:
      event.ignore()
      
      
  def createMenu(self):
      
    self.menu = QGroupBox("Forecast")
    layout = QGridLayout()
    self.GPSLabel = []
    for i in range(0,12):
      x = i * 4
      for j in range (0,4):
#        if j == 0:
#          label = QLabel()
#          pixmap = QPixmap("Images/sunny.png")
#          label.setPixmap(pixmap)
#          self.GPSLabel.append(label)
#        else:
        label = QLabel("This is a fairly long test")
        label.setFixedSize(50,10)
        self.GPSLabel.append(label)
        self.GPSLabel[x + j].setStyleSheet('QLabel {color:red;font: bold; font-size: 12px}')
        layout.addWidget(self.GPSLabel[x + j], j, i)   
                 
    self.menu.setLayout(layout)
    
  def createSysInfo(self):
      
    self.sysinfo = QGroupBox("System Info")
    layout = QGridLayout()
    self.TestLabel = []
    for i in range(0,3):
      x = i * 3
      for j in range (0,3):
        if j == 0:
          label = QLabel()
          pixmap = QPixmap("Images/sunny.png")
          label.setPixmap(pixmap)
          label.setFixedSize(50,50)
          self.TestLabel.append(label)
        else:
          label = QLabel(str(i) + " " + str(j))
          label.setFixedSize(50,50)
          self.TestLabel.append(label)
        self.TestLabel[x + j].setStyleSheet('QLabel {color:red;font: bold; font-size: 12px}')
        layout.addWidget(self.TestLabel[x + j], j, i)
    
    self.buttonCoAsst = QPushButton('NEW API CALL')
    self.buttonCoAsst.clicked.connect(functools.partial(self.UpdateSysInfo, None))  
    layout.addWidget(self.buttonCoAsst,0,2)
                 
    self.sysinfo.setLayout(layout)

  def UpdateSysInfo(self, ApiJson=None):
    if(ApiJson == None):
      s_Contents = urllib.request.urlopen(configs.s_FullAPI).read().decode("utf-8") 
      # dump the return string into a dictionary
      self.d_ForecastInformation = json.loads(s_Contents)
      # capture the hourly forecasts for ease of access 
      self.l_HourlyForecasts = self.d_ForecastInformation["hourly"]["data"]
    
    for i in range(len(self.GPSLabel)):
      if i % 4 == 0:
        x = self.l_HourlyForecasts[i % 12]["time"]
        y = datetime.datetime.fromtimestamp(x)
        self.GPSLabel[i].setText(y.strftime("%H:%M"))
      if i % 4 == 1:
        self.GPSLabel[i].setText(str(self.l_HourlyForecasts[i % 12]["icon"]))
      if i % 4 == 2:
        self.GPSLabel[i].setText(str(self.l_HourlyForecasts[i % 12]["temperature"]))
      if i % 4 == 3:
        self.GPSLabel[i].setText(str(self.l_HourlyForecasts[i % 12]["precipProbability"]))

if __name__ == "__main__":
  app = QApplication(sys.argv)
  gallery = WidgetGallery()
  gallery.show()
  sys.exit(app.exec_()) 
  gallery.TestLabel[3].setText("This is also a test")
################################## end file ###################################
