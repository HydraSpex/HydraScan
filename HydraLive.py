import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import numpy as np
import random as random
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import threading

CH1 = "Channel 1"
CH2 = "Channel 2"
CH3 = "Channel 3"
CH4 = "Channel 4"
CHA = "Luminescence"
CHB = "Scattering"
L2 = "L2"
L3 = "L3"

xstart = 0
ystart = 0
xstop = 100
ystop = 100
upperLimit1 = 100
lowerLimit1 = 0
upperLimit2 = 100
lowerLimit2 = 0
InvertXLive1 = False
InvertYLive1 = False
InvertXLive2 = False
InvertYLive2 = False

zNew = list()
zNew2 = list()
zPart = list()
zPart2 = list()
x = xstart
y = ystart
while y <= ystop:
    while x <= xstop:
        zPart.append(0)
        zPart2.append(0)
        x += 1
    x = xstart
    y += 1
    zNew.append(zPart)
    zNew2.append(zPart2)
    zPart = list()
    zPart2 = list()

y, x = np.meshgrid(np.linspace(ystart,ystop,(ystop-ystart+1)), np.linspace(xstart,xstop,(xstop-xstart+1)))

v = np.linspace(xstart,xstop,(xstop-xstart+1))
t = np.sin(v)*np.sin(v)
tt = np.cos(v)*np.cos(v)


class CustomMainWindow(QWidget):
    def __init__(self):
        super(CustomMainWindow, self).__init__()
        self.Fontsize = 8
        self.Fontstyle = "Arial"
        global CH1
        global CH2
        global CH3
        global CH4
        global CHA
        global CHB
        global L2
        global L3

        self.CH1 = CH1
        self.CH2 = CH2
        self.CH3 = CH3
        self.CH4 = CH4
        self.CHA = CHA
        self.CHB = CHB
        self.L2 = L2
        self.L3 = L3
        
        # Define the geometry of the main window
        self.setGeometry(300, 300, 1600, 850)
        self.setMinimumSize(QSize(1600,600))   
        self.setWindowTitle("Live Plot")
        
        # Create a Layout
        self.LAYOUT_A = QHBoxLayout()
        
        # Place the zoom button
        self.ButtonRefreshScale1 = QPushButton(text = 'Refresh Scale')
        self.ButtonRefreshScale1.setFixedSize(150, 35)
        self.ButtonRefreshScale1.clicked.connect(self.RefreshScale1)
        self.ButtonRefreshScale1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
        
        self.ButtonSave = QPushButton(text = 'Save Plots')
        self.ButtonSave.setFixedSize(150, 35)
        self.ButtonSave.clicked.connect(self.SavePlots)
        self.ButtonSave.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

        self.ButtonAutoScale1 = QPushButton(text = 'Auto Scale')
        self.ButtonAutoScale1.setCheckable(True)
        self.ButtonAutoScale1.setFixedSize(130, 35)
        self.ButtonAutoScale1.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

        self.ButtonAutoScale2 = QPushButton(text = 'Auto Scale')
        self.ButtonAutoScale2.setCheckable(True)
        self.ButtonAutoScale2.setFixedSize(130, 35)
        self.ButtonAutoScale2.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

        self.InvertXAxisLive1 = QCheckBox("Invert X", self)
        self.InvertXAxisLive1.stateChanged.connect(self.InvertXChanged1)
        self.InvertYAxisLive1 = QCheckBox("Invert Y", self)
        self.InvertYAxisLive1.stateChanged.connect(self.InvertYChanged1)

        self.InvertXAxisLive2 = QCheckBox("Invert X", self)
        self.InvertXAxisLive2.stateChanged.connect(self.InvertXChanged2)
        self.InvertYAxisLive2 = QCheckBox("Invert Y", self)
        self.InvertYAxisLive2.stateChanged.connect(self.InvertYChanged2)

        self.PlotColors1 = QComboBox(self)
        self.PlotColors1.setFixedSize(130, 25)
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Spectral.png"), "Spectral_r")
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Grey.png"), "gray_r")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Bone.png"), "bone")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Wistia.png"), "Wistia")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Copper.png"), "copper")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Heat.png"), "gist_heat")                                                                    #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Winter.png"), "winter")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Spring.png"), "spring")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Summer.png"), "summer")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Autumn.png"), "autumn")                                                                      #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Hot.png"), "hot")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Cool.png"), "cool")                                                                        #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_ncar.png"), "gist_ncar")                                                                      #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/nipy_spectral.png"), "nipy_spectral")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Reds.png"), "Reds")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Blues.png"), "Blues")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/BrBG.png"), "BrBG")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/BuGn.png"), "BuGn")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/BuPu.png"), "BuPu")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/CMRmap.png"), "CMRmap")                                                                        #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PiYG.png"), "PiYG")                                                                          #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PuOr.png"), "PuOr")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PuRd.png"), "PuRd")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PuBu.png"), "PuBu")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/RdGy.png"), "RdGy")                                                                         #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/RdYlBu.png"), "RdYlBu")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/RdYlGn.png"), "RdYlGn")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/YlOrRd.png"), "YlOrRd")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/brg.png"), "brg")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/bwr.png"), "bwr")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/coolwarm.png"), "coolwarm")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/cubehelix.png"), "cubehelix")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_earth.png"), "gist_earth")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_rainbow.png"), "gist_rainbow")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_stern.png"), "gist_stern")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gnuplot.png"), "gnuplot")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gnuplot2.png"), "gnuplot2")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/hsv.png"), "hsv")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/jet.png"), "jet")                                                                       #Setzt eine CheckBox
        self.PlotColors1.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/terrain.png"), "terrain")

        self.PlotColors2 = QComboBox(self)
        self.PlotColors2.setFixedSize(130, 25)
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Spectral.png"), "Spectral_r")
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Grey.png"), "gray_r")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Bone.png"), "bone")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Wistia.png"), "Wistia")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Copper.png"), "copper")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Heat.png"), "gist_heat")                                                                    #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Winter.png"), "winter")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Spring.png"), "spring")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Summer.png"), "summer")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Autumn.png"), "autumn")                                                                      #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Hot.png"), "hot")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Cool.png"), "cool")                                                                        #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_ncar.png"), "gist_ncar")                                                                      #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/nipy_spectral.png"), "nipy_spectral")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Reds.png"), "Reds")                                                                             #Setzt eine CheckBox                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/Blues.png"), "Blues")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/BrBG.png"), "BrBG")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/BuGn.png"), "BuGn")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/BuPu.png"), "BuPu")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/CMRmap.png"), "CMRmap")                                                                        #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PiYG.png"), "PiYG")                                                                          #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PuOr.png"), "PuOr")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PuRd.png"), "PuRd")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/PuBu.png"), "PuBu")                                                                         #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/RdYlBu.png"), "RdYlBu")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/RdYlGn.png"), "RdYlGn")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/YlOrRd.png"), "YlOrRd")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/brg.png"), "brg")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/bwr.png"), "bwr")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/coolwarm.png"), "coolwarm")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/cubehelix.png"), "cubehelix")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_earth.png"), "gist_earth")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_rainbow.png"), "gist_rainbow")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gist_stern.png"), "gist_stern")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gnuplot.png"), "gnuplot")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/gnuplot2.png"), "gnuplot2")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/hsv.png"), "hsv")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/jet.png"), "jet")                                                                       #Setzt eine CheckBox
        self.PlotColors2.addItem(QIcon("C:/Users/Marti/Desktop/Unibox_Projekt/HydraScan/Files/Styles/terrain.png"), "terrain")
        
        self.RangeUpper1 = QSlider(Qt.Horizontal)
        self.RangeUpper1.setMinimum(0)                                                                                               #Setzt ein Minimalwert für die Auswahl
        self.RangeUpper1.setMaximum(100)                                                                                             #Setzt ein Maximum für die Auswahl
        self.RangeUpper1.setValue(100)                                                                                                       #Setzt einen Startwert
        self.RangeUpper1.setTickPosition(QSlider.TicksBelow)                                                 #Setzt Rastpunkte unter dem Slider
        self.RangeUpper1.setTickInterval(101)                                                                                #Setzt 11 Rastpunkte also je einen alle 10 Schritte
        self.RangeUpper1.valueChanged.connect(self.UpperRange1)                                                #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
        self.RangeUpper1.setToolTip("Sets the upper Range")
        self.labelRangeUpper1 = QLabel("Upper Range", self)

        self.RangeLower1 = QSlider(Qt.Horizontal)
        self.RangeLower1.setMinimum(0)                                                                                               #Setzt ein Minimalwert für die Auswahl
        self.RangeLower1.setMaximum(100)                                                                                             #Setzt ein Maximum für die Auswahl
        self.RangeLower1.setValue(0)                                                                                                       #Setzt einen Startwert
        self.RangeLower1.setTickPosition(QSlider.TicksBelow)                                                 #Setzt Rastpunkte unter dem Slider
        self.RangeLower1.setTickInterval(101)                                                                                #Setzt 11 Rastpunkte also je einen alle 10 Schritte
        self.RangeLower1.valueChanged.connect(self.LowerRange1)                                                #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
        self.RangeLower1.setToolTip("Sets the lower Range")
        self.labelRangeLower1 = QLabel("Lower Range", self)

        self.RangeUpper2 = QSlider(Qt.Horizontal)
        self.RangeUpper2.setMinimum(0)                                                                                               #Setzt ein Minimalwert für die Auswahl
        self.RangeUpper2.setMaximum(100)                                                                                             #Setzt ein Maximum für die Auswahl
        self.RangeUpper2.setValue(100)                                                                                                       #Setzt einen Startwert
        self.RangeUpper2.setTickPosition(QSlider.TicksBelow)                                                 #Setzt Rastpunkte unter dem Slider
        self.RangeUpper2.setTickInterval(101)                                                                                #Setzt 11 Rastpunkte also je einen alle 10 Schritte
        self.RangeUpper2.valueChanged.connect(self.UpperRange2)                                                #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
        self.RangeUpper2.setToolTip("Sets the upper Range")
        self.labelRangeUpper2 = QLabel("Upper Range", self)

        self.RangeLower2 = QSlider(Qt.Horizontal)
        self.RangeLower2.setMinimum(0)                                                                                               #Setzt ein Minimalwert für die Auswahl
        self.RangeLower2.setMaximum(100)                                                                                             #Setzt ein Maximum für die Auswahl
        self.RangeLower2.setValue(0)                                                                                                       #Setzt einen Startwert
        self.RangeLower2.setTickPosition(QSlider.TicksBelow)                                                 #Setzt Rastpunkte unter dem Slider
        self.RangeLower2.setTickInterval(101)                                                                                #Setzt 11 Rastpunkte also je einen alle 10 Schritte
        self.RangeLower2.valueChanged.connect(self.LowerRange2)                                                #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
        self.RangeLower2.setToolTip("Sets the lower Range")
        self.labelRangeLower2 = QLabel("Lower Range", self)

        self.ch1Live1 = QComboBox(self) 
        self.ch1Live1.addItem(self.CH1)                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
        self.ch1Live1.addItem(self.CH2)
        self.ch1Live1.addItem(self.CH3)
        self.ch1Live1.addItem(self.CH4)
        self.ch1Live1.addItem(self.CHA)
        self.ch1Live1.addItem(self.CHB)
        self.ch1Live1.addItem(self.L2)
        self.ch1Live1.addItem(self.L3)
        self.ch1Live1.setCurrentIndex(4)
        self.CheckedChannel1 = self.ch1Live1.currentText()
        self.ch1Live1.setFixedSize(130, 25)
        
        self.ch2Live1 = QComboBox(self) 
        self.ch2Live1.addItem(self.CH1)                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
        self.ch2Live1.addItem(self.CH2)
        self.ch2Live1.addItem(self.CH3)
        self.ch2Live1.addItem(self.CH4)
        self.ch2Live1.addItem(self.CHA)
        self.ch2Live1.addItem(self.CHB)
        self.ch2Live1.addItem(self.L2)
        self.ch2Live1.addItem(self.L3)
        self.ch2Live1.setCurrentIndex(5)
        self.CheckedChannel2 = self.ch2Live1.currentText()
        self.ch2Live1.setFixedSize(130, 25)
        
        # Place the matplotlib figure
        self.labelFigureStretch1 = QLabel(" ", self)
        self.labelFigureStretch2 = QLabel(" ", self)
        self.myFig1 = LumiMeshplot()
        self.myFig1.adjustSize()
        self.myFig2 = ScatMeshplot()
        self.myFig2.adjustSize()
        self.myFig3 = LumiLineplot()
        self.myFig3.adjustSize()
        self.myFig4 = ScatLineplot()
        self.myFig4.adjustSize()

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter2 = QSplitter(Qt.Horizontal)

        self.groupboxRange1 = QGroupBox("Range", self)
        self.vboxRange1 = QVBoxLayout(self)
        self.vboxRange1.addWidget(self.labelRangeLower1)
        self.vboxRange1.addWidget(self.RangeLower1)
        self.vboxRange1.addWidget(self.labelRangeUpper1)
        self.vboxRange1.addWidget(self.RangeUpper1)
        self.groupboxRange1.setLayout(self.vboxRange1)
        self.groupboxRange1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

        self.groupboxRange2 = QGroupBox("Range", self)
        self.vboxRange2 = QVBoxLayout(self)
        self.vboxRange2.addWidget(self.labelRangeLower2)
        self.vboxRange2.addWidget(self.RangeLower2)
        self.vboxRange2.addWidget(self.labelRangeUpper2)
        self.vboxRange2.addWidget(self.RangeUpper2)
        self.groupboxRange2.setLayout(self.vboxRange2)
        self.groupboxRange2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

        self.groupboxManipulateLumi = QGroupBox(self.CheckedChannel1, self)
        self.vboxManipulateLumi = QVBoxLayout(self)
        self.vboxManipulateLumi.addWidget(self.ch1Live1)
        self.vboxManipulateLumi.addWidget(self.splitter1)
        self.vboxManipulateLumi.addStretch(2)
        self.vboxManipulateLumi.addWidget(self.PlotColors1)
        self.vboxManipulateLumi.addStretch(1)
        self.vboxManipulateLumi.addWidget(self.InvertXAxisLive1)
        self.vboxManipulateLumi.addWidget(self.InvertYAxisLive1)
        self.vboxManipulateLumi.addStretch(2)
        self.vboxManipulateLumi.addWidget(self.groupboxRange1)
        self.vboxManipulateLumi.addStretch(2)
        self.vboxManipulateLumi.addWidget(self.ButtonAutoScale1)
        self.groupboxManipulateLumi.setLayout(self.vboxManipulateLumi)
        self.groupboxManipulateLumi.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))        

        self.groupboxManipulateScat = QGroupBox(self.CheckedChannel2, self)
        self.vboxManipulateScat = QVBoxLayout(self)
        self.vboxManipulateScat.addWidget(self.ch2Live1)
        self.vboxManipulateLumi.addWidget(self.splitter2)
        self.vboxManipulateScat.addStretch(2)
        self.vboxManipulateScat.addWidget(self.PlotColors2)
        self.vboxManipulateScat.addStretch(1)
        self.vboxManipulateScat.addWidget(self.InvertXAxisLive2)
        self.vboxManipulateScat.addWidget(self.InvertYAxisLive2)
        self.vboxManipulateScat.addStretch(2)
        self.vboxManipulateScat.addWidget(self.groupboxRange2)
        self.vboxManipulateScat.addStretch(2)
        self.vboxManipulateScat.addWidget(self.ButtonAutoScale2)
        self.groupboxManipulateScat.setLayout(self.vboxManipulateScat)
        self.groupboxManipulateScat.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
        
        self.groupboxLumi = QGroupBox(self.CheckedChannel1, self) 
        self.vboxLumi = QVBoxLayout(self)
        self.vboxLumi.addWidget(self.myFig1)
        #self.vboxLumi.addStretch(1)
        self.vboxLumi.addWidget(self.myFig3)
        #self.vboxLumi.addWidget(self.labelFigureStretch1)
        self.groupboxLumi.setLayout(self.vboxLumi)
        self.groupboxLumi.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

        self.groupboxScat = QGroupBox(self.CheckedChannel2, self) 
        self.vboxScat = QVBoxLayout(self)
        self.vboxScat.addWidget(self.myFig2)
        #self.vboxScat.addStretch(1)
        self.vboxScat.addWidget(self.myFig4)
        #self.vboxScat.addWidget(self.labelFigureStretch2)
        self.groupboxScat.setLayout(self.vboxScat)
        self.groupboxScat.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

        self.groupboxChannelSettings = QGroupBox("Settings", self)
        self.LayoutChannelSettings = QVBoxLayout(self)
        self.LayoutChannelSettings.addWidget(self.ButtonRefreshScale1)
        self.LayoutChannelSettings.addWidget(self.ButtonSave)
        self.LayoutChannelSettings.addStretch(1)
        self.LayoutChannelSettings.addWidget(self.groupboxManipulateLumi)
        self.LayoutChannelSettings.addStretch(1)
        self.LayoutChannelSettings.addWidget(self.groupboxManipulateScat)
        self.groupboxChannelSettings.setLayout(self.LayoutChannelSettings)
        self.groupboxChannelSettings.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

        self.LAYOUT_A.addWidget(self.groupboxChannelSettings)
        self.LAYOUT_A.addWidget(self.groupboxLumi)
        self.LAYOUT_A.addWidget(self.groupboxScat)


        self.ch1Live1.currentTextChanged.connect(self.ChannelSelect)
        self.ch2Live1.currentTextChanged.connect(self.ChannelSelect)
        self.PlotColors1.currentTextChanged.connect(self.PlotsytleChanged1)
        self.PlotColors2.currentTextChanged.connect(self.PlotsytleChanged2)

        self.setLayout(self.LAYOUT_A)
        self.iteration1 = 0
        self.iteration2 = 0
        self.Maximum1 = 100
        self.Maximum2 = 100
        self.Minimum1 = 0
        self.Minimum2 = 0
        self.localMaximum1 = 0
        self.localMaximum2 = 0
        self.localMinimum1 = 0
        self.localMinimum2 = 0
        self.show()

    def NewLine(self):
        global zNew
        global zNew2
        self.CalcNewValues1()
        self.CalcNewValues2()

    def ChannelSelect(self):
        Channel1 = self.ch1Live1.currentText()
        Channel2 = self.ch2Live1.currentText()
            
        print("Selected Channels: " + Channel1 + "\t" + Channel2)

        self.CheckedChannel1 = Channel1
        self.CheckedChannel2 = Channel2
        self.groupboxManipulateLumi.setTitle(self.CheckedChannel1)
        self.groupboxManipulateScat.setTitle(self.CheckedChannel2)
        self.groupboxLumi.setTitle(self.CheckedChannel1)
        self.groupboxScat.setTitle(self.CheckedChannel2)
        self.myFig1.ChannelChanged()

    def RefreshScale1(self):
        self.NewLine()
        print("Refresh Scale 1")

    def SavePlots(self):
        self.myFig1.SaveFile()
        self.myFig2.SaveFile()
        print("SavePlots")

    def UpperRange1(self):
        global upperLimit1
        global lowerLimit1
        value = self.RangeUpper1.value()
        upperLimit1 = value
        self.myFig1.RangeChange(upperLimit1, lowerLimit1)
        self.myFig3.RangeChange(upperLimit1, lowerLimit1)
        print("Upper Range 1: " + str(upperLimit1))

    def UpperRange2(self):
        global upperLimit2
        global lowerLimit2
        value = self.RangeUpper2.value()
        upperLimit2 = value
        self.myFig2.RangeChange(upperLimit2, lowerLimit2)
        self.myFig4.RangeChange(upperLimit2, lowerLimit2)
        print("Upper Range 2: " + str(upperLimit2))

    def LowerRange1(self):
        global upperLimit1
        global lowerLimit1
        value = self.RangeLower1.value()
        lowerLimit1 = value
        self.myFig1.RangeChange(upperLimit1, lowerLimit1)
        self.myFig3.RangeChange(upperLimit1, lowerLimit1)
        print("Lower Range 1: " + str(lowerLimit1))

    def LowerRange2(self):
        global upperLimit2
        global lowerLimit2
        value = self.RangeLower2.value()
        lowerLimit2 = value
        self.myFig2.RangeChange(upperLimit2, lowerLimit2)
        self.myFig4.RangeChange(upperLimit2, lowerLimit2)
        print("Lower Range 2: " + str(lowerLimit2))

    def PlotsytleChanged1(self, Plotstyle):
        self.myFig1.UpdateCMAP(Plotstyle)
        print("Plotstyle 1: " + Plotstyle)

    def PlotsytleChanged2(self, Plotstyle):
        self.myFig2.UpdateCMAP(Plotstyle)
        print("Plotstyle 2: " + Plotstyle)

    def InvertXChanged1(self):
        global InvertXLive1
        InvertXLive1 = self.InvertXAxisLive1.isChecked()
        self.myFig1.InvertX(InvertXLive1)
        print("Invert X1: " + str(InvertXLive1))

    def InvertYChanged1(self):
        global InvertYLive1
        InvertYLive1 = self.InvertYAxisLive1.isChecked()
        self.myFig1.InvertY(InvertYLive1)
        print("Invert Y1: " + str(InvertYLive1))

    def InvertXChanged2(self):
        global InvertXLive2
        InvertXLive2 = self.InvertXAxisLive2.isChecked()
        self.myFig2.InvertX(InvertXLive2)
        print("Invert X2: " + str(InvertXLive2))

    def InvertYChanged2(self):
        global InvertYLive2
        InvertYLive2 = self.InvertYAxisLive2.isChecked()
        self.myFig2.InvertY(InvertYLive2)
        print("Invert Y2: " + str(InvertYLive2))

    def closeEvent(self, event):
        print("End")

    def CalcNewValues1(self):
        global zNew
        global t
        global xstop
        global ystop

        self.zNew = zNew
        self.t = t
        self.xstop = xstop
        self.ystop = ystop

        
        i = 0
        while i <= self.xstop:
            self.aNew = random.randint(0, 100)
            self.zNew[i][self.iteration1] = self.aNew
            self.t[i] = self.aNew
            i += 1
        self.iteration1 += 1

        if self.ButtonAutoScale1.isChecked() == True:
            self.localMaximum1 = max(self.t)
            self.localMinimum1 = min(self.t)
            print(str(self.Minimum1) + "\t" + str(self.Maximum1))

            self.myFig1.RangeChange(self.Maximum1, self.Minimum1)
            self.myFig3.RangeChange(self.Maximum1, self.Minimum1)

            if self.localMinimum1 < self.Minimum1 or self.iteration1 == 1:
                self.Minimum1 = self.localMinimum1
                print("New Min: " + str(self.Minimum1))
            if self.localMaximum1 > self.Maximum1:
                self.Maximum1 = self.localMaximum1
                print("New Max: " + str(self.Maximum1))
        
        self.myFig1.CalcNewLine1(self.zNew)
        self.myFig3.CalcNewLine1(self.t)
        zNew = self.zNew 

    def CalcNewValues2(self):
        global zNew2
        global tt
        global xstop
        global ystop

        self.zNew2 = zNew2
        self.tt = tt
        self.xstop = xstop
        self.ystop = ystop

        i = 0
        while i <= self.xstop:
            self.bNew = random.randint(0, 100)
            self.zNew2[i][self.iteration2] = self.bNew
            self.tt[i] = self.bNew
            i += 1
        self.iteration2 += 1

        if self.ButtonAutoScale2.isChecked() == True:
            self.localMaximum2 = max(self.tt)
            self.localMinimum2 = min(self.tt)
            print(str(self.Minimum2) + "\t" + str(self.Maximum2))

            self.myFig2.RangeChange(self.Maximum2, self.Minimum2)
            self.myFig4.RangeChange(self.Maximum2, self.Minimum2)

            if self.localMinimum2 < self.Minimum2 or self.iteration2 == 1:
                self.Minimum2 = self.localMinimum2
                print("New Min: " + str(self.Minimum2))
            if self.localMaximum2 > self.Maximum2:
                self.Maximum2 = self.localMaximum2
                print("New Max: " + str(self.Maximum2))

        self.myFig2.CalcNewLine1(self.zNew2)
        self.myFig4.CalcNewLine1(self.tt)
        zNew2 = self.zNew2 
        
class LumiMeshplot(FigureCanvas, TimedAnimation):
    def __init__(self):
        #print(matplotlib.__version__)
        
        # The data
        global xstart
        global ystart
        global xstop
        global ystop
        global upperLimit1
        global lowerLimit1
        global InvertXLive1
        global InvertYLive1

        self.AutoScale = True
        
        self.InvertXLive = InvertXLive1
        self.InvertYLive = InvertYLive1
        
        self.xstart = xstart
        self.ystart = ystart
        self.xstop = xstop
        self.ystop = ystop
        self.upperLimit = upperLimit1
        self.lowerLimit = lowerLimit1
        self.zNew = list()
        self.zPart = list()
        self.x = self.xstart
        self.y = self.ystart
        
        while self.y <= self.ystop:
            while self.x <= self.xstop:
                self.zPart.append(0)
                self.x += 1
            self.x = self.xstart
            self.y += 1
            self.zNew.append(self.zPart)
            self.zPart = list()
        
        self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))

        # The window
        self.fig = Figure(figsize=(7,7), dpi=100)
        self.cmap = plt.get_cmap('Spectral_r') 
        self.ax1 = self.fig.add_subplot()
        self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.ax1.set_xlabel('X [Bits]')
        self.ax1.set_ylabel('Y [Bits]')
        if self.InvertXLive == True:
            self.ax1.invert_xaxis()
        if self.InvertYLive == False:
            self.ax1.invert_yaxis()
        #self.ax1.set_title("Luminescence")
        self.ax1.set_aspect('equal')
        self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
        self.cb1.set_label("Counts")
        plt.tight_layout(self.fig)
        #self.fig.canvas.draw()
        FigureCanvas.__init__(self, self.fig)
        #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)

        self.iteration = 0

        #anim = animation.FuncAnimation(self.fig,self.animate,frames=(self.ystop-self.ystart+1),interval=(self.ystop-self.ystart+1),blit=False,repeat=False)

    def animate(self):
        self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.ax1.set_xlabel('X [Bits]')
        self.ax1.set_ylabel('Y [Bits]')
        self.ax1.set_aspect('equal')
        self.cb1.remove()
        self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
        self.cb1.set_label("Counts")
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()
        #line1.set_data(v,t)
        return self.quad1

    def SaveFile(self):
        self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.ax1.set_xlabel('X [Bits]')
        self.ax1.set_ylabel('Y [Bits]')
        self.ax1.set_aspect('equal')
        self.ax1.set_title("Luminescence")
        self.cb1.remove()
        self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
        self.cb1.set_label("Counts")
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()
        self.fig.savefig("C:/Users/Marti/Desktop/Luminescence.png")
        self.ax1.set_title("")
        self.animate()

    def UpdateCMAP(self, Plotstyle):
        self.cmap = plt.get_cmap(Plotstyle)
        self.animate()

    def InvertX(self, InvertXLive1):
        self.InvertXLive = InvertXLive1
        print("Invert X1: " + str(self.InvertXLive))
        self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.cb1.remove()
        self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
        self.cb1.set_label("Counts")
        self.ax1.invert_xaxis()
        self.ax1.set_xlabel('X [Bits]')
        self.ax1.set_ylabel('Y [Bits]')
        self.ax1.set_aspect('equal')
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()

    def InvertY(self, InvertYLive1):
        self.InvertYLive = InvertYLive1
        print("Invert Y1: " + str(self.InvertYLive))
        self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.cb1.remove()
        self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
        self.cb1.set_label("Counts")
        self.ax1.invert_yaxis()
        self.ax1.set_xlabel('X [Bits]')
        self.ax1.set_ylabel('Y [Bits]')
        self.ax1.set_aspect('equal')
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()

    def RangeChange(self, up, down):
        self.upperLimit = up
        self.lowerLimit = down
        self.animate()

    def CalcNewLine(self,AutoScale):
        self.AutoScale = AutoScale

    def CalcNewLine1(self,a):
        self.zNew = a
        self.animate()

class ScatMeshplot(FigureCanvas, TimedAnimation):
    def __init__(self):
        #print(matplotlib.__version__)
        
        # The data
        global xstart
        global ystart
        global xstop
        global ystop
        global upperLimit2
        global lowerLimit2
        global InvertXLive2
        global InvertYLive2
        
        self.InvertXLive = InvertXLive2
        self.InvertYLive = InvertYLive2
        
        self.xstart = xstart
        self.ystart = ystart
        self.xstop = xstop
        self.ystop = ystop
        self.upperLimit = upperLimit2
        self.lowerLimit = lowerLimit2
        
        self.zNew2 = list()
        self.zPart = list()
        self.x = self.xstart
        self.y = self.ystart
        while self.y <= self.ystop:
            while self.x <= self.xstop:
                self.zPart.append(0)
                self.x += 1
            self.x = self.xstart
            self.y += 1
            self.zNew2.append(self.zPart)
            self.zPart = list()

        self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))

        # The window
        self.fig = Figure(figsize=(7,7), dpi=100)
        self.cmap = plt.get_cmap('Spectral_r') 
        self.ax2 = self.fig.add_subplot()
        self.quad2 = self.ax2.pcolormesh(self.x, self.y, self.zNew2, cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.ax2.set_xlabel('X [Bits]')
        self.ax2.set_ylabel('Y [Bits]')
        if self.InvertXLive == True:
            self.ax2.invert_xaxis()
        if self.InvertYLive == False:
            self.ax2.invert_yaxis()
        #self.ax2.set_title("Scattering")
        self.ax2.set_aspect('equal')
        self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
        self.cb2.set_label("Counts")
        plt.tight_layout(self.fig)
        FigureCanvas.__init__(self, self.fig)
        #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        self.iteration = 0

    def animate(self):
        self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.ax2.set_xlabel('X [Bits]')
        self.ax2.set_ylabel('Y [Bits]')
        self.ax2.set_aspect('equal')
        self.cb2.remove()
        self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
        self.cb2.set_label("Counts")
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()
        #line1.set_data(v,t)
        return self.quad2

    def SaveFile(self):
        self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.ax2.set_xlabel('X [Bits]')
        self.ax2.set_ylabel('Y [Bits]')
        self.ax2.set_aspect('equal')
        self.ax2.set_title("Scattering")
        self.cb2.remove()
        self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
        self.cb2.set_label("Counts")
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()
        self.fig.savefig("C:/Users/Marti/Desktop/Scattering.png")
        self.ax2.set_title("")
        self.animate()

    def UpdateCMAP(self, Plotstyle):
        self.cmap = plt.get_cmap(Plotstyle)
        self.animate()

    def InvertX(self, InvertXLive1):
        if self.AutoScale == True:
            self.lowerLimit = self.Minimum2
            self.upperLimit = self.Maximum2
        self.InvertXLive = InvertXLive1
        print("Invert X1: " + str(self.InvertXLive))
        self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.cb2.remove()
        self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
        self.cb2.set_label("Counts")
        self.ax2.invert_xaxis()
        self.ax2.set_xlabel('X [Bits]')
        self.ax2.set_ylabel('Y [Bits]')
        self.ax2.set_aspect('equal')
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()

    def InvertY(self, InvertYLive1):
        if self.AutoScale == True:
            self.lowerLimit = self.Minimum2
            self.upperLimit = self.Maximum2
        self.InvertYLive = InvertYLive1
        print("Invert Y1: " + str(self.InvertYLive))
        self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
        self.cb2.remove()
        self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
        self.cb2.set_label("Counts")
        self.ax2.invert_yaxis()
        self.ax2.set_xlabel('X [Bits]')
        self.ax2.set_ylabel('Y [Bits]')
        self.ax2.set_aspect('equal')
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()

    def RangeChange(self, up, down):
        self.upperLimit = up
        self.lowerLimit = down
        self.animate()

    def CalcNewLine(self,b):
        #self.zNew2 = zNew2
        i = 0
        self.b = b
        while i <= self.xstop:
            self.bNew = self.b
            self.zNew2[i][self.iteration] = self.bNew
            i += 1
        self.iteration += 1
        #self.zNew2 = np.array(zNew2)
        #print(self.zNew2)
        self.animate()

    def CalcNewLine1(self,b):
        self.zNew2 = b
        #i = 0
        #self.b = b
        #while i <= self.xstop:
        #    self.bNew = self.b
        #    self.zNew2[i][self.iteration] = self.bNew
        #    i += 1
        #self.iteration += 1
        #self.zNew2 = np.array(b)
        #print(self.zNew2)
        self.animate()


class LumiLineplot(FigureCanvas, TimedAnimation):
    def __init__(self):
        #print(matplotlib.__version__)
        global t
        global v
        global xstart
        global ystart
        global xstop
        global ystop
        global upperLimit1
        global lowerLimit1
        
        self.xstart = xstart
        self.ystart = ystart
        self.xstop = xstop
        self.ystop = ystop
        self.upperLimit = upperLimit1
        self.lowerLimit = lowerLimit1

        self.t = t
        self.v = v
        
        # The window
        self.fig = Figure(figsize=(7,3), dpi=100)
        #cmap = plt.get_cmap('Spectral_r') 
        self.ax3 = self.fig.add_subplot(111)
        self.line1 = self.ax3.plot([],[],'-',linewidth=1)
        self.ax3.set_xlim(0,self.xstop-self.xstart)
        self.ax3.set_ylim(self.lowerLimit,self.upperLimit)
        self.ax3.set_xlabel('Counts')
        self.ax3.set_ylabel('Point')
        #self.ax3.set_title('Oscillationsssss')
        self.ax3.grid(True)
        plt.tight_layout(self.fig)
        FigureCanvas.__init__(self, self.fig)
        #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        self.iteration = 0
            
    def animate(self):
        self.ax3.clear()
        self.line1 = self.ax3.plot(self.v,self.t,'-',linewidth=1)
        self.ax3.set_xlim(0,self.xstop-self.xstart)
        self.ax3.set_ylim(self.lowerLimit,self.upperLimit)
        self.ax3.set_xlabel('Counts')
        self.ax3.set_ylabel('Point')
        #self.ax3.set_title('Oscillationsssss')
        self.ax3.grid(True)
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()
        #line1.set_data(v,t)
        #return self.quad2

    def RangeChange(self, up, down):
        self.upperLimit = up
        self.lowerLimit = down
        self.animate()

    def CalcNewLine(self,a):
        i = 0 
        self.a = a
        while i <= self.xstop:
            self.aNew = self.a
            self.t[i] = self.aNew
            i += 1
        self.iteration += 1
        #self.line1.set_data(self.v,self.t)
        
        #return self.line1
        self.animate()

    def CalcNewLine1(self,a):
        #i = 0 
        #self.a = a
        #while i <= self.xstop:
        #    self.aNew = self.a
        #    self.t[i] = self.aNew
        #    i += 1
        #self.iteration += 1
        #self.line1.set_data(self.v,self.t)
        self.t = a
        #return self.line1
        self.animate()


class ScatLineplot(FigureCanvas):
    def __init__(self):
        #print(matplotlib.__version__)
        global tt
        global v
        global xstart
        global ystart
        global xstop
        global ystop
        global upperLimit2
        global lowerLimit2
        
        self.xstart = xstart
        self.ystart = ystart
        self.xstop = xstop
        self.ystop = ystop
        self.upperLimit = upperLimit2
        self.lowerLimit = lowerLimit2

        self.tt = tt
        self.v = v
        
        # The window
        self.fig = Figure(figsize=(7,3), dpi=100)
        cmap = plt.get_cmap('Spectral_r') 
        self.ax4 = self.fig.add_subplot(111)
        self.line2, = self.ax4.plot([],[],'-',linewidth=2)
        self.ax4.set_xlim(0,self.xstop-self.xstart)
        self.ax4.set_ylim(self.lowerLimit,self.upperLimit)
        self.ax4.set_xlabel('Counts')
        self.ax4.set_ylabel('Point')
        #self.ax4.set_title('Oscillationsssss')
        self.ax4.grid(True)
        plt.tight_layout(self.fig)
        FigureCanvas.__init__(self, self.fig)
        #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        self.iteration = 0
            
    def animate(self):
        self.ax4.clear()
        self.line2 = self.ax4.plot(self.v,self.tt,'-',linewidth=1)
        self.ax4.set_xlim(0,self.xstop-self.xstart)
        self.ax4.set_ylim(self.lowerLimit,self.upperLimit)
        self.ax4.set_xlabel('Counts')
        self.ax4.set_ylabel('Point')
        #self.ax4.set_title('Oscillationsssss')
        self.ax4.grid(True)
        plt.tight_layout(self.fig)
        self.fig.canvas.draw()
        #line1.set_data(v,t)
        #return self.quad2

    def RangeChange(self, up, down):
        self.upperLimit = up
        self.lowerLimit = down
        self.animate()

    def CalcNewLine(self,b):
        i = 0 
        self.b = b
        while i <= self.xstop:
            self.bNew = self.b
            self.tt[i] = self.bNew
            i += 1
        self.iteration += 1
        #self.line1.set_data(self.v,self.t)
        
        #return self.line1
        self.animate()

    def CalcNewLine1(self,b):
        #i = 0 
        #self.b = b
        #while i <= self.xstop:
        #    self.bNew = self.b
        #    self.tt[i] = self.bNew
        #    i += 1
        #self.iteration += 1
        #self.line1.set_data(self.v,self.t)
        self.tt = b
        #return self.line1
        self.animate()



if __name__== '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())
