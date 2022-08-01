#HydraScan 1.22.1 - Gaia

#Info ---------------------------------------------------------------
Version = "1.22.1"
VersionName = "Gaia"
print("Version: HydraScan " + str(Version) + " - " + str(VersionName))
Updates = "Autofocus\n\tAuto Slope\n\tTTL Sync maxima\n\tminor fixes"
NumberUpdates = 5
print("Updates: " + Updates)
Copyright = "Property of HydraSpex UG"
print("Copyright: " + Copyright)
Contact = "info@hydrascan.de"
print("Contact: " + Contact)
Cite = "Available soon!"
print("If HydraScan contributes to publisch a work please cite: " + Cite + "\n\n")


#Global Variables ---------------------------------------------------
WindowPosX = 50
WindowPosY = 100
WindowWidth = 1200
WindowHeight = 775

PiezoDistanceX = 100000                                                                                                                                 #Nanometers
PiezoDistanceY = 100000                                                                                                                                 #Nanometers
PiezoDistanceZ = 20000                                                                                                                                  #Nanometers
PiezoVoltage = 10                                                                                                                                       #Volts
DeviceVoltageLow = 0                                                                                                                                    #Volts
DeviceVoltageHigh = 10                                                                                                                                  #Volts
DeviceVoltage = DeviceVoltageHigh - DeviceVoltageLow                                                                                                    #Volts
if PiezoVoltage <= DeviceVoltage:
        PotiStartVal = PiezoVoltage
else:
        PotiStartVal = DeviceVoltage
FullRangeDeviceX = PiezoDistanceX * (DeviceVoltage / PiezoVoltage)                                                                                      #Nanometers
FullRangeDeviceY = PiezoDistanceY * (DeviceVoltage / PiezoVoltage)                                                                                      #Nanometers
FullRangeDeviceZ = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)                                                                                      #Nanometers
print("Full Range: " + str(FullRangeDeviceX) + " x " + str(FullRangeDeviceY))

FocusZ = 2048

CHA = "Luminescence"                                                                                                                                    #Channel A
CHB = "Scattering"                                                                                                                                      #Channel B
L2 = "L2"                                                                                                                                               #Channel L2
L3 = "L3"                                                                                                                                               #Channel L3
CH1 = "CH1"                                                                                                                                             #Channel 1
CH2 = "CH2"                                                                                                                                             #Channel 2
CH3 = "CH3"                                                                                                                                             #Channel 3
CH4 = "CH4"                                                                                                                                             #Channel 4
CH5 = "CH5"                                                                                                                                             #Channel 5
PointSpeed = 15


PlotStyle = 1
FilePath = ""
FileName = ""
PlotName = ""
TXTFilePath = ""


NameTTL1 = "TTL 1"
TTL1OUT = 14
TTL1IN = 15
Wire1 = False
NameTTL2 = "TTL 2"
TTL2OUT = 17
TTL2IN = 18
Wire2 = False
LEDPin = 26

CurrentPage = 0

StyleName = "Fusion"            #'Fusion', 'Windows', 'windowsvista'(['bb10dark', 'bb10bright', 'cleanlooks', 'gtk2', 'cde', 'motif', 'plastique', 'qt5ct-style', 'Windows', 'Fusion'])
#StyleName = "Windows"
#StyleName = "windowsvista"
#StyleName = "qt5ct-style"
StyleColor = "dark"             #'light', 'dark'
#StyleColor = "light"


#Library import -------------------------------------------------------
#Python Imports
try:
        import threading
        from threading import Thread
        import sys
        sys.setrecursionlimit(1000000)
        import traceback
        import time
        import shlex, subprocess
        import os
        import sqlite3
        import math
        from shutil import copyfile
        from queue import Queue
        import keyboard
except:
        print("Python imports failed")

#GUI Imports
try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtGui import *
        from PyQt5 import *
        from PyQt5.QtCore import *
except:
        print("PyQt imports failed")

#print(QStyleFactory.keys())

#Tempsensor imports
try:
        import Adafruit_DHT
        TempSens = Adafruit_DHT.DHT22
        DHTPin = 22
        DHTon = 1
        TempWindowOn = 0
        #print("Temperature Sensor ready")                                                                                                              #Pin22 PullUp 10K
except:
        print("No Temperature Sensor connected")
        DHTon = 0
        TempWindowOn = 0

try:
        humidity, temperature = Adafruit_DHT.read_retry(TempSens, DHTPin)
except:
        temperature = 0.0
        humidity = 0.0
        DHTon = 0
        TempWindowOn = 0
        print("Reading from DHT failure")

#Raspberry imports and settings
try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIOon = 1
except:
        print("GPIO import failed")
        #Create virtual GPIOs to catch errors
        class GPIO_Virtual():
                OUT = 1
                IN = 1
                LOW = 0
                HIGH = 1
                RISING = 1

                def __init__(self):
                        pass

                def cleanup(self):
                        pass
                
                def setup(self, val):
                        pass

                def output(self, val, val1):
                        print("No GPIO" + str(val) + " - " + str(val1))

                def add_event_detect(self, val=0, val2=0, callback=None, bouncetime=0):
                        if callback != None:
                                self.callback

                def callback(self):
                        print("Test")

                def remove_event_detect(self, val):
                        pass
        GPIO = GPIO_Virtual()
        GPIOon = 0

try:
        GPIO.setup(TTL1OUT, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(TTL1IN, GPIO.IN)
        GPIO.setup(TTL2OUT, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(TTL2IN, GPIO.IN)
        GPIO.setup(LEDPin, GPIO.OUT, initial=GPIO.LOW)
except:
        print("TTL failed")

#DAC & Poti imports
try:
        from MCP4728_60 import MCP4728_60

        dacOffset = MCP4728_60()
        dacOffset.setAllVoltage(0, 0, 0, 0)

        NoOffset = 0

except:
        print("DAC imports failed")
        #Create virtual DACs to catch errors
        class Offset_Virtual():
                def __init__(self):
                        pass

                def setAllVoltage(self, val1, val2, val3, val4):
                        print("No Offset DAC: " + str(val1) + " - " + str(val2) + " - " + str(val3) + " - " + str(val4))

                def setOneVoltage(self, CH, volt):
                        print("No Offset DAC: Channel " + str(CH) + " - " + str(volt))

        dacOffset = Offset_Virtual()
        dacOffset.setAllVoltage(0, 0, 0, 0)
        NoOffset = 1

try:
        from MCP4151_0 import MCP4151_0

        Poti = MCP4151_0()
        Poti.write_range(PotiStartVal)
        print("Poti Range " + str(PotiStartVal) + " V")

        NoPoti = 0

except:
        print("Poti imports failed")
        #Create virtual DACs to catch errors
        class MCP4151_Virtual():
                def __init__(self):
                        pass

                def write_pot(self, input):
                        print("No Poti: " + str(input))

                def write_volt(self, input):
                        print("No Poti: " + str(input))

                def write_range(self, input):
                        print("No Poti: "+ str(input))

        Poti = MCP4151_Virtual()
        Poti.write_range(PotiStartVal)
        print("Poti Range " + str(PotiStartVal) + " V")
        NoPoti = 1

try:
        from MCP4725_61 import MCP4725_61
        dacX = MCP4725_61()
        dacX.set_voltage(0)

        from MCP4725_62 import MCP4725_62
        dacY = MCP4725_62()
        dacY.set_voltage(0)

        from MCP4725_63 import MCP4725_63
        dacZ = MCP4725_63()
        dacZ.set_voltage(FocusZ)
        
        NoDAC = 0

except:
        print("DAC imports failed")
        #Create virtual DACs to catch errors
        class DAC_Virtual():
                def __init__(self):
                        pass

                def set_voltage(self, val):
                        print("No DAC: " + str(val))

        dacZ = DAC_Virtual()
        dacX = DAC_Virtual()
        dacY = DAC_Virtual()
        dacZ.set_voltage(FocusZ)
        dacX.set_voltage(0)
        dacY.set_voltage(0)
        NoDAC = 1

#ADC imports
try:
        import Adafruit_ADS1x15
        adc = Adafruit_ADS1x15.ADS1115()
        GAIN = 2/3

        NoADC = 0
except:
        print("ADC imports failed")
        GAIN = 2/3
        #Create virtual ADCs to catch errors
        class ADC_Virtual():
                def __init__(self):
                        pass

                def read_adc(self, val, gain):
                        print("No ADC: " + str(val) + " - " + str(gain))
                        a = random.uniform(0, 5)
                        return a

                def stop_adc(self):
                        pass

        adc = ADC_Virtual()

#Matplotlib imports
try:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        import matplotlib
        matplotlib.use('Qt5Agg')
        import matplotlib.pyplot as plt
        #from matplotlib.colors import BoundaryNorm
        from matplotlib.colors import ListedColormap, LinearSegmentedColormap, BoundaryNorm
        from matplotlib.ticker import MaxNLocator, LinearLocator, FormatStrFormatter
        from matplotlib.figure import Figure
        from matplotlib.animation import TimedAnimation
        import matplotlib.animation as animation
        from matplotlib.lines import Line2D
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        import matplotlib.font_manager as fm
        import matplotlib as mpl
        mpl.rcParams.update({'text.color': "white",
                                'axes.labelcolor': "white",
                                'xtick.color': "white",
                                'ytick.color': "white"})
        import matplotlib.patches as patches
        from matplotlib.widgets  import RectangleSelector
        from matplotlib.widgets import SpanSelector
        from matplotlib.widgets import PolygonSelector
        from matplotlib.widgets import LassoSelector
        from matplotlib.path import Path
        import numpy as np
        import csv
        import functools
        import random as random
        from PIL import Image
        PlotOn = 0
except:
        print("Matplotlib imports failed")

#Plotimports
try:
        import HydraPlotLib
        import HydraPlot
except:
        print("HydraPlot lost his head")

#Directory build or check --------------------------------------------
try:
        os.makedirs('/home/pi/Desktop/Data')
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        os.makedirs('/Files')
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Settings.png", "/Files/Settings.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/About.png", "/Files/About.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Help.png", "/Files/Help.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/HydraScan_free.png", "/Files/HydraScan_free.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Hydra_logo_klein.png", "/Files/Hydra_logo_klein.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/ShowTemp.png", "/Files/ShowTemp.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/temperature.png", "/Files/temperature.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Temp_high.png", "/Files/Temp_high.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")

try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Temp_low.png", "/Files/Temp_low.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")


try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Temp_normal.png", "/Files/Temp_normal.png")
        print("Data folder created")
except:
        print("Data-Folder already exist")
        
#Initializing Databases ------------------------------------------------
#Measurement Settings
try:
        connMeasure = sqlite3.connect("settingsScanMeasure.db")
        MeasureSet = connMeasure.cursor()
except:
        print("no database 1 connection")

try:
        MeasureSet.execute("""
        CREATE TABLE settingsScanMeasure (
        name text,
        bits integer,
        xstart real,
        xstop real,
        ystart real,
        ystop real,
        slope integer,
        subgrid integer,
        stack integer,
        plot integer)""")
        print("Datenbank 1 wurde angelegt")
except:
        print("Datenbank 1 abgerufen")

try:
        connMeasure.commit()                                                                                                                            #never forget this, if you want the changes to be saved:
except:
        print("database 1 failed")
        
#TTL-Sync Settings
try:
        connSync = sqlite3.connect("settingsScanSync.db")
        SyncSet = connSync.cursor()
except:
        print("no database 2 connection")

try:
        SyncSet.execute("""
        CREATE TABLE settingsScanSync (
        name text,
        bits integer,
        xstart real,
        xstop real,
        ystart real,
        ystop real,
        xstep integer,
        ystep integer,
        steptime real,
        sendTTL integer,
        getTTL integer,
        ttl integer,
        channel integer)""")
        print("Datenbank 2 wurde angelegt")
except:
        print("Datenbank 2 abgerufen")

try:
        connSync.commit()                                                                                                                               #never forget this, if you want the changes to be saved:
except:
        print("database 2 failed")

#Z-Stack Settings
try:
        connStack = sqlite3.connect("settingsScanStack.db")
        StackSet = connStack.cursor()
except:
        print("no database 3 connection")

try:
        StackSet.execute("""
        CREATE TABLE settingsScanStack (
        name text,
        stacks integer,
        stackstep real,
        direct integer,
        zstart integer)""")
        print("Datenbank 3 wurde angelegt")
except:
        print("Datenbank 3 abgerufen")

try:
        connStack.commit()                                                                                                                              #never forget this, if you want the changes to be saved:
except:
        print("database 3 failed")

#Slopecompensation Settings
try:
        connSlope = sqlite3.connect("settingsScanSlope.db")
        SlopeSet = connSlope.cursor()
except:
        print("no database 4 connection")

try:
        SlopeSet.execute("""
        CREATE TABLE settingsScanSlope (
        name text,
        xslope real,
        yslope real)""")
        print("Datenbank 4 wurde angelegt")
except:
        print("Datenbank 4 abgerufen")

try:
        connSlope.commit()                                                                                                                              #never forget this, if you want the changes to be saved:
except:
        print("database 4 failed")

#Plot Settings
try:
        connPlot = sqlite3.connect("settingsScanPlot.db")
        PlotSet = connPlot.cursor()
except:
        print("no database 5 connection")

try:
        PlotSet.execute("""
        CREATE TABLE settingsScanPlot (
        ID integer,
        plotstyle integer,
        plotname text)""")
        print("Datenbank 5 wurde angelegt")
        PlotSet.execute("INSERT INTO settingsScanPlot (ID, plotstyle, plotname) VALUES (" + str(1) + ", " + str(PlotStyle) + ", " + "\"" + PlotName + "\")")
        print("Settings saved")
except:
        print("Datenbank 5 abgerufen")

try:
        PlotSet.execute("SELECT * FROM settingsScanPlot WHERE ID = 1")
        for dsatzPlot in PlotSet:
                plotstyle = dsatzPlot[1]
                plotname = dsatzPlot[2]
                
        PlotStyle = plotstyle
        FilePath = ""
        FileName = ""
        PlotName = plotname
except:
        pass

try:
        PlotSet.execute("SELECT * FROM settingsScanPlot")
        print(PlotSet.fetchall())
except:
        pass

try:
        connPlot.commit()                                                                                                                               #never forget this, if you want the changes to be saved:
except:
        print("database 5 failed")

#Device Settings
try:
        connDev = sqlite3.connect("settingsScanDev.db")
        DevSet = connDev.cursor()
except:
        print("no database 6 connection")

try:
        DevSet.execute("""
        CREATE TABLE settingsScanDev (
        ID integer,
        piezodistanceX integer,
        piezodistanceY integer,
        piezodistanceZ integer,
        piezovoltage real,
        ChA text,
        ChB text,
        L2 text,
        L3 text,
        Ch1 text,
        Ch2 text,
        Ch3 text,
        Ch4 text)""")
        print("Datenbank 6 wurde angelegt")   
        DevSet.execute("INSERT INTO settingsScanDev (ID, piezodistanceX, piezodistanceY, piezodistanceZ, piezovoltage, ChA, ChB, L2, L3, Ch1, Ch2, Ch3, Ch4) VALUES (" + str(1) + ", " + str(PiezoDistanceX) + ", " + str(PiezoDistanceY) + ", " + str(PiezoDistanceZ) + ", " + str(PiezoVoltage) + ", " + "\"" + CHA  + "\"" + ", " + "\"" + CHB  + "\"" + ", " + "\"" + L2  + "\"" + ", " + "\"" + L3  + "\"" + ", " + "\"" + CH1  + "\"" + ", " + "\"" + CH2  + "\"" + ", " + "\"" + CH3  + "\"" + ", " + "\"" + CH4  + "\")")
        print("Settings saved")
except:
        print("Datenbank 6 abgerufen")

try:
        DevSet.execute("SELECT * FROM settingsScanDev WHERE ID = 1")
        for dsatzDev in DevSet:
                piezodistanceX = dsatzDev[1]
                piezodistanceY = dsatzDev[2]
                piezodistanceZ = dsatzDev[3]
                piezovoltage = dsatzDev[4]
                ChA = dsatzDev[5]
                ChB = dsatzDev[6]
                l2 = dsatzDev[7]
                l3 = dsatzDev[8]
                Ch1 = dsatzDev[9]
                Ch2 = dsatzDev[10]
                Ch3 = dsatzDev[11]
                Ch4 = dsatzDev[12]
                #print(piezodistanceX + ", " + piezodistanceY + ", " + piezodistanceZ + ", " + piezovoltage + ", " + ChA + ", " + ChB + ", " + l2 + ", " + l2 + ", " + Ch1 + ", " + Ch2 + ", " + Ch3 + ", " + Ch4 + ", " + Ch5)

        PiezoDistanceX = piezodistanceX                     #Nanometers
        PiezoDistanceY = piezodistanceY                     #Nanometers
        PiezoDistanceZ = piezodistanceZ                     #Nanometers
        PiezoVoltage = piezovoltage                         #Volts
        CHA = ChA                                           #Channel A
        CHB = ChB                                           #Channel B
        L2 = l2                                             #Channel L2
        L3 = l3                                             #Channel L3
        CH1 = Ch1                                           #Channel 1
        CH2 = Ch2                                           #Channel 2
        CH3 = Ch3                                           #Channel 3
        CH4 = Ch4                                           #Channel 4
except:
        pass

try:                    
        DevSet.execute("SELECT * FROM settingsScanDev")
        print(DevSet.fetchall())
except:
        pass

try:
        connDev.commit()                                                                                                                                #never forget this, if you want the changes to be saved:
except:
        print("database 6 failed")

#TTL Settings
try:
        connTTL = sqlite3.connect("settingsScanTTL.db")
        TTLSet = connTTL.cursor()
except:
        print("no database 7 connection")

try:
        TTLSet.execute("""
        CREATE TABLE settingsScanTTL (
        ID ingeger,
        name1 text,
        wire1 integer,
        name2 text,
        wire2 integer)""")
        print("Datenbank 7 wurde angelegt")
        TTLSet.execute("INSERT INTO settingsScanTTL (ID, name1, wire1, name2, wire2) VALUES (" + str(1) + ", " + "\"" + NameTTL1  + "\"" + ", " + str(Wire1) + ", " + "\"" + NameTTL2  + "\"" + ", " + str(Wire2) + ")")
        print("Settings saved")
except:
        print("Datenbank 7 abgerufen")
        
try:
        TTLSet.execute("SELECT * FROM settingsScanTTL WHERE ID = 1")
        for dsatzTTL in TTLSet:
                name1 = dsatzTTL[1]
                wire1 = dsatzTTL[2]
                name2 = dsatzTTL[3]
                wire2 = dsatzTTL[4]      
        NameTTL1 = name1
        NameTTL2 = name2
        Wire1 = wire1
        Wire2 = wire2
except:
        pass

try:                    
        TTLSet.execute("SELECT * FROM settingsScanTTL")
        print(TTLSet.fetchall())
except:
        pass

try:
        connTTL.commit()                                                                                                                                #never forget this, if you want the changes to be saved:
except:
        print("database 7 failed")

#Logic imports
APDon = 0
APDWindowOn = 0
APDArduinoOn = 0
APDArduinoI2C = 0
APDArduinoSPI = 0
APDBSOn = 0
try:
        from APDArduinoLibI2C import ArduinoLogic
        APDs = ArduinoLogic()
        count1, count2 = APDs.captureDual(1)
        APDon = 1
        APDWindowOn = 1
        APDArduinoOn = 1
        APDArduinoI2C = 1
        APDArduinoSPI = 0
        APDBSOn = 0
        print("Arduino I2C")

except:
        print("No Arduino I2C")
        try:
                from APDArduinoLibSPI import ArduinoLogic
                APDs = ArduinoLogic()
                count1, count2 = APDs.captureDual(1)
                APDon = 1
                APDWindowOn = 1
                APDArduinoOn = 1
                APDArduinoI2C = 0
                APDArduinoSPI = 1
                APDBSOn = 0
                print("Arduino SPI")
        except:
                print("No Arduino SPI")
                try:
                        from APDread import APDLogic
                        APDs = APDLogic(5000,10)
                        APDs.capture_and_calc()
                        APDon = 1
                        APDWindowOn = 1
                        APDArduinoOn = 0
                        APDArduinoI2C = 0
                        APDArduinoSPI = 0
                        APDBSOn = 1
                        APDs.closeDevice()
                        print("BS APDs")
                except:
                        print("No APDs")
                        APDon = 0
                        APDWindowOn = 0
                        APDArduinoOn = 0
                        APDArduinoI2C = 0
                        APDArduinoSPI = 0
                        APDBSOn = 0
                        print("ADP imports failed")
                        #Create virtual APDs to catch errors
                        class ADP_Virtual():
                                def __init__(self):
                                        pass

                                def captureDual(self, val):
                                        print("No APD: " + str(val))
                                        a = random.uniform(0, (100*val))
                                        b = random.uniform(0, (100*val))
                                        return a, b
                                
                                def closeDevice(self):
                                        pass

                        APDs = ADP_Virtual()
                        count1, count2 = APDs.captureDual(1)

xstart = 0
ystart = 0
xstop = 255
ystop = 255
upperLimit1 = 100
lowerLimit1 = 0
upperLimit2 = 100
lowerLimit2 = 0
InvertXLive1 = False
InvertYLive1 = True
InvertXLive2 = False
InvertYLive2 = True
PlotBits = 256

zNew = list()
zNew2 = list()
zPart = list()
zPart2 = list()
x = xstart
y = ystart
while x <= xstop:
        while y <= ystop:
                if x >100 and x < 200 and y > 100 and y < 200:
                        zPart.append(x+y)
                else:
                        zPart.append(0)
                zPart2.append(0)
                y += 1
        y = ystart
        x += 1
        zNew.append(zPart)
        zNew2.append(zPart2)
        zPart = list()
        zPart2 = list()

y, x = np.meshgrid(np.linspace(ystart,ystop,(ystop-ystart+1)), np.linspace(xstart,xstop,(xstop-xstart+1)))

v = np.linspace(xstart,xstop,(xstop-xstart+1))
t = np.sin(v)*np.sin(v)
tt = np.cos(v)*np.cos(v)

N = 256
#---------------------------------------------------------------------------------------------
CMapMatrixWSXM = np.ones((N, 3))
CMapMatrixWSXM[0:67, 2] = np.linspace(6/255, 6/255, 67)                          #R
CMapMatrixWSXM[67:103, 2] = np.linspace(6/255, 17/255, (103-67))
CMapMatrixWSXM[103:161, 2] = np.linspace(17/255, 57/255, (161-103))
CMapMatrixWSXM[161:223, 2] = np.linspace(57/255, 136/255, (223-161))
CMapMatrixWSXM[223:255, 2] = np.linspace(136/255, 255/255, (255-223))

CMapMatrixWSXM[0:23, 1] = np.linspace(6/255, 7/255, 23)                          #G
CMapMatrixWSXM[23:73, 1] = np.linspace(7/255, 47/255, (73-23))
CMapMatrixWSXM[73:149, 1] = np.linspace(47/255, 159/255, (149-73))
CMapMatrixWSXM[149:208, 1] = np.linspace(159/255, 234/255, (208-149))
CMapMatrixWSXM[208:238, 1] = np.linspace(234/255, 255/255, (238-208))
CMapMatrixWSXM[238:255, 1] = np.linspace(255/255, 255/255, (255-238))

CMapMatrixWSXM[0:35, 0] = np.linspace(4/255, 43/255, 35)                         #B
CMapMatrixWSXM[35:95, 0] = np.linspace(43/255, 179/255, (95-35))
CMapMatrixWSXM[95:170, 0] = np.linspace(179/255, 255/255, (170-95))
CMapMatrixWSXM[170:255, 0] = np.linspace(255/255, 255/255, (255-170))

wsxmCMAP = ListedColormap(CMapMatrixWSXM)
inverseCMapMatrixWSXM = list(reversed(CMapMatrixWSXM))
wsxmCMAP_r = ListedColormap(inverseCMapMatrixWSXM)

#---------------------------------------------------------------------------------------------
CMapMatrixRHK = np.zeros((N, 3))

CMapMatrixRHK[0:N, 1] = np.linspace(1, 0, N)                          #G

CMapMatrixRHK[0:N, 0] = np.linspace(1, 1, N)                         #R

rhkCMAP_r = ListedColormap(CMapMatrixRHK)
inverseCMapMatrixRHK=list(reversed(CMapMatrixRHK))
rhkCMAP = ListedColormap(inverseCMapMatrixRHK)

#---------------------------------------------------------------------------------------------
CMapMatrixHydra = np.zeros((N, 3))
CMapMatrixHydra[0:256, 1] = np.linspace(0/255, 255/255, N)
HydraCMAP2 = ListedColormap(CMapMatrixHydra)
inverseCMapMatrixHydra=list(reversed(CMapMatrixHydra))
HydraCMAP2_r = ListedColormap(inverseCMapMatrixHydra)

#---------------------------------------------------------------------------------------------
CMapMatrixHydra2 = np.zeros((N, 3))
CMapMatrixHydra2[0:int(2*N/3), 1] = np.linspace(0/255, 255/255, int(2*N/3))
CMapMatrixHydra2[int(2*N/3):N, 1] = np.linspace(255/255, 255/255, int(1*N/3)+1)
CMapMatrixHydra2[0:int(N/2), 1] = np.linspace(0/255, 255/255, int(N/2))
CMapMatrixHydra2[int(N/2):N, 1] = np.linspace(255/255, 255/255, int(N/2))
CMapMatrixHydra2[int(N/2):N, 0] = np.linspace(0/255, 255/255, int(N/2))
CMapMatrixHydra2[int(N/2):N, 2] = np.linspace(0/255, 255/255, int(N/2))
HydraCMAP = ListedColormap(CMapMatrixHydra2)
inverseCMapMatrixHydra2=list(reversed(CMapMatrixHydra2))
HydraCMAP_r = ListedColormap(inverseCMapMatrixHydra2)


#---------------------------------------------------------------------------------------------
CMapMatrixBanksy = np.zeros((N, 3))
CMapMatrixBanksy[51:, 2] = np.linspace(0/255, 255/255, N-51)
CMapMatrixBanksy[51:, 1] = np.linspace(0/255, 255/255, N-51)
CMapMatrixBanksy[51:, 0] = np.linspace(0/255, 255/255, N-51)

CMapMatrixBanksy[0:50, 0] = np.linspace(255/255, 255/255, 50)
CMapMatrixBanksy[0:50, 2] = np.linspace(0/255, 0/255, 50)
CMapMatrixBanksy[0:50, 1] = np.linspace(0/255, 0/255, 50)
BanksyCMAP_r = ListedColormap(CMapMatrixBanksy)
inverseCMapMatrixBanksy=list(reversed(CMapMatrixBanksy))
BanksyCMAP = ListedColormap(inverseCMapMatrixBanksy)


try:
        GPIO.output(LEDPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LEDPin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(LEDPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LEDPin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(LEDPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LEDPin, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(LEDPin, GPIO.HIGH)
        GPIO.output(LEDPin, GPIO.LOW)
except:
        pass


# ---------------------------------------------------------------------------- Start ----------------------------------------------------------------------------

#-------Navigation Window
class NavWin(QWidget):
        progress_valueCheck = pyqtSignal(bool, bool, bool, int, int)
        progress_valueXY = pyqtSignal(int, int, int, int)
        progress_valueButton = pyqtSignal(bool)
        position_valueXY = pyqtSignal(float, float)
        progress_Focus = pyqtSignal(int)
        
        def __init__(self):
                #super(PlotWindow, self).__init__()
                super().__init__()
                global FullRangeDeviceX
                global FullRangeDeviceY
                global DeviceVoltage
                global PiezoVoltage
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.DimensionStepsX = round((FullRangeDeviceX*((PiezoVoltage/DeviceVoltage)/(DeviceVoltage*2)))/1000,3)
                self.DimensionStepsY = round((FullRangeDeviceY*((PiezoVoltage/DeviceVoltage)/(DeviceVoltage*2)))/1000,3)
                print(str(self.DimensionStepsX) + "x" + str(self.DimensionStepsY))

                self.XOld1 = 255
                self.YOld1 = 255
                self.XOldStart = 255
                self.YOldStart = 255
                self.XOldStop = 255
                self.YOldStop = 255
                self.geil = 0
                
                self.WindowPosX = WindowPosX + WindowWidth + 5
                self.WindowPosY = WindowPosY            

                # Define the geometry of the main window
                self.setGeometry(self.WindowPosX,self.WindowPosY,605,500)
                self.setMinimumSize(QSize(500,500))   
                self.setWindowTitle("Quick Navigation")                                                                                                 #Titelbalken
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Navigation.png"))
                self.BitVal = 255
                self.XStart = 0
                self.YStart = 0

                # Create a Layout
                self.LAYOUT_A = QVBoxLayout(self)
                self.LAYOUTH = QHBoxLayout(self)
                self.LAYOUTV = QVBoxLayout(self)

                self.myFig = NavPlot()
                self.myFig.progress_valueXYrect.connect(self.NewDimRect)
                self.myFig.progress_valueXYpos.connect(self.PosFromPlot)
                self.myFig.adjustSize()

                self.SpinX = QDoubleSpinBox(self)
                self.SpinX.setMinimum(0.000)                                                                                                            #Setzt ein Minimalwert für die Auswahl
                self.SpinX.setMaximum(round(FullRangeDeviceX/1000,3))                                                                                   #Setzt ein Maximum für die Auswahl
                self.SpinX.setValue(round(FullRangeDeviceX/1000,3))                                                                                     #Setzt einen Startwert
                self.SpinX.setSingleStep(self.DimensionStepsX)
                self.SpinX.setDecimals(3)
                self.SpinX.setToolTip("Sets the X-Dimensions [\u03BCm]")
                self.SpinX.valueChanged.connect(self.XChanged)
                self.labelSpinX = QLabel("X-Dimensions [\u03BCm]", self) 

                self.SpinY = QDoubleSpinBox(self)
                self.SpinY.setMinimum(0.000)                                                                                                            #Setzt ein Minimalwert für die Auswahl
                self.SpinY.setMaximum(round(FullRangeDeviceY/1000,3))                                                                                   #Setzt ein Maximum für die Auswahl
                self.SpinY.setValue(round(FullRangeDeviceY/1000,3))                                                                                     #Setzt einen Startwert
                self.SpinY.setSingleStep(self.DimensionStepsY)
                self.SpinY.setDecimals(3)
                self.SpinY.setToolTip("Sets the Y-Dimensions [\u03BCm]")
                self.SpinY.valueChanged.connect(self.YChanged)
                self.labelSpinY = QLabel("Y-Dimensions [\u03BCm]", self)

                self.Bits = QComboBox(self)
                self.Bits.addItem("64")
                self.Bits.addItem("128")
                self.Bits.addItem("256")
                self.Bits.addItem("512")
                self.Bits.addItem("1024")
                self.Bits.addItem("2048")
                self.Bits.addItem("4096")
                self.Bits.setCurrentIndex(2)
                self.Bits.currentIndexChanged.connect(self.updateCheck)

                self.Volts = QComboBox(self)
                self.Volts.addItem("10 V")
                self.Volts.addItem("9.5 V")
                self.Volts.addItem("9 V")
                self.Volts.addItem("8.5 V")
                self.Volts.addItem("8 V")
                self.Volts.addItem("7.5 V")
                self.Volts.addItem("7 V")
                self.Volts.addItem("6.5 V")
                self.Volts.addItem("6 V")
                self.Volts.addItem("5.5 V")
                self.Volts.addItem("5 V")
                self.Volts.addItem("4.5 V")
                self.Volts.addItem("4 V")
                self.Volts.addItem("3.5 V")
                self.Volts.addItem("3 V")
                self.Volts.addItem("2.5 V")
                self.Volts.addItem("2 V")
                self.Volts.addItem("1.5 V")
                self.Volts.addItem("1 V")
                self.Volts.addItem("0.5 V")
                self.Volts.setCurrentIndex(0)
                self.Volts.currentIndexChanged.connect(self.updateVolts)

                self.labelIntTime = QLabel("Integration Time [ms]", self)
                self.spinIntTime = QSpinBox(self)
                self.spinIntTime.setMinimum(1)
                self.spinIntTime.setMaximum(20)
                self.spinIntTime.setValue(1)
                self.spinIntTime.setToolTip("Set the Integrationtime of the Logic-Channels in Milliseconds")
                self.spinIntTime.valueChanged.connect(self.updateCheck)

                # Place the zoom button
                self.buttonStart = QPushButton(text = 'Start')
                self.buttonStart.setCheckable(True)
                self.buttonStart.setToolTip("Starts the Measurement")                                                                                   #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonStart.clicked[bool].connect(self.updateButton)
                self.buttonStart.setChecked(False)

                self.ButtonFull = QPushButton(text = 'Full Range')
                self.ButtonFull.clicked.connect(self.FullRect)
                #self.ButtonFull.clicked.connect(self.Resize)
                #self.ButtonFull.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.labelFullSpace = QLabel(" ", self)

                #self.ButtonLoad = QPushButton(text = 'Load Plot')
                #self.ButtonLoad.setFixedSize(150, 30)
                #self.ButtonLoad.clicked.connect(self.OpenPlotFile)
                #self.ButtonLoad.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                #self.ButtonClear = QPushButton(text = 'Clear all')
                #self.ButtonClear.setFixedSize(150, 30)
                #self.ButtonClear.clicked.connect(self.clear)
                #self.ButtonClear.clicked.connect(self.SetRect)
                #self.ButtonClear.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.ButtonFocus = QPushButton(text = 'Autofocus')
                self.ButtonFocus.setCheckable(True)
                self.ButtonFocus.setToolTip("Starts the Autofocus")                                                                                     #Setzt eine Buttonbeschreibung bei MouseOver
                self.ButtonFocus.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                #self.ButtonFocus.clicked.connect(self.FullRect)
                self.ButtonFocus.clicked[bool].connect(self.AutoFocus)
                self.ButtonFocus.setChecked(False)

                self.TTLSync = QCheckBox("Use TTL-Sync", self)
                self.TTLSync.stateChanged.connect(self.updateCheck)

                self.ZStack = QCheckBox("Use Z-Stack", self)
                self.ZStack.stateChanged.connect(self.ZStackCheck)

                self.Slope = QCheckBox("Use Slope", self)
                self.Slope.setChecked(False)
                self.Slope.stateChanged.connect(self.SlopeCheck)

                self.groupboxDimensions = QGroupBox("Dimensions", self)
                self.vboxX = QVBoxLayout(self)
                self.vboxX.addWidget(self.labelSpinX)
                self.vboxX.addWidget(self.SpinX)
                self.vboxX.addStretch(1)
                self.vboxY = QVBoxLayout(self)
                self.vboxY.addWidget(self.labelSpinY)
                self.vboxY.addWidget(self.SpinY)
                self.vboxY.addStretch(1)
                self.vboxFull = QVBoxLayout(self)
                self.vboxFull.addWidget(self.labelFullSpace)
                self.vboxFull.addWidget(self.ButtonFull)
                self.hboxDimensions = QHBoxLayout(self)
                self.hboxDimensions.addLayout(self.vboxX)
                self.hboxDimensions.addLayout(self.vboxY)
                self.hboxDimensions.addLayout(self.vboxFull)
                self.groupboxDimensions.setLayout(self.hboxDimensions)

                self.groupboxMeasure = QGroupBox("Measurement", self)
                self.vboxMeasure = QVBoxLayout(self)
                self.vboxMeasure.addWidget(self.buttonStart)
                self.vboxMeasure.addWidget(self.TTLSync)
                self.vboxMeasure.addWidget(self.ZStack)
                self.vboxMeasure.addWidget(self.Slope)
                self.vboxMeasure.addWidget(self.labelIntTime)
                self.vboxMeasure.addWidget(self.spinIntTime)
                self.groupboxMeasure.setLayout(self.vboxMeasure)

                self.groupboxSettings = QGroupBox("Settings", self)
                self.vboxSettings = QVBoxLayout(self)
                self.vboxSettings.addWidget(self.ButtonFocus)
                #self.vboxSettings.addWidget(self.ButtonLoad)
                #self.vboxSettings.addWidget(self.ButtonClear)
                self.vboxSettings.addWidget(self.Bits)
                self.vboxSettings.addWidget(self.Volts)
                self.groupboxSettings.setLayout(self.vboxSettings)

                self.LAYOUTV.addWidget(self.groupboxMeasure)
                self.LAYOUTV.addWidget(self.groupboxSettings)

                self.LAYOUTH.addLayout(self.LAYOUTV)
                self.LAYOUTH.addWidget(self.myFig)

                self.LAYOUT_A.addLayout(self.LAYOUTH)
                self.LAYOUT_A.addWidget(self.groupboxDimensions)

                self.setLayout(self.LAYOUT_A)


        def updateVolts(self):
                IDVolts = self.Volts.currentIndex()
                if IDVolts == 0:
                        Volts = 10
                elif IDVolts == 1:
                        Volts = 9.5
                elif IDVolts == 2:
                        Volts = 9
                elif IDVolts == 3:
                        Volts = 8.5
                elif IDVolts == 4:
                        Volts = 8
                elif IDVolts == 5:
                        Volts = 7.5
                elif IDVolts == 6:
                        Volts = 7
                elif IDVolts == 7:
                        Volts = 6.5
                elif IDVolts == 8:
                        Volts = 6
                elif IDVolts == 9:
                        Volts = 5.5
                elif IDVolts == 10:
                        Volts = 5
                elif IDVolts == 11:
                        Volts = 4.5
                elif IDVolts == 12:
                        Volts = 4
                elif IDVolts == 13:
                        Volts = 3.5
                elif IDVolts == 14:
                        Volts = 3
                elif IDVolts == 15:
                        Volts = 2.5
                elif IDVolts == 16:
                        Volts = 2
                elif IDVolts == 17:
                        Volts = 1.5
                elif IDVolts == 18:
                        Volts = 1
                elif IDVolts == 19:
                        Volts = 0.5
                #Poti.write_range(Volts)

        def UncheckButton(self):
                self.buttonStart.setToolTip("Start the Measurement")
                self.buttonStart.setChecked(False)
                self.buttonStart.setText("Start")
                self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")

        def PositionFromMain(self, XStart, YStart, XStop, YStop):
                self.XStart = XStart
                self.YStart = YStart
                self.XStop = XStop
                self.YStop = YStop
                XDim = round(((self.XStop-self.XStart)*(FullRangeDeviceX/self.BitVal))/1000,0)
                #print("From Main: " + str(XDim))
                #print(XDim % 5)
                if (XDim % 5) != 0:
                        if ((XDim) % 5) == 4:
                                XDim = XDim + 1
                        elif ((XDim) % 5) == 3:
                                XDim = XDim + 2
                        elif ((XDim) % 5) == 1:
                                XDim = XDim - 1
                        elif ((XDim) % 5) == 2:
                                XDim = XDim - 2
                YDim = XDim
                #print("From Main: " + str(XDim))
                if XDim != self.SpinX.value():
                        self.SpinX.setValue(XDim)
                if YDim != self.SpinY.value():
                        self.SpinY.setValue(YDim)

                IDVolts = XDim/10
                Volts = 0
                if IDVolts == 10:
                        Volts = 0
                elif IDVolts == 9.5:
                        Volts = 1
                elif IDVolts == 9:
                        Volts = 2
                elif IDVolts == 8.5:
                        Volts = 3
                elif IDVolts == 8:
                        Volts = 4
                elif IDVolts == 7.5:
                        Volts = 5
                elif IDVolts == 7:
                        Volts = 6
                elif IDVolts == 6.5:
                        Volts = 7
                elif IDVolts == 6:
                        Volts = 8
                elif IDVolts == 5.5:
                        Volts = 9
                elif IDVolts == 5:
                        Volts = 10
                elif IDVolts == 4.5:
                        Volts = 11
                elif IDVolts == 4:
                        Volts = 12
                elif IDVolts == 3.5:
                        Volts = 13
                elif IDVolts == 3:
                        Volts = 14
                elif IDVolts == 2.5:
                        Volts = 15
                elif IDVolts == 2:
                        Volts = 16
                elif IDVolts == 1.5:
                        Volts = 17
                elif IDVolts == 1:
                        Volts = 18
                elif IDVolts == 0.5:
                        Volts = 19
                self.Volts.setCurrentIndex(Volts)

        def XChanged(self):
                X = self.SpinX.value()
                Y = self.SpinY.value()
                if X != Y and X != 100:
                        Y = X
                if Y != self.YOld1:
                        self.SpinY.setValue(Y)
                        self.NewDimSpin()
                        #print("Test1")
                        self.XOld1 = X
                        self.YOld1 = Y

        def YChanged(self):
                X = self.SpinX.value()
                Y = self.SpinY.value()
                if Y != X and Y != 100:
                        X = Y
                if X != self.XOld1:
                        self.SpinX.setValue(X)
                        #print("Test2")
                        self.NewDimSpin()
                        self.XOld1 = X
                        self.YOld1 = Y

        def NewDimSpin(self):
                X = self.SpinX.value()
                Y = self.SpinY.value()
                X = int(round(self.XStart+((X*1000)/(FullRangeDeviceX/self.BitVal)),0))
                Y = int(round(self.YStart+((Y*1000)/(FullRangeDeviceY/self.BitVal)),0))
                if self.XOldStart != self.XStart or self.YOldStart != self.YStart or self.XOldStop != X or self.YOldStop != Y:
                        self.myFig.SetRect(self.XStart,self.YStart,X,Y)
                        self.NewDimRect(self.XStart,self.YStart,X,Y)

        def NewDimRect(self, XStart, YStart, XStop, YStop):
                self.XStart = XStart
                self.YStart = YStart
                self.XStop = XStop
                self.YStop = YStop
                DivX = (self.XStop-self.XStart)
                DivY = (self.YStop-self.YStart)
                print(str(self.YStart) + "x" + str(self.YStop))
                if DivX>DivY:
                        self.XStop = self.XStart + DivY
                self.progress_valueXY.emit(self.XStart, self.YStart, self.XStop, self.YStop)

        def PosFromPlot(self, X, Y):
                self.position_valueXY.emit(X, Y)

        def clear(self):
                self.myFig.clear(0,0,self.BitVal,self.BitVal)
                self.NewDimRect(0,0,self.BitVal,self.BitVal)

        def SetRect(self):
                self.myFig.SetRect(0,0,self.BitVal,self.BitVal)
                self.NewDimRect(0,0,self.BitVal,self.BitVal)

        def FullRect(self):
                self.myFig.FullRect(self.BitVal)
                self.NewDimRect(0,0,self.BitVal,self.BitVal)

        def ZStackCheck(self):
                if self.ZStack.isChecked():
                        self.Slope.setChecked(False)
                self.updateCheck()

        def SlopeCheck(self):
                if self.Slope.isChecked():
                        self.ZStack.setChecked(False)
                self.updateCheck()

        def updateCheck(self):
                val1 = self.TTLSync.isChecked()
                val2 = self.ZStack.isChecked()
                val3 = self.Slope.isChecked()
                val4 = self.spinIntTime.value()
                val5 = self.Bits.currentIndex()
                self.progress_valueCheck.emit(val1, val2, val3, val4, val5)
                self.myFig.UpdateBits(val5)

        def updateXY(self):
                val1 = self.TTLSync.isChecked()
                val2 = self.ZStack.isChecked()
                val3 = self.Slope.isChecked()
                self.progress_valueXY.emit(val1, val2, val3, val4)

        def updateButton(self):
                val1 = self.buttonStart.isChecked()
                self.progress_valueButton.emit(val1)

        def OpenPlotFile(self):
                global TXTFilePath
                        
                self.FilePath2 = ""
                self.FilePath1 = str(QFileDialog.getOpenFileName(self, "Open File", "/home/pi/Desktop/Data", "Textfile (*.txt)"))
                lengthFilePath1 = len(self.FilePath1) - 22
                self.FilePath2 = self.FilePath1[2:lengthFilePath1]
                
                lengthFilePath2 = len(self.FilePath1) - 26
                self.NewFilePath = self.FilePath1[2:lengthFilePath2]
                DataStart = 0

                try:
                        TXTFilePath = self.FilePath2
                except:
                        pass

                try:
                        with open(self.FilePath2,'r') as csvfile:
                                plots = list(csv.reader(csvfile, delimiter='\t'))

                                self.XCol = 1
                                self.YCol = 2

                                if self.groupboxHeadlines.isChecked() == False:
                                        HeaderLines = 0
                                        Header = plots[HeaderLines]
                                        while Header != []:
                                                Header = plots[HeaderLines]
                                                HeaderLines = HeaderLines + 1

                                                DataStartNew = HeaderLines + 1
                                                DataStart = DataStartNew                  

                                i = 0

                                PlotsLength = len(plots)-1

                                xstart = int(plots[DataStart][self.XCol])
                                ystart = int(plots[DataStart][self.YCol])
                                xstop = int(plots[PlotsLength][self.XCol])
                                ystop = int(plots[PlotsLength][self.YCol])

                                self.xlen = xstop - xstart
                                self.ylen = ystop - ystart
                except:
                        DataStart = DataStart + 1
                        try:
                                with open(self.FilePath2,'r') as csvfile:
                                        plots = list(csv.reader(csvfile, delimiter='\t'))
                                                                        
                                        self.XCol = 1
                                        self.YCol = 2
                                                                
                                        if self.groupboxHeadlines.isChecked() == False:
                                                HeaderLines = 0
                                                Header = plots[HeaderLines]
                                                while Header != []:
                                                        Header = plots[HeaderLines]
                                                        HeaderLines = HeaderLines + 1

                                                        DataStartNew = HeaderLines + 1
                                                        DataStart = DataStartNew

                                        i = 0

                                        PlotsLength = len(plots)-1

                                        xstart = int(plots[DataStart][self.XCol])
                                        ystart = int(plots[DataStart][self.YCol])
                                        xstop = int(plots[PlotsLength][self.XCol])
                                        ystop = int(plots[PlotsLength][self.YCol])

                                        self.xlen = xstop - xstart
                                        self.ylen = ystop - ystart
                        except:
                                pass

                print(self.FilePath2)

        def AutoFocus(self, down):                                                                                                                      #Setzt das Messfenster
                if down:
                        global FocusZ
                        self.FocusZ = FocusZ

                        self.ButtonFocus.setToolTip("Stop the Autofocus")
                        #self.ButtonFocus.setChecked(True)
                        self.ButtonFocus.setStyleSheet("color: black; background-color: rgb(255,0,0)")

                        self.Reading = SearchFocus(self.FocusZ)
                        self.Reading.progress_Focus.connect(self.setFocus)
                        self.Reading.start()
                else:
                        try:
                                self.Reading.kill()
                        except:
                                pass
                        self.ButtonFocus.setToolTip("Start the Autofocus")
                        self.ButtonFocus.setChecked(False)
                        self.ButtonFocus.setStyleSheet("color: black; background-color: rgb(0,255,0)")

        def setFocus(self, FocusNew):
                global FocusZ

                print("Old Focus: " + str(FocusZ) + " - New Focus: " + str(FocusNew))

                FocusZ = FocusNew
                self.progress_Focus.emit(FocusNew)
                self.ButtonFocus.setToolTip("Start the Autofocus")
                self.ButtonFocus.setChecked(False)
                self.ButtonFocus.setStyleSheet("color: black; background-color: rgb(0,255,0)")

class SearchFocus(QThread):
        progress_Focus = pyqtSignal(int)
        
        def __init__(self, FocusZ, parent=None):
                QThread.__init__(self, parent)
                self.i = 0   
                self.APD1 = 0
                self.APD2 = 0
                self.Integration = 10
                                
                GPIO.output(LEDPin, GPIO.HIGH)
                time.sleep(0.5)

                self.Voltage = round(10,1)
                print("Voltage: " + str(self.Voltage))
                Poti.write_range(self.Voltage)

                self.XOffset = 0
                self.YOffset = 0
                print("Offset: " + str(self.XOffset) + "x" + str(self.YOffset))
                dacOffset.setAllVoltage(self.XOffset, self.YOffset, 0, 0)
                
        def run(self):
                global APDon
                
                i = 0
                MaxValAPD1 = 0
                PosAPD1 = 2048
                MaxValAPD2 = 0
                PosAPD2 = 2048
                while i < 4000:
                        dacZ.set_voltage(i)
                        self.APD1, self.APD2 = APDs.captureDual(self.Integration)
                        if self.APD1 > MaxValAPD1:
                                MaxValAPD1 = self.APD1
                                PosAPD1 = i
                        if self.APD2 > MaxValAPD2:
                                MaxValAPD2 = self.APD2
                                PosAPD2 = i
                        i += 1

                if PosAPD1 != PosAPD2:
                        if MaxValAPD1 >= MaxValAPD2:
                                self.FocusMax = PosAPD1
                        else:
                                self.FocusMax = PosAPD2
                else:
                        self.FocusMax = PosAPD1

                self.progress_Focus.emit(self.FocusMax)
                dacZ.set_voltage(self.FocusMax)
                GPIO.output(LEDPin, GPIO.LOW)
                                
        def kill(self):
                self.i = 1
                GPIO.output(LEDPin, GPIO.LOW)


class NavPlot(FigureCanvas, TimedAnimation):
        progress_valueXYrect = pyqtSignal(int, int, int, int)
        progress_valueXYpos = pyqtSignal(float,float)
        
        def __init__(self):        
                # The data
                global xstart
                global ystart
                global xstop
                global ystop
                global upperLimit1
                global lowerLimit1
                global InvertXLive1
                global InvertYLive1
                global HydraCMAP
                global HydraCMAP_r

                self.HydraCMAP = HydraCMAP
                self.HydraCMAP_r = HydraCMAP_r
                
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
                self.cmap = self.HydraCMAP
                self.fig, self.ax1  = plt.subplots()
                plt.axis('off')
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)

                self.ax1.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))

                self.ax1.set_aspect('equal')
                
                FigureCanvas.__init__(self, self.fig)
                #cid3 = self.fig.canvas.mpl_connect('key_press_event', self.toggle_selector)
                cid1 = self.fig.canvas.mpl_connect('button_press_event', self.on_press2)
                #cid2 = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

                self.RS = RectangleSelector(self.ax1, self.line_select_callback,
                        drawtype='box', useblit=False, button=[1,3], 
                        minspanx=5, minspany=5, spancoords='pixels', 
                        interactive=True,rectprops = dict(facecolor="#58F107", edgecolor = "#58F107", linewidth=1.5, alpha=1, fill=False))

                self.iteration = 0

        def UpdateBits(self, Bits):
                global HydraCMAP
                global HydraCMAP_r
                
                self.HydraCMAP = HydraCMAP
                self.HydraCMAP_r = HydraCMAP_r
                #print(Bits)
                """
                if Bits == 0:
                        self.Bits = 63
                elif Bits == 1:
                        self.Bits = 127
                elif Bits == 2:
                        self.Bits = 255
                elif Bits == 3:
                        self.Bits = 511
                elif Bits == 4:
                        self.Bits = 1023
                elif Bits == 5:
                        self.Bits = 2047
                elif Bits == 6:
                        self.Bits = 4095
                """
                self.Bits = 255
                self.xstart = 0
                self.ystart = 0
                self.xstop = 255
                self.ystop = 255
                #self.xstop = self.Bits
                #self.ystop = self.Bits
                self.upperLimit = 10
                self.lowerLimit = 0
                self.zNew = list()
                self.zPart = list()
                self.x = self.xstart
                self.y = self.ystart
                """
                while self.y <= self.ystop:
                        while self.x <= self.xstop:
                                self.zPart.append(0)
                                self.x += 1
                        self.x = self.xstart
                        self.y += 1
                        self.zNew.append(self.zPart)
                        self.zPart = list()

                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))
                self.RS.set_visible(False)
                self.RS.update()
                self.ax1.clear()
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax1.set_xlabel('X [Bits]')
                self.ax1.set_ylabel('Y [Bits]')
                self.ax1.set_aspect('equal')
                #plt.tight_layout(self.fig)
                FigureCanvas.__init__(self, self.fig)
                cid3 = self.fig.canvas.mpl_connect('key_press_event', self.toggle_selector)
                cid1 = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
                cid2 = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

                self.RS = RectangleSelector(self.ax1, self.line_select_callback,
                        drawtype='box', useblit=False, button=[1,3], 
                        minspanx=5, minspany=5, spancoords='pixels', 
                        interactive=True,rectprops = dict(facecolor="#58F107", edgecolor = "#58F107", linewidth=1.5, alpha=1, fill=False))
                """

        def SetRect(self, XStart, YStart, XStop, YStop):
                self.RS.extents = (XStart,XStop,YStart,YStop)
                self.RS.update()

        def FullRect(self, Bits):
                #print("Full2")
                ext = (0,Bits,0,Bits)
                self.RS.draw_shape(ext)
                self.RS._corner_handles.set_data(*self.RS.corners)
                self.RS._edge_handles.set_data(*self.RS.edge_centers)
                self.RS._center_handle.set_data(*self.RS.center)
                #self.RS.set_visible(False)
                self.RS.update()
                
        def clear(self, XStart, YStart, XStop, YStop):
                #print("Clear")
                self.RS.extents = (XStart,XStop,YStart,YStop)
                #self.RS.set_active(False)
                self.RS.set_visible(False)
                self.RS.update()

        def line_select_callback(self, eclick, erelease):
                'eclick and erelease are the press and release events'
                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
                #print("Start: " + str(x1) + "x" + str(y1))
                #print("Stop: " + str(x2) + "x" + str(y2))
                #print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (round(x1,0), y1, x2, y2))
                #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
                self.progress_valueXYrect.emit(int(round(x1,0)), int(round(y1,0)), int(round(x2,0)), int(round(y2,0)))

        def toggle_selector(self, event):
                #print(' Key pressed.')
                if event.key in ['Q', 'q'] and self.RS1.active:
                        #print(' RectangleSelector deactivated.')
                        self.RS.set_active(False)
                if event.key in ['A', 'a'] and not self.RS1.active:
                        #print(' RectangleSelector activated.')
                        self.RS.set_active(True)

        def on_press(self, event):
                self.RS.set_visible(True)
                self.XStart = event.xdata
                self.YStart = event.ydata
                self.RS.update()
                #print('you pressed', event.button, event.xdata, event.ydata)

        def on_release(self, event):
                #print('you released', event.button, event.xdata, event.ydata)
                self.XStop = event.xdata
                self.YStop = event.ydata
                self.RS.update()
                #if self.XStart == self.XStop and self.YStart == self.YStop:
                        #self.progress_valuePosition.emit(self.XStart, self.YStart)
                        #print(self.XStart)
                        #print(self.YStart)
                #self.RS.set_visible(False)

        def on_press2(self, pos):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage
                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)
                #print(str(self.DimensionStepsX) + "x" + str(self.DimensionStepsY))
                X = round((int(round(pos.xdata,0)) * (self.DimensionStepsX/255)),3)
                Y = round((int(round(pos.ydata,0)) * (self.DimensionStepsY/255)),3)
                #print("Position: " + str(X) + " x " + str(Y))
                self.progress_valueXYpos.emit(X, Y)


#Live Plot Window
class PlotWindow(QWidget):
        progress_valueRect = pyqtSignal(int, int, int, int)
        progress_valuePos = pyqtSignal(int, int)

        def __init__(self):
                #super(PlotWindow, self).__init__()
                super().__init__()
                keyboard.on_press_key("enter", self.EnteredRect)
                self.Fontsize = 10
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
                self.setWindowTitle("Live Plot")                                                                                                        #Titelbalken
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/LivePlot.png"))
                #self.showMaximized() 
                
                # Create a Layout
                self.LAYOUT_A = QHBoxLayout()
                
                # Place the zoom button
                #self.ButtonLive = QPushButton(text = 'Stop Live Plot')
                #self.ButtonLive.setCheckable(True)
                #self.ButtonLive.setFixedSize(230, 30)
                #self.ButtonLive.clicked[bool].connect(self.StartStopLive)
                #self.ButtonLive.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                #self.ButtonLive.setChecked(True)

                self.ButtonSave = QPushButton(text = 'Save Plots')
                self.ButtonSave.setFixedSize(230, 30)
                self.ButtonSave.clicked.connect(self.SavePlots)
                #self.ButtonSave.clicked.connect(self.Resize)
                self.ButtonSave.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                self.ButtonRefresh1 = QPushButton(text = 'Refresh Plot')
                self.ButtonRefresh1.setFixedSize(210, 30)
                #self.ButtonRefresh1.clicked.connect(self.SavePlots)
                self.ButtonRefresh1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                self.ButtonRefresh2 = QPushButton(text = 'Refresh Plot')
                self.ButtonRefresh2.setFixedSize(210, 30)
                #self.ButtonRefresh2.clicked.connect(self.SavePlots)
                self.ButtonRefresh2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                #self.ButtonZoom1 = QPushButton(text = 'Zoom')
                #self.ButtonZoom1.setFixedSize(210, 30)
                #self.ButtonZoom1.clicked.connect(self.SavePlots)
                #self.ButtonZoom1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                #self.ButtonZoom2 = QPushButton(text = 'Zoom')
                #self.ButtonZoom2.setFixedSize(210, 30)
                #self.ButtonZoom2.clicked.connect(self.SavePlots)
                #self.ButtonZoom2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.ButtonAutoScale1 = QPushButton(text = 'Auto Scale')
                self.ButtonAutoScale1.setCheckable(True)
                self.ButtonAutoScale1.setFixedSize(210, 30)
                self.ButtonAutoScale1.setFont(QFont(self.Fontstyle, 15, QFont.Bold))
                self.ButtonAutoScale1.setChecked(True)

                self.ButtonAutoScale2 = QPushButton(text = 'Auto Scale')
                self.ButtonAutoScale2.setCheckable(True)
                self.ButtonAutoScale2.setFixedSize(210, 30)
                self.ButtonAutoScale2.setFont(QFont(self.Fontstyle, 15, QFont.Bold))
                self.ButtonAutoScale2.setChecked(True)

                self.InvertCMAPLive1 = QCheckBox("Invert Color", self)
                self.InvertCMAPLive1.stateChanged.connect(self.InvertCMAP1)
                self.InvertXAxisLive1 = QCheckBox("Invert X", self)
                self.InvertXAxisLive1.stateChanged.connect(self.InvertXChanged1)
                self.InvertYAxisLive1 = QCheckBox("Invert Y", self)
                self.InvertYAxisLive1.setChecked(True)
                self.InvertYAxisLive1.stateChanged.connect(self.InvertYChanged1)

                self.InvertCMAPLive2 = QCheckBox("Invert Color", self)
                self.InvertCMAPLive2.stateChanged.connect(self.InvertCMAP2)
                self.InvertXAxisLive2 = QCheckBox("Invert X", self)
                self.InvertXAxisLive2.stateChanged.connect(self.InvertXChanged2)
                self.InvertYAxisLive2 = QCheckBox("Invert Y", self)
                self.InvertYAxisLive2.setChecked(True)
                self.InvertYAxisLive2.stateChanged.connect(self.InvertYChanged2)

                self.PlotColors1 = QComboBox(self)
                self.PlotColors1.setFixedSize(210, 30)
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/HydraCMAP2.png"), "HydraCMAP2")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/HydraCMAP.png"), "HydraCMAP")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/rhkCMAP.png"), "rhkCMAP")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/WsxmCMAP.png"), "wsxmCMAP")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Viridis.png"), "viridis")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Spectral.png"), "Spectral")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Grey.png"), "gray")   
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Inferno.png"), "inferno")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Magma.png"), "magma")
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Plasma.png"), "plasma") 
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/cividis.png"), "cividis")                                       #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/CMRmap.png"), "CMRmap")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BanksyCMAP.png"), "BanksyCMAP")                                 #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Bone.png"), "bone")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Wistia.png"), "Wistia")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Copper.png"), "copper")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Heat.png"), "gist_heat")                                        #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Winter.png"), "winter")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Spring.png"), "spring")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Summer.png"), "summer")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Autumn.png"), "autumn")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Hot.png"), "hot")                                               #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Cool.png"), "cool")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_ncar.png"), "gist_ncar")                                   #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/nipy_spectral.png"), "nipy_spectral")                           #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Reds.png"), "Reds")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Blues.png"), "Blues")                                           #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BrBG.png"), "BrBG")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BuGn.png"), "BuGn")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BuPu.png"), "BuPu")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/CMRmap.png"), "CMRmap")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PiYG.png"), "PiYG")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PuOr.png"), "PuOr")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PuRd.png"), "PuRd")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PuBu.png"), "PuBu")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/RdGy.png"), "RdGy")                                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/RdYlBu.png"), "RdYlBu")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/RdYlGn.png"), "RdYlGn")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/YlOrRd.png"), "YlOrRd")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/YlOrBr.png"), "YlOrBr")                                         #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/brg.png"), "brg")                                               #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/bwr.png"), "bwr")                                               #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/coolwarm.png"), "coolwarm")                                     #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/cubehelix.png"), "cubehelix")                                   #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_earth.png"), "gist_earth")                                 #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_rainbow.png"), "gist_rainbow")                             #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_stern.png"), "gist_stern")                                 #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gnuplot.png"), "gnuplot")                                       #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gnuplot2.png"), "gnuplot2")                                     #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/hsv.png"), "hsv")                                               #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/jet.png"), "jet")                                               #Setzt eine CheckBox
                self.PlotColors1.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/terrain.png"), "terrain")   
                self.PlotColors1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.PlotColors2 = QComboBox(self)
                self.PlotColors2.setFixedSize(210, 30)
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/HydraCMAP2.png"), "HydraCMAP2")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/HydraCMAP.png"), "HydraCMAP")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/rhkCMAP.png"), "rhkCMAP")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/WsxmCMAP.png"), "wsxmCMAP")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Viridis.png"), "viridis")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Spectral.png"), "Spectral")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Grey.png"), "gray")   
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Inferno.png"), "inferno")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Magma.png"), "magma")
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Plasma.png"), "plasma") 
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/cividis.png"), "cividis")                                                       
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/CMRmap.png"), "CMRmap")                                                    
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BanksyCMAP.png"), "BanksyCMAP")                                                         
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Bone.png"), "bone")                                                               
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Wistia.png"), "Wistia")                                                             
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Copper.png"), "copper")                                                             
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Heat.png"), "gist_heat")                                                          
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Winter.png"), "winter")                                                     
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Spring.png"), "spring")                                                    
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Summer.png"), "summer")                                                     
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Autumn.png"), "autumn")                                          
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Hot.png"), "hot")                                              
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Cool.png"), "cool")                                                         
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_ncar.png"), "gist_ncar")                                      
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/nipy_spectral.png"), "nipy_spectral")                                                
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Reds.png"), "Reds")                                                            
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/Blues.png"), "Blues")                                              
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BrBG.png"), "BrBG")                                                          
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BuGn.png"), "BuGn")                                                     
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/BuPu.png"), "BuPu")                                                    
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/CMRmap.png"), "CMRmap")                                                              
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PiYG.png"), "PiYG")                                                        
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PuOr.png"), "PuOr")                                                         
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PuRd.png"), "PuRd")                                                        
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/PuBu.png"), "PuBu")                                                           
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/RdGy.png"), "RdGy")                                                         
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/RdYlBu.png"), "RdYlBu")                                                 
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/RdYlGn.png"), "RdYlGn")                                                   
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/YlOrRd.png"), "YlOrRd")                                                
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/YlOrBr.png"), "YlOrBr")                                                      
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/brg.png"), "brg")                                                    
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/bwr.png"), "bwr")                                            
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/coolwarm.png"), "coolwarm")                                            
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/cubehelix.png"), "cubehelix")                                           
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_earth.png"), "gist_earth")                                           
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_rainbow.png"), "gist_rainbow")                                                      
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gist_stern.png"), "gist_stern")                                                          
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gnuplot.png"), "gnuplot")                                                              
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/gnuplot2.png"), "gnuplot2")                                                     
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/hsv.png"), "hsv")                                                             
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/jet.png"), "jet")                                                      
                self.PlotColors2.addItem(QIcon("/home/pi/Desktop/HydraScan/Files/Styles/terrain.png"), "terrain")
                self.PlotColors2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                self.RangeUpper1 = QSlider(Qt.Horizontal)
                self.RangeUpper1.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeUpper1.setMaximum(100)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeUpper1.setValue(100)                                                                                                          #Setzt einen Startwert
                self.RangeUpper1.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.RangeUpper1.setTickInterval(101)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeUpper1.valueChanged.connect(self.UpperRange1)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeUpper1.setToolTip("Sets the upper Range")
                self.labelRangeUpper1 = QLabel("Upper Range", self)

                self.RangeLower1 = QSlider(Qt.Horizontal)
                self.RangeLower1.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeLower1.setMaximum(100)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeLower1.setValue(0)                                                                                                            #Setzt einen Startwert
                self.RangeLower1.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.RangeLower1.setTickInterval(101)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeLower1.valueChanged.connect(self.LowerRange1)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeLower1.setToolTip("Sets the lower Range")
                self.labelRangeLower1 = QLabel("Lower Range", self)

                self.RangeUpper2 = QSlider(Qt.Horizontal)
                self.RangeUpper2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeUpper2.setMaximum(100)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeUpper2.setValue(100)                                                                                                          #Setzt einen Startwert
                self.RangeUpper2.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.RangeUpper2.setTickInterval(101)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeUpper2.valueChanged.connect(self.UpperRange2)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeUpper2.setToolTip("Sets the upper Range")
                self.labelRangeUpper2 = QLabel("Upper Range", self)

                self.RangeLower2 = QSlider(Qt.Horizontal)
                self.RangeLower2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeLower2.setMaximum(100)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeLower2.setValue(0)                                                                                                            #Setzt einen Startwert
                self.RangeLower2.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.RangeLower2.setTickInterval(101)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeLower2.valueChanged.connect(self.LowerRange2)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeLower2.setToolTip("Sets the lower Range")
                self.labelRangeLower2 = QLabel("Lower Range", self)

                self.ch1Live1 = QComboBox(self) 
                self.ch1Live1.addItem(self.CH1)                                                                                                         #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.ch1Live1.addItem(self.CH2)
                self.ch1Live1.addItem(self.CH3)
                self.ch1Live1.addItem(self.CH4)
                self.ch1Live1.addItem(self.CHA)
                self.ch1Live1.addItem(self.CHB)
                self.ch1Live1.addItem(self.L2)
                self.ch1Live1.addItem(self.L3)
                self.ch1Live1.setCurrentIndex(4)
                self.CheckedChannel1 = self.ch1Live1.currentText()
                self.ch1Live1.setFixedSize(210, 30)
                
                self.ch2Live1 = QComboBox(self) 
                self.ch2Live1.addItem(self.CH1)                                                                                                         #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.ch2Live1.addItem(self.CH2)
                self.ch2Live1.addItem(self.CH3)
                self.ch2Live1.addItem(self.CH4)
                self.ch2Live1.addItem(self.CHA)
                self.ch2Live1.addItem(self.CHB)
                self.ch2Live1.addItem(self.L2)
                self.ch2Live1.addItem(self.L3)
                self.ch2Live1.setCurrentIndex(5)
                self.CheckedChannel2 = self.ch2Live1.currentText()
                self.ch2Live1.setFixedSize(210, 30)
                
                # Place the matplotlib figure
                self.labelFigureStretch1 = QLabel(" ", self)
                self.labelFigureStretch1.setFont(QFont(self.Fontstyle, 8, QFont.Normal))
                self.labelFigureStretch2 = QLabel(" ", self)
                self.labelFigureStretch2.setFont(QFont(self.Fontstyle, 8, QFont.Normal))
                self.myFig1 = LumiMeshplot()
                self.myFig1.adjustSize()
                self.myFig2 = ScatMeshplot()
                self.myFig2.adjustSize()
                self.myFig3 = LumiLineplot()
                self.myFig3.adjustSize()
                self.myFig4 = ScatLineplot()
                self.myFig4.adjustSize()
                self.myFig1.progress_valueLumi.connect(self.updateRectLumi)
                self.myFig1.progress_valuePosition.connect(self.updatePosition)
                self.myFig2.progress_valueScat.connect(self.updateRectScat)
                self.myFig2.progress_valuePosition.connect(self.updatePosition)
                self.myFig3.progress_valuePosition.connect(self.PointAnalysis3)
                self.myFig4.progress_valuePosition.connect(self.PointAnalysis4)
                self.selector1 = SelectFromCollection(1, self.myFig1.ax1, self.myFig1.quad1)
                self.selector2 = SelectFromCollection(2, self.myFig2.ax2, self.myFig2.quad2)
                self.selector1.progress_values.connect(self.LineAnalysis1)
                self.selector2.progress_values.connect(self.LineAnalysis2)
                self.selector1.progress_valuesPoint.connect(self.PointAnalysis1)
                self.selector2.progress_valuesPoint.connect(self.PointAnalysis2)

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
                #self.groupboxRange1.setFixedSize(120, 150)

                self.groupboxRange2 = QGroupBox("Range", self)
                self.vboxRange2 = QVBoxLayout(self)
                self.vboxRange2.addWidget(self.labelRangeLower2)
                self.vboxRange2.addWidget(self.RangeLower2)
                self.vboxRange2.addWidget(self.labelRangeUpper2)
                self.vboxRange2.addWidget(self.RangeUpper2)
                self.groupboxRange2.setLayout(self.vboxRange2)
                self.groupboxRange2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                #self.groupboxRange2.setFixedSize(120, 150)

                self.groupboxManipulateLumi = QGroupBox(self.CheckedChannel1, self)
                self.vboxManipulateLumi = QVBoxLayout(self)
                self.vboxManipulateLumi.addWidget(self.ch1Live1)
                self.vboxManipulateLumi.addWidget(self.splitter1)
                self.vboxManipulateLumi.addStretch(2)
                self.vboxManipulateLumi.addWidget(self.PlotColors1)
                self.vboxManipulateLumi.addStretch(1)
                self.vboxManipulateLumi.addWidget(self.InvertCMAPLive1)
                self.vboxManipulateLumiInvert = QHBoxLayout(self)
                self.vboxManipulateLumiInvert.addWidget(self.InvertXAxisLive1)
                self.vboxManipulateLumiInvert.addWidget(self.InvertYAxisLive1)
                self.vboxManipulateLumi.addLayout(self.vboxManipulateLumiInvert)
                self.vboxManipulateLumi.addStretch(2)
                self.vboxManipulateLumi.addWidget(self.groupboxRange1)
                self.vboxManipulateLumi.addStretch(2)
                self.vboxManipulateLumi.addWidget(self.ButtonAutoScale1)
                self.vboxManipulateLumi.addWidget(self.ButtonRefresh1)
                #self.vboxManipulateLumi.addWidget(self.ButtonZoom1)
                self.groupboxManipulateLumi.setLayout(self.vboxManipulateLumi)
                self.groupboxManipulateLumi.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                #self.groupboxManipulateLumi.setFixedSize(130, 500)

                self.groupboxManipulateScat = QGroupBox(self.CheckedChannel2, self)
                self.vboxManipulateScat = QVBoxLayout(self)
                self.vboxManipulateScat.addWidget(self.ch2Live1)
                self.vboxManipulateScat.addWidget(self.splitter2)
                self.vboxManipulateScat.addStretch(2)
                self.vboxManipulateScat.addWidget(self.PlotColors2)
                self.vboxManipulateScat.addStretch(1)
                self.vboxManipulateScat.addWidget(self.InvertCMAPLive2)
                self.vboxManipulateScatInvert = QHBoxLayout(self)
                self.vboxManipulateScatInvert.addWidget(self.InvertXAxisLive2)
                self.vboxManipulateScatInvert.addWidget(self.InvertYAxisLive2)
                self.vboxManipulateScat.addLayout(self.vboxManipulateScatInvert)
                self.vboxManipulateScat.addStretch(2)
                self.vboxManipulateScat.addWidget(self.groupboxRange2)
                self.vboxManipulateScat.addStretch(2)
                self.vboxManipulateScat.addWidget(self.ButtonAutoScale2)
                self.vboxManipulateScat.addWidget(self.ButtonRefresh2)
                #self.vboxManipulateScat.addWidget(self.ButtonZoom2)
                self.groupboxManipulateScat.setLayout(self.vboxManipulateScat)
                self.groupboxManipulateScat.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                #self.groupboxManipulateScat.setFixedSize(130, 500)
                
                self.groupboxLumi = QGroupBox(self.CheckedChannel1, self) 
                self.vboxLumi = QGridLayout(self)
                self.vboxLumi.addWidget(self.myFig1, 0, 0)
                self.vboxLumi.addWidget(self.myFig3, 1, 0)
                self.vboxLumi.addWidget(self.labelFigureStretch1)
                self.vboxLumi.setRowStretch(0, 3)
                self.vboxLumi.setRowStretch(1, 1)
                #self.vboxLumi = QVBoxLayout(self)
                #self.vboxLumi.addWidget(self.myFig1)
                #self.vboxLumi.addStretch(1)
                #self.vboxLumi.addWidget(self.myFig3)
                #self.vboxLumi.addWidget(self.labelFigureStretch1)
                self.groupboxLumi.setLayout(self.vboxLumi)
                self.groupboxLumi.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

                self.groupboxScat = QGroupBox(self.CheckedChannel2, self)            
                self.vboxScat = QGridLayout(self)
                self.vboxScat.addWidget(self.myFig2, 0, 0)
                self.vboxScat.addWidget(self.myFig4, 1, 0)
                self.vboxScat.addWidget(self.labelFigureStretch2)
                self.vboxScat.setRowStretch(0, 3)
                self.vboxScat.setRowStretch(1, 1)
                #self.vboxScat = QVBoxLayout(self)
                #self.vboxScat.addWidget(self.myFig2)
                #self.vboxScat.addStretch(1)
                #self.vboxScat.addWidget(self.myFig4)
                #self.vboxScat.addWidget(self.labelFigureStretch2)
                self.groupboxScat.setLayout(self.vboxScat)
                self.groupboxScat.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

                self.groupboxChannelSettings = QGroupBox("Settings", self)
                self.LayoutChannelSettings = QVBoxLayout(self)
                #self.LayoutChannelSettings.addWidget(self.ButtonLive)
                self.LayoutChannelSettings.addWidget(self.ButtonSave)
                #self.LayoutChannelSettings.addStretch(1)
                self.LayoutChannelSettings.addWidget(self.groupboxManipulateLumi)
                #self.LayoutChannelSettings.addStretch(1)
                self.LayoutChannelSettings.addWidget(self.groupboxManipulateScat)
                self.groupboxChannelSettings.setLayout(self.LayoutChannelSettings)
                self.groupboxChannelSettings.setFont(QFont(self.Fontstyle, 15, QFont.Bold))
                self.groupboxChannelSettings.setFixedSize(250, 1000)

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
                self.showMaximized()

        def updateRectLumi(self, val1, val2, val3, val4):
                self.progress_valueRect.emit(val1, val2, val3, val4)
                self.myFig2.HideRectangle()
                
        def updateRectScat(self, val1, val2, val3, val4):
                self.progress_valueRect.emit(val1, val2, val3, val4)
                self.myFig1.HideRectangle()

        def updatePosition(self, val1, val2):
                self.progress_valuePos.emit(val1, val2)

        def EnteredRect(self, val):
                #print("Test")
                self.myFig1.HideRectangle()
                self.myFig2.HideRectangle()

        def NewLine(self, Lumi, Scat):
                #global zNew
                #global zNew2
                #t1 = Thread(target=self.CalcNewValues1, args=(Lumi,))
                #t1.start()
                #t2 = Thread(target=self.CalcNewValues2, args=(Scat,))
                #t2.start()
                self.CalcNewValues1(Lumi)
                self.CalcNewValues2(Scat)

        def Date(self, Date):
                self.myFig1.UpdateFilename(Date)
                self.myFig2.UpdateFilename(Date)
                #print(Date)

        def printer(self, i):
                print(i)
                print(self.ch1Live1.currentText())

        def ChannelSelect(self):
                global CH1
                global CH2
                global CH3
                global CH4
                global CHA
                global CHB
                global L2
                global L3
                
                Channel1 = self.ch1Live1.currentText()
                Channel2 = self.ch2Live1.currentText()
                
                #print("Selected Channels: " + Channel1 + "\t" + Channel2)

                if Channel1 == CHA:
                        Axistext = Channel1 + " [Counts]"
                        Headline = Channel1
                elif Channel1 == CHB:
                        Axistext = Channel1 + " [Counts]"
                        Headline = Channel1
                elif Channel1 == L2:
                        Axistext = Channel1 + " [Counts]"
                        Headline = Channel1
                elif Channel1 == L3:
                        Axistext = Channel1 + " [Counts]"
                        Headline = Channel1
                elif Channel1 == CH1:
                        Axistext = Channel1 + " [V]"
                        Headline = Channel1
                elif Channel1 == CH2:
                        Axistext = Channel1 + " [V]"
                        Headline = Channel1
                elif Channel1 == CH3:
                        Axistext = Channel1 + " [V]"
                        Headline = Channel1
                elif Channel1 == CH4:
                        Axistext = Channel1 + " [V]"
                        Headline = Channel1
                else:
                        Axistext = ""
                        Headline = ""
                self.myFig1.ChannelChanged(Axistext, Headline)
                self.myFig3.ChannelChanged(Axistext, Headline)

                        
                if Channel2 == CHA:
                        Axistext = Channel2 + " [Counts]"
                        Headline = Channel2
                elif Channel2 == CHB:
                        Axistext = Channel2 + " [Counts]"
                        Headline = Channel2
                elif Channel2 == L2:
                        Axistext = Channel2 + " [Counts]"
                        Headline = Channel2
                elif Channel2 == L3:
                        Axistext = Channel2 + " [Counts]"
                        Headline = Channel2
                elif Channel2 == CH1:
                        Axistext = Channel2 + " [V]"
                        Headline = Channel2
                elif Channel2 == CH2:
                        Axistext = Channel2 + " [V]"
                        Headline = Channel2
                elif Channel2 == CH3:
                        Axistext = Channel2 + " [V]"
                        Headline = Channel2
                elif Channel2 == CH4:
                        Axistext = Channel2 + " [V]"
                        Headline = Channel2
                else:
                        Axistext = ""
                        Headline = ""
                self.myFig2.ChannelChanged(Axistext, Headline)
                self.myFig4.ChannelChanged(Axistext, Headline)

                self.CheckedChannel1 = Channel1
                self.CheckedChannel2 = Channel2
                self.groupboxManipulateLumi.setTitle(self.CheckedChannel1)
                self.groupboxManipulateScat.setTitle(self.CheckedChannel2)
                self.groupboxLumi.setTitle(self.CheckedChannel1)
                self.groupboxScat.setTitle(self.CheckedChannel2)

        def StartStopLive(self, down):
                #print(down)
                #self.NewLine()
                if down:
                        self.ButtonLive.setText("Stop LivePlot")
                else:
                        self.ButtonLive.setText("Start LivePlot")
                #print("Refresh Scale 1")

        def SavePlots(self):
                self.myFig1.SaveFile()
                self.myFig2.SaveFile()
                #print("SavePlots")

        def Resize(self, NewXStart, NewXStop, NewYStart, NewYStop, bits):
                global xstart
                global ystart
                global xstop
                global ystop
                global zNew
                global zNew2
                global t
                global tt
                global v
                global PlotBits

                try:
                        self.selector1.disconnect()
                except:
                        pass
                
                try:
                        self.selector2.disconnect()
                except:
                        pass
                PlotBits = bits
                xstart = NewXStart
                ystart = NewYStart
                xstop = NewXStop
                ystop = NewYStop
                zNew = list()
                zNew2 = list()
                zPart = list()
                zPart2 = list()
                x = 0
                y = 0
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

                v = np.linspace(xstart,xstop,(xstop-xstart+1))
                t = np.sin(v)*np.sin(v)
                tt = np.cos(v)*np.cos(v)
                
                self.ReplaceLabel1 = QLabel(" ")
                self.ReplaceLabel2 = QLabel(" ")
                self.ReplaceLabel3 = QLabel(" ")
                self.ReplaceLabel4 = QLabel(" ")
                self.vboxLumi.replaceWidget(self.myFig1, self.ReplaceLabel1)
                self.vboxScat.replaceWidget(self.myFig2, self.ReplaceLabel2)
                self.vboxLumi.replaceWidget(self.myFig3, self.ReplaceLabel3)
                self.vboxScat.replaceWidget(self.myFig4, self.ReplaceLabel4)
                self.myFig1.close()
                self.myFig2.close()
                self.myFig3.close()
                self.myFig4.close()
                self.myFig1 = LumiMeshplot()
                self.myFig1.adjustSize()
                self.myFig2 = ScatMeshplot()
                self.myFig2.adjustSize()
                self.myFig3 = LumiLineplot()
                self.myFig3.adjustSize()
                self.myFig4 = ScatLineplot()
                self.myFig4.adjustSize()
                self.myFig1.progress_valueLumi.connect(self.updateRectLumi)
                self.myFig1.progress_valuePosition.connect(self.updatePosition)
                self.myFig2.progress_valueScat.connect(self.updateRectScat)
                self.myFig2.progress_valuePosition.connect(self.updatePosition)
                self.myFig3.progress_valuePosition.connect(self.PointAnalysis3)
                self.myFig4.progress_valuePosition.connect(self.PointAnalysis4)
                self.selector1 = SelectFromCollection(1, self.myFig1.ax1, self.myFig1.quad1)
                self.selector2 = SelectFromCollection(2, self.myFig2.ax2, self.myFig2.quad2)
                self.selector1.progress_values.connect(self.LineAnalysis1)
                self.selector2.progress_values.connect(self.LineAnalysis2)
                self.selector1.progress_valuesPoint.connect(self.PointAnalysis1)
                self.selector2.progress_valuesPoint.connect(self.PointAnalysis2)
                
                self.vboxLumi.replaceWidget(self.ReplaceLabel1, self.myFig1)
                self.vboxScat.replaceWidget(self.ReplaceLabel2, self.myFig2)
                self.vboxLumi.replaceWidget(self.ReplaceLabel3, self.myFig3)
                self.vboxScat.replaceWidget(self.ReplaceLabel4, self.myFig4)
                self.iteration1 = 0
                self.iteration2 = 0

        def UpperRange1(self):
                global upperLimit1
                global lowerLimit1
                value = self.RangeUpper1.value()
                upperLimit1 = value
                self.myFig1.RangeChangeAnimate(upperLimit1, lowerLimit1)
                self.myFig3.RangeChangeAnimate(upperLimit1, lowerLimit1)
                #print("Upper Range 1: " + str(upperLimit1))

        def UpperRange2(self):
                global upperLimit2
                global lowerLimit2
                value = self.RangeUpper2.value()
                upperLimit2 = value
                self.myFig2.RangeChangeAnimate(upperLimit2, lowerLimit2)
                self.myFig4.RangeChangeAnimate(upperLimit2, lowerLimit2)
                #print("Upper Range 2: " + str(upperLimit2))

        def LowerRange1(self):
                global upperLimit1
                global lowerLimit1
                value = self.RangeLower1.value()
                lowerLimit1 = value
                self.myFig1.RangeChangeAnimate(upperLimit1, lowerLimit1)
                self.myFig3.RangeChangeAnimate(upperLimit1, lowerLimit1)
                #print("Lower Range 1: " + str(lowerLimit1))

        def LowerRange2(self):
                global upperLimit2
                global lowerLimit2
                value = self.RangeLower2.value()
                lowerLimit2 = value
                self.myFig2.RangeChangeAnimate(upperLimit2, lowerLimit2)
                self.myFig4.RangeChangeAnimate(upperLimit2, lowerLimit2)
                #print("Lower Range 2: " + str(lowerLimit2))

        def PlotsytleChanged1(self, Plotstyle):
                InvertCMAPLive1 = self.InvertCMAPLive1.isChecked()
                self.myFig1.UpdateCMAP(InvertCMAPLive1,Plotstyle)

        def PlotsytleChanged2(self, Plotstyle):
                InvertCMAPLive2 = self.InvertCMAPLive2.isChecked()
                self.myFig2.UpdateCMAP(InvertCMAPLive2,Plotstyle)

        def InvertCMAP1(self):
                InvertCMAPLive1 = self.InvertCMAPLive1.isChecked()
                Plotstyle = self.PlotColors1.currentText()
                self.myFig1.UpdateCMAP(InvertCMAPLive1,Plotstyle)
                        
        def InvertCMAP2(self):
                InvertCMAPLive2 = self.InvertCMAPLive2.isChecked()
                Plotstyle = self.PlotColors1.currentText()
                self.myFig2.UpdateCMAP(InvertCMAPLive2,Plotstyle)

        def InvertXChanged1(self):
                global InvertXLive1
                InvertXLive1 = self.InvertXAxisLive1.isChecked()
                self.myFig1.InvertX(InvertXLive1)
                #print("Invert X1: " + str(InvertXLive1))

        def InvertYChanged1(self):
                global InvertYLive1
                InvertYLive1 = self.InvertYAxisLive1.isChecked()
                self.myFig1.InvertY(InvertYLive1)
                #print("Invert Y1: " + str(InvertYLive1))

        def InvertXChanged2(self):
                global InvertXLive2
                InvertXLive2 = self.InvertXAxisLive2.isChecked()
                self.myFig2.InvertX(InvertXLive2)
                #print("Invert X2: " + str(InvertXLive2))

        def InvertYChanged2(self):
                global InvertYLive2
                InvertYLive2 = self.InvertYAxisLive2.isChecked()
                self.myFig2.InvertY(InvertYLive2)
                #print("Invert Y2: " + str(InvertYLive2))

        def closeEvent(self, event):
                print("End")

        def CalcNewValues1(self, Lumi):
                global zNew
                global t
                global xstop
                global ystop
                global xstart
                global ystart

                self.zNew = zNew
                self.t = t
                self.xstop = xstop
                self.ystop = ystop
                """
                self.zNew[self.iteration1] = Lumi
                """
                i = 0
                while i < self.ystop:
                        self.aNew = Lumi[i]
                        self.zNew[i][self.iteration1] = self.aNew
                        self.t[i] = self.aNew
                        #print("Point: " + str(self.zNew[i][self.iteration1]) + " x " + str(self.t[i]) + " x " + str(self.aNew))
                        i += 1
                self.iteration1 += 1

                if self.ButtonAutoScale1.isChecked() == True:
                        self.localMaximum1 = max(self.t)
                        self.localMinimum1 = min(self.t)
                        #print("Local Min/Max 1: " + str(self.Minimum1) + "\t" + str(self.Maximum1))

                        if self.localMinimum1 < self.Minimum1 or self.iteration1 == 1:
                                self.Minimum1 = int(self.localMinimum1)
                                self.RangeLower1.setValue(self.Minimum1)
                        if self.localMaximum1 > self.Maximum1 or self.iteration1 == 1:
                                self.Maximum1 = int(self.localMaximum1)
                                self.RangeUpper1.setValue(self.Maximum1)
                                self.RangeLower1.setMaximum(self.Maximum1+5)
                                self.RangeUpper1.setMaximum(self.Maximum1+5)
                                self.RangeLower1.setTickInterval(self.Maximum1+6)
                                self.RangeUpper1.setTickInterval(self.Maximum1+6)

                        self.myFig1.RangeChange(self.Maximum1+1, self.Minimum1)
                        self.myFig3.RangeChange(self.Maximum1+1, self.Minimum1)
                        
                self.myFig1.CalcNewLine1(self.zNew)
                self.myFig3.CalcNewLine1(self.t)
                zNew = self.zNew 

        def CalcNewValues2(self, Scat):
                global zNew2
                global tt
                global xstop
                global ystop
                global xstart
                global ystart

                self.zNew2 = zNew2
                self.tt = tt
                self.xstop = xstop
                self.ystop = ystop

                i = 0
                while i <= self.xstop:
                        #self.bNew = random.randint(0, 100)
                        self.bNew = Scat[i]
                        self.zNew2[i][self.iteration2] = self.bNew
                        self.tt[i] = self.bNew
                        i += 1
                self.iteration2 += 1

                if self.ButtonAutoScale2.isChecked() == True:
                        self.localMaximum2 = max(self.tt)
                        self.localMinimum2 = min(self.tt)
                        #print("Local Min/Max 2: " + str(self.Minimum2) + "\t" + str(self.Maximum2))

                        if self.localMinimum2 < self.Minimum2 or self.iteration2 == 1:
                                self.Minimum2 = int(self.localMinimum2)
                                self.RangeLower2.setValue(self.Minimum2)
                        if self.localMaximum2 > self.Maximum2 or self.iteration2 == 1:
                                self.Maximum2 = int(self.localMaximum2)
                                self.RangeUpper2.setValue(self.Maximum2)
                                self.RangeLower2.setMaximum(self.Maximum2+5)
                                self.RangeUpper2.setMaximum(self.Maximum2+5)
                                self.RangeLower2.setTickInterval(self.Maximum1+6)
                                self.RangeUpper2.setTickInterval(self.Maximum1+6)

                        self.myFig2.RangeChange(self.Maximum2+1, self.Minimum2)
                        self.myFig4.RangeChange(self.Maximum2+1, self.Minimum2)

                self.myFig2.CalcNewLine1(self.zNew2)
                self.myFig4.CalcNewLine1(self.tt)
                zNew2 = self.zNew2
                
        def LineAnalysis1(self, data):
                self.myFig3.LineAnalysis(data)

        def LineAnalysis2(self, data):
                self.myFig4.LineAnalysis(data)

        def PointAnalysis1(self, X, Y, Z):
                self.labelFigureStretch1.setText("Point: " + str(X) + " x " + str(Y) + "\tValue: " + str(Z))

        def PointAnalysis2(self, X, Y, Z):
                self.labelFigureStretch2.setText("Point: " + str(X) + " x " + str(Y) + "\tValue: " + str(Z))

        def PointAnalysis3(self, X, Y):
                self.labelFigureStretch1.setText("Point: " + str(X) + " x " + str(Y))

        def PointAnalysis4(self, X, Y):
                self.labelFigureStretch2.setText("Point: " + str(X) + " x " + str(Y))


class SelectFromCollection(QWidget):
        progress_values = pyqtSignal(list)
        progress_valuesPoint = pyqtSignal(int, int, int)
        
        def __init__(self, ID, ax, collection, alpha_other=0.3):
                super().__init__()
                self.ID = ID
                self.canvas = ax.figure.canvas
                self.collection = collection
                self.alpha_other = alpha_other

                self.xys = collection.get_offsets()
                self.Npts = len(self.xys)

                # Ensure that we have separate colors for each object
                self.fc = collection.get_facecolors()
                if len(self.fc) == 0:
                        raise ValueError('Collection must have a facecolor')
                elif len(self.fc) == 1:
                        self.fc = np.tile(self.fc, (self.Npts, 1))
                lineprops = {'color': (0,1,0), 'linewidth': 2, 'alpha': 1}
                self.lasso = LassoSelector(ax, onselect=self.onselect, lineprops = lineprops, button = 1)
                self.ind = []
                cid1 = self.canvas.mpl_connect('button_press_event', self.on_press)
                cid2 = self.canvas.mpl_connect('key_press_event', self.on_press)
                cid3 = self.canvas.mpl_connect('button_release_event', self.on_press)

        def on_press(self, pos):
                global zNew
                global zNew2
                if self.ID == 1:
                        ValueSource = zNew
                else:
                        ValueSource = zNew2
                X = int(round(pos.xdata,0))
                Y = int(round(pos.xdata,0))
                Z = int(round(ValueSource[X][Y],0))
                #print("Position: " + str(X) + " x " + str(Y) + "\tValue: " + str(Z))
                self.progress_valuesPoint.emit(X,Y,Z)

        def onselect(self, verts):
                global zNew
                global zNew2
                if self.ID == 1:
                        ValueSource = zNew
                else:
                        ValueSource = zNew2
                path = Path(verts)
                #print(verts)
                self.data=[]
                self.dataStorage = list()
                i = 0
                counter = 0
                XOld = -1
                YOld = -1
                if len(verts) == 1:
                        pass
                else:
                        while i < len(verts):
                                X = int(round(verts[i][0],0))
                                Y = int(round(verts[i][1],0))
                                if XOld == -1 and YOld == -1:
                                        value = ValueSource[X][Y]
                                        self.data = {
                                                "Counter":counter,
                                                "X":X,
                                                "Y":Y,
                                                "value":value}
                                        self.dataStorage.append(self.data)
                                        counter += 1                
                                elif X == XOld and Y == YOld:
                                        #print("Doppelter Wert: " + str(X) + " x " + str(Y))
                                        pass
                                elif X == XOld and (Y != YOld-1 or Y != YOld+1):
                                        #print("Bevorstehender Y Schritt zuweit: " + str(X) + " x " + str(Y))
                                        YNew = YOld
                                        while YNew > Y:
                                                YNew -= 1
                                                #print("Y Schritt zuweit: " + str(X) + " x " + str(YNew))
                                                value = ValueSource[X][YNew]
                                                self.data = {
                                                        "Counter":counter,
                                                        "X":X,
                                                        "Y":YNew,
                                                        "value":value}
                                                self.dataStorage.append(self.data)
                                                counter += 1
                                        while YNew < Y:
                                                YNew += 1
                                                #print("Y Schritt zuweit: " + str(X) + " x " + str(YNew))
                                                value = ValueSource[X][YNew]
                                                self.data = {
                                                        "Counter":counter,
                                                        "X":X,
                                                        "Y":YNew,
                                                        "value":value}
                                                self.dataStorage.append(self.data)
                                                counter += 1
                                elif Y == YOld and (X != XOld-1 or X != XOld+1):
                                        #print("Bevorstehender X Schritt zuweit: " + str(X) + " x " + str(Y))
                                        XNew = XOld
                                        while XNew > X:
                                                XNew -= 1
                                                #print("X Schritt zuweit: " + str(XNew) + " x " + str(Y))
                                                value = ValueSource[XNew][Y]
                                                self.data = {
                                                        "Counter":counter,
                                                        "X":XNew,
                                                        "Y":Y,
                                                        "value":value}
                                                self.dataStorage.append(self.data)
                                                counter += 1
                                        while XNew < X:
                                                XNew += 1
                                                #print("X Schritt zuweit: " + str(XNew) + " x " + str(Y))
                                                value = ValueSource[XNew][Y]
                                                self.data = {
                                                        "Counter":counter,
                                                        "X":XNew,
                                                        "Y":Y,
                                                        "value":value}
                                                self.dataStorage.append(self.data)
                                                counter += 1
                                elif (Y != YOld-1 or Y != YOld+1) and (X != XOld-1 or X != XOld+1):
                                        #print("Bevorstehender X und Y zuweit: " + str(X) + " x " + str(Y))
                                        XNew = XOld
                                        YNew = YOld
                                        if X < XOld and Y < YOld:
                                                while XNew > X:
                                                        XNew -= 1
                                                        if YNew > Y:
                                                                YNew -= 1
                                                        #print("-X und -Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                        value = ValueSource[XNew][YNew]
                                                        self.data = {
                                                                "Counter":counter,
                                                                "X":XNew,
                                                                "Y":YNew,
                                                                "value":value}
                                                        self.dataStorage.append(self.data)
                                                        counter += 1
                                                if YNew > Y:
                                                        while YNew > Y:
                                                                YNew -= 1
                                                                #print("X und -Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                                value = ValueSource[XNew][YNew]
                                                                self.data = {
                                                                        "Counter":counter,
                                                                        "X":XNew,
                                                                        "Y":YNew,
                                                                        "value":value}
                                                                self.dataStorage.append(self.data)
                                                                counter += 1
                                        elif X < XOld and Y > YOld:
                                                while XNew > X:
                                                        XNew -= 1
                                                        if YNew < Y:
                                                                YNew += 1
                                                        #print("-X und +Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                        value = ValueSource[XNew][YNew]
                                                        self.data = {
                                                                "Counter":counter,
                                                                "X":XNew,
                                                                "Y":YNew,
                                                                "value":value}
                                                        self.dataStorage.append(self.data)
                                                        counter += 1
                                                if YNew < Y:
                                                        while YNew < Y:
                                                                YNew += 1
                                                                #print("X und +Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                                value = ValueSource[XNew][YNew]
                                                                self.data = {
                                                                        "Counter":counter,
                                                                        "X":XNew,
                                                                        "Y":YNew,
                                                                        "value":value}
                                                                self.dataStorage.append(self.data)
                                                                counter += 1
                                        elif X > XOld and Y < YOld:
                                                while XNew < X:
                                                        XNew += 1
                                                        if YNew > Y:
                                                                YNew -= 1
                                                        #print("+X und Y- Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                        value = ValueSource[XNew][YNew]
                                                        self.data = {
                                                                "Counter":counter,
                                                                "X":XNew,
                                                                "Y":YNew,
                                                                "value":value}
                                                        self.dataStorage.append(self.data)
                                                        counter += 1
                                                if YNew > Y:
                                                        while YNew > Y:
                                                                YNew -= 1
                                                                #print("X und -Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                                value = ValueSource[XNew][YNew]
                                                                self.data = {
                                                                        "Counter":counter,
                                                                        "X":XNew,
                                                                        "Y":YNew,
                                                                        "value":value}
                                                                self.dataStorage.append(self.data)
                                                                counter += 1
                                        elif X > XOld and Y > YOld:
                                                while XNew < X:
                                                        XNew += 1
                                                        if YNew < Y:
                                                                YNew += 1
                                                        #print("+X und +Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                        value = ValueSource[XNew][YNew]
                                                        self.data = {
                                                                "Counter":counter,
                                                                "X":XNew,
                                                                "Y":YNew,
                                                                "value":value}
                                                        self.dataStorage.append(self.data)
                                                        counter += 1
                                                if YNew < Y:
                                                        while YNew < Y:
                                                                YNew += 1
                                                                #print("X und +Y Schritt zuweit: " + str(XNew) + " x " + str(YNew))
                                                                value = ValueSource[XNew][YNew]
                                                                self.data = {
                                                                        "Counter":counter,
                                                                        "X":XNew,
                                                                        "Y":YNew,
                                                                        "value":value}
                                                                self.dataStorage.append(self.data)
                                                                counter += 1
                                else:
                                        #print("X und Y perfekt: " + str(X) + " x " + str(Y))
                                        value = ValueSource[X][Y]
                                        self.data = {
                                                "Counter":counter,
                                                "X":X,
                                                "Y":Y,
                                                "value":value}
                                        self.dataStorage.append(self.data)
                                        counter += 1
                                XOld = X
                                YOld = Y
                                i += 1
                        #print(self.dataStorage)
                        i = 0
                        while i < len(self.dataStorage):
                                #print(self.dataStorage[i])
                                i += 1
                        if len(self.dataStorage) != 1:
                                self.progress_values.emit(self.dataStorage)

        def disconnect(self):
                self.lasso.disconnect_events()
                self.fc[:, -1] = 1
                self.collection.set_facecolors(self.fc)
                self.canvas.draw_idle()


class LumiMeshplot(FigureCanvas, TimedAnimation):
        progress_valueLumi = pyqtSignal(int, int, int, int)
        progress_valuePosition = pyqtSignal(int, int)

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
                global HydraCMAP
                global HydraCMAP_r
                global HydraCMAP2
                global HydraCMAP2_r
                global BanksyCMAP
                global BanksyCMAP_r
                global rhkCMAP
                global rhkCMAP_r
                global wsxmCMAP
                global wsxmCMAP_r

                self.HydraCMAP = HydraCMAP
                self.HydraCMAP_r = HydraCMAP_r
                self.HydraCMAP2 = HydraCMAP2
                self.HydraCMAP2_r = HydraCMAP2_r
                self.BanksyCMAP = BanksyCMAP
                self.BanksyCMAP_r = BanksyCMAP_r
                self.rhkCMAP = rhkCMAP
                self.rhkCMAP_r = rhkCMAP_r
                self.wsxmCMAP = wsxmCMAP
                self.wsxmCMAP_r = wsxmCMAP_r

                self.Axistext = "Luminescence [Counts]"
                self.Headline = "Luminescence"

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

                while self.x <= self.xstop:
                        while self.y <= self.ystop:
                                self.zPart.append(0)
                                self.y += 1
                        self.y = self.ystart
                        self.x += 1
                        self.zNew.append(self.zPart)
                        self.zPart = list()

                #if self.ystart == 0:
                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))
                #else:
                #        self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+2)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+2)))

                # The window
                #self.fig = Figure(figsize=(7,7), dpi=100)
                self.cmap = self.HydraCMAP2
                self.fig, self.ax1  = plt.subplots() 
                #self.ax1 = self.fig.add_subplot()
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax1.set_xlabel('X [Bits]')
                self.ax1.set_ylabel('Y [Bits]')
                self.ax1.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                if self.InvertXLive == True:
                        self.ax1.invert_xaxis()
                if self.InvertYLive == False:
                        self.ax1.invert_yaxis()
                #self.ax1.set_title("Luminescence")
                self.ax1.set_aspect('equal')

                # Add the patch to the Axes
                #rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')
                #self.ax1.add_patch(rect)
                
                self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
                self.cb1.set_label(self.Axistext)
                #plt.tight_layout(self.fig)
                #self.fig.canvas.draw()
                FigureCanvas.__init__(self, self.fig)
                #cid3 = self.fig.canvas.mpl_connect('key_press_event', self.toggle_selector)
                #cid1 = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
                #cid2 = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

                #self.LS = RectangleSelector(self.ax1, self.line_select_callback,
                #               drawtype='box', useblit=False, button=[1,3], 
                #               minspanx=5, minspany=5, spancoords='pixels', 
                #               interactive=True,rectprops = dict(facecolor="#58F107", edgecolor = "#58F107", linewidth=1.5, alpha=1, fill=False))
                #self.LS = LassoSelector(self.ax1, self.onselect)
                #self.RS.rectprops = dict(facecolor="#58F107", edgecolor = "red", linewidth=1.5, alpha=1, fill=True)
                
                #self.selector = SelectFromCollection(self.ax1, self.quad1)
                #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)

                self.iteration = 0

                #anim = animation.FuncAnimation(self.fig,self.animate,frames=(self.ystop-self.ystart+1),interval=(self.ystop-self.ystart+1),blit=False,repeat=False)

        def onselect(self, verts):
                path = Path(verts)
                self.ind = np.nonzero(path.contains_points(self.xys))[0]
                self.fc[:, -1] = self.alpha_other
                self.fc[self.ind, -1] = 1
                self.collection.set_facecolors(self.fc)
                self.canvas.draw_idle()

        def disconnect(self):
                self.lasso.disconnect_events()
                self.fc[:, -1] = 1
                self.collection.set_facecolors(self.fc)
                self.canvas.draw_idle()

        def line_select_callback(self, eclick, erelease):
                'eclick and erelease are the press and release events'
                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
                #print("(%3.0f, %3.0f) --> (%3.0f, %3.0f)" % (int(round(x1,0)),int(round(y1,0)),int(round(x2,0)),int(round(y2,0))))
                #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
                self.progress_valueLumi.emit(int(round(x1,0)), int(round(y1,0)), int(round(x2,0)), int(round(y2,0)))

        def toggle_selector(self, event):
                print(' Key pressed.')
                if event.key in ['Q', 'q'] and self.RS.active:
                        #print(' RectangleSelector deactivated.')
                        self.RS.set_active(False)
                if event.key in ['A', 'a'] and not self.RS.active:
                        #print(' RectangleSelector activated.')
                        self.RS.set_active(True)

        def on_press(self, event):
                #self.RS.set_visible(True)
                self.XStart = event.xdata
                self.YStart = event.ydata
                #print('you pressed', event.button, event.xdata, event.ydata)

        def on_release(self, event):
                #print('you released', event.button, event.xdata, event.ydata)
                self.X = event.xdata
                self.Y = event.ydata
                self.progress_valuePosition.emit(self.X, self.Y)
                #self.RS.set_visible(False)
                #self.RS.clear()

        def HideRectangle(self):
                print("Hide RS")
                #self.RS.set_visible(False)
                #self.RS.update()

        def animate(self):
                self.ax1.clear()
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax1.set_xlabel('X [Bits]')
                self.ax1.set_ylabel('Y [Bits]')
                self.ax1.set_aspect('equal')
                if self.InvertXLive == True:
                        self.ax1.invert_xaxis()
                if self.InvertYLive == False:
                        self.ax1.invert_yaxis()
                try:
                        self.cb1.remove()
                except:
                        pass
                self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
                self.cb1.set_label(self.Axistext)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                #line1.set_data(v,t)
                return self.quad1

        def Resize(self):
                self.ystart = 0
                self.xstart = 0
                self.ystop = 63
                self.xstop = 63
                self.zNew = list()
                self.zPart = list()
                self.x = self.xstart
                self.y = self.ystart

                while self.x <= self.xstop:
                        while self.y <= self.ystop:
                                self.zPart.append(0)
                                self.y += 1
                        self.y = self.ystart
                        self.x += 1
                        self.zNew.append(self.zPart)
                        self.zPart = list()

                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))

                self.animate()

        def SaveFile(self):
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax1.set_xlabel('X [Bits]')
                self.ax1.set_ylabel('Y [Bits]')
                self.ax1.set_aspect('equal')
                self.ax1.set_title(self.Headline)
                self.cb1.remove()
                self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
                self.cb1.set_label(self.Axistext)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                self.fig.savefig(self.Filename)
                self.ax1.set_title("")
                self.animate()

        def UpdateCMAP(self, InvertCMAPLive1, Plotstyle):
                self.InvertCMAPLive = InvertCMAPLive1
                if self.InvertCMAPLive:
                        self.cmap_new = Plotstyle + "_r"
                else:
                        self.cmap_new = Plotstyle
                self.cmap = self.cmap_new
                if self.cmap_new == "HydraCMAP":
                        self.cmap = self.HydraCMAP
                if self.cmap_new == "HydraCMAP_r":
                        self.cmap = self.HydraCMAP_r
                if self.cmap_new == "HydraCMAP2":
                        self.cmap = self.HydraCMAP2
                if self.cmap_new == "HydraCMAP2_r":
                        self.cmap = self.HydraCMAP2_r
                if self.cmap_new == "BanksyCMAP":
                        self.cmap = self.BanksyCMAP
                if self.cmap_new == "BanksyCMAP_r":
                        self.cmap = self.BanksyCMAP_r
                if self.cmap_new == "rhkCMAP":
                        self.cmap = self.rhkCMAP
                if self.cmap_new == "rhkCMAP_r":
                        self.cmap = self.rhkCMAP_r
                if self.cmap_new == "wsxmCMAP":
                        self.cmap = self.wsxmCMAP
                if self.cmap_new == "wsxmCMAP_r":
                        self.cmap = self.wsxmCMAP_r
                #self.cmap = plt.get_cmap(Plotstyle)
                self.animate()

        def UpdateFilename(self, Date):
                self.Filename = "/home/pi/Desktop/Data/" + self.Headline + "_" + Date + ".png"
                #print(self.Filename)

        def InvertX(self, InvertXLive1):
                self.InvertXLive = InvertXLive1
                #print("Invert X1: " + str(self.InvertXLive))
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.cb1.remove()
                self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
                self.cb1.set_label(self.Axistext)
                self.ax1.invert_xaxis()
                self.ax1.set_xlabel('X [Bits]')
                self.ax1.set_ylabel('Y [Bits]')
                self.ax1.set_aspect('equal')
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()

        def InvertY(self, InvertYLive1):
                self.InvertYLive = InvertYLive1
                #print("Invert Y1: " + str(self.InvertYLive))
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.cb1.remove()
                self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax1)
                self.cb1.set_label(self.Axistext)
                self.ax1.invert_yaxis()
                self.ax1.set_xlabel('X [Bits]')
                self.ax1.set_ylabel('Y [Bits]')
                self.ax1.set_aspect('equal')
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()

        def RangeChange(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down

        def RangeChangeAnimate(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down
                self.animate()

        def ChannelChanged(self, Axistext, Headline):
                print(Axistext + "\t" + Headline)
                self.Axistext = Axistext
                self.Headline = Headline

        def CalcNewLine(self,AutoScale):
                self.AutoScale = AutoScale

        def CalcNewLine1(self,a):
                self.zNew = a
                self.animate()

class ScatMeshplot(FigureCanvas, TimedAnimation):
        progress_valueScat = pyqtSignal(int, int, int, int)
        progress_valuePosition = pyqtSignal(int, int)
        
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
                global HydraCMAP
                global HydraCMAP_r
                global HydraCMAP2
                global HydraCMAP2_r
                global BanksyCMAP
                global BanksyCMAP_r
                global rhkCMAP
                global rhkCMAP_r
                global wsxmCMAP
                global wsxmCMAP_r

                self.HydraCMAP = HydraCMAP
                self.HydraCMAP_r = HydraCMAP_r
                self.HydraCMAP2 = HydraCMAP2
                self.HydraCMAP2_r = HydraCMAP2_r
                self.BanksyCMAP = BanksyCMAP
                self.BanksyCMAP_r = BanksyCMAP_r
                self.rhkCMAP = rhkCMAP
                self.rhkCMAP_r = rhkCMAP_r
                self.wsxmCMAP = wsxmCMAP
                self.wsxmCMAP_r = wsxmCMAP_r

                self.Axistext = "Scattering [Counts]"
                self.Headline = "Scattering"
                
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

                while self.x <= self.xstop:
                        while self.y <= self.ystop:
                                self.zPart.append(0)
                                self.y += 1
                        self.y = self.ystart
                        self.x += 1
                        self.zNew2.append(self.zPart)
                        self.zPart = list()

                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))


                # The window
                #self.fig = Figure(figsize=(7,7), dpi=100)
                self.cmap = self.HydraCMAP2
                self.fig, self.ax2  = plt.subplots() 
                #self.ax2 = self.fig.add_subplot()
                self.quad2 = self.ax2.pcolormesh(self.x, self.y, self.zNew2, cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                if self.InvertXLive == True:
                        self.ax2.invert_xaxis()
                if self.InvertYLive == False:
                        self.ax2.invert_yaxis()
                #self.ax2.set_title("Scattering")
                self.ax2.set_aspect('equal')
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                #plt.tight_layout(self.fig)
                FigureCanvas.__init__(self, self.fig)
                #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
                #cid4 = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
                #cid5 = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
                #cid6 = self.fig.canvas.mpl_connect('key_press_event', self.toggle_selector)

                #self.RS1 = RectangleSelector(self.ax2, self.line_select_callback,
                #               drawtype='box', useblit=False, button=[1,3], 
                #               minspanx=5, minspany=5, spancoords='pixels', 
                #               interactive=True,rectprops = dict(facecolor="#58F107", edgecolor = "#58F107", linewidth=1.5, alpha=1, fill=False))
                
                self.iteration = 0

        def line_select_callback(self, eclick, erelease):
                'eclick and erelease are the press and release events'
                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
                #print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (round(x1,0), y1, x2, y2))
                #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
                self.progress_valueScat.emit(int(round(x1,0)), int(round(y1,0)), int(round(x2,0)), int(round(y2,0)))


        def toggle_selector(self, event):
                #print(' Key pressed.')
                if event.key in ['Q', 'q'] and self.RS1.active:
                        #print(' RectangleSelector deactivated.')
                        self.RS1.set_active(False)
                if event.key in ['A', 'a'] and not self.RS1.active:
                        #print(' RectangleSelector activated.')
                        self.RS1.set_active(True)

        def on_press(self, event):
                self.RS1.set_visible(True)
                self.XStart = event.xdata
                self.YStart = event.ydata
                #print('you pressed', event.button, event.xdata, event.ydata)

        def on_release(self, event):
                print('you released', event.button, event.xdata, event.ydata)
                self.XStop = event.xdata
                self.YStop = event.ydata
                if self.XStart == self.XStop and self.YStart == self.YStop:
                        self.progress_valuePosition.emit(self.XStart, self.YStart)
                #self.RS1.set_visible(False)

        def HideRectangle(self):
                print("Hide RS1")
                #self.RS1.set_visible(False)
                #self.RS1.update()

        def animate(self):
                self.ax2.clear()
                self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_aspect('equal')
                if self.InvertXLive == True:
                        self.ax2.invert_xaxis()
                if self.InvertYLive == False:
                        self.ax2.invert_yaxis()
                try:
                        self.cb2.remove()
                except:
                        pass
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                #line1.set_data(v,t)
                return self.quad2

        def SaveFile(self):
                self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_aspect('equal')
                self.ax2.set_title(self.Headline)
                self.cb2.remove()
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                self.fig.savefig(self.Filename)
                self.ax2.set_title("")
                self.animate()

        def UpdateCMAP(self, InvertCMAPLive2, Plotstyle):
                self.InvertCMAPLive = InvertCMAPLive2
                if self.InvertCMAPLive:
                        self.cmap_new = Plotstyle + "_r"
                else:
                        self.cmap_new = Plotstyle
                self.cmap = self.cmap_new
                if self.cmap_new == "HydraCMAP":
                        self.cmap = self.HydraCMAP
                if self.cmap_new == "HydraCMAP_r":
                        self.cmap = self.HydraCMAP_r
                if self.cmap_new == "HydraCMAP2":
                        self.cmap = self.HydraCMAP2
                if self.cmap_new == "HydraCMAP2_r":
                        self.cmap = self.HydraCMAP2_r
                if self.cmap_new == "BanksyCMAP":
                        self.cmap = self.BanksyCMAP
                if self.cmap_new == "BanksyCMAP_r":
                        self.cmap = self.BanksyCMAP_r
                if self.cmap_new == "rhkCMAP":
                        self.cmap = self.rhkCMAP
                if self.cmap_new == "rhkCMAP_r":
                        self.cmap = self.rhkCMAP_r
                if self.cmap_new == "wsxmCMAP":
                        self.cmap = self.wsxmCMAP
                if self.cmap_new == "wsxmCMAP_r":
                        self.cmap = self.wsxmCMAP_r
                #self.cmap = plt.get_cmap(Plotstyle)
                self.animate()

        def UpdateFilename(self, Date):
                self.Filename = "/home/pi/Desktop/Data/" + self.Headline + "_" + Date + ".png"
                #print(self.Filename)

        def ChannelChanged(self, Axistext, Headline):
                self.Axistext = Axistext
                self.Headline = Headline

        def InvertX(self, InvertXLive2):
                self.InvertXLive = InvertXLive2
                #print("Invert X1: " + str(self.InvertXLive))
                self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.cb2.remove()
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                self.ax2.invert_xaxis()
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_aspect('equal')
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()

        def InvertY(self, InvertYLive2):
                self.InvertYLive = InvertYLive2
                #print("Invert Y1: " + str(self.InvertYLive))
                self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.cb2.remove()
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                self.ax2.invert_yaxis()
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_aspect('equal')
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()


        """
        def InvertX(self, InvertXLive1):
                if self.AutoScale == True:
                        self.lowerLimit = self.Minimum2
                        self.upperLimit = self.Maximum2
                self.InvertXLive = InvertXLive1
                #print("Invert X1: " + str(self.InvertXLive))
                self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.cb2.remove()
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                self.ax2.invert_xaxis()
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_aspect('equal')
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()

        def InvertY(self, InvertYLive1):
                if self.AutoScale == True:
                        self.lowerLimit = self.Minimum2
                        self.upperLimit = self.Maximum2
                self.InvertYLive = InvertYLive1
                #print("Invert Y1: " + str(self.InvertYLive))
                self.quad2 = self.ax2.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.cb2.remove()
                self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax2)
                self.cb2.set_label(self.Axistext)
                self.ax2.invert_yaxis()
                self.ax2.set_xlabel('X [Bits]')
                self.ax2.set_ylabel('Y [Bits]')
                self.ax2.set_aspect('equal')
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
        """
        
        def RangeChange(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down

        def RangeChangeAnimate(self, up, down):
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
                self.animate()


class LumiLineplot(FigureCanvas, TimedAnimation):
        progress_valuePosition = pyqtSignal(int, int)
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

                self.Axistext = "Luminescence [Counts]"
                self.Headline = "Luminescence"
                
                self.xstart = xstart
                self.ystart = ystart
                self.xstop = xstop
                self.ystop = ystop
                self.upperLimit = upperLimit1
                self.lowerLimit = lowerLimit1

                self.t = t
                self.v = v

                # The window
                self.fig, self.ax3  = plt.subplots() 
                self.line1 = self.ax3.plot([],[],color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax3.set_xlim(0,self.xstop-self.xstart)
                self.ax3.set_ylim(self.lowerLimit,self.upperLimit)
                self.ax3.set_xlabel('X [Bits]')
                self.ax3.set_ylabel(self.Axistext)
                self.ax3.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                #self.ax3.set_title('Oscillationsssss')
                self.ax3.grid(True)
                #plt.tight_layout(self.fig)
                FigureCanvas.__init__(self, self.fig)
                #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
                self.iteration = 0
                #self.fig.canvas.mpl_connect('pick_event', self.onpick1)
                #cid4 = self.fig.canvas.mpl_connect('button_press_event', self.on_pick)
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        def on_pick(self, event):
                if isinstance(event.artist, Line2D):
                        thisline = event.artist
                        xdata = thisline.get_xdata()
                        ydata = thisline.get_ydata()
                        ind = event.ind
                        data = np.column_stack([xdata[ind], ydata[ind]])
                        length = int(round(len(data)/2,0))
                        dataNew = data[length]
                        dataX = dataNew[0]
                        dataY = dataNew[1]
                self.progress_valuePosition.emit(dataX, dataY)

        def LineAnalysis(self, data):
                #print("LineAnalysis LinePlot")
                self.dataStorage = data
                self.ax3.clear()
                x = list()
                y = list()
                xHigh = 5
                yHigh = 1
                yLow = -1
                i = 0
                while i < len(self.dataStorage):
                        X = self.dataStorage[i]["Counter"]
                        Y = self.dataStorage[i]["value"]
                        x.append(X)
                        y.append(Y)
                        if X > xHigh:
                                xHigh = X
                        if Y > yHigh:
                                yHigh = Y
                        if Y < yLow or yLow == -1:
                                yLow = Y
                        i += 1
                        #print("Point: " + str(X) + " x " + str(Y) + "\tHighs" + str(xHigh) + " x " + str(yHigh))
                self.line1 = self.ax3.plot(x,y,color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax3.set_xlim(0,xHigh)
                if yLow <= 0:
                        self.ax3.set_ylim((yLow),(yHigh+int(round(yHigh/10,0))))
                        #print("\tHighs" + str(yLow) + " x " + str(yHigh+int(round(yHigh/10,0))))
                elif yLow <= 5:
                        self.ax3.set_ylim((yLow-1),(yHigh+int(round(yHigh/10,0))))
                        #print("\tHighs" + str(yLow-1) + " x " + str(yHigh+int(round(yHigh/10,0))))
                else:
                        self.ax3.set_ylim((yLow-5),(yHigh+int(round(yHigh/10,0))))
                        #print("\tHighs" + str(yLow-5) + " x " + str(yHigh+int(round(yHigh/10,0))))
                self.ax3.set_xlabel('X [Bits]')
                self.ax3.set_ylabel(self.Axistext)
                self.ax3.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                #self.ax3.set_title('Oscillationsssss')
                self.ax3.grid(True)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)
                
                
                
        def animate(self):
                self.ax3.clear()
                self.line1 = self.ax3.plot(self.v,self.t,color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax3.set_xlim(0,self.xstop-self.xstart)
                self.ax3.set_ylim(self.lowerLimit,self.upperLimit)
                self.ax3.set_xlabel('X [Bits]')
                self.ax3.set_ylabel(self.Axistext)
                self.ax3.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                #self.ax3.set_title('Oscillationsssss')
                self.ax3.grid(True)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)
                #line1.set_data(v,t)
                #return self.quad2

        def RangeChange(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down

        def ChannelChanged(self, Axistext, Headline):
                print(Axistext + "\t" + Headline)
                self.Axistext = Axistext
                self.Headline = Headline

        def RangeChangeAnimate(self, up, down):
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
        progress_valuePosition = pyqtSignal(int, int)
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

                self.Axistext = "Scattering [Counts]"
                self.Headline = "Scattering"
                
                self.xstart = xstart
                self.ystart = ystart
                self.xstop = xstop
                self.ystop = ystop
                self.upperLimit = upperLimit2
                self.lowerLimit = lowerLimit2

                self.tt = tt
                self.v = v
                
                # The window
                #self.fig = Figure(figsize=(7,3), dpi=100)
                cmap = plt.get_cmap('Spectral_r') 
                self.fig, self.ax4  = plt.subplots() 
                #self.ax4 = self.fig.add_subplot(111)
                self.line2, = self.ax4.plot([],[],color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax4.set_xlim(0,self.xstop-self.xstart)
                self.ax4.set_ylim(self.lowerLimit,self.upperLimit)
                self.ax4.set_xlabel('X [Bits]')
                self.ax4.set_ylabel(self.Axistext)
                self.ax4.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                #self.ax4.set_title('Oscillationsssss')
                self.ax4.grid(True)
                #plt.tight_layout(self.fig)
                FigureCanvas.__init__(self, self.fig)
                #TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
                self.iteration = 0
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        def on_pick(self, event):
                if isinstance(event.artist, Line2D):
                        thisline = event.artist
                        xdata = thisline.get_xdata()
                        ydata = thisline.get_ydata()
                        ind = event.ind
                        data = np.column_stack([xdata[ind], ydata[ind]])
                        length = int(round(len(data)/2,0))
                        dataNew = data[length]
                        dataX = dataNew[0]
                        dataY = dataNew[1]
                self.progress_valuePosition.emit(dataX, dataY)

        def LineAnalysis(self, data):
                self.dataStorage = data
                self.ax4.clear()
                x = list()
                y = list()
                xHigh = 5
                yHigh = 1
                yLow = -1
                i = 0
                while i < len(self.dataStorage):
                        X = self.dataStorage[i]["Counter"]
                        Y = self.dataStorage[i]["value"]
                        x.append(X)
                        y.append(Y)
                        if X > xHigh:
                                xHigh = X
                        if Y > yHigh:
                                yHigh = Y
                        if Y < yLow or yLow == -1:
                                yLow = Y
                        i += 1
                        #print("Point: " + str(X) + " x " + str(Y) + "\tHighs" + str(xHigh) + " x " + str(yHigh))
                self.line1 = self.ax4.plot(x,y,color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax4.set_xlim(0,xHigh)
                if yLow <= 0:
                        self.ax4.set_ylim((yLow),(yHigh+int(round(yHigh/10,0))))
                        #print("\tHighs" + str(yLow) + " x " + str(yHigh+int(round(yHigh/10,0))))
                elif yLow <= 5:
                        self.ax4.set_ylim((yLow-1),(yHigh+int(round(yHigh/10,0))))
                        #print("\tHighs" + str(yLow-1) + " x " + str(yHigh+int(round(yHigh/10,0))))
                else:
                        self.ax4.set_ylim((yLow-5),(yHigh+int(round(yHigh/10,0))))
                        #print("\tHighs" + str(yLow-5) + " x " + str(yHigh+int(round(yHigh/10,0))))
                self.ax4.set_xlabel('X [Bits]')
                self.ax4.set_ylabel(self.Axistext)
                self.ax4.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                #self.ax4.set_title('Oscillationsssss')
                self.ax4.grid(True)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)
                
                
        def animate(self):
                self.ax4.clear()
                self.line2 = self.ax4.plot(self.v,self.tt,color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax4.set_xlim(0,self.xstop-self.xstart)
                self.ax4.set_ylim(self.lowerLimit,self.upperLimit)
                self.ax4.set_xlabel('X [Bits]')
                self.ax4.set_ylabel(self.Axistext)
                self.ax4.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                #self.ax4.set_title('Oscillationsssss')
                self.ax4.grid(True)
                #plt.tight_layout(self.fig)
                self.fig.canvas.draw()
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)
                #line1.set_data(v,t)
                #return self.quad2

        def RangeChange(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down

        def ChannelChanged(self, Axistext, Headline):
                self.Axistext = Axistext
                self.Headline = Headline

        def RangeChangeAnimate(self, up, down):
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



#APD Window --------------------------------------------------------------
class APDWindow(QWidget):
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight
                global APDon
                global APDWindowOn
                global APDArduinoOn
                global APDBSOn

                self.WindowPosX = WindowPosX + WindowWidth + 5
                self.WindowPosY = WindowPosY + 500 + 35

                #print(self.WindowPosX)
                #print(self.WindowPosY)                        
                
                self.setWindowTitle("APD Readings")
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/APD2.png"))
                self.setGeometry(self.WindowPosX,self.WindowPosY,300,240)
                
                self.APD1 = 0
                self.APD2 = 0
                self.APD1Val = 0
                self.APD2Val = 0

                #Spinbox definieren
                self.WaitTime = QDoubleSpinBox(self)
                self.WaitTime.setMinimum(0.1)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.WaitTime.setMaximum(10)     
                self.WaitTime.setToolTip("Set the Rate of APD readings")
                self.WaitTime.setValue(0.5)
                self.WaitTime.setSingleStep(0.1)
                self.WaitTime.setDecimals(1)                                                                                                            #Setzt einen Startwert
                self.WaitTime.valueChanged.connect(self.StartMeasure)
                self.WaitTime.move(140, 151)

                self.labelWaitTime = QLabel("Reading Time: ", self)
                self.labelWaitTime.move(30, 155)
                
                self.IntTime = QSpinBox(self)
                self.IntTime.setMinimum(1)                                                                                                              #Setzt ein Minimalwert für die Auswahl
                self.IntTime.setMaximum(10)  
                self.IntTime.setToolTip("Set the Integrationtime of APD readings") 
                self.IntTime.setValue(10)                                                                                                               #Setzt einen Startwert
                self.IntTime.valueChanged.connect(self.StartMeasure)
                self.IntTime.move(140, 116)

                self.labelIntTime = QLabel("Integration Time: ", self)
                self.labelIntTime.move(30, 120)

                #Widgets setzen                
                self.labelAPD1 = QLabel("APD 1: " + str(self.APD1) + " khz\n\t" + str(self.APD1) + " counts", self)
                self.labelAPD1.adjustSize()
                self.labelAPD1.move(30, 50)

                self.labelAPD2 = QLabel("APD 2 : " + str(self.APD2) + " khz\n\t" + str(self.APD2) + " counts", self)
                self.labelAPD2.adjustSize()
                self.labelAPD2.move(30, 85)

                self.labelTest = QLabel(" ", self)
                self.labelTest.move(190, 30)
                

                if APDon == 1:
                        self.labelValid = QLabel(("APD connected"), self)
                        self.labelValid.move(30, 15)
                        
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2_green.png")
                        pixmap_mini = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

                        #Start Reading
                        if APDBSOn == 1:
                                self.StartMeasureBS()
                        elif APDArduinoOn == 1:
                                self.StartMeasureArduino()
                else:
                        self.labelValid = QLabel(("No APD connected"), self)
                        self.labelValid.move(30, 15)
                        
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2.png")
                        pixmap_mini = pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

                #Restart
                self.restart = QPushButton("Restart", self)                                                                                             #setzt einen Ende-Button
                self.restart.setToolTip("Restart with new")                                                                                             #Setzt eine Buttonbeschreibung bei MouseOver    
                self.restart.move(30,190)
                self.restart.clicked.connect(self.StartMeasure)
                
                if APDBSOn == 1:                                                                                                                        #Setzt ein Minimalwert für die Auswahl
                        self.IntTime.setMaximum(10) 
                elif APDArduinoOn == 1:                                                                                                                 #Setzt ein Minimalwert für die Auswahl
                        self.IntTime.setMaximum(100) 

                #Ende
                self.end = QPushButton("Quit", self)                                                                                                    #setzt einen Ende-Button
                self.end.setToolTip("Quit the Window")                                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end.move(180,190)
                self.end.clicked.connect(self.WindowClose)
                
        def Restart(self):
                self.StopMeasure()
                self.StartMeasure()

        def StopMeasure(self):
                try:
                        self.Reading.kill()
                except:
                        pass

        def StartMeasure(self):
                print("Start APDs")
                if APDBSOn == 1:
                        self.StartMeasureBS()
                elif APDArduinoOn == 1:
                        self.StartMeasureArduino()

        def StartMeasureBS(self):
                try:
                        self.Reading.kill()
                except:
                        pass
                self.APDTime = self.WaitTime.value()
                self.Integration = self.IntTime.value()
                self.Reading = APDReadBS(self.Integration, self.APDTime)
                self.Reading.progress_APD1.connect(self.UpdateAPD1)
                self.Reading.progress_APD2.connect(self.UpdateAPD2)
                self.Reading.start()

        def StartMeasureArduino(self):
                try:
                        self.Reading.kill()
                except:
                        pass
                self.APDTime = self.WaitTime.value()
                self.Integration = self.IntTime.value()
                self.Reading = APDReadArduino(self.Integration, self.APDTime)
                self.Reading.progress_APD1.connect(self.UpdateAPD1)
                self.Reading.progress_APD2.connect(self.UpdateAPD2)
                self.Reading.start()

        def UpdateAmpel(self):
                if self.APD1Val < 1000 and self.APD1Val >= 0 and self.APD2Val < 1000 and self.APD2Val >= 0:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2_green.png")
                        pixmap_mini = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                elif self.APD1Val == 0 and self.APD2Val == 0:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2.png")
                        pixmap_mini = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                else:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2_red.png")
                        pixmap_mini = pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

        def UpdateAPD1(self, val):
                self.APD1Val = (val/self.Integration)
                #print("APD 1: " + str(val))
                self.labelAPD1.setText("APD 1:\t" + str(round(self.APD1Val,2)) + " khz\n\t" + str(val) + " counts")
                self.labelAPD1.adjustSize()
                self.UpdateAmpel()

        def UpdateAPD2(self, val):
                self.APD2Val = (val/self.Integration)
                #print("APD 2: " + str(val))
                self.labelAPD2.setText("APD 2:\t" + str(round(self.APD2Val,2)) + " khz\n\t" + str(val) + " counts")
                self.labelAPD2.adjustSize()
                self.UpdateAmpel()

        def closeEvent(self, event):
                global APDWindowOn
                APDWindowOn = 0
                try:
                        self.Reading.kill()
                except:
                        pass

        def WindowClose(self):
                global APDWindowOn
                APDWindowOn = 0
                try:
                        self.Reading.kill()
                except:
                        pass
                self.close()


class APDReadBS(QThread):
        progress_APD1 = pyqtSignal(int)
        progress_APD2 = pyqtSignal(int)

        def __init__(self, Integration, APDTime, parent=None):
                QThread.__init__(self, parent)
                self.APDTime = APDTime
                self.Integration = Integration
                self.i = 0   
                self.APD1 = 0
                self.APD2 = 0

        def run(self):
                global APDon

                APDs = APDLogic(5000,self.Integration)
                
                if APDon == 0:
                        while self.i == 0:  
                                try:
                                        self.APD1, self.APD2 , L2, L3= APDs.capture_and_calc()
                                except:
                                        self.APD1 = self.APD1 + 2
                                        self.APD2 = self.APD2 + 10
                                        
                                self.progress_APD1.emit(self.APD1)
                                self.progress_APD2.emit(self.APD2)
                                time.sleep(self.APDTime)
                elif APDon == 1:
                        while self.i == 0:  
                                self.APD1, self.APD2 , L2, L3= APDs.capture_and_calc()
                                self.progress_APD1.emit(self.APD1)
                                self.progress_APD2.emit(self.APD2)
                                time.sleep(self.APDTime)
                                
        def kill(self):
                self.i = 1
                APDs.closeDevice()

class APDReadArduino(QThread):
        progress_APD1 = pyqtSignal(int)
        progress_APD2 = pyqtSignal(int)

        def __init__(self, Integration, APDTime, parent=None):
                QThread.__init__(self, parent)
                self.APDTime = APDTime
                self.Integration = Integration
                self.i = 0   
                self.APD1 = 0
                self.APD2 = 0
                
        def run(self):
                global APDon
                
                if APDon == 0:
                        while self.i == 0:  
                                try:
                                        self.APD1, self.APD2 = APDs.captureDual(self.Integration)
                                except:
                                        self.APD1 = self.APD1 + 2
                                        self.APD2 = self.APD2 + 10
                                        
                                self.progress_APD1.emit(self.APD1)
                                self.progress_APD2.emit(self.APD2)
                                time.sleep(self.APDTime)
                elif APDon == 1:
                        while self.i == 0:  
                                self.APD1, self.APD2 = APDs.captureDual(self.Integration)
                                self.progress_APD1.emit(self.APD1)
                                self.progress_APD2.emit(self.APD2)
                                time.sleep(self.APDTime)
                                
        def kill(self):
                self.i = 1


#Temp Window -------------------------------------------------------------
class TempWindow(QWidget):
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global temperature
                global humidity
                global DHTon
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.WindowPosX = WindowPosX + WindowWidth + 10 + 300
                self.WindowPosY = WindowPosY + 500 + 35

                print(self.WindowPosX)
                print(self.WindowPosY)  
                
                self.setWindowTitle("Temperature")
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/ShowTemp.png"))
                self.setGeometry(self.WindowPosX,self.WindowPosY,300,240)
                

                #Spinbox definieren
                self.WaitTime = QSpinBox(self)
                self.WaitTime.setMinimum(3)                                                                                                             #Setzt ein Minimalwert für die Auswahl
                self.WaitTime.setMaximum(99)     
                self.WaitTime.setToolTip("Set the Rate of Temperature readings")
                self.WaitTime.setValue(5)                                                                                                               #Setzt einen Startwert
                self.WaitTime.valueChanged.connect(self.TimeChanged)
                self.WaitTime.move(140, 126)

                self.labelWaitTime = QLabel("Reading Time: ", self)
                self.labelWaitTime.move(30, 130)

                #Widgets setzen
                self.labelTest = QLabel(" ", self)
                self.labelTest.move(220, 40)

                if DHTon == 1:
                        self.labelValid = QLabel(("Sensor connected"), self)
                        self.labelValid.move(30, 25)
                        
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Temp_normal.png")
                        pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

                        #Start Reading
                        self.StartMeasure() 
                else:
                        self.labelValid = QLabel(("No Sensor connected"), self)
                        self.labelValid.move(30, 25)
                        
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/temperature.png")
                        pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                
                self.labelTemp = QLabel(("Temperature: " + str(temperature)), self)
                self.labelTemp.move(30, 60)

                self.labelHum = QLabel(("Humidity: " + str(humidity)), self)
                self.labelHum.move(30, 95)

                #Ende
                self.end = QPushButton("Quit", self)                                                                                                    #setzt einen Ende-Button
                self.end.setToolTip("Quit the Window")                                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end.move(180,190)
                self.end.clicked.connect(self.WindowClose)

        def TimeChanged(self):
                self.Reading.kill()
                self.StartMeasure()                

        def StartMeasure(self):
                try:
                        self.Reading.kill()
                except:
                        pass
                
                self.TempTime = self.WaitTime.value()
                self.Reading = TempRead(self.TempTime)
                self.Reading.progress_Temp.connect(self.UpdateTemp)
                self.Reading.progress_Hum.connect(self.UpdateHum)
                self.Reading.start()
        
        def StopMeasure(self):
                self.Reading.kill()

        def UpdateTemp(self, val):
                global temperature
                temperature = val
                self.labelTemp.setText("Temperature: " + str(val))
                self.labelTemp.adjustSize()
                if val <= 22:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Temp_low.png")
                        pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                elif val >= 28:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Temp_high.png")
                        pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                else:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Temp_normal.png")
                        pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

        def UpdateHum(self, val):
                global humidity
                humidity = val
                self.labelHum.setText("Humidity: " + str(val))
                self.labelHum.adjustSize()

        def closeEvent(self, event):
                global TempWindowOn
                TempWindowOn = 0
                try:
                        self.Reading.kill()
                except:
                        pass

        def WindowClose(self):
                global TempWindowOn
                TempWindowOn = 0
                try:
                        self.Reading.kill()
                except:
                        pass
                self.close()

class TempRead(QThread):
        progress_Temp = pyqtSignal(float)
        progress_Hum = pyqtSignal(float)

        def __init__(self, TempTime, parent=None):
                QThread.__init__(self, parent)
                self.TempTime = TempTime
                self.i = 0   
                self.Temp = 0
                self.Hum = 0
                
        def run(self):
                global DHTPin
                while self.i == 0:  
                        try:
                                self.Hum, self.Temp = Adafruit_DHT.read_retry(TempSens, DHTPin)
                        except:
                                self.Temp = self.Temp + 2
                                self.Hum = self.Hum + 2
                                
                        self.progress_Temp.emit(self.Temp)
                        self.progress_Hum.emit(self.Hum)
                        time.sleep(self.TempTime)

        def kill(self):
                self.i = 1


#Settings Windows ------------------------------------------------------
class PlotSettings(QWidget):
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global PlotStyle
                global PlotName
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50
                
                self.setWindowTitle("Plot Settings")
                self.setGeometry(self.WindowPosX,self.WindowPosY,420,480)
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Settings.png"))

                self.layoutv = QVBoxLayout(self)
                
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.Plotname = QLineEdit(self)
                self.Filename = QLineEdit(self)
                self.buttonPath = QPushButton("Filepath", self)
                self.labelPath = QLabel("", self)
                self.labelPlot = QLabel("Headline", self)
                self.labelFile = QLabel("Filename", self)

                self.buttonPath.setToolTip("Set the Filepath")
                self.buttonPath.clicked.connect(self.OpenPath)
                self.Plotname.setToolTip("Sets the Headline of the Plot")
                self.Filename.setToolTip("Sets the Filename")


                self.Plotname.setText(PlotName) 

                #Checkboxen setzen
                self.cbStyle1 = QCheckBox("Spectral_r", self)                                                                                           #Setzt eine CheckBox
                self.cbStyle1.setToolTip("Sets the Plotstyle to Spectral_r (Rainbowcolors)")                                                            #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbStyle2 = QCheckBox("gray_r", self)                                                                      
                self.cbStyle2.setToolTip("Sets the Plotstyle to gray_r (50 Shades of Gray)")                                    
                self.cbStyle3 = QCheckBox("bone", self)                                                                         
                self.cbStyle3.setToolTip("Sets the Plotstyle to bone (black - blue - white)")                                   
                self.cbStyle4 = QCheckBox("Wistia", self)                                                                      
                self.cbStyle4.setToolTip("Sets the Plotstyle to Wistia (yellow - orange)")                                     
                self.cbStyle5 = QCheckBox("copper", self)                                                                       
                self.cbStyle5.setToolTip("Sets the Plotstyle to copper (get to the copper)")                                    
                self.cbStyle6 = QCheckBox("gist_heat", self)                                                                   
                self.cbStyle6.setToolTip("Sets the Plotstyle to gist_heat (black - red - white)")                                       
                self.cbStyle7 = QCheckBox("winter", self)                                                                       
                self.cbStyle7.setToolTip("Sets the Plotstyle to summer (Brace yourself)")                                       
                self.cbStyle8 = QCheckBox("spring", self)                                                                      
                self.cbStyle8.setToolTip("Sets the Plotstyle to spring (purple - yellow)")                                     
                self.cbStyle9 = QCheckBox("summer", self)                                                                      
                self.cbStyle9.setToolTip("Sets the Plotstyle to summer (green - yellow)")                                      
                self.cbStyle10 = QCheckBox("autumn", self)                                                                     
                self.cbStyle10.setToolTip("Sets the Plotstyle to autumn (red - yellow)")                                       
                self.cbStyle11 = QCheckBox("hot", self)                                                                       
                self.cbStyle11.setToolTip("Sets the Plotstyle to hot_r (red - yellow)")                                        
                self.cbStyle12 = QCheckBox("cool", self)                                                                     
                self.cbStyle12.setToolTip("Sets the Plotstyle to cool (lite blue - purple)")                                       
                self.cbStyle13 = QCheckBox("gist_ncar", self)                                                                   
                self.cbStyle13.setToolTip("Sets the Plotstyle to gist_ncar (red - yellow)")                               
                self.cbStyle14 = QCheckBox("nipy_spectral", self)                                                                
                self.cbStyle14.setToolTip("Sets the Plotstyle to nipy_spectral (red - yellow)")                                 
                self.cbStyle15 = QCheckBox("Reds", self)                                                                      
                self.cbStyle15.setToolTip("Sets the Plotstyle to Reds (White - Red)")                                        


                if PlotStyle == 1:
                        self.cbStyle1.setChecked(True)
                elif PlotStyle == 2:
                        self.cbStyle2.setChecked(True)
                elif PlotStyle == 3:
                        self.cbStyle3.setChecked(True)
                elif PlotStyle == 4:
                        self.cbStyle4.setChecked(True)
                elif PlotStyle == 5:
                        self.cbStyle5.setChecked(True)
                elif PlotStyle == 6:
                        self.cbStyle6.setChecked(True)
                elif PlotStyle == 7:
                        self.cbStyle7.setChecked(True)
                elif PlotStyle == 8:
                        self.cbStyle8.setChecked(True)
                elif PlotStyle == 9:
                        self.cbStyle9.setChecked(True)
                elif PlotStyle == 10:
                        self.cbStyle10.setChecked(True)
                elif PlotStyle == 11:
                        self.cbStyle11.setChecked(True)
                elif PlotStyle == 12:
                        self.cbStyle12.setChecked(True)
                elif PlotStyle == 13:
                        self.cbStyle13.setChecked(True)
                elif PlotStyle == 14:
                        self.cbStyle14.setChecked(True)
                elif PlotStyle == 15:
                        self.cbStyle15.setChecked(True)

                        
                #Checkboxen als ButtonGroup zusammenfassen
                self.cbgStyle = QButtonGroup()                                                                                                          #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbgStyle.addButton(self.cbStyle1, 1)                                                                                               #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle2, 2)                                                                                               #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle3, 3)                                                                                               #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle4, 4)                                                                                               #....
                self.cbgStyle.addButton(self.cbStyle5, 5)                                                                                               
                self.cbgStyle.addButton(self.cbStyle6, 6)                                                                                            
                self.cbgStyle.addButton(self.cbStyle7, 7)                                                                                         
                self.cbgStyle.addButton(self.cbStyle8, 8)
                self.cbgStyle.addButton(self.cbStyle9, 9)                                                                                           
                self.cbgStyle.addButton(self.cbStyle10, 10)                                                                                    
                self.cbgStyle.addButton(self.cbStyle11, 11)                                                                                     
                self.cbgStyle.addButton(self.cbStyle12, 12)                                                                                  
                self.cbgStyle.addButton(self.cbStyle13, 13)                                                                                   
                self.cbgStyle.addButton(self.cbStyle14, 14)                                                                                          
                self.cbgStyle.addButton(self.cbStyle15, 15)

                
                #Ende
                self.end = QPushButton("Save + Quit", self)                                                                                             #setzt einen Ende-Button
                self.end.setToolTip("Save the Changes and Quit the Window")
                self.end.clicked.connect(self.SaveAndClose)

                self.groupboxcbg = QGroupBox("Plotcolor", self)
                self.groupboxcbg.layoutcbg = QVBoxLayout(self)                                                                                          #Fügt das Label ein
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle1)                                                                                     #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle2)                                                                                     #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle3)                                                                                     #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle4)
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle5)                                                                                    
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle6)                                                                               
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle7)                                                                                    
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle8)
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle9)                                                                               
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle10)                                                                          
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle11)                                                                                  
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle12)                                                                               
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle13)                                                                           
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle14)                                                                                   
                self.groupboxcbg.layoutcbg.addWidget(self.cbStyle15)
                self.groupboxcbg.layoutcbg.addStretch(2)
                self.groupboxcbg.setLayout(self.groupboxcbg.layoutcbg)

                self.groupboxPlotSet = QGroupBox("Plotsettings", self)
                self.groupboxPlotSet.layoutHPlotname = QHBoxLayout(self)
                self.groupboxPlotSet.layoutHPlotname.addWidget(self.Plotname)
                self.groupboxPlotSet.layoutHPlotname.addWidget(self.labelPlot)
                
                self.groupboxPlotSet.layoutHFilename = QHBoxLayout(self)
                self.groupboxPlotSet.layoutHFilename.addWidget(self.Filename)
                self.groupboxPlotSet.layoutHFilename.addWidget(self.labelFile)

                self.groupboxPlotSet.layoutHPath = QHBoxLayout(self)
                self.groupboxPlotSet.layoutHPath.addWidget(self.buttonPath)
                self.groupboxPlotSet.layoutHPath.addWidget(self.labelPath)
                
                self.groupboxPlotSet.layoutPlotSet = QVBoxLayout(self)                                                                                  #Fügt das Label ein
                self.groupboxPlotSet.layoutPlotSet.addLayout(self.groupboxPlotSet.layoutHPlotname)                                                      #Fügt das Label ein
                self.groupboxPlotSet.layoutPlotSet.addLayout(self.groupboxPlotSet.layoutHFilename)                                                      #Fügt das Label ein
                self.groupboxPlotSet.layoutPlotSet.addLayout(self.groupboxPlotSet.layoutHPath)                                                          #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.groupboxPlotSet.setLayout(self.groupboxPlotSet.layoutPlotSet)


                #Layouts                                                                                                                                #Abstandshalter                                                                                               #Setzt den Ende-Button          
                self.layoutV = QVBoxLayout(self)                                                                                                        #Setzt einen Abstandshalter ein
                self.layoutV.addWidget(self.groupboxPlotSet)
                self.layoutV.addStretch(1)

                self.layoutGrid = QGridLayout(self)
                self.layoutGrid.addWidget(self.groupboxcbg, 0, 0)
                self.layoutGrid.addLayout(self.layoutV, 0, 2)
                self.layoutGrid.setColumnStretch(0, 3)
                self.layoutGrid.setColumnStretch(1, 1)
                self.layoutGrid.setColumnStretch(2, 9)
                
                self.layoutSave = QHBoxLayout(self)                                                                                                     #Setzt ein horizontales Layout
                self.layoutSave.addStretch(1)                                                                                                           #Setzt einen Abstandshalter ein
                self.layoutSave.addWidget(self.end)

                self.layoutv.addLayout(self.layoutGrid)                                                                                                 #Setzt ein vertikales Layout
                self.layoutv.addStretch(1)                                                                                                              #Fügt das Ende-Layout zum vertikalen Layout hinzu
                self.layoutv.addLayout(self.layoutSave)
                
                self.setLayout(self.layoutv)
                
        def usesettings(self):
                PlotSet.execute("SELECT * FROM settingsScanPlot WHERE ID = 1")
                for dsatzPlot in PlotSet:
                        plotstyle = dsatzPlot[1]
                        plotname = dsatzPlot[2]

                PlotName = plotname
                PlotStyle = plotstyle

                self.Plotname.setText(plotname)
                
                if PlotStyle == 1:
                        self.cbStyle1.setChecked(True)
                elif PlotStyle == 2:
                        self.cbStyle2.setChecked(True)
                elif PlotStyle == 3:
                        self.cbStyle3.setChecked(True)
                elif PlotStyle == 4:
                        self.cbStyle4.setChecked(True)
                elif PlotStyle == 5:
                        self.cbStyle5.setChecked(True)
                elif PlotStyle == 6:
                        self.cbStyle6.setChecked(True)
                elif PlotStyle == 7:
                        self.cbStyle7.setChecked(True)
                elif PlotStyle == 8:
                        self.cbStyle8.setChecked(True)
                elif PlotStyle == 9:
                        self.cbStyle9.setChecked(True)
                elif PlotStyle == 10:
                        self.cbStyle10.setChecked(True)
                elif PlotStyle == 11:
                        self.cbStyle11.setChecked(True)
                elif PlotStyle == 12:
                        self.cbStyle12.setChecked(True)
                elif PlotStyle == 13:
                        self.cbStyle13.setChecked(True)
                elif PlotStyle == 14:
                        self.cbStyle14.setChecked(True)
                elif PlotStyle == 15:
                        self.cbStyle15.setChecked(True)
                
                connPlot.commit()

        def closeEvent(self, event):
                global PlotStyle
                PlotStyle = self.cbgStyle.checkedId()
                global PlotName
                PlotName = self.Plotname.text()
                global FileName
                FileName = self.Filename.text()
                PlotSet.execute("UPDATE settingsScanPlot SET plotstyle=?, plotname=? WHERE ID=?", (PlotStyle, PlotName, 1))
                PlotSet.execute("SELECT * FROM settingsScanPlot")
                #print(PlotSet.fetchall())
                connPlot.commit()

        def SaveAndClose(self):
                global PlotStyle
                PlotStyle = self.cbgStyle.checkedId()
                global PlotName
                PlotName = self.Plotname.text()
                global FileName
                FileName = self.Filename.text()
                PlotSet.execute("UPDATE settingsScanPlot SET plotstyle=?, plotname=? WHERE ID=?", (PlotStyle, PlotName, 1))
                PlotSet.execute("SELECT * FROM settingsScanPlot")
                #print(PlotSet.fetchall())
                connPlot.commit()
                self.close()

        def OpenPath(self):
                global FilePath
                FilePath = str(QFileDialog.getExistingDirectory(self, "Open Path", "/home/pi/Desktop/Data/"))
                #print(FilePath)
                self.labelPath.setText(FilePath)
                
class TTLSettings(QWidget):
        progress_save = pyqtSignal(int)
        
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global NameTTL1
                TTL1 = 1
                global TTL1IN
                global TTL1OUT
                global Wire1
                global NameTTL2
                TTL2 = 2
                global TTL2IN
                global TTL2OUT
                global Wire2
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50

                self.setWindowTitle("TTL Settings")
                self.setGeometry(self.WindowPosX,self.WindowPosY,500,250)
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Settings.png"))

                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.NameTTL1 = QLineEdit(self)
                self.NameTTL2 = QLineEdit(self)
                self.buttonTestTTL1 = QPushButton("Test TTL 1", self)
                self.buttonTestTTL2 = QPushButton("Test TTL 2", self)
                self.labelTTL1 = QLabel("Name TTL1:", self)
                self.labelTTL2 = QLabel("Name TTL2:", self)
                self.TTL1Wire = QCheckBox("Activate 1-Wire for TTL1", self)                                                                             #Setzt eine CheckBox
                self.TTL1Wire.setToolTip("Sets the TTL to 1-Wire Communication, the TTL1OUT-BNC will work as In- and Output")
                self.TTL2Wire = QCheckBox("Activate 1-Wire for TTL2", self)                                                                             #Setzt eine CheckBox
                self.TTL2Wire.setToolTip("Sets the TTL to 1-Wire Communication, the TTL2OUT-BNC will work as In- and Output")
                self.buttonTestTTL1.setToolTip("Set the Filepath")
                self.buttonTestTTL1.clicked.connect(self.TestTTL1)
                self.buttonTestTTL2.setToolTip("Set the Filepath")
                self.buttonTestTTL2.clicked.connect(self.TestTTL2)
                self.NameTTL1.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL2.setToolTip("Choose a Name for the TTL connection")

                if Wire1 == True:
                        self.TTL1Wire.setChecked(True)
                else:
                        self.TTL1Wire.setChecked(False)                       
                if Wire2 == True:
                        self.TTL2Wire.setChecked(True)
                else:
                        self.TTL2Wire.setChecked(False)  

                self.NameTTL1.setText(NameTTL1)
                self.NameTTL2.setText(NameTTL2) 

                self.NameTTL1.move(130,30)
                self.NameTTL2.move(130,70)
                self.buttonTestTTL1.move(30,140)
                self.buttonTestTTL2.move(140,140)
                self.labelTTL1.move(30,32)
                self.labelTTL2.move(30,72)
                self.TTL1Wire.move(280,32)
                self.TTL2Wire.move(280,72)

                
                #Ende
                self.end = QPushButton("Save + Quit", self)                                                                                             #setzt einen Ende-Button
                self.end.setToolTip("Save the Changes and Quit the Window")                                                                             #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end.move(375,200)
                self.end.clicked.connect(self.SaveAndClose)                                                                                             #Ruft die end2-Funktion auf, wenn der Button gedrückt wird

        def TestTTL1(self):
                print("1")
                global TTL1IN
                global TTL1OUT
                self.getTTL = False
                self.TTLOUT = TTL1OUT
                self.TTLIN = TTL1IN
                self.OneWire = self.TTL1Wire.isChecked()
                
                if self.OneWire == 1:
                        self.TTLIN = self.TTLOUT
                        GPIO.setup(self.TTLOUT, GPIO.OUT, initial=GPIO.HIGH)
                        #print(str(self.TTLOUT) + " Output High")
                else:
                        GPIO.output(self.TTLOUT, GPIO.HIGH)
                        #print(str(self.TTLOUT) + " High")
                #print("TTL sent")
                time.sleep(0.1)
                GPIO.output(self.TTLOUT, GPIO.LOW)
                #print(str(self.TTLOUT) + " Low")

                                                        
                if self.getTTL == True:                                                
                        if self.OneWire == 1:
                                GPIO.setup(self.TTLIN, GPIO.IN)
                                #print(str(self.TTLIN) + " Input")
                        #print("Waiting for TTL Signal")
                        self.TTL = 0
                        GPIO.add_event_detect(self.TTLIN, GPIO.RISING, callback=self.EventHandler_rising1, bouncetime = 5)
                        #print(str(self.TTLIN) + " Event added")
                        while self.TTL == 0:
                                pass
                        #print("TTL recieved")
                        GPIO.remove_event_detect(self.TTLIN)
                        #print(str(self.TTLIN) + " Event removed")

        def TestTTL2(self):
                #print("2")
                global TTL2IN
                global TTL2OUT
                self.getTTL = False
                self.TTLOUT = TTL2OUT
                self.TTLIN = TTL2IN
                self.OneWire = self.TTL2Wire.isChecked()
                
                if self.OneWire == 1:
                        self.TTLIN = self.TTLOUT
                        GPIO.setup(self.TTLOUT, GPIO.OUT, initial=GPIO.HIGH)
                        #print(str(self.TTLOUT) + " Output High")
                else:
                        GPIO.output(self.TTLOUT, GPIO.HIGH)
                        #print(str(self.TTLOUT) + " High")
                #print("TTL sent")
                time.sleep(0.1)
                GPIO.output(self.TTLOUT, GPIO.LOW)
                #print(str(self.TTLOUT) + " Low")

                                                        
                if self.getTTL == True:                                                
                        if self.OneWire == 1:
                                GPIO.setup(self.TTLIN, GPIO.IN)
                                #print(str(self.TTLIN) + " Input")
                        #print("Waiting for TTL Signal")
                        self.TTL = 0
                        GPIO.add_event_detect(self.TTLIN, GPIO.RISING, callback=self.EventHandler_rising1, bouncetime = 5)
                        #print(str(self.TTLIN) + " Event added")
                        while self.TTL == 0:
                                pass
                        #print("TTL recieved")
                        GPIO.remove_event_detect(self.TTLIN)
                        #print(str(self.TTLIN) + " Event removed")

        def EventHandler_rising1(self):
                self.TTL = 1

        def closeEvent(self, event):
                global NameTTL1
                NameTTL1 = self.NameTTL1.text()
                global NameTTL2
                NameTTL2 = self.NameTTL2.text()
                global Wire1
                Wire1 = self.TTL1Wire.isChecked()
                global Wire2
                Wire2 = self.TTL2Wire.isChecked()
                TTLSet.execute("UPDATE settingsScanTTL SET name1=?, wire1=?, name2=?, wire2=? WHERE ID=?", (NameTTL1, Wire1, NameTTL2, Wire2, 1))
                TTLSet.execute("SELECT * FROM settingsScanTTL")
                #print(TTLSet.fetchall())
                connTTL.commit()
                self.progress_save.emit(1)

        def SaveAndClose(self):
                global NameTTL1
                NameTTL1 = self.NameTTL1.text()
                global NameTTL2
                NameTTL2 = self.NameTTL2.text()
                global Wire1
                Wire1 = self.TTL1Wire.isChecked()
                global Wire2
                Wire2 = self.TTL2Wire.isChecked()
                TTLSet.execute("UPDATE settingsScanTTL SET name1=?, wire1=?, name2=?, wire2=? WHERE ID=?", (NameTTL1, Wire1, NameTTL2, Wire2, 1))
                TTLSet.execute("SELECT * FROM settingsScanTTL")
                #print(TTLSet.fetchall())
                connTTL.commit()
                self.progress_save.emit(1)
                self.close()


class DeviceSettings(QWidget):
        progress_save = pyqtSignal(int)
        
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                
                global CHA
                global CHB
                global L2
                global L3
                global CH1
                global CH2
                global CH3
                global CH4
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50
                
                self.setWindowTitle("Device Settings")
                self.setGeometry(self.WindowPosX,self.WindowPosY,450,720)
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Settings.png"))

                #Tools
                self.ChannelA = QLineEdit(self)
                self.ChannelA.setToolTip("Set the Channelname")
                self.ChannelB = QLineEdit(self)
                self.ChannelB.setToolTip("Set the Channelname")
                self.ChannelL2 = QLineEdit(self)
                self.ChannelL2.setToolTip("Set the Channelname")
                self.ChannelL3 = QLineEdit(self)
                self.ChannelL3.setToolTip("Set the Channelname")
                self.Channel1 = QLineEdit(self)
                self.Channel1.setToolTip("Set the Channelname")
                self.Channel2 = QLineEdit(self)
                self.Channel2.setToolTip("Set the Channelname")
                self.Channel3 = QLineEdit(self)
                self.Channel3.setToolTip("Set the Channelname")
                self.Channel4 = QLineEdit(self)
                self.Channel4.setToolTip("Set the Channelname")
                
                self.PiezodistanceX = QSpinBox(self)
                self.PiezodistanceY = QSpinBox(self)
                self.PiezodistanceZ = QSpinBox(self)
                self.Piezovoltage = QDoubleSpinBox(self)


                #Label
                self.labelChA = QLabel("Channel A", self)
                self.labelChB = QLabel("Channel B", self)
                self.labelL2 = QLabel("Channel L2", self)
                self.labelL3 = QLabel("Channel L3", self)
                self.labelCh1 = QLabel("Channel 1", self)
                self.labelCh2 = QLabel("Channel 2", self)
                self.labelCh3 = QLabel("Channel 3", self)
                self.labelCh4 = QLabel("Channel 4", self)
                self.labelPiezodistanceX = QLabel("Piezo X-Range", self)
                self.labelXunit = QLabel("[nm]", self)
                self.labelPiezodistanceY = QLabel("Piezo Y-Range", self)
                self.labelYunit = QLabel("[nm]", self)
                self.labelPiezodistanceZ = QLabel("Piezo Z-Range", self)
                self.labelZunit = QLabel("[nm]", self)
                self.labelPiezovoltage = QLabel("Piezo Inputvoltage", self)
                self.labelVunit = QLabel("[V]", self)


                #Spinbox definieren
                self.PiezodistanceX.setMinimum(0)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.PiezodistanceX.setMaximum(1000000)     
                self.PiezodistanceX.setToolTip("Set the Maximum X-Range of the Piezotable in Nanometers")
                self.PiezodistanceX.setValue(PiezoDistanceX)                                                                                            #Setzt einen Startwert
                #self.PiezodistanceX.valueChanged.connect(self.savesettings)
                
                self.PiezodistanceY.setMinimum(0)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.PiezodistanceY.setMaximum(1000000) 
                self.PiezodistanceY.setToolTip("Set the Maximum Y-Range of the Piezotable in Nanometers")
                self.PiezodistanceY.setValue(PiezoDistanceY)                                                                                            #Setzt einen Startwert
                #self.PiezodistanceY.valueChanged.connect(self.savesettings)
                
                self.PiezodistanceZ.setMinimum(0)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.PiezodistanceZ.setMaximum(1000000) 
                self.PiezodistanceZ.setToolTip("Set the Maximum Z-Range of the Piezotable in Nanometers")
                self.PiezodistanceZ.setValue(PiezoDistanceZ)                                                                                            #Setzt einen Startwert
                #self.PiezodistanceZ.valueChanged.connect(self.savesettings)

                self.Piezovoltage.setMinimum(0.00)                                                                                                      #Setzt ein Minimalwert für die Auswahl
                self.Piezovoltage.setMaximum(25.00)                                                                                                     #Setzt ein Maximum für die Auswahl
                self.Piezovoltage.setValue(PiezoVoltage)                                                                                                #Setzt einen Startwert
                self.Piezovoltage.setSingleStep(0.01)
                self.Piezovoltage.setDecimals(2)                                                                                                        #Setzt einen Startwert
                #self.Piezovoltage.valueChanged.connect(self.savesettings)
                self.Piezovoltage.setToolTip("Set the Maximum Inputvoltage of the Piezotable in Volts")


                #Move
                self.ChannelA.move(200,250)
                self.labelChA.move(50,250)
                self.ChannelB.move(200,300)
                self.labelChB.move(50,300)
                self.ChannelL2.move(200,350)
                self.labelL2.move(50,350)
                self.ChannelL3.move(200,400)
                self.labelL3.move(50,400)
                self.Channel1.move(200,450)
                self.labelCh1.move(50,450)
                self.Channel2.move(200,500)
                self.labelCh2.move(50,500)
                self.Channel3.move(200,550)
                self.labelCh3.move(50,550)
                self.Channel4.move(200,600)
                self.labelCh4.move(50,600)
                self.PiezodistanceX.move(200,50)
                self.labelPiezodistanceX.move(50,50)
                self.labelXunit.move(310,50)
                self.PiezodistanceY.move(200,100)
                self.labelPiezodistanceY.move(50,100)
                self.labelYunit.move(310,100)
                self.PiezodistanceZ.move(200,150)
                self.labelPiezodistanceZ.move(50,150)
                self.labelZunit.move(310,150)
                self.Piezovoltage.move(200,200)
                self.labelPiezovoltage.move(50,200)
                self.labelVunit.move(280,200)


                #Set Values
                self.ChannelA.setText(str(CHA))
                self.ChannelB.setText(str(CHB))
                self.ChannelL2.setText(str(L2))
                self.ChannelL3.setText(str(L3))
                self.Channel1.setText(str(CH1))
                self.Channel2.setText(str(CH2))
                self.Channel3.setText(str(CH3))
                self.Channel4.setText(str(CH4))
                self.PiezodistanceX.setValue(PiezoDistanceX)
                self.PiezodistanceY.setValue(PiezoDistanceY)
                self.PiezodistanceZ.setValue(PiezoDistanceZ)
                self.Piezovoltage.setValue(PiezoVoltage)


                #Ende
                self.end = QPushButton("Save + Quit", self)                                                                                             #setzt einen Ende-Button
                self.end.setToolTip("Save the Changes and Quit the Window")                                                                             #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end.move(340,670)
                self.end.clicked.connect(self.SaveAndClose)  
                
        def usesettings(self):
                DevSet.execute("SELECT * FROM settingsScanDev WHERE ID = 1")
                for dsatzDev in DevSet:
                        piezodistanceX = dsatzDev[0]
                        piezodistanceY = dsatzDev[1]
                        piezodistanceZ = dsatzDev[2]
                        piezovoltage = dsatzDev[3]
                        ChA = dsatzDev[4]
                        ChB = dsatzDev[5]
                        l2 = dsatzDev[6]
                        l3 = dsatzDev[7]
                        Ch1 = dsatzDev[8]
                        Ch2 = dsatzDev[9]
                        Ch3 = dsatzDev[10]
                        Ch4 = dsatzDev[11]
                        #print(piezodistanceX + ", " + piezodistanceY + ", " + piezodistanceZ + ", " + piezovoltage + ", " + ChA + ", " + ChB + ", " + l2 + ", " + l3 + ", " + Ch1 + ", " + Ch2 + ", " + Ch3 + ", " + Ch4)

                PiezoDistanceX = piezodistanceX                     #Nanometers
                PiezoDistanceY = piezodistanceY                     #Nanometers
                PiezoDistanceZ = piezodistanceZ                     #Nanometers
                PiezoVoltage = piezovoltage                         #Volts
                FullRangeDeviceX = PiezoDistanceX * (DeviceVoltage / PiezoVoltage)
                FullRangeDeviceY = PiezoDistanceY * (DeviceVoltage / PiezoVoltage)
                FullRangeDeviceZ = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)
                CHA = ChA                                           #Channel A
                CHB = ChB                                           #Channel B
                L2 = l2                                             #Channel L2
                L3 = l3                                             #Channel L3
                CH1 = Ch1                                           #Channel 1
                CH2 = Ch2                                           #Channel 2
                CH3 = Ch3                                           #Channel 3
                CH4 = Ch4                                           #Channel 4
                        
                self.ChannelA.setText(CHA)
                self.ChannelB.setText(CHB)
                self.ChannelL2.setText(L2)
                self.ChannelL3.setText(L3)
                self.Channel1.setText(CH1)
                self.Channel2.setText(CH2)
                self.Channel3.setText(CH3)
                self.Channel4.setText(CH4)
                self.PiezodistanceX.setValue(PiezoDistanceX)
                self.PiezodistanceY.setValue(PiezoDistanceY)
                self.PiezodistanceZ.setValue(PiezoDistanceZ)
                self.Piezovoltage.setValue(PiezoVoltage)
                
                connDev.commit()

        def closeEvent(self, event):
                global CHA
                global CHB
                global L2
                global L3
                global CH1
                global CH2
                global CH3
                global CH4
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoDistanceZ
                global PiezoVoltage
                global FullRangeDeviceX
                global FullRangeDeviceY
                global FullRangeDeviceZ

                PiezoDistanceX = self.PiezodistanceX.value()                         #Nanometers
                PiezoDistanceY = self.PiezodistanceY.value()                         #Nanometers
                PiezoDistanceZ = self.PiezodistanceZ.value()                         #Nanometers
                PiezoVoltage = self.Piezovoltage.value()                             #Volts
                FullRangeDeviceX = PiezoDistanceX * (DeviceVoltage / PiezoVoltage)
                FullRangeDeviceY = PiezoDistanceY * (DeviceVoltage / PiezoVoltage)
                FullRangeDeviceZ = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)
                CHA = self.ChannelA.text()                                           #Channel A
                CHB = self.ChannelB.text()                                           #Channel B
                L2 = self.ChannelL2.text()                                           #Channel L2
                L3 = self.ChannelL3.text()                                           #Channel L3
                CH1 = self.Channel1.text()                                           #Channel 1
                CH2 = self.Channel2.text()                                           #Channel 2
                CH3 = self.Channel3.text()                                           #Channel 3
                CH4 = self.Channel4.text()                                           #Channel 4
                DevSet.execute("UPDATE settingsScanDev SET piezodistanceX=?, piezodistanceY=?, piezodistanceZ=?, piezovoltage=?, ChA=?, ChB=?, L2=?, L3=?, Ch1=?, Ch2=?, Ch3=?, Ch4=? WHERE ID=?", (PiezoDistanceX, PiezoDistanceY, PiezoDistanceZ, PiezoVoltage, CHA, CHB, L2, L3, CH1, CH2, CH3, CH4, 1))
                DevSet.execute("SELECT * FROM settingsScanDev")
                #print(DevSet.fetchall())
                connDev.commit()
                self.progress_save.emit(1)
                
        def SaveAndClose(self):
                global CHA
                global CHB
                global L2
                global L3
                global CH1
                global CH2
                global CH3
                global CH4
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoDistanceZ
                global PiezoVoltage
                global FullRangeDeviceX
                global FullRangeDeviceY
                global FullRangeDeviceZ

                PiezoDistanceX = self.PiezodistanceX.value()                         #Nanometers
                PiezoDistanceY = self.PiezodistanceY.value()                         #Nanometers
                PiezoDistanceZ = self.PiezodistanceZ.value()                         #Nanometers
                PiezoVoltage = self.Piezovoltage.value()                             #Volts
                FullRangeDeviceX = PiezoDistanceX * (DeviceVoltage / PiezoVoltage)
                FullRangeDeviceY = PiezoDistanceY * (DeviceVoltage / PiezoVoltage)
                FullRangeDeviceZ = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)
                CHA = self.ChannelA.text()                                           #Channel A
                CHB = self.ChannelB.text()                                           #Channel B
                L2 = self.ChannelL2.text()                                           #Channel L2
                L3 = self.ChannelL3.text()                                           #Channel L3
                CH1 = self.Channel1.text()                                           #Channel 1
                CH2 = self.Channel2.text()                                           #Channel 2
                CH3 = self.Channel3.text()                                           #Channel 3
                CH4 = self.Channel4.text()                                           #Channel 4
                DevSet.execute("UPDATE settingsScanDev SET piezodistanceX=?, piezodistanceY=?, piezodistanceZ=?, piezovoltage=?, ChA=?, ChB=?, L2=?, L3=?, Ch1=?, Ch2=?, Ch3=?, Ch4=? WHERE ID=?", (PiezoDistanceX, PiezoDistanceY, PiezoDistanceZ, PiezoVoltage, CHA, CHB, L2, L3, CH1, CH2, CH3, CH4, 1))
                DevSet.execute("SELECT * FROM settingsScanDev")
                #print(DevSet.fetchall())
                connDev.commit()
                self.progress_save.emit(1)
                self.close()

class AboutMe(QWidget):
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global Version
                global Updates
                global NumberUpdates
                global Copyright
                global Contact
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50
                
                self.setWindowTitle("About")
                self.setGeometry(self.WindowPosX,self.WindowPosY,400,(150 + (NumberUpdates * 25)))
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/About.png"))

                #Widgets setzen
                self.labelVersion = QLabel(("Version:\t HydraScan " + str(Version)), self)
                self.labelVersion.move(30, 25)

                self.labelUpdates = QLabel(("Updates: " + Updates), self)
                self.labelUpdates.move(30, 60)
                
                self.labelContact = QLabel(("Contact:    " + Contact), self)
                self.labelContact.move(30, ((NumberUpdates * 25) + 60))
                
                self.labelCopyright = QLabel(("Copyright:" + Copyright), self)
                self.labelCopyright.move(30, ((NumberUpdates * 25) + 95))

class HelpMe(QWidget):
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global CurrentPage
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50
                                        
                self.CurrentPage = CurrentPage

                self.setGeometry(self.WindowPosX,self.WindowPosY,400,100)
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Help.png"))

                if self.CurrentPage == 0:
                        self.setWindowTitle("Help for Tab \"Positioning\"")
                elif self.CurrentPage == 1:
                        self.setWindowTitle("Help for Tab \"Measurement\"")
                elif self.CurrentPage == 2:
                        self.setWindowTitle("Help for Tab \"TTL Sync\"")
                elif self.CurrentPage == 3:
                        self.setWindowTitle("Help for Tab \"Z-Stack\"")
                elif self.CurrentPage == 4:
                        self.setWindowTitle("Help for Tab \"Slope Compensation\"")
                elif self.CurrentPage == 10:
                        self.setWindowTitle("Help for Connecting your HydraBox")
                elif self.CurrentPage == 11:
                        self.setWindowTitle("Help for your HydraScan Software")
                elif self.CurrentPage == 12:
                        self.setWindowTitle("Help with the TroubleShooting")
                        

                #Widgets setzen
                self.labelHelp = QLabel("Uhhh, so custom!", self)
                self.labelHelp.move(30, 25)

class HydraPopup(QWidget):
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                self.setWindowTitle("Hail Hydra!")
                self.setGeometry(100,100,300,200)

                vbox = QVBoxLayout()
                labelImage = QLabel(self)
                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/HydraLogo_grün.png")
                labelImage.setPixmap(pixmap)
                vbox.addWidget(labelImage)
                self.setLayout(vbox)
 
class HydraClose(QThread):
        progress_value = pyqtSignal(int)

        def __init__(self, parent=None):
                QThread.__init__(self, parent)
                
        def run(self):
                #print("start counter")
                time.sleep(0.5)
                self.killFred()

        def killFred(self):                                                                                                                             #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                #GPIO.output(14, GPIO.LOW)
                print("Hail Hydra!")
                self.progress_value.emit(1)


#Programm starts here! ;-)
#Main Window ---------------------------------------------------------
class Fenster(QMainWindow):                                                                                                                             #Das Fenster wird hier als Klasse definiert
        def __init__(self):                                                                                                                             #Die init methode wird immer ausgeführt
                super().__init__()                                                                                                                      #super-Funktion gibt Style-Methoden an die Klasse
                self.initMe()                                                                                                                           #Aufruf der initMe-Funktion

        def initMe(self):
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight
                self.setGeometry(WindowPosX, WindowPosY, WindowWidth, WindowHeight)                                                                     #Fensergröße und Position
                self.setMinimumSize(QSize(1000,700))                                                                                                    #Setzt einen Minimalwert für das Fenster, kleiner kann es nicht gezogen werden
                self.setWindowTitle("HydraScan " + str(Version))                                                                                        #Titelbalken
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/HydraScan_free.png")) 
             
                self.table_widget = MyTables(self)                                                                              
                self.setCentralWidget(self.table_widget)                                                                                                #Icon oben links

                self.statusBar().showMessage("Property of University Tübingen")                                                                         #Setzt im StatusBar des Fensters den Text

                mainMenu = self.menuBar()
                setMenu = mainMenu.addMenu("Settings")
                helpMenu = mainMenu.addMenu("Help")

                helpConnect = QAction("Connections", self)
                helpConnect.setShortcut("Ctrl+Alt+C")
                helpConnect.setStatusTip("All you need to know about the Hardwere setup")
                helpConnect.triggered.connect(self.show_helpConnect)
                helpMenu.addAction(helpConnect) 

                helpSoftware = QAction("Software", self)
                helpSoftware.setShortcut("Ctrl+Alt+S")
                helpSoftware.setStatusTip("All you need to know about the Software setup")
                helpSoftware.triggered.connect(self.show_helpSoftware)
                helpMenu.addAction(helpSoftware) 

                helpTrouble = QAction("Troubleshooting", self)
                helpTrouble.setShortcut("Ctrl+Alt+H")
                helpTrouble.setStatusTip("All you need to know about Troubleshooting")
                helpTrouble.triggered.connect(self.show_helpTrouble)
                helpMenu.addAction(helpTrouble) 

                helpCurrent = QAction("Current Tab", self)
                helpCurrent.setShortcut("Ctrl+H")
                helpCurrent.setStatusTip("All you need to know about the current Tab")
                helpCurrent.triggered.connect(self.show_helpCurrent)
                helpMenu.addAction(helpCurrent) 
  
                aboutMe = QAction("About", self)
                aboutMe.setShortcut("Ctrl+A")
                aboutMe.setStatusTip("All you need to know")
                aboutMe.triggered.connect(self.show_about)
                mainMenu.addAction(aboutMe)
   
                DeviceSettings = QAction("Device Settngs", self)
                DeviceSettings.setShortcut("Ctrl+D")
                DeviceSettings.setStatusTip("Setup the Deviceproperties")
                DeviceSettings.triggered.connect(self.show_devset)
                setMenu.addAction(DeviceSettings)                                                                                                       #ruft die Klasse MyTables als Widget auf

                PlotSettings = QAction("Plot Settings", self)
                PlotSettings.setShortcut("Ctrl+P")
                PlotSettings.setStatusTip("Define the Plot")
                PlotSettings.triggered.connect(self.show_pltset)
                #setMenu.addAction(PlotSettings)

                TTLSettings = QAction("TTL Settings", self)
                TTLSettings.setShortcut("Ctrl+T")
                TTLSettings.setStatusTip("Define the TTL Funktion")
                TTLSettings.triggered.connect(self.show_ttlset)
                setMenu.addAction(TTLSettings)
                
                ExitButton = QAction("Exit", self)
                ExitButton.setShortcut("Ctrl+Q")
                ExitButton.setStatusTip("Exit application")
                ExitButton.triggered.connect(self.Hydra)
                setMenu.addAction(ExitButton)

                PLTShow = QAction("Show Plot", self)
                PLTShow.setShortcut("Ctrl+Alt+P")
                PLTShow.setStatusTip("Show Live Plot")
                PLTShow.triggered.connect(self.table_widget.show_plot)
                mainMenu.addAction(PLTShow)

                NavShow = QAction("Show Navigation", self)
                NavShow.setShortcut("Ctrl+Alt+N")
                NavShow.setStatusTip("Shop the Navigation Window")
                NavShow.triggered.connect(self.table_widget.show_NavWin)
                mainMenu.addAction(NavShow)

                TempHumSens = QAction("Show Temp", self)
                TempHumSens.setShortcut("Ctrl+Alt+T")
                TempHumSens.setStatusTip("Show Temperature readings")
                TempHumSens.triggered.connect(self.table_widget.show_temp)
                mainMenu.addAction(TempHumSens)

                APDShow = QAction("Show APD", self)
                APDShow.setShortcut("Ctrl+Alt+A")
                APDShow.setStatusTip("Show APD readings")
                APDShow.triggered.connect(self.table_widget.show_apd)
                mainMenu.addAction(APDShow)

                self.show_NavWin()
                #self.show_temp()
                #self.show_apd()

                self.show()                                                                                                                             #Die Show funktion zeigt das MainWindow an

        def closeEvent(self, event):
                #print("Close")
                self.quitall()
                GPIO.cleanup()
                #print("Cleanup2")
                self.Hydra()

        def show_NavWin(self):
                self.table_widget.show_NavWin()

        def show_apd(self):
                global APDWindowOn
                self.APDWin = APDWindow()
                self.APDWin.show()
                APDWindowOn = 1
                
        def show_temp(self):
                global TempWindowOn
                self.TempSens = TempWindow()
                self.TempSens.show()
                TempWindowOn = 1
                
        def show_plot(self):
                #global TempWindowOn
                self.PlotWin = PlotWindow()
                self.PlotWin.show()
                #TempWindowOn = 1

        def quitall(self):
                global TempWindowOn
                global APDWindowOn                
                try:
                        self.APDWin.WindowClose()
                        APDWindowOn = 0
                except:
                        pass
                try:
                        self.TempSens.WindowClose()
                        TempWindowOn = 0
                except:
                        pass
                try:
                        self.PlotWin.WindowClose()
                        #TempWindowOn = 0
                except:
                        pass

                try:
                        self.table_widget.exit()
                except:
                        pass

        def moveEvent(self, e):
                self.WindowPosition()
                super(Fenster, self).moveEvent(e)

        def WindowPosition(self):
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight
                
                WindowPosX = self.geometry().x()
                WindowPosY = self.geometry().y()
                WindowWidth = self.geometry().width()
                WindowHeight = self.geometry().height()
                #print("WindowX: " + str(WindowPosX) + "\t" + str(WindowWidth))
                #print("WindowY: " + str(WindowPosY) + "\t" + str(WindowHeight))

        def show_devset(self):
                self.devset = DeviceSettings()
                self.devset.progress_save.connect(self.UpdateTabsDevice)
                self.devset.show()

        def show_ttlset(self):
                self.ttlset = TTLSettings()
                self.ttlset.progress_save.connect(self.UpdateTabsTTL)
                self.ttlset.show()

        def UpdateTabsDevice(self):
                self.table_widget.UpdateChannelNames()

        def UpdateTabsTTL(self):
                self.table_widget.UpdateTTLNames()

        def show_pltset(self):
                self.pltset = PlotSettings()
                self.pltset.show()

        def show_about(self):
                self.aboutme = AboutMe()
                self.aboutme.show()
                self.WindowPosition()

        def show_helpCurrent(self):
                global CurrentPage
                CurrentPage = self.table_widget.tabs.currentIndex()
                self.helpme = HelpMe()
                self.helpme.show()

        def show_helpConnect(self):
                global CurrentPage
                CurrentPage = 10
                self.helpme = HelpMe()
                self.helpme.show()

        def show_helpSoftware(self):
                global CurrentPage
                CurrentPage = 11
                self.helpme = HelpMe()
                self.helpme.show()

        def show_helpTrouble(self):
                global CurrentPage
                CurrentPage = 12
                self.helpme = HelpMe()
                self.helpme.show()

        def Hydra(self):
                self.H = HydraPopup()
                self.H.show()
                self.HY = HydraClose()     
                self.HY.progress_value.connect(self.HYconnect)
                self.HY.start()

        def HYconnect(self, val):
                if val == 1:
                        self.HYende()

        def HYende(self):                                                                                                                               #Die Ende-Funktion beendet alle Prozesse
                try:
                        connMeasure.commit()                                                           
                        connMeasure.close()
                except:
                        connMeasure.close()

                try:
                        connSync.commit()                                                           
                        connSync.close()
                except:
                        connSync.close()

                try:
                        connStack.commit()                                                           
                        connStack.close()
                except:
                        connStack.close()

                try:
                        connSlope.commit()                                                           
                        connSlope.close()
                except:
                        connSlope.close()

                try:
                        connDev.commit()                                                           
                        connDev.close()
                except:
                        connDev.close()

                try:
                        connPlot.commit()                                                           
                        connPlot.close()
                except:
                        connPlot.close()

                try:
                        connTTL.commit()                                                           
                        connTTL.close()
                except:
                        connTTL.close()
                        
                try:
                        self.Txt_out.close()
                        self.Txt_sub.close()
                except:
                        pass
                        
                try:
                        self.Manfred.killFred()
                except:
                        pass

                try:
                        self.Monty.killFred()
                except:
                        pass

                try:
                        self.FylingCircus.killFred()
                except:
                        pass

                try:
                        dacX.set_voltage(0)
                        dacY.set_voltage(0)
                        dacZ.set_voltage(0)
                except:
                        pass
                
                try:
                        adc.stop_adc()
                except:
                        pass
                        
                try:
                        plt.close()
                except:
                        pass

                try:
                        GPIO.output(14, 0)
                except:
                        pass

                try:
                        GPIO.output(15, 0)
                except:
                        pass
                
                try:
                        GPIO.output(17, 0)
                except:
                        pass
                
                try:
                        GPIO.output(18, 0)
                except:
                        pass

                try:
                        GPIO.output(22, 0)
                except:
                        pass

                try:
                        GPIO.output(27, 0)
                except:
                        pass                
                GPIO.cleanup()
                #print("Cleanup3")                        
                print("Programm beendet")

                sys.exit()                                                                                                                              #Beendet das Fenster

                        
class MyTables(QWidget):     
        def __init__(self, parent):
                super(QWidget, self).__init__(parent)

                global APDon
                global DHTon
                global StyleColor
                global StyleName
                PLTon = 1
                if PLTon == 1:
                        self.show_plot()
                if APDon == 1:
                        self.show_apd()
                if DHTon == 1:
                        self.show_temp()
                
                self.layout = QVBoxLayout(self)
                self.show_NavWin()
                
                #Definition lokaler Variablen
                self.PositionX = 0
                self.PositionY = 0
                self.StartX = 0
                self.StartY = 0
                self.StopX = 0
                self.StopY = 0
                self.bitval = 256
                self.bitval2 = 255
                self.bitval3 = 256
                self.XSlopeUp = 0
                self.XSlopeDown = 0
                self.XSlope = 0
                self.YSlopeUp = 0
                self.YSlopeDown = 0
                self.YSlope = 0         
                self.monty = 0
                self.flyingcircus = 0

                #Tabs definieren
                self.tabs = QTabWidget()
                self.tab1 = QWidget()
                self.tab2 = QWidget()
                self.tab3 = QWidget()
                self.tab4 = QWidget()
                self.tab5 = QWidget()
                #self.tab6 = QWidget()
                if StyleColor == "dark" and StyleName == "windowsvista":
                        self.tabs.setStyleSheet("color: black;"
                                                "background-color: rgb(153,153,153);")
                        #self.tabs.setStyleSheet("QPushButton {color: white}")
                #für weiter Tabs hier eine neue Zeile einfügen
                
                #Tabs zum Widget hinzufügen
                self.tabs.addTab(self.tab1, "Positioning")
                self.tabs.addTab(self.tab2, "Measurement")
                self.tabs.addTab(self.tab3, "TTL Sync")
                self.tabs.addTab(self.tab4, "Z-Stack")
                self.tabs.addTab(self.tab5, "Slope Compensation")
                #self.tabs.addTab(self.tab6, "Plot Files")
                #für weiter Tabs hier eine neue Zeile einfügen
                
#------------------------ Tab1 -----------------------------
                global CHA
                global CHB
                global L2
                global L3
                global CH1
                global CH2
                global CH3
                global CH4
                global NameTTL1
                global NameTTL2
                global Wire1
                global Wire2
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoDistanceZ
                global PiezoVoltage
                global DeviceVoltage
                global FullRangeDeviceX
                global FullRangeDeviceY
                global FullRangeDeviceZ
                global PlotStyle
                global FilePath
                global FileName
                global PlotName
                global PointSpeed
                
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am anfang zu definieren, da sonst später aufruffehler auftretten können
                self.buttonPos = QPushButton("Start Positioning", self)                                                                                 #setzt einen Button                                                                             
                self.buttonPoint = QPushButton("Start Measurement", self)
                self.PointDelay = QDoubleSpinBox(self)                                                                                                  #setzt eine Spinbox
                self.TTLroot = QComboBox(self)
                self.labelX1 = QLabel("X-Position [nm]", self)  
                self.slideX = QSlider(Qt.Horizontal)
                self.spinX = QDoubleSpinBox(self)
                self.labelY1 = QLabel("Y-Position [nm]", self)  
                self.slideY = QSlider(Qt.Horizontal)                                                                                                    #setzt einen horizontalen Slider
                self.spinY = QDoubleSpinBox(self)
                self.labelVal = QLabel("Value:", self)                                                                                                  #Setzt ein Label 
                self.textVal = QLabel("None", self)                                                                                                     #Setzt ein Label
                self.labelVal2 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal2 = QLabel("None", self)                                                                                                    #Setzt ein Label
                self.labelVal3 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal3 = QLabel("None", self)                                                                                                    #Setzt ein Label
                self.labelVal4 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal4 = QLabel("None", self)                                                                                                    #Setzt ein Label
                self.labelVal5 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal5 = QLabel("None", self)                                                                                                    #Setzt ein Label 
                self.labelVal6 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal6 = QLabel("None", self)                                                                                                    #Setzt ein Label     
                self.labelVal7 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal7 = QLabel("None", self)                                                                                                    #Setzt ein Label     
                self.labelVal8 = QLabel("Value:", self)                                                                                                 #Setzt ein Label 
                self.textVal8 = QLabel("None", self)                                                                                                    #Setzt ein Label 
                self.labelPointDelay = QLabel("Delay [s]", self)            
                self.labelSendTTL1 = QLabel("Send TTL Signal\nto Device", self)  
                self.labelGetTTL1 = QLabel("Wait for TTL\nDevice to answer", self)          
                self.labelStretch1Tab1 = QLabel("", self)
                self.labelStretch2Tab1 = QLabel("", self) 
                self.labelIntTime1 = QLabel("Integration [ms]", self)
                self.spinIntTime1 = QSpinBox(self) 
                self.bitval = 255        

                self.labelVal.setAlignment(Qt.AlignRight)
                self.labelVal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.labelVal2.setAlignment(Qt.AlignRight)
                self.labelVal2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.labelVal3.setAlignment(Qt.AlignRight)
                self.labelVal3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.labelVal4.setAlignment(Qt.AlignRight)
                self.labelVal4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.labelVal5.setAlignment(Qt.AlignRight)
                self.labelVal5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.labelVal6.setAlignment(Qt.AlignRight)
                self.labelVal6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
                #Checkboxen setzen
                self.TTLgetPoint1 = QCheckBox("Wait for TTL", self)

                self.cbch11 = QCheckBox(CH1, self)                                                                                                      #Setzt eine CheckBox
                self.cbch11.setToolTip("Sets the Input to " + CH1)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch12 = QCheckBox(CH2, self)                                                                                                      #Setzt eine CheckBox
                self.cbch12.setToolTip("Sets the Input to " + CH2)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch13 = QCheckBox(CH3, self)                                                                                                      #Setzt eine CheckBox
                self.cbch13.setToolTip("Sets the Input to " + CH3)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch14 = QCheckBox(CH4, self)                                                                                                      #Setzt eine CheckBox
                self.cbch14.setToolTip("Sets the Input to " + CH4)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch15 = QCheckBox(CHA, self)                                                                                                      #Setzt eine CheckBox
                self.cbch15.setToolTip("Sets the Input to " + CHA)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch16 = QCheckBox(CHB, self)                                                                                                      #Setzt eine CheckBox
                self.cbch16.setToolTip("Sets the Input to " + CHB)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch17 = QCheckBox(L2, self)                                                                                                       #Setzt eine CheckBox
                self.cbch17.setToolTip("Sets the Input to " + L2)                                                                                       #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch18 = QCheckBox(L3, self)                                                                                                       #Setzt eine CheckBox
                self.cbch18.setToolTip("Sets the Input to " + L3)                                                                                       #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch15.setChecked(True)
                self.cbch16.setChecked(True)

                #Checkboxen Window setzen
                self.cb10 = QCheckBox("64 Pixel", self)                                                                                                 #Setzt eine CheckBox
                self.cb10.setToolTip("Sets the resolution to 64 Pixel")                                                                                 #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb11 = QCheckBox("128 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb11.setToolTip("Sets the resolution to 128 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb12 = QCheckBox("256 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb12.setToolTip("Sets the resolution to 256 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb12.setChecked(True)
                self.cb13 = QCheckBox("512 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb13.setToolTip("Sets the resolution to 512 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb14 = QCheckBox("1024 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb14.setToolTip("Sets the resolution to 1024 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb15 = QCheckBox("2048 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb15.setToolTip("Sets the resolution to 2048 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb16 = QCheckBox("4096 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb16.setToolTip("Sets the resolution to 4096 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver

                #Button definieren
                self.buttonPos.setCheckable(True)                                                                                                       #macht den Button chackbar
                self.buttonPos.setToolTip("Starts the Positioning")                                                                                     #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonPos.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                #self.buttonPos.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonPos.clicked[bool].connect(self.clickedPos)                                                                                   #ruft die clickedPos-Funktion auf, wenn der Button betätigt wird und gibt einen true Wert an die Funktion, wenn der Button unten bleibt und einen false Wert, wenn er wieder oben ist
                self.buttonPos.setFixedSize(130, 25)
                
                self.buttonPoint.setCheckable(True)
                self.buttonPoint.setToolTip("Start the Measurement at the Point")
                self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonPoint.clicked[bool].connect(self.clickedPoint)               
                self.buttonPoint.setFixedSize(130, 25)
                
                #ComboBox definieren
                self.TTLroot.addItem(NameTTL1)
                self.TTLroot.addItem(NameTTL2)

                #Slider definieren
                self.slideX.setMinimum(0)                                                                                                               #Setzt ein Minimalwert für die Auswahl
                self.slideX.setMaximum(255)                                                                                                             #Setzt ein Maximum für die Auswahl
                self.slideX.setValue(0)                                                                                                                 #Setzt einen Startwert
                self.slideX.setTickPosition(QSlider.TicksBelow)                                                                                         #Setzt Rastpunkte unter dem Slider
                self.slideX.setTickInterval(256)                                                                                                        #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideX.valueChanged.connect(self.positionX)                                                                                        #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideX.setToolTip("Sets the X-Position")                                                                                           #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideY.setMinimum(0)                                                                                                               #Setzt ein Minimalwert für die Auswahl
                self.slideY.setMaximum(255)                                                                                                             #Setzt ein Maximum für die Auswahl
                self.slideY.setValue(0)                                                                                                                 #Setzt einen Startwert
                self.slideY.setTickPosition(QSlider.TicksBelow)                                                                                         #Setzt Rastpunkte unter dem Slider
                self.slideY.setTickInterval(256)                                                                                                        #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideY.valueChanged.connect(self.positionY)                                                                                        #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideY.setToolTip("Sets the Y-Position")                                                                                           #Setzt eine Buttonbeschreibung bei MouseOver

                #Spinbox definieren
                self.spinX.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.spinX.setMaximum(FullRangeDeviceX/1000)                                                                                            #Setzt ein Maximum für die Auswahl
                self.spinX.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.spinX.valueChanged.connect(self.spinboxX)                                                                                          #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinX.setSingleStep(round((FullRangeDeviceX/1000)/256,3))
                self.spinX.setDecimals(3)
                self.spinX.setToolTip("Sets the X-Position")                                                                                            #Setzt eine Buttonbeschreibung bei MouseOver
                
                self.spinY.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.spinY.setMaximum(FullRangeDeviceY/1000)                                                                                            #Setzt ein Maximum für die Auswahl
                self.spinY.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.spinY.valueChanged.connect(self.spinboxY)                                                                                          #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinY.setSingleStep(round((FullRangeDeviceY/1000)/256,3))
                self.spinY.setDecimals(3)
                self.spinY.setToolTip("Sets the Y-Position")                                                                                            #Setzt eine Buttonbeschreibung bei MouseOver
                
                self.PointDelay.setMinimum(0.000)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.PointDelay.setMaximum(60.000)                                                                                                      #Setzt ein Maximum für die Auswahl
                self.PointDelay.setValue(1.000)                                                                                                         #Setzt einen Startwert
                self.PointDelay.setSingleStep(0.001)
                self.PointDelay.setDecimals(3)
                self.PointDelay.setToolTip("Sets the Measurementtime in Seconds")                                                                       #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinIntTime1.setMinimum(1)
                self.spinIntTime1.setMaximum(20)
                self.spinIntTime1.setValue(1)
                self.spinIntTime1.setToolTip("Set the Integrationtime of the Logic-Channels in Milliseconds")
                if self.cbch15.isChecked() == True or self.cbch16.isChecked() == True or self.cbch17.isChecked() == True or self.cbch18.isChecked() == True:
                        self.spinIntTime1.setVisible(True)
                        self.labelIntTime1.setVisible(True)
                else:
                        self.spinIntTime1.setVisible(False)
                        self.labelIntTime1.setVisible(False)                                                                                            #Setzt einen Startwert
                self.spinIntTime1.valueChanged.connect(self.IntChange) 
                
                #Checkboxen definieren
                self.cb10.stateChanged.connect(self.stopAll)                                                                                            #Ruft die stopAll-Funktion auf, wenn der eine der CheckBoxen geklickt wird
                self.cb11.stateChanged.connect(self.stopAll)                                                            
                self.cb12.stateChanged.connect(self.stopAll)                                                         
                self.cb13.stateChanged.connect(self.stopAll)                                                           
                self.cb14.stateChanged.connect(self.stopAll)                                                           
                self.cb15.stateChanged.connect(self.stopAll)                                                        
                self.cb16.stateChanged.connect(self.stopAll)                                                          
                self.cbch15.stateChanged.connect(self.CBCH1LogicSelected)
                self.cbch16.stateChanged.connect(self.CBCH1LogicSelected)
                self.cbch17.stateChanged.connect(self.CBCH1LogicSelected)
                self.cbch18.stateChanged.connect(self.CBCH1LogicSelected)
                        
                #Ende
                self.end1 = QPushButton("Exit", self)                                                                                                   #setzt einen Ende-Button
                self.end1.setToolTip("Programm beenden")                                                                                                #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end1.clicked.connect(self.Hydra)


                #Checkboxen als ButtonGroup zusammenfassen
                self.cbg1 = QButtonGroup()                                                                                                              #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg1.addButton(self.cb10, 0)                                                                                                       #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbg1.addButton(self.cb11, 1)                                                                                                       #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbg1.addButton(self.cb12, 2)                                                                                                       #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbg1.addButton(self.cb13, 3)                                                                                                       #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbg1.addButton(self.cb14, 4)                                                                                                       #Fügt die vierte Checkbox zur ButtonGroup hinzu
                self.cbg1.addButton(self.cb15, 5)                                                                                                       #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbg1.addButton(self.cb16, 6)                                                                                                       #Ruft die ende1-Funktion auf, wenn der Button gedrückt wird


                #Groupboxes
                self.groupboxRes1 = QGroupBox("Windowresolution", self)
                self.vboxRes1 = QVBoxLayout(self)                                                                                                       #Setzt das Label
                self.vboxRes1.addWidget(self.cb10)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes1.addWidget(self.cb11)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes1.addWidget(self.cb12)                                                                                                      #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxRes1.addWidget(self.cb13)                                                                                                      #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxRes1.addWidget(self.cb14)
                self.vboxRes1.addWidget(self.cb15)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes1.addWidget(self.cb16)
                self.groupboxRes1.setLayout(self.vboxRes1)

                self.groupboxSendTTL1 = QGroupBox("Send TTL", self) 
                self.groupboxSendTTL1.setCheckable(True)
                self.groupboxSendTTL1.setChecked(False)
                self.vboxSendTTL1 = QVBoxLayout(self)
                self.vboxSendTTL1.addWidget(self.labelSendTTL1)
                self.vboxSendTTL1.addWidget(self.TTLroot)
                self.vboxSendTTL1.addStretch(1)
                self.vboxSendTTL1.addWidget(self.labelPointDelay)
                self.vboxSendTTL1.addWidget(self.PointDelay)
                self.vboxSendTTL1.addStretch(1)
                self.vboxSendTTL1.addWidget(self.TTLgetPoint1)
                self.vboxSendTTL1.addWidget(self.labelGetTTL1)
                self.groupboxSendTTL1.setLayout(self.vboxSendTTL1)
                                
                self.groupboxCH1 = QGroupBox("Activated Channels", self)            
                self.layoutCH11 = QHBoxLayout(self)
                self.layoutCH11.addWidget(self.cbch11)
                self.layoutCH11.addStretch(1)
                self.layoutCH11.addWidget(self.labelVal)
                self.layoutCH11.addWidget(self.textVal)
                self.layoutCH12 = QHBoxLayout(self)
                self.layoutCH12.addWidget(self.cbch12)
                self.layoutCH12.addStretch(1)
                self.layoutCH12.addWidget(self.labelVal2)
                self.layoutCH12.addWidget(self.textVal2)
                self.layoutCH13 = QHBoxLayout(self)
                self.layoutCH13.addWidget(self.cbch13)
                self.layoutCH13.addStretch(1)
                self.layoutCH13.addWidget(self.labelVal3)
                self.layoutCH13.addWidget(self.textVal3)
                self.layoutCH14 = QHBoxLayout(self)
                self.layoutCH14.addWidget(self.cbch14)
                self.layoutCH14.addStretch(1)
                self.layoutCH14.addWidget(self.labelVal4)
                self.layoutCH14.addWidget(self.textVal4)
                self.layoutCH15 = QHBoxLayout(self)
                self.layoutCH15.addWidget(self.cbch15)
                self.layoutCH15.addStretch(1)
                self.layoutCH15.addWidget(self.labelVal5)
                self.layoutCH15.addWidget(self.textVal5)
                self.layoutCH16 = QHBoxLayout(self)
                self.layoutCH16.addWidget(self.cbch16)
                self.layoutCH16.addStretch(1)
                self.layoutCH16.addWidget(self.labelVal6)
                self.layoutCH16.addWidget(self.textVal6)
                self.layoutCH17 = QHBoxLayout(self)
                self.layoutCH17.addWidget(self.cbch17)
                self.layoutCH17.addStretch(1)
                self.layoutCH17.addWidget(self.labelVal7)
                self.layoutCH17.addWidget(self.textVal7)
                self.layoutCH18 = QHBoxLayout(self)
                self.layoutCH18.addWidget(self.cbch18)
                self.layoutCH18.addStretch(1)
                self.layoutCH18.addWidget(self.labelVal8)
                self.layoutCH18.addWidget(self.textVal8)
                self.vboxCH1 = QVBoxLayout(self)
                self.vboxCH1.addLayout(self.layoutCH11)
                self.vboxCH1.addLayout(self.layoutCH12)
                self.vboxCH1.addLayout(self.layoutCH13)
                self.vboxCH1.addLayout(self.layoutCH14)
                self.vboxCH1.addLayout(self.layoutCH15)
                self.vboxCH1.addLayout(self.layoutCH16)
                self.vboxCH1.addLayout(self.layoutCH17)
                self.vboxCH1.addLayout(self.layoutCH18)
                self.groupboxCH1.setLayout(self.vboxCH1)

                self.groupboxPos = QGroupBox("Position", self)   
                self.vboxPos = QVBoxLayout(self)
                self.vboxPos.addWidget(self.labelX1)
                self.vboxPos.addWidget(self.slideX)
                self.vboxPos.addWidget(self.spinX)
                self.vboxPos.addStretch(1)
                self.vboxPos.addWidget(self.labelY1)
                self.vboxPos.addWidget(self.slideY)
                self.vboxPos.addWidget(self.spinY)
                self.groupboxPos.setLayout(self.vboxPos)


                #Layout
                self.tab1.layoutVInt = QVBoxLayout(self)
                self.tab1.layoutVInt.addWidget(self.labelIntTime1)
                self.tab1.layoutVInt.addWidget(self.spinIntTime1)
                        
                self.tab1.layoutV1 = QVBoxLayout(self)
                self.tab1.layoutV1.addWidget(self.buttonPos)
                self.tab1.layoutV1.addStretch(1)
                self.tab1.layoutV1.addWidget(self.buttonPoint)
                self.tab1.layoutV1.addStretch(1)
                self.tab1.layoutV1.addLayout(self.tab1.layoutVInt)
                self.tab1.layoutV1.addStretch(1)
                                
                self.tab1.layoutEnd = QHBoxLayout(self)                                                                                                 #Setzt ein horizontales Layout
                self.tab1.layoutEnd.addStretch(1)                                                                                                       #Setzt einen Abstandshalter ein
                self.tab1.layoutEnd.addWidget(self.end1)                                                                                                #Setzt den Ende-Button          
                
                self.tab1.layoutGrid = QGridLayout(self)
                self.tab1.layoutGrid.addWidget(self.groupboxRes1, 0, 0)
                self.tab1.layoutGrid.addWidget(self.labelStretch1Tab1, 1, 0)
                self.tab1.layoutGrid.addWidget(self.groupboxSendTTL1, 2, 0)
                self.tab1.layoutGrid.addWidget(self.groupboxPos, 0, 2)
                self.tab1.layoutGrid.addWidget(self.labelStretch2Tab1, 1, 2)
                self.tab1.layoutGrid.addWidget(self.groupboxCH1, 2, 2)
                self.tab1.layoutGrid.addLayout(self.tab1.layoutV1, 0, 4)
                self.tab1.layoutGrid.setColumnStretch(0, 1)
                self.tab1.layoutGrid.setColumnStretch(1, 1)
                self.tab1.layoutGrid.setColumnStretch(2, 8)
                self.tab1.layoutGrid.setColumnStretch(3, 1)
                self.tab1.layoutGrid.setColumnStretch(4, 1)
                self.tab1.layoutGrid.setColumnStretch(5, 1)
                
                self.tab1.layoutGes = QVBoxLayout(self)                                                                                                 #Setzt ein vertikales Layout
                self.tab1.layoutGes.addStretch(8)                                                                                                       #Setzt einen Abstandshalter
                self.tab1.layoutGes.addLayout(self.tab1.layoutGrid)                                                                                     #Fügt das horizontale Layout zum vertikalen Layout hinzu
                self.tab1.layoutGes.addStretch(21)                                                                                                      #Setzt einen Abstandshalter
                self.tab1.layoutGes.addLayout(self.tab1.layoutEnd)                                                                                      #Fügt das horizontale Layout zum vertikalen Layout hinzu
                
                self.tab1.setLayout(self.tab1.layoutGes)                                                                                                #Setzt das vertikale Layout als Tab-Layout
                
                
#---------------------------- Tab2 --------------------------
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.buttonStart = QPushButton("Start", self)                                                                                           #setzt einen Button             
                self.labelXStart = QLabel("X-Start [\u03BCm]", self)                                                                                    #setzt ein Label                
                self.slideXStart = QSlider(Qt.Horizontal)                                                                                               #setzt einen horizontalen Slider
                self.spinXStart = QDoubleSpinBox(self)                                                                                                  #setzt eine Spinbox
                self.labelXStop = QLabel("X-Stop [\u03BCm]", self)                                                                                      #setzt ein Label
                self.slideXStop = QSlider(Qt.Horizontal)                                                                                                #setzt einen horizontalen Slider
                self.spinXStop = QDoubleSpinBox(self)                                                                                                   #setzt eine Spinbox
                self.labelYStart = QLabel("Y-Start [\u03BCm]", self)                                                                                    #setzt ein Label
                self.slideYStart = QSlider(Qt.Horizontal)                                                                                               #setzt einen horizontalen Slider
                self.spinYStart = QDoubleSpinBox(self)                                                                                                  #setzt eine Spinbox
                self.labelYStop = QLabel("Y-Stop [\u03BCm]", self)                                                                                      #setzt ein Label
                self.slideYStop = QSlider(Qt.Horizontal)                                                                                                #setzt einen horizontalen Slider
                self.spinYStop = QDoubleSpinBox(self)                                                                                                   #setzt eine Spinbox
                self.delay = QSpinBox(self)                                                                                                             #setzt eine Spinbox
                self.labelDelay = QLabel("Step-Delay [ms]", self)                                                                                       #setzt ein Label
                self.labelIntTime = QLabel("Integration Time [ms]", self)
                self.spinIntTime2 = QSpinBox(self)
                self.progress1 = QProgressBar(self)
                self.Subgrid1 = QCheckBox("TTL-Sync")
                self.Slope1 = QCheckBox("Slope Compensation")
                self.Stack1 = QCheckBox("ZStack")
                self.Plot1 = QCheckBox("Plot Data")

                self.labelProgTime = QLabel("", self)                                                                                                   #Setzt ein Label 
                self.labelStretch1Tab2 = QLabel("  \n  \n  ", self)
                self.labelStretch2Tab2 = QLabel("", self) 
                self.labelStretch3Tab2 = QLabel("", self) 

                #Save - Settings
                self.nameMeasure = QLineEdit(self)                                                                                                      #Setzt eine Textbox
                self.saveMeasure = QPushButton("Save", self)                                                                                            #Setzt einen Button
                self.namesMeasure = QComboBox(self)                                                                                                     #Setzt eine Auswahlbox
                self.useMeasure = QPushButton("Use", self)                                                                                              #Setzt einen Button

                #Stack
                self.Stack1.setToolTip("Adds a multiple Layers to the Measurement")
                self.Stack1.stateChanged.connect(self.StackSelect)
                #self.Stack1.stateChanged.connect(self.NavWinCheckboxen)
                self.Stack1.setChecked(False)
                
                #Slopecompensation
                self.Slope1.setToolTip("Adds a Slope Compensation to the Measurement")   
                self.Slope1.stateChanged.connect(self.SlopeSelect)
                #self.Slope1.stateChanged.connect(self.NavWinCheckboxen)
                self.Slope1.setChecked(False)

                #Subgrid
                self.Subgrid1.setToolTip("Adds a Subgrid to the Measurement and syncronises the selected TTL Device")   
                self.Subgrid1.setChecked(False)
                self.Subgrid1.stateChanged.connect(self.NavWinCheckboxen)
                
                #Plot
                self.Plot1.setToolTip("Plots the recorded Data")        
                self.Plot1.setChecked(True)

                #Checkboxen setzen
                self.cbch21 = QCheckBox(CH1, self)                                                                                                      #Setzt eine CheckBox
                self.cbch21.setToolTip("Sets the Input to " + CH1)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch22 = QCheckBox(CH2, self)                                                                                                      #Setzt eine CheckBox
                self.cbch22.setToolTip("Sets the Input to " + CH2)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch23 = QCheckBox(CH3, self)                                                                                                      #Setzt eine CheckBox
                self.cbch23.setToolTip("Sets the Input to " + CH3)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch24 = QCheckBox(CH4, self)                                                                                                      #Setzt eine CheckBox
                self.cbch24.setToolTip("Sets the Input to " + CH4)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch25 = QCheckBox(CHA, self)                                                                                                      #Setzt eine CheckBox
                self.cbch25.setToolTip("Sets the Input to " + CHA)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch26 = QCheckBox(CHB, self)                                                                                                      #Setzt eine CheckBox
                self.cbch26.setToolTip("Sets the Input to " + CHB)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch27 = QCheckBox(L2, self)                                                                                                       #Setzt eine CheckBox
                self.cbch27.setToolTip("Sets the Input to " + L2)                                                                                       #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch28 = QCheckBox(L3, self)                                                                                                       #Setzt eine CheckBox
                self.cbch28.setToolTip("Sets the Input to " + L3)                                                                                       #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch25.setChecked(True)
                self.cbch26.setChecked(True)
                
                #Checkboxen Window setzen                                                                                                               #Setzt ein Label 
                self.cb20 = QCheckBox("64 Pixel", self)                                                                                                 #Setzt eine CheckBox
                self.cb20.setToolTip("Sets the resolution to 64 Pixel")                                                                                 #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb21 = QCheckBox("128 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb21.setToolTip("Sets the resolution to 128 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb22 = QCheckBox("256 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb22.setToolTip("Sets the resolution to 256 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb22.setChecked(True)
                self.cb23 = QCheckBox("512 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb23.setToolTip("Sets the resolution to 512 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb24 = QCheckBox("1024 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb24.setToolTip("Sets the resolution to 1024 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb25 = QCheckBox("2048 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb25.setToolTip("Sets the resolution to 2048 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb26 = QCheckBox("4096 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb26.setToolTip("Sets the resolution to 4096 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver

                #Button definieren
                self.buttonStart.setCheckable(True)                                                                                                     #Macht den Button chackbar
                self.buttonStart.setToolTip("Starts the Measurement")                                                                                   #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonStart.clicked[bool].connect(self.StartMeasurement)

                #Settings
                self.saveMeasure.setToolTip("Saves the Settings")                                                                                       #Setzt eine Buttenbeschreibung bei MouseOver
                self.saveMeasure.clicked.connect(self.savesettingsScanMeasure)                                                                          #Ruft die savesettings-Funktion auf
                self.namesMeasure.setToolTip("Old Settings")
                MeasureSet.execute("SELECT name FROM settingsScanMeasure")
                for dsatzMeasure in MeasureSet:
                        x = dsatzMeasure[0]
                        #print(str(x))
                        self.namesMeasure.addItem(x)
                self.useMeasure.setToolTip("Uses the Settings")
                self.useMeasure.clicked.connect(self.usesettingsScanMeasure)
                
                
                #Slider definieren
                self.slideXStart.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.slideXStart.setMaximum(int(round(255*((FullRangeDeviceX)/255),0)))                                                                 #Setzt ein Maximum für die Auswahl
                self.slideXStart.setValue(0)                                                                                                            #Setzt einen Startwert
                self.slideXStart.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.slideXStart.setTickInterval(256)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStart.valueChanged.connect(self.slideXstart)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideXStart.setToolTip("Sets the X-Startposition")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideYStart.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.slideYStart.setMaximum(int(round(255*((FullRangeDeviceX)/255),0)))                                                                 #Setzt ein Maximum für die Auswahl
                self.slideYStart.setValue(0)                                                                                                            #Setzt einen Startwert
                self.slideYStart.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.slideYStart.setTickInterval(256)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStart.valueChanged.connect(self.slideYstart)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideYStart.setToolTip("Sets the Y-Startposition")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideXStop.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.slideXStop.setMaximum(int(round(255*((FullRangeDeviceX)/255),0)))                                                                  #Setzt ein Maximum für die Auswahl
                self.slideXStop.setValue(int(round(255*((FullRangeDeviceX)/255),0)))                                                                    #Setzt einen Startwert
                self.slideXStop.setTickPosition(QSlider.TicksBelow)                                                                                     #Setzt Rastpunkte unter dem Slider
                self.slideXStop.setTickInterval(256)                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStop.valueChanged.connect(self.slideXstop)                                                                                   #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideXStop.setToolTip("Sets the X-Stopposition")                                                                                   #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideYStop.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.slideYStop.setMaximum(int(round(255*((FullRangeDeviceX)/255),0)))                                                                  #Setzt ein Maximum für die Auswahl
                self.slideYStop.setValue(int(round(255*((FullRangeDeviceX)/255),0)))                                                                    #Setzt einen Startwert
                self.slideYStop.setTickPosition(QSlider.TicksBelow)                                                                                     #Setzt Rastpunkte unter dem Slider
                self.slideYStop.setTickInterval(256)                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStop.valueChanged.connect(self.slideYstop)                                                                                   #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideYStop.setToolTip("Sets the Y-Stopposition")                                                                                   #Setzt eine Buttonbeschreibung bei MouseOver

                #Spinbox definieren
                self.spinXStart.setMinimum(round(0*((FullRangeDeviceY/1000)/255),3))                                                                    #Setzt ein Minimalwert für die Auswahl
                self.spinXStart.setMaximum(round(255*((FullRangeDeviceX/1000)/255),3))                                                                  #Setzt ein Maximum für die Auswahl
                self.spinXStart.setValue(round(0*((FullRangeDeviceX/1000)/255),3))                                                                      #Setzt einen Startwert
                self.spinXStart.valueChanged.connect(self.spinXstart)                                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStart.setSingleStep(round(((FullRangeDeviceX/1000)/255),3))                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStart.setDecimals(3)
                self.spinXStart.setToolTip("Sets the X-Startposition")                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinYStart.setMinimum(round(0*((FullRangeDeviceY/1000)/255),3))                                                                    #Setzt ein Minimalwert für die Auswahl
                self.spinYStart.setMaximum(round(255*((FullRangeDeviceY/1000)/255),3))                                                                  #Setzt ein Maximum für die Auswahl
                self.spinYStart.setValue(round(0*((FullRangeDeviceY/1000)/255),3))                                                                      #Setzt einen Startwert
                self.spinYStart.valueChanged.connect(self.spinYstart)                                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStart.setSingleStep(round(((FullRangeDeviceY/1000)/255),3))                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStart.setDecimals(3)
                self.spinYStart.setToolTip("Sets the Y-Startposition")                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinXStop.setMinimum(round(0*((FullRangeDeviceX/1000)/255),3))                                                                     #Setzt ein Minimalwert für die Auswahl
                self.spinXStop.setMaximum(round(255*((FullRangeDeviceX/1000)/255),3))                                                                   #Setzt ein Maximum für die Auswahl
                self.spinXStop.setValue(round(255*((FullRangeDeviceX/1000)/255),3))                                                                     #Setzt einen Startwert
                self.spinXStop.valueChanged.connect(self.spinXstop)                                                                                     #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStop.setSingleStep(round(((FullRangeDeviceX/1000)/255),3))                                                                    #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStop.setDecimals(3)
                self.spinXStop.setToolTip("Sets the X-Stopposition")                                                                                    #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinYStop.setMinimum(round(0 * ((FullRangeDeviceY/1000)/255),3))                                                                   #Setzt ein Minimalwert für die Auswahl
                self.spinYStop.setMaximum(round(255 * ((FullRangeDeviceY/1000)/255),3))                                                                 #Setzt ein Maximum für die Auswahl
                self.spinYStop.setValue(round(255 * ((FullRangeDeviceY/1000)/255),3))                                                                   #Setzt einen Startwert
                self.spinYStop.valueChanged.connect(self.spinYstop)                                                                                     #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStop.setSingleStep(round(((FullRangeDeviceY/1000)/255),3))                                                                    #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStop.setDecimals(3)
                self.spinYStop.setToolTip("Sets the Y-Stopposition")                                                                                    #Setzt eine Buttonbeschreibung bei MouseOver

                self.delay.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.delay.setMaximum(100)                                                                                                              #Setzt ein Maximum für die Auswahl
                self.delay.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.delay.setToolTip("Sets the Steptime in Milliseconds")                                                                              #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinIntTime2.setMinimum(1)
                self.spinIntTime2.setMaximum(20)
                self.spinIntTime2.setValue(1)
                self.spinIntTime2.setToolTip("Set the Integrationtime of the Logic-Channels in Milliseconds")
                self.spinIntTime2.valueChanged.connect(self.NavWinIntTime)

                #Label definieren
                XDistance = (PiezoDistanceX * (DeviceVoltage/PiezoVoltage))
                YDistance = (PiezoDistanceY * (DeviceVoltage/PiezoVoltage))
                pixelsizeX = round(XDistance/256, 2)
                pixelsizeY = round(YDistance/256, 2)
                XDist = round(100, 3)
                YDist = round(100, 3)
                NormalTime = 532.1455
                TimeMins = NormalTime // 60
                TimeSecs1 = NormalTime % 60
                TimeSecs = TimeSecs1 // 1
                TimeMilsecs = round(((TimeSecs1 % 1) * 1000), 2)
                self.labelProgTime.setText("Expected Time:\t" + str(int(TimeMins)) + " min  \t" + str(int(TimeSecs)) + " s\t" + str(int(TimeMilsecs)) + " ms\nPixelsize:\t\t" + str(pixelsizeX) + " x " + str(pixelsizeY) + " nm" + " s\nWindowsize:\t" + str(XDist) + " x " + str(YDist) + " [\u03BCm]")                                                                  #Setzt ein Label 

                #Checkboxen als ButtonGroup zusammenfassen
                self.cbg2 = QButtonGroup()                                                                                                              #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg2.addButton(self.cb20, 0)                                                                                                       #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg2.addButton(self.cb21, 1)                                                                                                       #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb22, 2)                                                                                                       #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb23, 3)                                                                                                       #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb24, 4)                                                                                                       #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb25, 5)                                                                                                       #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb26, 6)                                                                                                       #Fügt die vierte Checkbox zur ButtonGroup hinzu
                
                #Voreinstellungen Änderung                                                                                                              #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn der Amplifier umgestellt wird
                self.cbg2.buttonClicked.connect(self.stopAll2)                                                                                          #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn der Amplifier umgestellt wird
                #self.slideXStart.valueChanged.connect(self.stopAll2)                                                                                   #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinXStart.valueChanged.connect(self.stopAll2)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideYStart.valueChanged.connect(self.stopAll2)                                                                                   #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinYStart.valueChanged.connect(self.stopAll2)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideXStop.valueChanged.connect(self.stopAll2)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinXStop.valueChanged.connect(self.stopAll2)                                                                                     #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideYStop.valueChanged.connect(self.stopAll2)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinYStop.valueChanged.connect(self.stopAll2)                                                                                     #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                self.Plot1.stateChanged.connect(self.stopAll2)
                
                self.delay.valueChanged.connect(self.updateProgTime)
                self.spinIntTime2.valueChanged.connect(self.updateProgTime)
                self.Plot1.stateChanged.connect(self.updateProgTime)
                self.Subgrid1.stateChanged.connect(self.updateProgTime)
                self.Stack1.stateChanged.connect(self.updateProgTime)
                self.cbch21.stateChanged.connect(self.updateProgTime)
                self.cbch22.stateChanged.connect(self.updateProgTime)
                self.cbch23.stateChanged.connect(self.updateProgTime)
                self.cbch24.stateChanged.connect(self.updateProgTime)
                self.cbch25.stateChanged.connect(self.updateProgTime)
                self.cbch26.stateChanged.connect(self.updateProgTime)
                self.cbch27.stateChanged.connect(self.updateProgTime)
                self.cbch28.stateChanged.connect(self.updateProgTime)
                self.cbg2.buttonClicked.connect(self.updateProgTime) 
                
                #Ende
                self.end2 = QPushButton("Exit", self)                                                                                                   #setzt einen Ende-Button
                self.end2.setToolTip("Programm beenden")                                                                                                #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end2.clicked.connect(self.Hydra)                                                                                                   #Ruft die end2-Funktion auf, wenn der Button gedrückt wird

                #Buttongroups
                self.groupboxRes2 = QGroupBox("Windowresolution", self)
                self.vboxRes2 = QVBoxLayout(self)                                                                                                       #Setzt das Label
                self.vboxRes2.addWidget(self.cb20)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes2.addWidget(self.cb21)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes2.addWidget(self.cb22)                                                                                                      #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxRes2.addWidget(self.cb23)                                                                                                      #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxRes2.addWidget(self.cb24)
                self.vboxRes2.addWidget(self.cb25)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes2.addWidget(self.cb26)
                self.groupboxRes2.setLayout(self.vboxRes2)

                self.groupboxCH2 = QGroupBox("Activated Channel", self)
                self.vboxCH2 = QVBoxLayout(self)                                                                                                        #Fügt das Label ein
                self.vboxCH2.addWidget(self.cbch21)                                                                                                     #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxCH2.addWidget(self.cbch22)                                                                                                     #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxCH2.addWidget(self.cbch23)                                                                                                     #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxCH2.addWidget(self.cbch24)                                                                                                     #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxCH2.addWidget(self.cbch25)                                                                                                     #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxCH2.addWidget(self.cbch26)
                self.vboxCH2.addWidget(self.cbch27)
                self.vboxCH2.addWidget(self.cbch28)
                self.groupboxCH2.setLayout(self.vboxCH2)

                self.groupboxMesWin = QGroupBox("Measurement Window", self)  
                self.layoutXStart = QVBoxLayout(self)                                                                                                   #Setzt ein vetikales Layout
                self.layoutXStart.addWidget(self.labelXStart)                                                                                           #Fügt das Label ein
                self.layoutXStart.addWidget(self.slideXStart)                                                                                           #Fügt den Slider hinzu
                self.layoutXStart.addWidget(self.spinXStart)                                                                                            #Fügt die Zahlauswahlbox hinzu
                
                self.layoutYStart = QVBoxLayout(self)                                                                                                   #Setzt ein vetikales Layout
                self.layoutYStart.addWidget(self.labelYStart)                                                                                           #Fügt das Label ein
                self.layoutYStart.addWidget(self.slideYStart)                                                                                           #Fügt den Slider hinzu
                self.layoutYStart.addWidget(self.spinYStart)                                                                                            #Fügt die Zahlauswahlbox hinzu
                        
                self.layoutStart = QHBoxLayout(self)                                                                                                    #Setzt ein horizontales Layout
                self.layoutStart.addLayout(self.layoutXStart)                                                                                           #Fügt ein Layout hinzu
                self.layoutStart.addLayout(self.layoutYStart)                                                                                           #Fügt ein Layout hinzu
                
                self.layoutXStop = QVBoxLayout(self)                                                                                                    #Setzt ein vetikales Layout
                self.layoutXStop.addWidget(self.labelXStop)                                                                                             #Fügt das Label ein
                self.layoutXStop.addWidget(self.slideXStop)                                                                                             #Fügt den Slider hinzu
                self.layoutXStop.addWidget(self.spinXStop)                                                                                              #Fügt die Zahlauswahlbox hinzu
                
                self.layoutYStop = QVBoxLayout(self)                                                                                                    #Setzt ein vetikales Layout
                self.layoutYStop.addWidget(self.labelYStop)                                                                                             #Fügt das Label ein
                self.layoutYStop.addWidget(self.slideYStop)                                                                                             #Fügt den Slider hinzu
                self.layoutYStop.addWidget(self.spinYStop)                                                                                              #Fügt die Zahlauswahlbox hinzu
                        
                self.layoutStop = QHBoxLayout(self)                                                                                                     #Setzt ein horizontales Layout
                self.layoutStop.addLayout(self.layoutXStop)                                                                                             #Fügt ein Layout hinzu
                self.layoutStop.addLayout(self.layoutYStop) 

                self.vboxMesWin = QVBoxLayout(self)                                                                                                     #Setzt einen Abstandshalter
                self.vboxMesWin.addLayout(self.layoutStart)                                                                                             #Fügt das Range1-Layout zum vertikalen Layout hinzu
                self.vboxMesWin.addStretch(1)                                                                                                           #Setzt einen Abstandshalter
                self.vboxMesWin.addLayout(self.layoutStop)
                self.groupboxMesWin.setLayout(self.vboxMesWin)

                self.groupboxMesSet = QGroupBox("Measurement Settings", self)
                self.layoutCBs = QHBoxLayout(self)
                self.layoutCBs.addWidget(self.Slope1)
                self.layoutCBs.addStretch(1)
                self.layoutCBs.addWidget(self.Subgrid1)    
                self.layoutCBs.addStretch(1)       
                self.layoutCBs.addWidget(self.Stack1)                                                                                                   #Setzt das Widget   
                self.layoutCBs.addStretch(1)       
                self.layoutCBs.addWidget(self.Plot1)

                self.layoutDelay = QHBoxLayout(self)                                                                                                    #Setzt ein horizontales Layout
                self.layoutDelay.addWidget(self.delay)                                                                                                  #Fügt ein Layout hinzu
                self.layoutDelay.addWidget(self.labelDelay)
                self.layoutDelay.addWidget(self.spinIntTime2)
                self.layoutDelay.addWidget(self.labelIntTime)
                
                self.vboxMesSet = QVBoxLayout(self)                                                                                                     #Setzt einen Abstandshalter
                self.vboxMesSet.addLayout(self.layoutCBs)
                self.vboxMesSet.addStretch(1)
                self.vboxMesSet.addLayout(self.layoutDelay)
                self.groupboxMesSet.setLayout(self.vboxMesSet)

                self.groupboxSave2 = QGroupBox("Save Settings", self)
                self.vboxSave2 = QVBoxLayout(self)                                                                                                      #Fügt das Label ein
                self.vboxSave2.addWidget(self.nameMeasure)                                                                                              #Setzt das Widget
                self.vboxSave2.addWidget(self.saveMeasure)                                                                                              #Setzt das Widget
                self.vboxSave2.addWidget(self.namesMeasure)                                                                                             #Setzt das Widget
                self.vboxSave2.addWidget(self.useMeasure) 
                self.groupboxSave2.setLayout(self.vboxSave2)
                
                #Layouts                
                self.tab2.layoutV1 = QVBoxLayout(self)                                                                                                  #Setzt einen Abstandshalter
                self.tab2.layoutV1.addWidget(self.groupboxMesSet)                                                                                       #Fügt das Range2-Layout zum vertikalen Layout hinzu             
                self.tab2.layoutV1.addWidget(self.labelStretch1Tab2)
                self.tab2.layoutV1.addWidget(self.progress1)
                self.tab2.layoutV1.addWidget(self.labelProgTime)                                                                                        #Setzt einen Abstandshalter                     

                self.tab2.layoutButton = QVBoxLayout(self)
                self.tab2.layoutButton.addWidget(self.buttonStart)
                self.tab2.layoutButton.addStretch(1)

                self.tab2.layoutEnd = QHBoxLayout(self)                                                                                                 #Setzt ein horizontales Layout
                self.tab2.layoutEnd.addStretch(1)                                                                                                       #Setzt einen Abstandshalter ein
                self.tab2.layoutEnd.addWidget(self.end2)                                                                                                #Setzt den Ende-Button          
                
                self.tab2.layoutGrid = QGridLayout(self)
                self.tab2.layoutGrid.addWidget(self.groupboxRes2, 0, 0)
                self.tab2.layoutGrid.addWidget(self.labelStretch2Tab2, 1, 0)
                self.tab2.layoutGrid.addWidget(self.groupboxCH2, 2, 0)
                self.tab2.layoutGrid.addWidget(self.groupboxMesWin, 0, 2)
                self.tab2.layoutGrid.addWidget(self.labelStretch3Tab2, 1, 0)
                self.tab2.layoutGrid.addLayout(self.tab2.layoutV1, 2, 2)                
                self.tab2.layoutGrid.addLayout(self.tab2.layoutButton, 0, 4)
                self.tab2.layoutGrid.addWidget(self.groupboxSave2, 0, 6)
                self.tab2.layoutGrid.setColumnStretch(0, 1)
                self.tab2.layoutGrid.setColumnStretch(1, 1)
                self.tab2.layoutGrid.setColumnStretch(2, 7)
                self.tab2.layoutGrid.setColumnStretch(3, 1)
                self.tab2.layoutGrid.setColumnStretch(4, 1)
                self.tab2.layoutGrid.setColumnStretch(5, 1)
                self.tab2.layoutGrid.setColumnStretch(6, 1)
                
                self.tab2.layoutv = QVBoxLayout(self)                                                                                                   #Setzt ein vertikales Layout
                self.tab2.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab2.layoutv.addLayout(self.tab2.layoutGrid)                                                                                       #Fügt das erste horizontale Layout zum vertikalen Layout hinzu
                self.tab2.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab2.layoutv.addLayout(self.tab2.layoutEnd)                                                                                        #Fügt das Ende-Layout zum vertikalen Layout hinzu
                
                self.tab2.setLayout(self.tab2.layoutv)                                                                                                  #Setzt das vertikale Layout als Tab-Layout

#-------------- Tab 3 -----------------------------------
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.labelXStart2 = QLabel("X-Start [nm]", self)                                                                                        #setzt ein Label                
                self.slideXStart2 = QSlider(Qt.Horizontal)                                                                                              #setzt einen horizontalen Slider
                self.spinXStart2 = QDoubleSpinBox(self)                                                                                                 #setzt eine Spinbox
                self.labelXStop2 = QLabel("X-Stop [nm]", self)                                                                                          #setzt ein Label
                self.slideXStop2 = QSlider(Qt.Horizontal)                                                                                               #setzt einen horizontalen Slider
                self.spinXStop2 = QDoubleSpinBox(self)                                                                                                  #setzt eine Spinbox
                self.labelYStart2 = QLabel("Y-Start [nm]", self)                                                                                        #setzt ein Label
                self.slideYStart2 = QSlider(Qt.Horizontal)                                                                                              #setzt einen horizontalen Slider
                self.spinYStart2 = QDoubleSpinBox(self)                                                                                                 #setzt eine Spinbox
                self.labelYStop2 = QLabel("Y-Stop [nm]", self)                                                                                          #setzt ein Label
                self.slideYStop2 = QSlider(Qt.Horizontal)                                                                                               #setzt einen horizontalen Slider
                self.spinYStop2 = QDoubleSpinBox(self)                                                                                                  #setzt eine Spinbox
                self.labelXStep = QLabel("X-Steps [nm]", self)                                                                                          #setzt ein Label
                self.slideXStep = QSlider(Qt.Horizontal)                                                                                                #setzt einen horizontalen Slider
                self.spinXStep = QDoubleSpinBox(self)                                                                                                   #setzt eine Spinbox
                self.labelYStep = QLabel("Y-Steps [nm]", self)                                                                                          #setzt ein Label
                self.slideYStep = QSlider(Qt.Horizontal)                                                                                                #setzt einen horizontalen Slider
                self.spinYStep = QDoubleSpinBox(self)                                                                                                   #setzt eine Spinbox
                self.labelStepTime = QLabel("Delay [s]", self)                                                                                          #setzt ein Label
                self.spinStepTime = QDoubleSpinBox(self)                                                                                                #setzt eine Spinbox                                                                  #setzt eine Spinbox
                self.TTLroot2 = QComboBox(self)                                                                                                         #Setzt eine CheckBox
                self.TTLgetPoint2 = QCheckBox("Wait for TTL", self)                                                                                     #Setzt eine CheckBox
                self.channeltimeing = QCheckBox("Use Channel", self)
                self.labelPoints = QLabel("Number of Subgridpoints: 65536.0", self)            
                self.labelSendTTL3 = QLabel("Send TTL Signal\nto Device", self)  
                self.labelGetTTL3 = QLabel("Wait for TTL\nDevice to answer", self)          
                self.labelStretch1Tab3 = QLabel("", self)
                self.labelStretch2Tab3 = QLabel("", self)
                self.spinCount = QSpinBox(self)
                self.LabelSpinCount = QLabel("Number of Points", self)

                #TTL
                self.TTLroot2.addItem(NameTTL1)
                self.TTLroot2.addItem(NameTTL2)

                #Save - Settings
                self.nameSync = QLineEdit(self)                                                                                                         #Setzt eine Textbox
                self.saveSync = QPushButton("Save", self)                                                                                               #Setzt einen Button
                self.namesSync = QComboBox(self)                                                                                                        #Setzt eine Auswahlbox
                self.useSync = QPushButton("Use", self)                                                                                                 #Setzt einen Button
                
                #Checkboxen setzen
                self.cb30 = QCheckBox("64 Pixel", self)                                                                                                 #Setzt eine CheckBox
                self.cb30.setToolTip("Sets the resolution to 128 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb31 = QCheckBox("128 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb31.setToolTip("Sets the resolution to 128 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb32 = QCheckBox("256 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb32.setToolTip("Sets the resolution to 256 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb32.setChecked(True)
                self.cb33 = QCheckBox("512 Pixel", self)                                                                                                #Setzt eine CheckBox
                self.cb33.setToolTip("Sets the resolution to 512 Pixel")                                                                                #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb34 = QCheckBox("1024 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb34.setToolTip("Sets the resolution to 1024 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb35 = QCheckBox("2048 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb35.setToolTip("Sets the resolution to 2048 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cb36 = QCheckBox("4096 Pixel", self)                                                                                               #Setzt eine CheckBox
                self.cb36.setToolTip("Sets the resolution to 4096 Pixel")                                                                               #Setzt eine CheckBox-Beschreibung bei MouseOver

                self.TTLgetPoint2.setToolTip("Waits for the Measurementdevice to send a TTL-Signal")                                                    #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.channeltimeing.setToolTip("Measure Channel while waiting at the Subgridpoints")

                #Settings
                self.saveSync.setToolTip("Saves the Settings")                                                                                          #Setzt eine Buttenbeschreibung bei MouseOver
                self.saveSync.clicked.connect(self.savesettingsScanSync)                                                                                #Ruft die savesettings-Funktion auf
                self.namesSync.setToolTip("Old Settings")
                SyncSet.execute("SELECT name FROM settingsScanSync")
                for dsatzSync in SyncSet:
                        x = dsatzSync[0]
                        #print(str(x))
                        self.namesSync.addItem(x)
                self.useSync.setToolTip("Uses the Settings")
                self.useSync.clicked.connect(self.usesettingsScanSync)
                
                
                #Slider definieren
                self.slideXStart2.setMinimum(0)                                                                                                         #Setzt ein Minimalwert für die Auswahl
                self.slideXStart2.setMaximum(255)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.slideXStart2.setValue(0)                                                                                                           #Setzt einen Startwert
                self.slideXStart2.setTickPosition(QSlider.TicksBelow)                                                                                   #Setzt Rastpunkte unter dem Slider
                self.slideXStart2.setTickInterval(256)                                                                                                  #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStart2.valueChanged.connect(self.slideXstart2)                                                                               #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideXStart2.setToolTip("Sets the X-Startposition")                                                                                #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideYStart2.setMinimum(0)                                                                                                         #Setzt ein Minimalwert für die Auswahl
                self.slideYStart2.setMaximum(255)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.slideYStart2.setValue(0)                                                                                                           #Setzt einen Startwert
                self.slideYStart2.setTickPosition(QSlider.TicksBelow)                                                                                   #Setzt Rastpunkte unter dem Slider
                self.slideYStart2.setTickInterval(256)                                                                                                  #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStart2.valueChanged.connect(self.slideYstart2)                                                                               #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideYStart2.setToolTip("Sets the Y-Startposition")                                                                                #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideXStop2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.slideXStop2.setMaximum(255)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.slideXStop2.setValue(255)                                                                                                          #Setzt einen Startwert
                self.slideXStop2.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.slideXStop2.setTickInterval(256)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStop2.valueChanged.connect(self.slideXstop2)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideXStop2.setToolTip("Sets the X-Stopposition")                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideYStop2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.slideYStop2.setMaximum(255)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.slideYStop2.setValue(255)                                                                                                          #Setzt einen Startwert
                self.slideYStop2.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.slideYStop2.setTickInterval(256)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStop2.valueChanged.connect(self.slideYstop2)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideYStop2.setToolTip("Sets the Y-Stopposition")                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideYStep.setMinimum(1)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.slideYStep.setMaximum(255)                                                                                                         #Setzt ein Maximum für die Auswahl
                self.slideYStep.setValue(1)                                                                                                             #Setzt einen Startwert
                self.slideYStep.setTickPosition(QSlider.TicksBelow)                                                                                     #Setzt Rastpunkte unter dem Slider
                self.slideYStep.setTickInterval(256)                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStep.valueChanged.connect(self.slideYstep)                                                                                   #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideYStep.setToolTip("Sets the Y-Steps")                                                                                          #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideXStep.setMinimum(1)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.slideXStep.setMaximum(255)                                                                                                         #Setzt ein Maximum für die Auswahl
                self.slideXStep.setValue(1)                                                                                                             #Setzt einen Startwert
                self.slideXStep.setTickPosition(QSlider.TicksBelow)                                                                                     #Setzt Rastpunkte unter dem Slider
                self.slideXStep.setTickInterval(256)                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStep.valueChanged.connect(self.slideXstep)                                                                                   #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideXStep.setToolTip("Sets the X-Steps")                                                                                          #Setzt eine Buttonbeschreibung bei MouseOver
                                
                #Spinbox definieren
                self.spinXStart2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.spinXStart2.setMaximum(FullRangeDeviceX/1000)                                                                                      #Setzt ein Maximum für die Auswahl
                self.spinXStart2.setValue(0)                                                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStart2.setSingleStep(round(((FullRangeDeviceX/1000)/255),3))                                                                  #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStart2.setDecimals(3)                                                                                                         #Setzt einen Startwert
                self.spinXStart2.valueChanged.connect(self.spinXstart2)                                                                                 #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStart2.setToolTip("Sets the X-Startposition")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinYStart2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.spinYStart2.setMaximum(FullRangeDeviceY/1000)                                                                                      #Setzt ein Maximum für die Auswahl
                self.spinYStart2.setValue(0)                                                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStart2.setSingleStep(round(((FullRangeDeviceY/1000)/255),3))                                                                  #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStart2.setDecimals(3)                                                                                                         #Setzt einen Startwert
                self.spinYStart2.valueChanged.connect(self.spinYstart2)                                                                                 #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStart2.setToolTip("Sets the Y-Startposition")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinXStop2.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.spinXStop2.setMaximum(FullRangeDeviceX/1000)                                                                                       #Setzt ein Maximum für die Auswahl
                self.spinXStop2.setValue(FullRangeDeviceX/1000)                                                                                         #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStop2.setSingleStep(round(((FullRangeDeviceX/1000)/255),3))                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStop2.setDecimals(3)                                                                                                          #Setzt einen Startwert
                self.spinXStop2.valueChanged.connect(self.spinXstop2)                                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStop2.setToolTip("Sets the X-Stopposition")                                                                                   #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinYStop2.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.spinYStop2.setMaximum(FullRangeDeviceY/1000)                                                                                       #Setzt ein Maximum für die Auswahl
                self.spinYStop2.setValue(FullRangeDeviceY/1000)                                                                                         #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStop2.setSingleStep(round(((FullRangeDeviceY/1000)/255),3))                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStop2.setDecimals(3)                                                                                                          #Setzt einen Startwert
                self.spinYStop2.valueChanged.connect(self.spinYstop2)                                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStop2.setToolTip("Sets the Y-Stopposition")                                                                                   #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinXStep.setMinimum(0)                                                                                                            #Setzt ein Minimalwert für die Auswahl
                self.spinXStep.setMaximum(FullRangeDeviceX/1000)                                                                                        #Setzt ein Maximum für die Auswahl
                self.spinXStep.setValue(round(((FullRangeDeviceX/1000)/255),3))                                                                         #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStep.setSingleStep(round(((FullRangeDeviceX/1000)/255),3))                                                                    #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStep.setDecimals(3)                                                                                                           #Setzt einen Startwert
                self.spinXStep.valueChanged.connect(self.spinXstep)                                                                                     #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXStep.setToolTip("Sets the X-Steps")                                                                                           #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinYStep.setMinimum(0)                                                                                                            #Setzt ein Minimalwert für die Auswahl
                self.spinYStep.setMaximum(FullRangeDeviceY/1000)                                                                                        #Setzt ein Maximum für die Auswahl
                self.spinYStep.setValue(round(((FullRangeDeviceY/1000)/255),3))                                                                         #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStep.setSingleStep(round(((FullRangeDeviceY/1000)/255),3))                                                                    #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStep.setDecimals(3)                                                                                                           #Setzt einen Startwert
                self.spinYStep.valueChanged.connect(self.spinYstep)                                                                                     #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYStep.setToolTip("Sets the Y-Steps")                                                                                           #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinStepTime.setMinimum(0.000)                                                                                                     #Setzt ein Minimalwert für die Auswahl
                self.spinStepTime.setMaximum(60.000)                                                                                                    #Setzt ein Maximum für die Auswahl
                self.spinStepTime.setValue(1.000)                                                                                                       #Setzt einen Startwert
                self.spinStepTime.setSingleStep(0.001)
                self.spinStepTime.setDecimals(3)
                self.spinStepTime.valueChanged.connect(self.spinsteptime)                                                                               #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinStepTime.setToolTip("Sets the Steptime in Seconds")                                                                            #Setzt eine Buttonbeschreibung bei MouseOver
                                
                #Checkboxen als ButtonGroup zusammenfassen
                self.cbg3 = QButtonGroup()                                                                                                              #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg3.addButton(self.cb30, 0)                                                                                                       #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg3.addButton(self.cb31, 1)                                                                                                       #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbg3.addButton(self.cb32, 2)                                                                                                       #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbg3.addButton(self.cb33, 3)                                                                                                       #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbg3.addButton(self.cb34, 4)                                                                                                       #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg3.addButton(self.cb35, 5)                                                                                                       #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg3.addButton(self.cb36, 6)                                                                                                       #Fügt die vierte Checkbox zur ButtonGroup hinzu
                
                #Voreinstellungen Änderung
                self.TTLgetPoint2.stateChanged.connect(self.updateProgTime)
                self.channeltimeing.stateChanged.connect(self.updateProgTime)
                self.cbg3.buttonClicked.connect(self.updateProgTime)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn der Amplifier umgestellt wird

                self.cbg3.buttonClicked.connect(self.stopAll3)                                                                                          #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn der Amplifier umgestellt wird
                #self.slideXStart2.valueChanged.connect(self.stopAll3)                                                                                  #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinXStart2.valueChanged.connect(self.stopAll3)                                                                                   #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideYStart2.valueChanged.connect(self.stopAll3)                                                                                  #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinYStart2.valueChanged.connect(self.stopAll3)                                                                                   #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideXStop2.valueChanged.connect(self.stopAll3)                                                                                   #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinXStop2.valueChanged.connect(self.stopAll3)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideYStop2.valueChanged.connect(self.stopAll3)                                                                                   #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinYStop2.valueChanged.connect(self.stopAll3)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideXStep.valueChanged.connect(self.stopAll3)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinXStep.valueChanged.connect(self.stopAll3)                                                                                     #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.slideYStep.valueChanged.connect(self.stopAll3)                                                                                    #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                #self.spinYStep.valueChanged.connect(self.stopAll3)                                                                                     #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
                
                #Ende
                self.end3 = QPushButton("Exit", self)                                                                                                   #setzt einen Ende-Button
                self.end3.setToolTip("Programm beenden")                                                                                                #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end3.clicked.connect(self.Hydra)                                                                                                   #Ruft die end2-Funktion auf, wenn der Button gedrückt wird

                #Groupboxes
                self.groupboxRes3 = QGroupBox("Windowresolution", self)
                self.vboxRes3 = QVBoxLayout(self)                                                                                                       #Setzt das Label
                self.vboxRes3.addWidget(self.cb30)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes3.addWidget(self.cb31)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes3.addWidget(self.cb32)                                                                                                      #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxRes3.addWidget(self.cb33)                                                                                                      #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxRes3.addWidget(self.cb34)
                self.vboxRes3.addWidget(self.cb35)                                                                                                      #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxRes3.addWidget(self.cb36)
                self.groupboxRes3.setLayout(self.vboxRes3)

                self.groupboxSendTTL3 = QGroupBox("Send TTL", self) 
                self.groupboxSendTTL3.setCheckable(True)
                self.groupboxSendTTL3.setChecked(False)
                self.groupboxSendTTL3.setToolTip("Sends a TTL-Signal when a point is reached")                                                          #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.groupboxSendTTL3.toggled.connect(self.updateProgTime)
                self.vboxSendTTL3 = QVBoxLayout(self)
                self.vboxSendTTL3.addWidget(self.labelSendTTL3)
                self.vboxSendTTL3.addWidget(self.TTLroot2)
                self.vboxSendTTL3.addStretch(1)
                self.vboxSendTTL3.addWidget(self.channeltimeing)
                self.vboxSendTTL3.addWidget(self.labelStepTime)                                                                                         #Fügt das Label ein
                self.vboxSendTTL3.addWidget(self.spinStepTime)
                self.vboxSendTTL3.addStretch(1)
                self.vboxSendTTL3.addWidget(self.TTLgetPoint2)
                self.vboxSendTTL3.addWidget(self.labelGetTTL3)
                self.groupboxSendTTL3.setLayout(self.vboxSendTTL3)

                self.groupboxSave3 = QGroupBox("Save Settings", self) 
                self.vboxSave3 = QVBoxLayout(self)                                                                                                      #Setzt ein vertikales Layout
                self.vboxSave3.addWidget(self.nameSync)                                                                                                 #Setzt das Widget
                self.vboxSave3.addWidget(self.saveSync)                                                                                                 #Setzt das Widget
                self.vboxSave3.addWidget(self.namesSync)                                                                                                #Setzt das Widget
                self.vboxSave3.addWidget(self.useSync)                                                                                                  #Setzt das Widget
                #self.vboxSave3.addStretch(1)
                self.groupboxSave3.setLayout(self.vboxSave3)


                self.groupboxSteps = QGroupBox("Measurement Settings", self) 
                self.groupboxManuel = QGroupBox("Manuel Grid", self)
                self.groupboxManuel.setCheckable(True)
                self.groupboxManuel.setChecked(True)
                #self.groupboxManuel.setFlat(True)
                #self.groupboxManuel.toggled.connect(self.updateProgTime)

                self.layoutXStep = QVBoxLayout(self)                                                                                                    #Setzt einen Abstandshalter
                self.layoutXStep.addWidget(self.labelXStep)                                                                                             #Fügt das Label ein
                self.layoutXStep.addWidget(self.slideXStep)                                                                                             #Fügt den Slider hinzu
                self.layoutXStep.addWidget(self.spinXStep)                                                                                              #Setzt ein vetikales Layout
                self.layoutXStep.addStretch(2)                                                                                                          #Fügt die Zahlauswahlbox hinzu
                
                self.layoutYStep = QVBoxLayout(self)                                                                                                    #Setzt einen Abstandshalter
                self.layoutYStep.addWidget(self.labelYStep)                                                                                             #Fügt das Label ein
                self.layoutYStep.addWidget(self.slideYStep)                                                                                             #Fügt den Slider hinzu
                self.layoutYStep.addWidget(self.spinYStep)                                                                                              #Setzt ein vetikales Layout
                self.layoutYStep.addStretch(2)                                                                                                          #Fügt die Zahlauswahlbox hinzu
                        
                self.layoutStepH = QHBoxLayout(self)                                                                                                    #Setzt ein horizontales Layout
                self.layoutStepH.addLayout(self.layoutXStep)                                                                                            #Fügt ein Layout hinzu
                self.layoutStepH.addLayout(self.layoutYStep)                                                                                            #Fügt ein Layout hinzu

                self.groupboxManuel.setLayout(self.layoutStepH)

                self.groupboxAuto = QGroupBox("Auto Grid", self)
                self.groupboxAuto.setCheckable(True)
                self.groupboxAuto.setChecked(False)
                #self.groupboxAuto.toggled.connect(self.updateProgTime)
                self.layoutCount = QHBoxLayout(self)    
                self.layoutCount.addWidget(self.spinCount)                                                                                                #Setzt ein horizontales Layout
                self.layoutCount.addWidget(self.LabelSpinCount)
                #self.layoutCount.addStretch(1)
                self.groupboxAuto.setLayout(self.layoutCount)
                
                self.vboxSteps = QVBoxLayout(self)                                                                                                      #Setzt ein horizontales Layout
                self.vboxSteps.addWidget(self.groupboxManuel)
                self.vboxSteps.addStretch(1)
                self.vboxSteps.addWidget(self.groupboxAuto)
                self.vboxSteps.addStretch(1)
                self.vboxSteps.addWidget(self.labelPoints)
                self.vboxSteps.addStretch(1)
                self.groupboxSteps.setLayout(self.vboxSteps)

                self.groupboxSyncWin = QGroupBox("Measurement Window", self) 
                self.layoutXStart = QVBoxLayout(self)                                                                                                   #Setzt ein vetikales Layout
                self.layoutXStart.addWidget(self.labelXStart2)                                                                                          #Fügt das Label ein
                self.layoutXStart.addWidget(self.slideXStart2)                                                                                          #Fügt den Slider hinzu
                self.layoutXStart.addWidget(self.spinXStart2)                                                                                           #Setzt ein vetikales Layout
                self.layoutXStart.addStretch(2)                                                                                                         #Fügt die Zahlauswahlbox hinzu
                
                self.layoutYStart = QVBoxLayout(self)                                                                                                   #Setzt ein vetikales Layout
                self.layoutYStart.addWidget(self.labelYStart2)                                                                                          #Fügt das Label ein
                self.layoutYStart.addWidget(self.slideYStart2)                                                                                          #Fügt den Slider hinzu
                self.layoutYStart.addWidget(self.spinYStart2)                                                                                           #Setzt ein vetikales Layout
                self.layoutYStart.addStretch(2)                                                                                                         #Fügt die Zahlauswahlbox hinzu
                        
                self.layoutStart = QHBoxLayout(self)                                                                                                    #Setzt ein horizontales Layout
                self.layoutStart.addLayout(self.layoutXStart)                                                                                           #Fügt ein Layout hinzu
                self.layoutStart.addLayout(self.layoutYStart)                                                                                           #Fügt ein Layout hinzu
                
                self.layoutXStop = QVBoxLayout(self)                                                                                                    #Setzt ein vetikales Layout
                self.layoutXStop.addWidget(self.labelXStop2)                                                                                            #Fügt das Label ein
                self.layoutXStop.addWidget(self.slideXStop2)                                                                                            #Fügt den Slider hinzu
                self.layoutXStop.addWidget(self.spinXStop2)                                                                                             #Setzt ein vetikales Layout
                self.layoutXStop.addStretch(2)                                                                                                          #Fügt die Zahlauswahlbox hinzu
                
                self.layoutYStop = QVBoxLayout(self)                                                                                                    #Setzt ein vetikales Layout
                self.layoutYStop.addWidget(self.labelYStop2)                                                                                            #Fügt das Label ein
                self.layoutYStop.addWidget(self.slideYStop2)                                                                                            #Fügt den Slider hinzu
                self.layoutYStop.addWidget(self.spinYStop2)                                                                                             #Setzt ein vetikales Layout
                self.layoutYStop.addStretch(2)                                                                                                          #Fügt die Zahlauswahlbox hinzu
                        
                self.layoutStop = QHBoxLayout(self)                                                                                                     #Setzt ein horizontales Layout
                self.layoutStop.addLayout(self.layoutXStop)                                                                                             #Fügt ein Layout hinzu
                self.layoutStop.addLayout(self.layoutYStop)

                self.vboxSyncWin = QVBoxLayout(self)                                                                                                    #Setzt ein vetikales Layout
                self.vboxSyncWin.addLayout(self.layoutStart)                                                                                            #Setzt ein vetikales Layout
                self.vboxSyncWin.addLayout(self.layoutStop)
                self.groupboxSyncWin.setLayout(self.vboxSyncWin)
                


                #Layouts                        
                self.tab3.layoutEnd = QHBoxLayout(self)                                                                                                 #Setzt ein horizontales Layout
                self.tab3.layoutEnd.addStretch(1)                                                                                                       #Setzt einen Abstandshalter ein
                self.tab3.layoutEnd.addWidget(self.end3)                                                                                                #Setzt den Ende-Button          
                
                self.tab3.layoutGrid = QGridLayout(self)
                self.tab3.layoutGrid.addWidget(self.groupboxRes3, 0, 0)
                self.tab3.layoutGrid.addWidget(self.labelStretch1Tab3, 1, 0)
                self.tab3.layoutGrid.addWidget(self.groupboxSendTTL3, 2, 0)
                self.tab3.layoutGrid.addWidget(self.groupboxSyncWin, 0, 2)
                self.tab3.layoutGrid.addWidget(self.labelStretch2Tab3, 1, 2)
                self.tab3.layoutGrid.addWidget(self.groupboxSteps, 2, 2)
                self.tab3.layoutGrid.addWidget(self.groupboxSave3, 0, 4)
                self.tab3.layoutGrid.setRowStretch(0, 2)
                self.tab3.layoutGrid.setColumnStretch(0, 1)
                self.tab3.layoutGrid.setColumnStretch(1, 1)
                self.tab3.layoutGrid.setColumnStretch(2, 8)
                self.tab3.layoutGrid.setColumnStretch(3, 1)
                self.tab3.layoutGrid.setColumnStretch(4, 1)

                
                self.tab3.layoutv = QVBoxLayout(self)                                                                                                   #Setzt ein vertikales Layout
                self.tab3.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab3.layoutv.addLayout(self.tab3.layoutGrid)                                                                                       #Fügt das erste horizontale Layout zum vertikalen Layout hinzu
                self.tab3.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab3.layoutv.addLayout(self.tab3.layoutEnd)                                                                                        #Fügt das Ende-Layout zum vertikalen Layout hinzu
                
                self.tab3.setLayout(self.tab3.layoutv)                                                                                                  #Setzt das vertikale Layout als Tab-Layout

#---------------------------- Tab4 --------------------------
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am anfang zu definieren, da sonst später aufruffehler auftretten können
                self.ZStepsize = QDoubleSpinBox(self)                                                                                                   #setzt eine Spinbox
                self.ZDirection = QComboBox(self)
                self.StackCount = QSpinBox(self)
                self.labelStackSize = QLabel("", self)                                                                                                  #Setzt ein Label 
                self.labelStacks = QLabel("Stacks:", self)                                                                                              #Setzt ein Label 
                self.labelStackStep = QLabel("Stepsize [\u03BCm]:", self)                                                                               #Setzt ein Label 
                self.labelDirect = QLabel("Direction:", self)                                                                                           #Setzt ein Label
                self.ZStartSpin = QSpinBox(self)
                self.ZStartSlide = QSlider(Qt.Horizontal)
                self.buttonSetZ = QPushButton("Set Z", self)
                self.labelStretch1Tab4 = QLabel(" ", self)
                self.labelSpacerStack = QLabel(" ", self) 
                self.labelSpacerStack2 = QLabel(" ", self) 
                self.labelSpacerStack3 = QLabel("         ", self) 
                self.labelSpacerStack4 = QLabel("         ", self)   
                self.labelSpacerStack5 = QLabel("  ", self)                                                                                             #setzt eine Spinbox
                self.labelAmpel = QLabel(" ", self)

                #Ampel
                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_green.png")
                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                self.labelAmpel.setPixmap(pixmap_mini)
                self.labelAmpel.show()             

                #Label
                MaxStackSize = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)
                StackSize = 5.0
                self.labelStackSize.setText("Maximum Stacksize: " + str((MaxStackSize/1000)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]")
                
                #Button definieren
                self.buttonSetZ.setCheckable(True)                                                                                                      #Macht den Button chackbar
                self.buttonSetZ.setToolTip("Sets the Stage to the Value")                                                                               #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonSetZ.clicked[bool].connect(self.StartZChange)

                #Slider definieren
                self.ZStartSlide.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.ZStartSlide.setMaximum(4095)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.ZStartSlide.setValue(0)                                                                                                            #Setzt einen Startwert
                self.ZStartSlide.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.ZStartSlide.setTickInterval(256)                                                                                                   #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.ZStartSlide.valueChanged.connect(self.slideZChange)                                                                                #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ZStartSlide.setToolTip("Sets the Z-Startposition")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver
                                
                #Spinbox definieren
                self.ZStartSpin.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.ZStartSpin.setMaximum(4095)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.ZStartSpin.setValue(0)                                                                                                             #Setzt einen Startwert
                self.ZStartSpin.valueChanged.connect(self.spinZChange)                                                                                  #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ZStartSpin.setToolTip("Sets the Z-Startposition")                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver

                #ComboBox definieren
                self.ZDirection.addItem("Up")
                self.ZDirection.addItem("Down")
                self.ZDirection.addItem("Both")
                self.ZDirection.currentIndexChanged.connect(self.DirectChange)
                
                #Spinbox definieren
                self.StackCount.setMinimum(2)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.StackCount.setMaximum(100)                                                                                                         #Setzt ein Maximum für die Auswahl
                self.StackCount.setValue(11)                                                                                                            #Setzt einen Startwert
                self.StackCount.valueChanged.connect(self.StackCountChange)                                                                             #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.StackCount.setToolTip("Sets the number of Z-Stacks")                                                                               #Setzt eine Buttonbeschreibung bei MouseOver
                
                #Spinbox definieren
                self.ZStepsize.setMinimum(0.000)                                                                                                        #Setzt ein Minimalwert für die Auswahl
                self.ZStepsize.setMaximum(50.000)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.ZStepsize.setValue(0.500)                                                                                                          #Setzt einen Startwert
                self.ZStepsize.setSingleStep(0.01)
                self.ZStepsize.setDecimals(2)
                self.ZStepsize.valueChanged.connect(self.StackStepChange)
                self.ZStepsize.setToolTip("Sets the Z-Stepsize in Micrometer")                                                                          #Setzt eine Buttonbeschreibung bei MouseOver


                #Save - Settings
                self.nameStack = QLineEdit(self)                                                                                                        #Setzt eine Textbox
                self.saveStack = QPushButton("Save", self)                                                                                              #Setzt einen Button
                self.namesStack = QComboBox(self)                                                                                                       #Setzt eine Auswahlbox
                self.useStack = QPushButton("Use", self)                                                                                                #Setzt einen Button

                #Settings
                self.saveStack.setToolTip("Saves the Settings")                                                                                         #Setzt eine Buttenbeschreibung bei MouseOver
                self.saveStack.clicked.connect(self.savesettingsScanStack)                                                                              #Ruft die savesettings-Funktion auf
                self.namesStack.setToolTip("Old Settings")
                StackSet.execute("SELECT name FROM settingsScanStack")
                for dsatzStack in StackSet:
                        x = dsatzStack[0]
                        #print(str(x))
                        self.namesStack.addItem(x)
                self.useStack.setToolTip("Uses the Settings")
                self.useStack.clicked.connect(self.usesettingsScanStack)
                
                        
                #Ende
                self.end4 = QPushButton("Exit", self)                                                                                                   #setzt einen Ende-Button
                self.end4.setToolTip("Programm beenden")                                                                                                #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end4.clicked.connect(self.Hydra)                                                                                                   #Ruft die ende1-Funktion auf, wenn der Button gedrückt wird

                #Groupboxes
                self.groupboxSave4 = QGroupBox("Save Settings", self) 
                self.vboxSave4 = QVBoxLayout(self)                 
                self.vboxSave4.addWidget(self.nameStack)                                                                                                #Setzt das Widget
                self.vboxSave4.addWidget(self.saveStack)                                                                                                #Setzt das Widget
                self.vboxSave4.addWidget(self.namesStack)                                                                                               #Setzt das Widget
                self.vboxSave4.addWidget(self.useStack)                                                                                                 #Setzt das Widget
                #self.vboxSave4.addStretch(1)
                self.groupboxSave4.setLayout(self.vboxSave4)

                
                #Layouts setzen und Widgets einfügen
                self.tab4.layoutH0 = QHBoxLayout(self)
                self.tab4.layoutH0.addWidget(self.labelDirect)
                
                self.tab4.layoutH1 = QHBoxLayout(self)
                self.tab4.layoutH1.addWidget(self.ZDirection)

                self.tab4.layoutH2 = QHBoxLayout(self)
                self.tab4.layoutH2.addWidget(self.labelStacks)
                self.tab4.layoutH2.addWidget(self.labelStackStep)
                
                self.tab4.layoutH3 = QHBoxLayout(self)
                self.tab4.layoutH3.addWidget(self.StackCount)
                self.tab4.layoutH3.addWidget(self.ZStepsize)

                self.tab4.layoutH4 = QHBoxLayout(self)
                self.tab4.layoutH4.addWidget(self.labelStackSize)

                self.tab4.layoutV0 = QVBoxLayout(self)                                                                                                  #Setzt ein vertikales Layout
                self.tab4.layoutV0.addWidget(self.ZStartSlide)  
                self.tab4.layoutV0.addWidget(self.ZStartSpin)   

                self.tab4.layoutH5 = QHBoxLayout(self)
                self.tab4.layoutH5.addLayout(self.tab4.layoutV0)
                self.tab4.layoutH5.addWidget(self.buttonSetZ)

                self.tab4.layoutV1 = QVBoxLayout(self)                                                                                                  #Setzt ein vertikales Layout
                self.tab4.layoutV1.addLayout(self.tab4.layoutH0)  
                self.tab4.layoutV1.addLayout(self.tab4.layoutH1)                                                                                        #Setzt das Widget
                self.tab4.layoutV1.addWidget(self.labelSpacerStack)                                                                                     #Setzt das Widget
                self.tab4.layoutV1.addLayout(self.tab4.layoutH2)                                                                                        #Setzt das Widget
                self.tab4.layoutV1.addLayout(self.tab4.layoutH3)                                                                                        #Setzt das Widget
                self.tab4.layoutV1.addLayout(self.tab4.layoutH4) 
                self.tab4.layoutV1.addWidget(self.labelSpacerStack2)  
                self.tab4.layoutV1.addLayout(self.tab4.layoutH5)                 
                                
                self.tab4.layoutEnd = QHBoxLayout(self)                                                                                                 #Setzt ein horizontales Layout
                self.tab4.layoutEnd.addStretch(1)                                                                                                       #Setzt einen Abstandshalter ein
                self.tab4.layoutEnd.addWidget(self.end4)                                                                                                #Setzt den Ende-Button          

                self.tab4.layoutVAmpel = QVBoxLayout(self)
                self.tab4.layoutVAmpel.addWidget(self.labelSpacerStack5)
                self.tab4.layoutVAmpel.addWidget(self.labelAmpel)
                self.tab4.layoutVAmpel.addStretch(1)

                self.tab4.layoutHAmpel = QHBoxLayout(self)
                self.tab4.layoutHAmpel.addWidget(self.labelSpacerStack3)
                self.tab4.layoutHAmpel.addLayout(self.tab4.layoutVAmpel)
                self.tab4.layoutHAmpel.addWidget(self.labelSpacerStack4)
                
                self.tab4.layoutGrid = QGridLayout(self)
                self.tab4.layoutGrid.addLayout(self.tab4.layoutV1, 0, 0)
                self.tab4.layoutGrid.addLayout(self.tab4.layoutHAmpel, 0, 1)
                self.tab4.layoutGrid.addWidget(self.groupboxSave4, 0, 2)
                self.tab4.layoutGrid.setColumnStretch(0, 8)
                self.tab4.layoutGrid.setColumnStretch(1, 1)
                self.tab4.layoutGrid.setColumnStretch(2, 1)
                
                self.tab4.layoutGes = QVBoxLayout(self)                                                                                                 #Setzt ein vertikales Layout
                self.tab4.layoutGes.addStretch(8)                                                                                                       #Setzt einen Abstandshalter
                self.tab4.layoutGes.addLayout(self.tab4.layoutGrid)                                                                                     #Fügt das horizontale Layout zum vertikalen Layout hinzu
                self.tab4.layoutGes.addStretch(21)                                                                                                      #Setzt einen Abstandshalter
                self.tab4.layoutGes.addLayout(self.tab4.layoutEnd)                                                                                      #Fügt das horizontale Layout zum vertikalen Layout hinzu
                
                self.tab4.setLayout(self.tab4.layoutGes)                                                                                                #Setzt das vertikale Layout als Tab-Layout
                


#---------------------------- Tab5 --------------------------
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.buttonAutoSlope = QPushButton("Auto Slope", self)
                self.buttonXSlope = QPushButton("Define X Slope", self)                                                                                 #setzt einen Button             
                self.buttonYSlope = QPushButton("Define Y Slope", self)
                self.labelXSlope = QLabel("X-Slope", self)                                                                                              #setzt ein Label                
                self.slideXSlope = QSlider(Qt.Horizontal)                                                                                               #setzt einen horizontalen Slider
                self.spinXSlope = QSpinBox(self)                                                                                                        #setzt eine Spinbox
                self.labelYSlope = QLabel("Y-Slope", self)                                                                                              #setzt ein Label
                self.slideYSlope = QSlider(Qt.Horizontal)                                                                                               #setzt einen horizontalen Slider
                self.spinYSlope = QSpinBox(self) 
                self.labelSpace51 = QLabel("  ", self)    
                self.labelSpace52 = QLabel("  ", self)                                                                                                  #setzt ein Label
                

                #Save - Settings
                self.nameSlope = QLineEdit(self)                                                                                                        #Setzt eine Textbox
                self.saveSlope = QPushButton("Save", self)                                                                                              #Setzt einen Button
                self.namesSlope = QComboBox(self)                                                                                                       #Setzt eine Auswahlbox
                self.useSlope = QPushButton("Use", self)                                                                                                #Setzt einen Button
      
                #Button definieren
                self.buttonAutoSlope.setCheckable(True)                                                                                                 #Macht den Button chackbar
                self.buttonAutoSlope.setToolTip("Start the AutoSlope")                                                                                  #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonAutoSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonAutoSlope.clicked[bool].connect(self.AutoSlope)

                self.buttonXSlope.setCheckable(True)                                                                                                    #Macht den Button chackbar
                self.buttonXSlope.setToolTip("Define the X Slope")                                                                                      #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonXSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonXSlope.clicked[bool].connect(self.SlopeStartX)

                #Button definieren
                self.buttonYSlope.setCheckable(True)                                                                                                    #Macht den Button chackbar
                self.buttonYSlope.setToolTip("Define the Y Slope")                                                                                      #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonYSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonYSlope.clicked[bool].connect(self.SlopeStartY)

                #Settings
                self.saveSlope.setToolTip("Saves the Settings")                                                                                         #Setzt eine Buttenbeschreibung bei MouseOver
                self.saveSlope.clicked.connect(self.savesettingsScanSlope)                                                                              #Ruft die savesettings-Funktion auf
                self.namesSlope.setToolTip("Old Settings")
                SlopeSet.execute("SELECT name FROM settingsScanSlope")
                for dsatzSlope in SyncSet:
                        y = dsatzSlope[0]
                        #print(str(y))
                        self.namesSlope.addItem(y)
                self.useSlope.setToolTip("Uses the Settings")
                self.useSlope.clicked.connect(self.usesettingsScanSlope)
                
                
                #Slider definieren
                self.slideXSlope.setMinimum(-1000)                                                                                                      #Setzt ein Minimalwert für die Auswahl
                self.slideXSlope.setMaximum(1000)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.slideXSlope.setValue(0)                                                                                                            #Setzt einen Startwert
                self.slideXSlope.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.slideXSlope.setTickInterval(2001)                                                                                                  #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXSlope.valueChanged.connect(self.slideXslope)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideXSlope.setToolTip("Sets the X-Slope")                                                                                         #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideYSlope.setMinimum(-1000)                                                                                                      #Setzt ein Minimalwert für die Auswahl
                self.slideYSlope.setMaximum(1000)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.slideYSlope.setValue(0)                                                                                                            #Setzt einen Startwert
                self.slideYSlope.setTickPosition(QSlider.TicksBelow)                                                                                    #Setzt Rastpunkte unter dem Slider
                self.slideYSlope.setTickInterval(2001)                                                                                                  #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYSlope.valueChanged.connect(self.slideYslope)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideYSlope.setToolTip("Sets the Y-Slope")                                                                                         #Setzt eine Buttonbeschreibung bei MouseOver
                                
                #Spinbox definieren
                self.spinXSlope.setMinimum(-1000)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.spinXSlope.setMaximum(1000)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.spinXSlope.setValue(0)                                                                                                             #Setzt einen Startwert
                self.spinXSlope.valueChanged.connect(self.spinXslope)                                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinXSlope.setToolTip("Sets the X-Slope")                                                                                          #Setzt eine Buttonbeschreibung bei MouseOver

                self.spinYSlope.setMinimum(-1000)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.spinYSlope.setMaximum(1000)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.spinYSlope.setValue(0)                                                                                                             #Setzt einen Startwert
                self.spinYSlope.valueChanged.connect(self.spinYslope)                                                                                   #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinYSlope.setToolTip("Sets the Y-Slope")                                                                                          #Setzt eine Buttonbeschreibung bei MouseOver
                                
                #Ende
                self.end5 = QPushButton("Exit", self)                                                                                                   #setzt einen Ende-Button
                self.end5.setToolTip("Programm beenden")                                                                                                #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end5.clicked.connect(self.Hydra)                                                                                                   #Ruft die end2-Funktion auf, wenn der Button gedrückt wird


                #Groupboxes
                self.groupboxSave5 = QGroupBox("Save Settings", self) 
                self.vboxSave5 = QVBoxLayout(self)                     
                self.vboxSave5.addWidget(self.nameSlope)                                                                                                #Setzt das Widget
                self.vboxSave5.addWidget(self.saveSlope)                                                                                                #Setzt das Widget
                self.vboxSave5.addWidget(self.namesSlope)                                                                                               #Setzt das Widget
                self.vboxSave5.addWidget(self.useSlope)                                                                                                 #Setzt das Widget
                #self.vboxSave5.addStretch(1)
                self.groupboxSave5.setLayout(self.vboxSave5)


                #Layouts
                self.tab5.layoutXSlope = QVBoxLayout(self)                                                                                              #Setzt ein vetikales Layout
                self.tab5.layoutXSlope.addWidget(self.labelXSlope)                                                                                      #Fügt das Label ein
                self.tab5.layoutXSlope.addWidget(self.slideXSlope)                                                                                      #Fügt den Slider hinzu
                self.tab5.layoutXSlope.addWidget(self.spinXSlope)                                                                                       #Fügt die Zahlauswahlbox hinzu

                self.tab5.layoutX = QHBoxLayout(self)
                self.tab5.layoutX.addLayout(self.tab5.layoutXSlope)
                self.tab5.layoutX.addWidget(self.buttonXSlope)
                
                self.tab5.layoutYSlope = QVBoxLayout(self)                                                                                              #Setzt ein vetikales Layout
                self.tab5.layoutYSlope.addWidget(self.labelYSlope)                                                                                      #Fügt das Label ein
                self.tab5.layoutYSlope.addWidget(self.slideYSlope)                                                                                      #Fügt den Slider hinzu
                self.tab5.layoutYSlope.addWidget(self.spinYSlope)                                                                                       #Fügt die Zahlauswahlbox hinzu

                self.tab5.layoutY = QHBoxLayout(self)
                self.tab5.layoutY.addLayout(self.tab5.layoutYSlope)
                self.tab5.layoutY.addWidget(self.buttonYSlope)
                
                self.tab5.layoutV1 = QVBoxLayout(self)                                                                                                  #Setzt ein vetikales Layout
                self.tab5.layoutV1.addStretch(2)                                                                                                        #Setzt einen Abstandshalter
                self.tab5.layoutV1.addLayout(self.tab5.layoutX)                                                                                         #Fügt das Range1-Layout zum vertikalen Layout hinzu
                self.tab5.layoutV1.addStretch(1)                                                                                                        #Setzt einen Abstandshalter
                self.tab5.layoutV1.addLayout(self.tab5.layoutY)                                                                                         #Setzt das Widget
                
                self.tab5.layoutGrid = QGridLayout(self)
                self.tab5.layoutGrid.addLayout(self.tab5.layoutV1, 0, 1)
                self.tab5.layoutGrid.addWidget(self.groupboxSave5, 0, 3)
                self.tab5.layoutGrid.addWidget(self.labelSpace51, 1, 1)
                self.tab5.layoutGrid.addWidget(self.labelSpace52, 2, 1)
                self.tab5.layoutGrid.addWidget(self.buttonAutoSlope, 3, 1)
                self.tab5.layoutGrid.setColumnStretch(0, 1)
                self.tab5.layoutGrid.setColumnStretch(1, 7)
                self.tab5.layoutGrid.setColumnStretch(2, 1)
                self.tab5.layoutGrid.setColumnStretch(3, 1)

                self.tab5.layoutEnd = QHBoxLayout(self)                                                                                                 #Setzt ein horizontales Layout
                self.tab5.layoutEnd.addStretch(1)                                                                                                       #Setzt einen Abstandshalter ein
                self.tab5.layoutEnd.addWidget(self.end5)                                                                                                #Setzt den Ende-Button  
                
                self.tab5.layoutv = QVBoxLayout(self)                                                                                                   #Setzt ein vertikales Layout
                self.tab5.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab5.layoutv.addLayout(self.tab5.layoutGrid)                                                                                       #Fügt das erste horizontale Layout zum vertikalen Layout hinzu
                self.tab5.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab5.layoutv.addLayout(self.tab5.layoutEnd)                                                                                        #Fügt das Ende-Layout zum vertikalen Layout hinzu
                        
                self.tab5.setLayout(self.tab5.layoutv)                                                                                                  #Setzt das vertikale Layout als Tab-Layout

                """
                #-------------- Tab 6 Plot ----------------------------------
                #Variablen definieren
                self.FilePath2 = ""
                self.SavePath = ""
                
                #Widgets setzen
                self.buttonPlot = QPushButton("Start Plot", self)
                
                self.buttonPath = QPushButton("Open File", self)
                self.labelPath = QLabel(" ", self)
                self.labelPlotSize = QLabel(" ", self)

                self.buttonSave = QPushButton("Save to:", self)
                self.labelSave = QLabel("/home/pi/Desktop/Data/", self)
                self.SaveAs = QComboBox(self)
                self.labelSaveAs = QLabel("Save as: ")
                
                self.ComboStyle = QComboBox(self)
                self.labelStyle = QLabel("Plotstyle", self)                                                                                             #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.Plotname = QLineEdit(self)
                self.labelPlot = QLabel(" Headline", self)
                self.Filename = QLineEdit(self)
                self.labelFile = QLabel("Filename", self)
                self.FileStart = QSpinBox(self)
                self.labelFileStart = QLabel("File Headerlines:", self)
                self.ComboRow = QComboBox(self)
                self.labelRow = QLabel("Row to Plot", self) 
                
                self.XAxis = QLineEdit(self)
                self.YAxis = QLineEdit(self)
                self.ZAxis = QLineEdit(self)
                self.InvertXAxis = QCheckBox("Invert X", self)
                self.InvertYAxis = QCheckBox("Invert Y", self)
                self.InvertYAxis.setChecked(True)
                self.labelXAxis = QLabel("X Axis     ", self)
                self.labelYAxis = QLabel("Y Axis     ", self)
                self.labelZAxis = QLabel("Z Axis     ", self)
                self.Range = QCheckBox("Convert Axis to um", self)
                self.Range.stateChanged.connect(self.RangeTrue)
                
                self.XStartValue = QSpinBox(self)
                self.XStopValue = QSpinBox(self)
                self.YStartValue = QSpinBox(self)
                self.YStopValue = QSpinBox(self)
                self.labelPlotsize = QLabel("Zoom Plot to:                                  ", self)
                self.labelXStartValue = QLabel("X Start", self)
                self.labelXStopValue = QLabel("X Stop", self)
                self.labelYStartValue = QLabel("Y Start", self)
                self.labelYStopValue = QLabel("Y Stop", self)
                
                self.labelPlotSpacer = QLabel("              ", self)
                self.labelPlotSpacer2 = QLabel("                           ", self)
                self.labelPlotSpacer3 = QLabel("               ", self)
                self.labelPlotSpacer4 = QLabel(" ", self)
                self.labelPlotSpacer5 = QLabel(" ", self)
                self.labelPlotSpacer6 = QLabel(" ", self)
                self.labelPlotSpacer7 = QLabel(" ", self)

                self.ScaleBarFontsize = QSpinBox(self)
                self.labelScaleBarFontsize = QLabel("Fontsize", self)
                self.FontColor = QComboBox(self)
                self.labelFontColor = QLabel("Fontcolor", self)
                self.ScaleBarFontweight = QComboBox(self)
                self.labelScaleBarFontweight = QLabel("Fontweight", self)
                self.ScaleBarSize = QDoubleSpinBox(self)
                self.labelScaleBarSize = QLabel("Barsize [\u03BCm]", self)
                self.ScaleBarSizeVertical = QDoubleSpinBox(self)
                self.labelScaleBarSizeVertical = QLabel("Barwidth", self)
                self.ScaleBarPosition = QComboBox(self)
                self.labelScaleBarPosition = QLabel("Bar Position", self)
                self.ScaleBarOffset = QDoubleSpinBox(self)
                self.labelScaleBarOffset = QLabel("Bar Offset", self)
                self.ColorBarMax = QSpinBox(self)
                self.labelColorBarMax1 = QLabel("Bar Maximum", self)
                self.labelColorBarMax2 = QLabel(" ", self)
                self.ColorBarMin = QSpinBox(self)
                self.labelColorBarMin1 = QLabel("Bar Minimum ", self)
                self.labelColorBarMin2 = QLabel(" ", self)

                self.buttonPath.setToolTip("Set the Filepath")
                self.buttonPath.clicked.connect(self.OpenPlotFile)
                self.Plotname.setToolTip("Sets the Headline of the Plot")
                self.Filename.setToolTip("Sets the Filename")
                self.Plotname.setText(PlotName)
                self.Filename.setText(FileName)
                self.XAxis.setText("X-Position [Bit]")
                self.YAxis.setText("Y-Position [Bit]")

                
                #ComboBox definieren
                self.SaveAs.addItem(".png")
                self.SaveAs.addItem(".jpg")
                self.SaveAs.addItem(".svg")
                self.SaveAs.setCurrentIndex(0)
                #self.SaveAs.currentIndexChanged.connect(self.SaveAsFile)
                
                self.ComboStyle.addItem("PColorMesh")
                self.ComboStyle.addItem("Contours")
                self.ComboStyle.addItem("PColor and Contour")
                self.ComboStyle.addItem("3D Surface")
                self.ComboStyle.addItem("3D Contour")
                self.ComboStyle.addItem("3D Contour Fill")
                self.ComboStyle.addItem("Scatter")
                self.ComboStyle.setCurrentIndex(0)
                
                self.ComboRow.addItem("- Select Row -")
                self.ComboRow.setCurrentIndex(0)
                self.ComboRow.currentIndexChanged.connect(self.UpdateZAxis)

                self.ScaleBarFontweight.addItem("normal")
                self.ScaleBarFontweight.addItem("light")
                self.ScaleBarFontweight.addItem("bold")
                self.ScaleBarFontweight.addItem("extra bold")
                self.ScaleBarFontweight.setCurrentIndex(0)

                self.FontColor.addItem("black")
                self.FontColor.addItem("white")
                self.FontColor.setCurrentIndex(0)
                
                self.ScaleBarPosition.addItem("upper right")
                self.ScaleBarPosition.addItem("upper center")
                self.ScaleBarPosition.addItem("upper left")
                self.ScaleBarPosition.addItem("center left")
                self.ScaleBarPosition.addItem("center")
                self.ScaleBarPosition.addItem("center right")
                self.ScaleBarPosition.addItem("lower left")
                self.ScaleBarPosition.addItem("lower center")
                self.ScaleBarPosition.addItem("lower right")
                self.ScaleBarPosition.setCurrentIndex(8)
                                     
                #Button definieren
                self.buttonPlot.setCheckable(False)                                                                                                     #macht den Button chackbar
                self.buttonPlot.setToolTip("Start Plotting")                                                                                            #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonPlot.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonPlot.clicked[bool].connect(self.PlotFile)                                                                                    #ruft die clickedM1-Funktion auf, wenn der Button betätigt wird und gibt einen true Wert an die Funktion, wenn der Button unten bleibt und einen false Wert, wenn er wieder oben ist

                self.buttonSave.setCheckable(False)                                                                                                     #macht den Button chackbar
                self.buttonSave.setToolTip("Search for Save-Directory")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonSave.clicked[bool].connect(self.SaveAsPath)                                                                                  #ruft die clickedM1-Funktion auf, wenn der Button betätigt wird und gibt einen true Wert an die Funktion, wenn der Button unten bleibt und einen false Wert, wenn er wieder oben ist

                #Spinbox definieren
                self.ColorBarMax.setMinimum(0)
                self.ColorBarMax.setMaximum(2000)                                                                                                       #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ColorBarMax.setToolTip("Sets the Colorbar-Maximum")
                
                self.ColorBarMin.setMinimum(0)
                self.ColorBarMin.setMaximum(2000)                                                                                                       #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ColorBarMin.setToolTip("Sets the Colorbar-Minimum")
                
                self.ScaleBarFontsize.setMinimum(0)                                                                                                     #Setzt ein Minimalwert für die Auswahl
                self.ScaleBarFontsize.setMaximum(100)                                                                                                   #Setzt ein Maximum für die Auswahl
                self.ScaleBarFontsize.setValue(12)                                                                                                      #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ScaleBarFontsize.setToolTip("Sets the Fontsize")
                
                self.ScaleBarSize.setMinimum(0)                                                                                                         #Setzt ein Minimalwert für die Auswahl
                self.ScaleBarSize.setMaximum(50000)                                                                                                     #Setzt einen Startwert
                self.ScaleBarSizeVertical.setSingleStep(0.1)                                                                                            #Setzt ein Maximum für die Auswahl
                self.ScaleBarSize.setValue(10)                                                                                                          #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ScaleBarSize.setToolTip("Sets the horizontal Barsize")

                self.ScaleBarSizeVertical.setMinimum(0.0)                                                                                               #Setzt ein Minimalwert für die Auswahl
                self.ScaleBarSizeVertical.setMaximum(100.0)                                                                                             #Setzt einen Startwert
                self.ScaleBarSizeVertical.setSingleStep(0.1)
                self.ScaleBarSizeVertical.setDecimals(1)                                                                                                #Setzt ein Maximum für die Auswahl
                self.ScaleBarSizeVertical.setValue(0.2)                                                                                                 #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ScaleBarSizeVertical.setToolTip("Sets the vertical Barsize")
                
                self.ScaleBarOffset.setMinimum(0.0)                                                                                                     #Setzt ein Minimalwert für die Auswahl
                self.ScaleBarOffset.setMaximum(1000.0)                                                                                                  #Setzt einen Startwert
                self.ScaleBarOffset.setSingleStep(0.1)
                self.ScaleBarOffset.setDecimals(1)                                                                                                      #Setzt ein Maximum für die Auswahl
                self.ScaleBarOffset.setValue(1)                                                                                                         #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.ScaleBarOffset.setToolTip("Sets the Bar Offset")

                self.FileStart.setMinimum(0)                                                                                                            #Setzt ein Minimalwert für die Auswahl
                self.FileStart.setMaximum(100)                                                                                                          #Setzt ein Maximum für die Auswahl
                self.FileStart.setValue(7)                                 
                self.FileStart.setToolTip("Sets the number of Lines that will be ignored")
                self.FileStart.valueChanged.connect(self.UpdatePlotLabel)

                self.XStartValue.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.XStartValue.setMaximum(4096)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.XStartValue.setValue(0)                                                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.XStartValue.valueChanged.connect(self.UpdatePlotLabels)                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.XStartValue.setToolTip("Sets the X-Start Value, everything bevor will be ignored")
                
                self.XStopValue.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.XStopValue.setMaximum(4096)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.XStopValue.setValue(0)                                                                                                             #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.XStopValue.valueChanged.connect(self.UpdatePlotLabels)                                                                             #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.XStopValue.setToolTip("Sets the X-Stop Value, everything after there will be ignored")
                
                self.YStartValue.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.YStartValue.setMaximum(4096)                                                                                                       #Setzt ein Maximum für die Auswahl
                self.YStartValue.setValue(0)                                                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.YStartValue.valueChanged.connect(self.UpdatePlotLabels)                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.YStartValue.setToolTip("Sets the Y-Start Value, everything bevor will be ignored")
                
                self.YStopValue.setMinimum(0)                                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.YStopValue.setMaximum(4096)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.YStopValue.setValue(0)                                                                                                             #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.YStopValue.valueChanged.connect(self.UpdatePlotLabels)                                                                             #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.YStopValue.setToolTip("Sets the Y-Stop Value, everything after there will be ignored")

                #Ende
                self.end6 = QPushButton("Exit", self)                                                                                                   #setzt einen Ende-Button
                self.end6.setToolTip("Programm beenden")                                                                                                #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end6.clicked.connect(self.Hydra)                                                                                                   #Ruft die ende1-Funktion auf, wenn der Button gedrückt wird

                #Checkboxen setzen
                #self.labelcbStyle = QLabel("Plotcolor", self)                                                                                          #Setzt ein Label 
                self.cbStyle1 = QCheckBox("Spectral_r", self)                                                                                           #Setzt eine CheckBox
                self.cbStyle1.setToolTip("Sets the Plotstyle to Spectral_r (Rainbowcolors)")                                                            #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbStyle2 = QCheckBox("gray_r", self)                                                                     
                self.cbStyle2.setToolTip("Sets the Plotstyle to gray_r (50 Shades of Gray)")                                 
                self.cbStyle3 = QCheckBox("bone", self)                                                                       
                self.cbStyle3.setToolTip("Sets the Plotstyle to bone (black - blue - white)")                                 
                self.cbStyle4 = QCheckBox("Wistia", self)                                                                   
                self.cbStyle4.setToolTip("Sets the Plotstyle to Wistia (yellow - orange)")                              
                self.cbStyle5 = QCheckBox("copper", self)                                                                  
                self.cbStyle5.setToolTip("Sets the Plotstyle to copper (get to the copper)")                                   
                self.cbStyle6 = QCheckBox("gist_heat", self)                                                                  
                self.cbStyle6.setToolTip("Sets the Plotstyle to gist_heat (black - red - white)")                               
                self.cbStyle7 = QCheckBox("winter", self)                                                                     
                self.cbStyle7.setToolTip("Sets the Plotstyle to summer (Brace yourself)")                               
                self.cbStyle8 = QCheckBox("spring", self)                                                                     
                self.cbStyle8.setToolTip("Sets the Plotstyle to spring (purple - yellow)")                            
                self.cbStyle9 = QCheckBox("summer", self)                                                              
                self.cbStyle9.setToolTip("Sets the Plotstyle to summer (green - yellow)")                           
                self.cbStyle10 = QCheckBox("autumn", self)                                                             
                self.cbStyle10.setToolTip("Sets the Plotstyle to autumn (red - yellow)")                             
                self.cbStyle11 = QCheckBox("hot", self)                                                               
                self.cbStyle11.setToolTip("Sets the Plotstyle to hot_r (red - yellow)")                                     
                self.cbStyle12 = QCheckBox("cool", self)                                                                     
                self.cbStyle12.setToolTip("Sets the Plotstyle to cool (lite blue - purple)")                               
                self.cbStyle13 = QCheckBox("gist_ncar", self)                                                                 
                self.cbStyle13.setToolTip("Sets the Plotstyle to gist_ncar (red - yellow)")                                    
                self.cbStyle14 = QCheckBox("nipy_spectral", self)                                                                    
                self.cbStyle14.setToolTip("Sets the Plotstyle to nipy_spectral (red - yellow)")                                 
                self.cbStyle15 = QCheckBox("Reds", self)                                                                     
                self.cbStyle15.setToolTip("Sets the Plotstyle to Reds (White - Red)")                                 


                if PlotStyle == 1:
                        self.cbStyle1.setChecked(True)
                elif PlotStyle == 2:
                        self.cbStyle2.setChecked(True)
                elif PlotStyle == 3:
                        self.cbStyle3.setChecked(True)
                elif PlotStyle == 4:
                        self.cbStyle4.setChecked(True)
                elif PlotStyle == 5:
                        self.cbStyle5.setChecked(True)
                elif PlotStyle == 6:
                        self.cbStyle6.setChecked(True)
                elif PlotStyle == 7:
                        self.cbStyle7.setChecked(True)
                elif PlotStyle == 8:
                        self.cbStyle8.setChecked(True)
                elif PlotStyle == 9:
                        self.cbStyle9.setChecked(True)
                elif PlotStyle == 10:
                        self.cbStyle10.setChecked(True)
                elif PlotStyle == 11:
                        self.cbStyle11.setChecked(True)
                elif PlotStyle == 12:
                        self.cbStyle12.setChecked(True)
                elif PlotStyle == 13:
                        self.cbStyle13.setChecked(True)
                elif PlotStyle == 14:
                        self.cbStyle14.setChecked(True)
                elif PlotStyle == 15:
                        self.cbStyle15.setChecked(True)

                        
                #Checkboxen als ButtonGroup zusammenfassen                
                self.cbgStyle = QButtonGroup()                                                                                                          #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbgStyle.addButton(self.cbStyle1, 1)                                                                                               #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle2, 2)                                                                                               #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle3, 3)                                                                                               #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle4, 4)
                self.cbgStyle.addButton(self.cbStyle5, 5)                                                                                               #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle6, 6)                                                                                               #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle7, 7)                                                                                               #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle8, 8)
                self.cbgStyle.addButton(self.cbStyle9, 9)                                                                                               #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle10, 10)                                                                                             #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle11, 11)                                                                                             #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle12, 12)                                                                                             #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle13, 13)                                                                                             #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle14, 14)                                                                                             #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbgStyle.addButton(self.cbStyle15, 15)

                #Groupboxen definieren
                self.groupboxHeadlines = QGroupBox("Manuel", self)
                self.groupboxHeadlines.setCheckable(True)
                self.groupboxHeadlines.setChecked(False)
                self.vboxStart = QVBoxLayout(self)
                self.vboxStart.addWidget(self.labelFileStart)
                self.vboxStart.addWidget(self.FileStart)
                self.groupboxHeadlines.setLayout(self.vboxStart)
                
                self.groupboxAxes = QGroupBox("Axes", self)
                self.hboxXAxis = QHBoxLayout()                
                self.hboxXAxis.addWidget(self.XAxis)             
                self.hboxXAxis.addWidget(self.labelXAxis)
                self.hboxYAxis = QHBoxLayout()                
                self.hboxYAxis.addWidget(self.YAxis)             
                self.hboxYAxis.addWidget(self.labelYAxis)
                self.hboxZAxis = QHBoxLayout()                
                self.hboxZAxis.addWidget(self.ZAxis)             
                self.hboxZAxis.addWidget(self.labelZAxis)
                self.hboxInvert = QHBoxLayout()                
                self.hboxInvert.addWidget(self.InvertXAxis)             
                self.hboxInvert.addWidget(self.InvertYAxis)
                self.hboxInvert.addWidget(self.Range)
                self.layoutAxes = QVBoxLayout(self)
                self.layoutAxes.addLayout(self.hboxXAxis)
                self.layoutAxes.addLayout(self.hboxYAxis)
                self.layoutAxes.addLayout(self.hboxZAxis)
                self.layoutAxes.addLayout(self.hboxInvert)
                self.groupboxAxes.setLayout(self.layoutAxes)
                
                self.groupboxColor = QGroupBox("Plotcolor", self)
                self.vboxColor = QVBoxLayout()                
                self.vboxColor.addWidget(self.cbStyle1)                                                                                                 #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxColor.addWidget(self.cbStyle2)                                                                                                 #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxColor.addWidget(self.cbStyle3)                                                                                                 #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxColor.addWidget(self.cbStyle4)
                self.vboxColor.addWidget(self.cbStyle5)                                                                                                 #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxColor.addWidget(self.cbStyle6)                                                                                                 #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxColor.addWidget(self.cbStyle7)                                                                                                 #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxColor.addWidget(self.cbStyle8)
                self.vboxColor.addWidget(self.cbStyle9)                                                                                                 #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxColor.addWidget(self.cbStyle10)                                                                                                #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxColor.addWidget(self.cbStyle11)                                                                                                #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxColor.addWidget(self.cbStyle12)                                                                                                #Jede CheckBox muss seperat zum Layout hinzugefügt werden
                self.vboxColor.addWidget(self.cbStyle13)                                                                                                #Die ButtonGroup ist kein Widget, das zu einem Layout hinzugefügt werden kann
                self.vboxColor.addWidget(self.cbStyle14)                                                                                                #Die ButtonGroup ist nur ein Eigenschaften-Container
                self.vboxColor.addWidget(self.cbStyle15)
                self.groupboxColor.setLayout(self.vboxColor)

                self.groupboxZoom = QGroupBox("Zoom", self)
                self.groupboxZoom.setCheckable(True)
                self.groupboxZoom.setChecked(False)
                self.layoutVZoomXStart = QVBoxLayout(self)
                self.layoutVZoomXStart.addWidget(self.labelXStartValue)
                self.layoutVZoomXStart.addWidget(self.XStartValue)                
                self.layoutVZoomXStop = QVBoxLayout(self)
                self.layoutVZoomXStop.addWidget(self.labelXStopValue)
                self.layoutVZoomXStop.addWidget(self.XStopValue)
                self.layoutVZoomYStart = QVBoxLayout(self)
                self.layoutVZoomYStart.addWidget(self.labelYStartValue)
                self.layoutVZoomYStart.addWidget(self.YStartValue)
                self.layoutVZoomYStop = QVBoxLayout(self)
                self.layoutVZoomYStop.addWidget(self.labelYStopValue)
                self.layoutVZoomYStop.addWidget(self.YStopValue)
                self.layoutHZoomX = QHBoxLayout(self)
                self.layoutHZoomX.addLayout(self.layoutVZoomXStart)
                self.layoutHZoomX.addLayout(self.layoutVZoomXStop)
                self.layoutHZoomY = QHBoxLayout(self)
                self.layoutHZoomY.addLayout(self.layoutVZoomYStart)
                self.layoutHZoomY.addLayout(self.layoutVZoomYStop)
                self.layoutVZoom = QVBoxLayout(self)
                self.layoutVZoom.addWidget(self.labelPlotsize)
                self.layoutVZoom.addLayout(self.layoutHZoomX)
                self.layoutVZoom.addLayout(self.layoutHZoomY)
                self.groupboxZoom.setLayout(self.layoutVZoom)

                self.groupboxFile = QGroupBox("Plot", self)
                self.hboxPlotname = QHBoxLayout(self)
                self.hboxPlotname.addWidget(self.Plotname)
                self.hboxPlotname.addWidget(self.labelPlot)
                self.hboxStyle = QHBoxLayout(self)
                self.hboxStyle.addWidget(self.ComboStyle)
                self.hboxStyle.addWidget(self.labelStyle)
                self.hboxStyle.addWidget(self.ComboRow)
                self.hboxStyle.addWidget(self.labelRow)
                self.vboxFile = QVBoxLayout(self) 
                self.vboxFile.addLayout(self.hboxPlotname)
                self.vboxFile.addLayout(self.hboxStyle)
                self.groupboxFile.setLayout(self.vboxFile)

                self.groupboxPath = QGroupBox("File", self)
                self.hboxButton = QHBoxLayout(self)
                self.hboxButton.addWidget(self.buttonPath)
                self.hboxButton.addStretch(1)
                self.vboxPath = QVBoxLayout(self)
                self.vboxPath.addLayout(self.hboxButton)
                self.vboxPath.addWidget(self.labelPath)
                self.vboxPath.addWidget(self.labelPlotSize)
                self.hboxPath = QHBoxLayout() 
                self.hboxPath.addLayout(self.vboxPath)
                self.hboxPath.addStretch(1)
                self.hboxPath.addWidget(self.groupboxHeadlines)
                self.groupboxPath.setLayout(self.hboxPath)

                self.groupboxSave = QGroupBox("Save", self)
                self.hboxFilename = QHBoxLayout(self)
                self.hboxFilename.addWidget(self.Filename)
                self.hboxFilename.addWidget(self.labelFile)
                self.hboxSavePath = QHBoxLayout(self)
                self.hboxSavePath.addWidget(self.buttonSave)
                self.hboxSavePath.addStretch(1)
                self.hboxSavePath.addWidget(self.labelSave)
                self.hboxSaveType = QHBoxLayout(self)
                self.hboxSaveType.addWidget(self.labelSaveAs)
                self.hboxSaveType.addWidget(self.SaveAs)
                self.hboxSaveType.addStretch(1)
                self.vboxSave = QVBoxLayout(self)
                self.vboxSave.addLayout(self.hboxFilename)
                self.vboxSave.addLayout(self.hboxSavePath)
                self.vboxSave.addLayout(self.hboxSaveType)
                self.groupboxSave.setLayout(self.vboxSave)
                
                self.groupboxScaleBar = QGroupBox("ScaleBar", self)
                self.groupboxScaleBar.setCheckable(True)
                self.groupboxScaleBar.setChecked(False)
                self.hboxFontsize = QHBoxLayout()
                self.hboxFontsize.addWidget(self.ScaleBarFontsize)
                self.hboxFontsize.addWidget(self.labelScaleBarFontsize)
                self.hboxFontcolor = QHBoxLayout()
                self.hboxFontcolor.addWidget(self.FontColor)
                self.hboxFontcolor.addWidget(self.labelFontColor)
                self.hboxFontweight = QHBoxLayout()
                self.hboxFontweight.addWidget(self.ScaleBarFontweight)
                self.hboxFontweight.addWidget(self.labelScaleBarFontweight)
                self.hboxBarSize = QHBoxLayout()
                self.hboxBarSize.addWidget(self.ScaleBarSize)
                self.hboxBarSize.addWidget(self.labelScaleBarSize)
                self.hboxBarSizeVertical = QHBoxLayout()
                self.hboxBarSizeVertical.addWidget(self.ScaleBarSizeVertical)
                self.hboxBarSizeVertical.addWidget(self.labelScaleBarSizeVertical)
                self.hboxBarPosition = QHBoxLayout()
                self.hboxBarPosition.addWidget(self.ScaleBarPosition)
                self.hboxBarPosition.addWidget(self.labelScaleBarPosition)
                self.hboxBarOffset = QHBoxLayout()
                self.hboxBarOffset.addWidget(self.ScaleBarOffset)
                self.hboxBarOffset.addWidget(self.labelScaleBarOffset)
                self.vboxBar = QVBoxLayout() 
                self.vboxBar.addLayout(self.hboxBarPosition)
                self.vboxBar.addLayout(self.hboxBarOffset)
                self.vboxBar.addLayout(self.hboxBarSize)
                self.vboxBar.addLayout(self.hboxBarSizeVertical)
                self.vboxBar.addWidget(self.labelPlotSpacer4)
                self.vboxBar.addLayout(self.hboxFontsize)
                self.vboxBar.addLayout(self.hboxFontweight)
                self.vboxBar.addLayout(self.hboxFontcolor)
                self.groupboxScaleBar.setLayout(self.vboxBar)

                self.groupboxColorBar = QGroupBox("ColorBar", self)
                self.groupboxColorBar.setCheckable(True)
                self.groupboxColorBar.setChecked(False)
                self.hboxColorBarMax = QHBoxLayout()
                self.hboxColorBarMax.addWidget(self.labelColorBarMax1)
                self.hboxColorBarMax.addWidget(self.ColorBarMax)
                self.hboxColorBarMax.addWidget(self.labelColorBarMax2)
                self.hboxColorBarMin = QHBoxLayout()
                self.hboxColorBarMin.addWidget(self.labelColorBarMin1)
                self.hboxColorBarMin.addWidget(self.ColorBarMin)
                self.hboxColorBarMin.addWidget(self.labelColorBarMin2)
                self.vboxColorBar = QVBoxLayout()
                self.vboxColorBar.addLayout(self.hboxColorBarMin)
                self.vboxColorBar.addLayout(self.hboxColorBarMax)
                self.groupboxColorBar.setLayout(self.vboxColorBar)

                #Layouts
                self.tab6.layoutcbgStyle = QVBoxLayout(self)                                                                                            #Setzt ein vertikales Layout
                self.tab6.layoutcbgStyle.addWidget(self.groupboxColor)
                
                self.tab6.layoutHSpacer = QHBoxLayout(self)
                self.tab6.layoutHSpacer.addWidget(self.labelPlotSpacer)
                
                self.tab6.layoutHSpacer2 = QHBoxLayout(self)
                self.tab6.layoutHSpacer2.addWidget(self.labelPlotSpacer2)
                
                self.tab6.layoutHSpacer3 = QHBoxLayout(self)
                self.tab6.layoutHSpacer3.addWidget(self.labelPlotSpacer3)

                self.tab6.layoutVStart = QVBoxLayout(self)
                self.tab6.layoutVStart.addWidget(self.buttonPlot)
                self.tab6.layoutVStart.addStretch(1)
                

                self.tab6.layoutVMiddle1 = QVBoxLayout(self)
                self.tab6.layoutVMiddle1.addWidget(self.groupboxPath)
                self.tab6.layoutVMiddle1.addWidget(self.groupboxSave)
                self.tab6.layoutVMiddle1.addWidget(self.groupboxFile)
                self.tab6.layoutVMiddle1.addWidget(self.groupboxAxes)
                
                self.tab6.layoutVMiddle2 = QVBoxLayout(self)
                self.tab6.layoutVMiddle2.addWidget(self.groupboxZoom)
                self.tab6.layoutVMiddle2.addWidget(self.groupboxScaleBar)
                self.tab6.layoutVMiddle2.addWidget(self.groupboxColorBar)

                self.tab6.layoutHMiddle = QHBoxLayout(self)
                self.tab6.layoutHMiddle.addLayout(self.tab6.layoutVMiddle1)
                self.tab6.layoutHMiddle.addLayout(self.tab6.layoutHSpacer3)
                self.tab6.layoutHMiddle.addLayout(self.tab6.layoutVMiddle2)

                self.tab6.layoutVPath = QVBoxLayout(self)
                self.tab6.layoutVPath.addLayout(self.tab6.layoutHMiddle)
                
                self.tab6.layoutHges = QHBoxLayout(self)
                self.tab6.layoutHges.addLayout(self.tab6.layoutcbgStyle)
                self.tab6.layoutHges.addLayout(self.tab6.layoutHSpacer)
                self.tab6.layoutHges.addLayout(self.tab6.layoutVPath)
                self.tab6.layoutHges.addLayout(self.tab6.layoutHSpacer2)
                self.tab6.layoutHges.addLayout(self.tab6.layoutVStart)
                
                self.tab6.layoutEnd = QHBoxLayout(self)                                                                                                 #Setzt ein horizontales Layout
                self.tab6.layoutEnd.addStretch(1)                                                                                                       #Setzt einen Abstandshalter ein
                self.tab6.layoutEnd.addWidget(self.end6)                                                                                                #Setzt den Ende-Button          
                
                self.tab6.layoutv = QVBoxLayout(self)                                                                                                   #Setzt ein vertikales Layout
                self.tab6.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab6.layoutv.addLayout(self.tab6.layoutHges)
                self.tab6.layoutv.addStretch(1)                                                                                                         #Setzt einen Abstandshalter ein
                self.tab6.layoutv.addLayout(self.tab6.layoutEnd)                                                                                        #Fügt das Ende-Layout zum vertikalen Layout hinzu
                
                self.tab6.setLayout(self.tab6.layoutv)
                """


#-------------- Tabs zum Widget hinzufügen ------------------
                global Cite
                self.labelCite = QLabel("If HydraScan contributes to publisch a work please cite:\n" + Cite + "\nSee \"About\" for Details", self)                                                                                              #setzt ein Label    
                self.labelCite.setFont(QFont('Arial', 8))
                
                self.layout.addWidget(self.tabs)                                                                                                        #Fügt die Tabs zum Layout hinzu
                self.layout.addWidget(self.labelCite)
                self.setLayout(self.layout)                                                                                                             #Setzt das Layout als Seiten-Layout             


#---------------------- Tab Funktionen ----------------------
        def PositionToNavWin(self):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage
                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)
                
                if self.cb20.isChecked():
                        Calc = 255/63
                elif self.cb21.isChecked(): 
                        Calc = 255/127                                                                                                                  #Setzt eine CheckBox
                elif self.cb22.isChecked(): 
                        Calc = 255/255                                                                                                                  #Setzt eine CheckBox
                elif self.cb23.isChecked():
                        Calc = 255/511                                                                                                                  #Setzt eine CheckBox
                elif self.cb24.isChecked():
                        Calc = 255/1023                                                                                                                 #Setzt eine CheckBox
                elif self.cb25.isChecked():
                        Calc = 255/2047
                elif self.cb26.isChecked():
                        Calc = 255/4095
                #print("Calc: " + str(Calc))
                XStart = int(round((self.slideXStart.value()/1000)/(self.DimensionStepsX/255)))
                XStop = int(round((self.slideXStop.value()/1000)/(self.DimensionStepsX/255)))
                YStart = int(round((self.slideYStart.value()/1000)/(self.DimensionStepsY/255)))
                YStop = int(round((self.slideYStop.value()/1000)/(self.DimensionStepsY/255)))
                print("-----------2" + str(XStart) + "-" + str(XStop) + " \t " + str(YStart) + "-" + str(YStop))
                self.NavWin.PositionFromMain(XStart, YStart, XStop, YStop)
                #self.NavWin.NewDimRect(XStart, YStart, XStop, YStop)
                
        def StackSelect(self):
                if self.Stack1.isChecked():
                        self.Slope1.setChecked(False)
                self.NavWinCheckboxen()

        def SlopeSelect(self):
                if self.Slope1.isChecked():
                        self.Stack1.setChecked(False)
                self.NavWinCheckboxen()

        def NavWinIntTime(self):
                self.NavWin.spinIntTime.setValue(self.spinIntTime2.value())
                
        def NavWinBits(self, Index):
                if self.NavWin.Bits.currentIndex() != Index:
                        self.NavWin.Bits.setCurrentIndex(Index)

        def NavWinCheckboxen(self):
                if self.Subgrid1.isChecked():
                        self.NavWin.TTLSync.setChecked(True)
                else:
                        self.NavWin.TTLSync.setChecked(False)
                        
                if self.Stack1.isChecked():
                        self.NavWin.ZStack.setChecked(True)
                        self.NavWin.Slope.setChecked(False)
                else:
                        self.NavWin.ZStack.setChecked(False)
        
                if self.Slope1.isChecked():
                        self.NavWin.Slope.setChecked(True)
                        self.NavWin.ZStack.setChecked(False)
                else:
                        self.NavWin.Slope.setChecked(False)
                        
        def show_NavWin(self):
                self.NavWin = NavWin()
                self.NavWin.progress_valueCheck.connect(self.updateFromNavWinCheck)
                self.NavWin.progress_valueXY.connect(self.updateFromNavWinXY)
                self.NavWin.progress_valueButton.connect(self.updateFromNavWinButton)
                self.NavWin.position_valueXY.connect(self.updateFromNavWinPosition)
                self.NavWin.progress_Focus.connect(self.FocusFromNavWin)
                self.NavWin.show()

        def FocusFromNavWin(self, FocusNew):
                print("New Focus in Main: " + str(FocusNew))
                self.Slope1.setChecked(False)

        def updateFromNavWinPosition(self, X, Y):
                self.spinX.setValue(X)
                self.spinY.setValue(Y)

        def updateFromNavWinCheck(self, TTL, Stack, Slope, IntTime, Bits):
                self.Subgrid1.setChecked(TTL)
                self.Stack1.setChecked(Stack)
                self.Slope1.setChecked(Slope)
                self.spinIntTime2.setValue(IntTime)
                
                if Bits == 0 and self.cb20.isChecked() != True:
                        self.cb20.setChecked(True)                                                                                                      #Setzt eine CheckBox
                        self.cb21.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb22.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb23.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb24.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(False)
                if Bits == 1 and self.cb21.isChecked() != True:
                        self.cb20.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb21.setChecked(True)                                                                                                      #Setzt eine CheckBox
                        self.cb22.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb23.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb24.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(False)
                if Bits == 2 and self.cb22.isChecked() != True:
                        self.cb20.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb21.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb22.setChecked(True)                                                                                                      #Setzt eine CheckBox
                        self.cb23.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb24.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(False)
                if Bits == 3 and self.cb23.isChecked() != True:
                        self.cb20.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb21.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb22.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb23.setChecked(True)                                                                                                      #Setzt eine CheckBox
                        self.cb24.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(False)
                if Bits == 4 and self.cb24.isChecked() != True:
                        self.cb20.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb21.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb22.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb23.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb24.setChecked(True)                                                                                                      #Setzt eine CheckBox
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(False)
                if Bits == 5 and self.cb25.isChecked() != True:
                        self.cb20.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb21.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb22.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb23.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb24.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb25.setChecked(True)
                        self.cb26.setChecked(False) 
                if Bits == 6 and self.cb25.isChecked() != True:
                        self.cb20.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb21.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb22.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb23.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb24.setChecked(False)                                                                                                     #Setzt eine CheckBox
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(True)                                                                                                      #Setzt eine CheckBox
                
        def updateFromNavWinXY(self, XStart, YStart, XStop, YStop):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage
                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)

                XStart = round((XStart*(self.DimensionStepsX/255)),3)
                YStart = round((YStart*(self.DimensionStepsY/255)),3)
                XStop = round((XStop*(self.DimensionStepsX/255)),3)
                YStop = round((YStop*(self.DimensionStepsY/255)),3)

                if self.cb20.isChecked():
                        Calc = 63/255
                elif self.cb21.isChecked(): 
                        Calc = 127/255                                                                                                                  #Setzt eine CheckBox
                elif self.cb22.isChecked(): 
                        Calc = 255/255                                                                                                                  #Setzt eine CheckBox
                elif self.cb23.isChecked():
                        Calc = 511/255                                                                                                                  #Setzt eine CheckBox
                elif self.cb24.isChecked():
                        Calc = 1023/255                                                                                                                 #Setzt eine CheckBox
                elif self.cb25.isChecked():
                        Calc = 2047/255
                elif self.cb26.isChecked():
                        Calc = 4095/255


                #print("XStart: " + str(XStart) + " XStop: " + str(XStop) + " YStart: " + str(YStart) + " YStop: " + str(YStop))
                #print("XStart: " + str(self.slideXStart.value()) + " XStop: " + str(self.slideXStop.value()) + " YStart: " + str(self.slideYStart.value()) + " YStop: " + str(self.slideYStop.value()))
                
                if self.slideXStart.value() != XStart:
                        self.slideXStart.setValue(int(XStart*1000))
                if self.slideYStart.value() != YStart:
                        self.slideYStart.setValue(int(YStart*1000))
                if self.slideXStop.value() != XStop:
                        self.slideXStop.setValue(int(XStop*1000))
                if self.slideYStop.value() != YStop: 
                        self.slideYStop.setValue(int(YStop*1000))

        def updateFromNavWinButton(self, check):
                if check:
                        self.buttonStart.setChecked(True)
                else:
                        self.buttonStart.setChecked(False)
                self.StartMeasurement(check)

        def show_apd(self):
                global APDWindowOn
                try:
                        print("APD")
                        self.APDWin = APDWindow()
                        self.APDWin.show()
                        APDWindowOn = 1
                except:
                        print("APD Thread failed")
                
        def show_temp(self):
                global TempWindowOn
                try:
                        print("Temp")
                        self.TempSens = TempWindow()
                        self.TempSens.show()
                        TempWindowOn = 1
                except:
                        print("Temp Thread failed")
                        
        def show_plot(self):
                #try:
                print("Plot")
                self.PlotWin = PlotWindow()
                self.PlotWin.progress_valueRect.connect(self.updateRect)
                self.PlotWin.progress_valuePos.connect(self.updatePos)
                self.PlotWin.show()
                #APDWindowOn = 1
                #except:
                #        print("Plot Thread failed")

        def updateRect(self, val1, val2, val3, val4):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage
                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)

                XStart = round((val1*(self.DimensionStepsX/255)),3)
                YStart = round((val2*(self.DimensionStepsY/255)),3)
                XStop = round((val3*(self.DimensionStepsX/255)),3)
                YStop = round((val4*(self.DimensionStepsY/255)),3)
                
                #print("New Window: " + str(val1) + " x " + str(val2) + " --> " + str(val3) + " x " + str(val4))                                        #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.slideXStart.setValue(XStart*1000)
                self.slideYStart.setValue(YStart*1000)
                self.slideXStop.setValue(XStop*1000)
                self.slideYStop.setValue(YStop*1000)

        def updatePos(self, val1, val2):
                #print("New Position: " + str(val1) + " x " + str(val2))
                self.slideX.setValue(int(val1))
                self.slideY.setValue(int(val2))

        def ResizeLivePlot(self, NewXStart, NewXStop, NewYStart, NewYStop, bits):
                self.PlotWin.Resize(NewXStart, NewXStop, NewYStart, NewYStop, bits)

        #Tab1 - Motor Funktionen definieren
        def IntChange(self):
                if self.buttonPos.isChecked():
                        self.clickedPos(False)
                        self.clickedPos(True)  
                
        def positionX(self):                                                                                                                            #Funktion setzt die Geschwindigkeitsvariable des ersten Motors auf den Wert des Sliders (Tab1)
                global FullRangeDeviceX

                checkedBits = self.cbg1.checkedId()
                if checkedBits == 0:
                        self.bitval = 63
                elif checkedBits == 1:
                        self.bitval = 127
                elif checkedBits == 2:
                        self.bitval = 255
                elif checkedBits == 3:
                        self.bitval = 511
                elif checkedBits == 4:
                        self.bitval = 1023
                elif checkedBits == 5:
                        self.bitval = 2047
                elif checkedBits == 6:
                        self.bitval = 4095                                                                                                              #Gibt den Wert des Sliders im cmd aus
                self.PositionX = (self.slideX.value())                                                                                                  #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                NewVal = round((self.slideX.value()*((FullRangeDeviceX/1000)/(self.bitval))),3)
                if self.spinX.value() != NewVal:
                        self.spinX.setValue(NewVal)                                                                                                     #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())             
        
        def spinboxX(self):                                                                                                                             #Funktion setzt die Geschwindigkeitsvariable des ersten Motors auf den Wert der Zahlenauswahlbox (Tab1)
                global FullRangeDeviceX

                checkedBits = self.cbg1.checkedId()
                if checkedBits == 0:
                        self.bitval = 63
                elif checkedBits == 1:
                        self.bitval = 127
                elif checkedBits == 2:
                        self.bitval = 255
                elif checkedBits == 3:
                        self.bitval = 511
                elif checkedBits == 4:
                        self.bitval = 1023
                elif checkedBits == 5:
                        self.bitval = 2047
                elif checkedBits == 6:
                        self.bitval = 4095                                                                                                              #Gibt den Wert der Zahlauswahlbox im cmd aus
                self.PositionX = int(round((self.spinX.value()*1000)/((FullRangeDeviceX/1000)/self.bitval)/1000,0))
                if self.slideX.value() != self.PositionX:
                        self.slideX.setValue(int(self.PositionX))                                                                                       #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())                                                                             #Ruft die clickedM1-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                
        def positionY(self):                                                                                                                            #Funktion setzt die Geschwindigkeitsvariable des zweiten Motors auf den Wert des Sliders (Tab1)
                global FullRangeDeviceY 

                checkedBits = self.cbg1.checkedId()
                if checkedBits == 0:
                        self.bitval = 63
                elif checkedBits == 1:
                        self.bitval = 127
                elif checkedBits == 2:
                        self.bitval = 255
                elif checkedBits == 3:
                        self.bitval = 511
                elif checkedBits == 4:
                        self.bitval = 1023
                elif checkedBits == 5:
                        self.bitval = 2047
                elif checkedBits == 6:
                        self.bitval = 4095                                                                                                              #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden

                self.PositionY = (self.slideY.value())                                                                                                  #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                NewVal = round((self.slideY.value()*((FullRangeDeviceY/1000)/(self.bitval))),3)
                if self.spinY.value() != NewVal:
                        self.spinY.setValue(NewVal)                                                                                                     #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())    
                
        def spinboxY(self):                                                                                                                             #Funktion setzt die Geschwindigkeitsvariable des zweiten Motors auf den Wert der Zahlenauswahlbox (Tab1)
                global FullRangeDeviceY 

                checkedBits = self.cbg1.checkedId()
                if checkedBits == 0:
                        self.bitval = 63
                elif checkedBits == 1:
                        self.bitval = 127
                elif checkedBits == 2:
                        self.bitval = 255
                elif checkedBits == 3:
                        self.bitval = 511
                elif checkedBits == 4:
                        self.bitval = 1023
                elif checkedBits == 5:
                        self.bitval = 2047
                elif checkedBits == 6:
                        self.bitval = 4095                                                                                                              #Gibt den Wert der Zahlauswahlbox im cmd aus
                self.PositionY = int(round((self.spinY.value()*1000)/((FullRangeDeviceY/1000)/self.bitval)/1000,0))
                if self.slideY.value() != self.PositionY:
                        self.slideY.setValue(int(self.PositionY))                                                                                       #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())                                                                             #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
        
        def clickedPos(self, down):          
                if down:                                                                                                                                #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        
                        try:
                                self.APDWin.StopMeasure()
                        except:
                                pass
                        self.buttonPoint.setChecked(0)
                        self.buttonPoint.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPoint.setText("Start Measurement")
                        self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.buttonPos.setToolTip("Stops the Positioning") 
                        self.buttonPos.setText("Stop Positioning")
                        self.buttonPos.setStyleSheet("background-color: rgb(255,63,0)")

                        if self.flyingcircus == 1:
                                self.FlyingCircus.killFred()
                                self.flyingcircus = 0
                        
                        if self.XSlope != self.YSlope:
                                self.XSlopePosition = (self.PositionX * (self.XSlope/self.bitval))
                                self.YSlopePosition = (self.PositionY * (self.YSlope/self.bitval))
                                self.SlopePosition = (self.XSlopePosition + self.YSlopePosition)
                                self.SlopeVal = ((((self.SlopePosition) / 4000) * self.bitval))
                        else:
                                self.SlopeVal = FocusZ
                        print("Position: ", self.PositionX, " x ", self.PositionY, " x ", self.SlopeVal)
                        
                        dacX.set_voltage(int(self.PositionX*(4095 / self.bitval)))
                        dacY.set_voltage(int(self.PositionY*(4095 / self.bitval)))
                        dacZ.set_voltage(int(self.SlopeVal))
                        
                        integrationtime = self.spinIntTime1.value()
                        
                        CH1 = self.cbch11.isChecked()
                        CH2 = self.cbch12.isChecked()
                        CH3 = self.cbch13.isChecked()
                        CH4 = self.cbch14.isChecked()
                        CHA = self.cbch15.isChecked()
                        CHB = self.cbch16.isChecked()
                        L2 = self.cbch17.isChecked()
                        L3 = self.cbch18.isChecked()
                        if CH1 == False:
                                self.updateVal1(-1)
                        if CH2 == False:
                                self.updateVal2(-1)
                        if CH3 == False:
                                self.updateVal3(-1)
                        if CH4 == False:
                                self.updateVal4(-1)
                        if CHA == False:
                                self.updateValA(-1)
                        if CHB == False:
                                self.updateValB(-1)
                        if L2 == False:
                                self.updateValL2(-1)
                        if L3 == False:
                                self.updateValL3(-1)
                        
                        if self.monty == 0:
                                self.Monty = Positioning(integrationtime,CH1,CH2,CH3,CH4,CHA,CHB,L2,L3)                                                 #Übergibt die Werte an den Thread
                                self.Monty.progress_value1.connect(self.updateVal1)
                                self.Monty.progress_value2.connect(self.updateVal2)
                                self.Monty.progress_value3.connect(self.updateVal3)
                                self.Monty.progress_value4.connect(self.updateVal4)
                                self.Monty.progress_value5.connect(self.updateValA)
                                self.Monty.progress_value6.connect(self.updateValB)
                                self.Monty.progress_value7.connect(self.updateValL2)
                                self.Monty.progress_value8.connect(self.updateValL3)
                                self.Monty.start()      
                                self.monty = 1
                                #self.Calculator = Calculator(q)
                                #self.Calculator.start()
                else:
                        try:
                                self.Monty.killFred()
                        except:
                                print("No Monty")
                        
                        try:
                                if APDWindowOn == 1:
                                        self.APDWin.StartMeasure()
                        except:
                                pass
                        
                        self.buttonPos.setToolTip("Starts the Positioning") 
                        self.buttonPos.setText("Start Positioning")                                                                                     #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPos.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                        self.textVal.setText("None")
                        self.textVal2.setText("None")
                        self.textVal3.setText("None")
                        self.textVal4.setText("None")
                        self.textVal5.setText("None")
                        self.textVal6.setText("None")
                        self.textVal7.setText("None")
                        self.textVal8.setText("None")
                        self.monty = 0

        def buttonPointUnchecked(self, val):
                if val == 1:
                        self.buttonPoint.setToolTip("Starts the Measurement")
                        self.buttonPoint.setChecked(False) 
                        self.buttonPoint.setText("Start Measurement")
                        self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.flyingcircus = 0

        def clickedPoint(self, down):                                                                                                                   #Setzt die Position
                if down:                                                                                                                                #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        global FocusZ
                        try:
                                self.APDWin.StopMeasure()
                        except:
                                pass
                        self.buttonPoint.setToolTip("Stops the Measurement") 
                        self.buttonPoint.setText("Stop Measurement")                                                                                    #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPoint.setStyleSheet("background-color: rgb(255,63,0)")
                        self.buttonPos.setChecked(0)
                        self.buttonPos.setToolTip("Starts the Positioning") 
                        self.buttonPos.setText("Start Positioning")
                        self.buttonPos.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        
                        try:
                                self.Monty.killFred()
                                self.monty = 0
                        except:
                                print("No Monty")

                        integrationtime = self.spinIntTime1.value()
                        CH1 = self.cbch11.isChecked()
                        CH2 = self.cbch12.isChecked()
                        CH3 = self.cbch13.isChecked()
                        CH4 = self.cbch14.isChecked()
                        CHA = self.cbch15.isChecked()
                        CHB = self.cbch15.isChecked()
                        L2 = self.cbch15.isChecked()
                        L3 = self.cbch15.isChecked()
                        if CH1 == False:
                                self.updateVal1(-1)
                        if CH2 == False:
                                self.updateVal2(-1)
                        if CH3 == False:
                                self.updateVal3(-1)
                        if CH4 == False:
                                self.updateVal4(-1)
                        if CHA == False:
                                self.updateValA(-1)
                        if CHB == False:
                                self.updateValB(-1)
                        if L2 == False:
                                self.updateValL2(-1)
                        if L3 == False:
                                self.updateValL3(-1)
                        
                        PointDelay = self.PointDelay.value()
                        TTLsendPoint = self.groupboxSendTTL1.isChecked()
                        TTLgetPoint = self.TTLgetPoint1.isChecked()

                        if self.XSlope != self.YSlope:
                                self.XSlopePosition = (self.PositionX * (self.XSlope/self.bitval))
                                self.YSlopePosition = (self.PositionY * (self.YSlope/self.bitval))
                                self.SlopePosition = (self.XSlopePosition + self.YSlopePosition)
                                self.SlopeVal = ((((self.SlopePosition) / 4000) * self.bitval))
                        else:
                                self.SlopeVal = FocusZ
                        print("Position: ", self.PositionX, " x ", self.PositionY, " x ", self.SlopeVal)

                        XPoint = self.PositionX
                        YPoint = self.PositionY
                        ZPoint = self.SlopeVal

                        checkedBits = self.cbg1.checkedId()

                        if checkedBits == 0:
                                BitsPoint = 64                        
                        elif checkedBits == 1:
                                BitsPoint = 128
                        elif checkedBits == 2:
                                BitsPoint = 256
                        elif checkedBits == 3:
                                BitsPoint = 512
                        elif checkedBits == 4:
                                BitsPoint = 1024
                        elif checkedBits == 5:
                                BitsPoint = 2048
                        elif checkedBits == 6:
                                BitsPoint = 4096

                        if self.flyingcircus == 0:
                                self.FlyingCircus = Pointmeasurement(integrationtime,CH1,CH2,CH3,CH4,CHA,CHB,L2,L3,TTLsendPoint,TTLgetPoint,PointDelay, XPoint, YPoint, ZPoint, BitsPoint)                                                                                        #Übergibt die Werte an den Thread
                                self.FlyingCircus.progress_value1.connect(self.updateVal1)
                                self.FlyingCircus.progress_value2.connect(self.updateVal2)
                                self.FlyingCircus.progress_value3.connect(self.updateVal3)
                                self.FlyingCircus.progress_value4.connect(self.updateVal4)
                                self.FlyingCircus.progress_value5.connect(self.updateValA)
                                self.FlyingCircus.progress_value6.connect(self.updateValB)
                                self.FlyingCircus.progress_value7.connect(self.updateValL2)
                                self.FlyingCircus.progress_value8.connect(self.updateValL3)
                                self.FlyingCircus.progress_value.connect(self.buttonPointUnchecked)
                                self.FlyingCircus.start()       
                                self.flyingcircus = 1
                else:
                        try:
                               self.FlyingCircus.killFred()
                        except:
                               print("No FlyingCircus")
                        
                        try:
                                if APDWindowOn == 1:
                                        self.APDWin.StartMeasure()
                        except:
                                pass
                                
                        self.buttonPoint.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPoint.setText("Start Measurement")
                        self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                        self.textVal.setText("None")
                        self.textVal2.setText("None")
                        self.textVal3.setText("None")
                        self.textVal4.setText("None")
                        self.textVal5.setText("None")
                        self.textVal6.setText("None")
                        self.textVal7.setText("None")
                        self.textVal8.setText("None")
                        self.flyingcircus = 0



        def updateVal1(self, val):
                self.textVal.setText(str(val))
                if val == -1:
                        self.textVal.setText("None")

        def updateVal2(self, val):
                self.textVal2.setText(str(val))
                if val == -1:
                        self.textVal2.setText("None")

        def updateVal3(self, val):
                self.textVal3.setText(str(val))
                if val == -1:
                        self.textVal3.setText("None")

        def updateVal4(self, val):
                self.textVal4.setText(str(val))
                if val == -1:
                        self.textVal4.setText("None")

        def updateValA(self, val):
                integrationtime = self.spinIntTime1.value()
                self.textVal5.setText(str(val) + " counts\t" + str(round(val/integrationtime,1)) + " kHz")
                if val == -1:
                        self.textVal5.setText("None")

        def updateValB(self, val):
                integrationtime = self.spinIntTime1.value()
                self.textVal6.setText(str(val) + " counts\t" + str(round(val/integrationtime,1)) + " kHz")
                if val == -1:
                        self.textVal6.setText("None")

        def updateValL2(self, val):
                integrationtime = self.spinIntTime1.value()
                self.textVal7.setText(str(val) + " counts\t" + str(round(val/integrationtime,1)) + " kHz")
                if val == -1:
                        self.textVal7.setText("None")

        def updateValL3(self, val):
                integrationtime = self.spinIntTime1.value()
                self.textVal8.setText(str(val) + " counts\t" + str(round(val/integrationtime,1)) + " kHz")
                if val == -1:
                        self.textVal8.setText("None")

        def CBCH1LogicSelected(self):                                                                                                                   #wird zweimal ausgeführt, da bei einem stateChange in der ButtonGroup immer zwei Werte geändert werden (eine box wird unchecked eine wird gechecked)
                if self.cbch15.isChecked() == True or self.cbch16.isChecked() == True or self.cbch17.isChecked() == True or self.cbch18.isChecked() == True:
                        self.spinIntTime1.setVisible(True)
                        self.labelIntTime1.setVisible(True)
                else:
                        self.spinIntTime1.setVisible(False)
                        self.labelIntTime1.setVisible(False)
                

        def stopAll(self):                                                                                                                              #wird zweimal ausgeführt, da bei einem stateChange in der ButtonGroup immer zwei Werte geändert werden (eine box wird unchecked eine wird gechecked)
                if self.cbch15.isChecked() == True or self.cbch16.isChecked() == True or self.cbch17.isChecked() == True or self.cbch18.isChecked() == True:
                        self.spinIntTime1.setVisible(True)
                        self.labelIntTime1.setVisible(True)
                else:
                        self.spinIntTime1.setVisible(False)
                        self.labelIntTime1.setVisible(False)
                        
                self.buttonPos.setChecked(0)
                self.buttonPoint.setChecked(0) 
                self.buttonPos.setText("Start Positioning") 
                self.buttonPos.setToolTip("Starts the Positioning")                                                                                     #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                self.buttonPos.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonPoint.setText("Start Measurement")
                self.buttonPoint.setToolTip("Starts the Measurement")                                                                                   #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                dacX.set_voltage(0)
                dacY.set_voltage(0)
                dacZ.set_voltage(0)
                bitvalOld = self.bitval-1
                checkedBits = self.cbg1.checkedId()
                XPosOld = self.slideX.value()
                YPosOld = self.slideY.value()
                if checkedBits == 0:
                        self.bitval = 64
                elif checkedBits == 1:
                        self.bitval = 128
                elif checkedBits == 2:
                        self.bitval = 256
                elif checkedBits == 3:
                        self.bitval = 512
                elif checkedBits == 4:
                        self.bitval = 1024
                elif checkedBits == 5:
                        self.bitval = 2048
                elif checkedBits == 6:
                        self.bitval = 4096
                self.slideX.setMaximum(self.bitval-1)
                self.slideY.setMaximum(self.bitval-1)
                self.slideX.setValue(int((XPosOld/bitvalOld)*(self.bitval-1)))
                self.slideY.setValue(int((YPosOld/bitvalOld)*(self.bitval-1)))
                self.spinX.setMaximum(FullRangeDeviceX/1000)
                self.spinY.setMaximum(FullRangeDeviceY/1000)
                self.spinX.setSingleStep(round((FullRangeDeviceX/1000)/(self.bitval-1),3))
                self.spinY.setSingleStep(round((FullRangeDeviceY/1000)/(self.bitval-1),3))


        #Tab2 - Funktion um die Spannung zu halten
        def slideXstart(self):                                                                                                                          #Gibt den Wert des Sliders im cmd aus
                global FullRangeDeviceX
                NewVal = int(self.slideXStart.value()/1000)
                print(NewVal)
                if NewVal != self.spinXStart.value():
                        self.StartX = (NewVal / 100)                                                                                                    #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStart.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStop.setMinimum(NewVal)
                        self.spinXStop.setMinimum(NewVal)
                        self.updateProgTime()
                        self.PositionToNavWin()
        
        def spinXstart(self):                                                                                                                           #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                global FullRangeDeviceX
                NewVal = int(self.spinXStart.value()*1000)
                if NewVal != self.slideXStart.value():
                        self.slideXStart.setValue(NewVal)                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStop.setMinimum(NewVal)
                        self.spinXStop.setMinimum(self.spinXStart.value())                                                                              #Gibt den Wert des Sliders im cmd aus
                        self.StartX = (NewVal / 100)
                        self.updateProgTime()
                        self.PositionToNavWin()

        def slideYstart(self):                                                                                                                          #Gibt den Wert des Sliders im cmd aus
                global FullRangeDeviceY
                NewVal = int(self.slideYStart.value()/1000)
                if NewVal != self.spinYStart.value():
                        self.StartY = (NewVal / 100)                                                                                                    #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStart.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStop.setMinimum(NewVal)
                        self.spinYStop.setMinimum(NewVal)
                        self.updateProgTime()
                        self.PositionToNavWin()
        
        def spinYstart(self):                                                                                                                           #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                global FullRangeDeviceY
                NewVal = int(self.spinYStart.value()*1000)
                if NewVal != self.slideYStart.value():
                        self.slideYStart.setValue(NewVal)                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStop.setMinimum(NewVal)
                        self.spinYStop.setMinimum(self.spinYStart.value())                                                                              #Gibt den Wert des Sliders im cmd aus
                        self.StartY = (NewVal / 100)
                        self.updateProgTime()
                        self.PositionToNavWin()
        
        def slideXstop(self,x):                                                                                                                         #Gibt den Wert des Sliders im cmd aus
                global FullRangeDeviceX
                NewVal = int(self.slideXStop.value()/1000)
                if NewVal != self.spinXStop.value():
                        self.StopX = (NewVal / 100)                                                                                                     #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStop.setValue(NewVal)                                                                                                 #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.updateProgTime()
                        self.PositionToNavWin()
                
        def spinXstop(self,x):
                global FullRangeDeviceX
                NewVal = int(self.spinXStop.value()*1000)
                if NewVal != self.slideXStop.value():
                        self.StopX = (NewVal / 100)                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideXStop.setValue(NewVal)
                        self.updateProgTime()
                        self.PositionToNavWin()
                
        def slideYstop(self,x):
                global FullRangeDeviceY
                NewVal = int(self.slideYStop.value()/1000)
                if NewVal != self.spinYStop.value:
                        self.StopY = (NewVal / 100)                                                                                                     #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStop.setValue(NewVal) 
                        self.updateProgTime()
                        self.PositionToNavWin()
                
        def spinYstop(self,x):                                                                                                                          #Funktion setzt die Geschwindigkeitsvariable des zweiten Motors auf den Wert der Zahlenauswahlbox (Tab1)
                global FullRangeDeviceY
                NewVal = int(self.spinYStop.value()*1000)
                if NewVal != self.slideYStop.value():
                        self.StopY = (NewVal / 100)                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideYStop.setValue(NewVal)
                        self.updateProgTime()
                        self.PositionToNavWin()
                
        def savesettingsScanMeasure(self):
                name = self.nameMeasure.text()
                if len(name) == 0:
                        name = time.strftime("%d.%m.%Y %H:%M:%S")
                bits = self.cbg2.checkedId()
                xstart = self.slideXStart.value()
                xstop = self.slideXStop.value()
                ystart = self.slideYStart.value()
                ystop = self.slideYStop.value()
                plot = self.Plot1.isChecked()
                slope = self.Slope1.isChecked()
                stack = self.Stack1.isChecked()
                subgrid = self.Subgrid1.isChecked()
                
                if plot == True:
                        plot = 1
                else:
                        plot = 0

                if slope == True:
                        slope = 1
                else:
                        slope = 0

                if subgrid == True:
                        subgrid = 1
                else:
                        subgrid = 0
                
                MeasureSet.execute("INSERT INTO settingsScanMeasure (name, bits, xstart, xstop, ystart, ystop, slope, subgrid, stack, plot) VALUES (\"" + name + "\", " + str(bits) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(slope) + ", " + str(subgrid) + ", " + str(stack) + ", " + str(plot) + ")")
                MeasureSet.execute("SELECT * FROM settingsScanMeasure")
                #print(MeasureSet.fetchall())
                connMeasure.commit()
                self.namesMeasure.addItem(name)
                
        def usesettingsScanMeasure(self):
                set = self.namesMeasure.currentText()
                MeasureSet.execute(("SELECT * FROM settingsScanMeasure WHERE name = \"") + set + ("\""))
                for dsatzMeasure in MeasureSet:
                        name = dsatzMeasure[0]
                        bits = dsatzMeasure[1]
                        xstart = dsatzMeasure[2]
                        xstop = dsatzMeasure[3]
                        ystart = dsatzMeasure[4]
                        ystop = dsatzMeasure[5]
                        slope = dsatzMeasure[6]
                        subgrid = dsatzMeasure[7]
                        stack = dsatzMeasure[8]
                        plot = dsatzMeasure[9]
                        #print(str(name) + ", " + str(bits) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(slope) + ", " + str(subgrid) + ", " + str(plot))

                if bits == 0:
                        self.cb20.setChecked(True)                
                elif bits == 1:
                        self.cb21.setChecked(True)
                elif bits == 2:
                        self.cb22.setChecked(True)
                elif bits == 3:
                        self.cb23.setChecked(True)
                elif bits == 4:
                        self.cb24.setChecked(True)
                elif bits == 5:
                        self.cb25.setChecked(True)
                elif bits == 6:
                        self.cb26.setChecked(True)
                elif bits == -1:
                        self.cb20.setChecked(False)
                        self.cb21.setChecked(False)
                        self.cb22.setChecked(False)
                        self.cb23.setChecked(False)
                        self.cb24.setChecked(False)
                        self.cb25.setChecked(False)
                        self.cb26.setChecked(False)

                        
                self.slideXStart.setValue(int(xstart))
                self.slideXStop.setValue(int(xstop))
                self.slideYStart.setValue(int(ystart))
                self.slideYStop.setValue(int(ystop))
                self.Slope1.setChecked(slope)
                self.Subgrid1.setChecked(subgrid)
                self.Stack1.setChecked(stack)
                self.Plot1.setChecked(plot)

                connMeasure.commit()
        
        def clickedStart(self, down):                                                                                                                   #Setzt das Messfenster
                if down:
                        self.StartX = self.slideXStart.value()
                        self.StartY = self.slideYStop.value()
                        self.StopX = self.slideXStart.value()
                        self.StopY = self.slideYStop.value()
                        #print ("Start: ", self.StartX, " x ", self.StartY)                                                                             #Gibt die Richtung im cmd aus
                        #print ("Stop: ", self.StopX, " x ", self.StopY)                                                                                #Gibt den Geschwindigkeitswert im cmd aus
                        self.buttonStart.setToolTip("Stops the Measurement")                                                                            #Gibt den Geschwindigkeitswert im cmd aus
                        self.buttonStart.setText("Stop")
                        self.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")                                                               #Gibt den Geschwindigkeitswert im cmd aus
                        self.NavWin.buttonStart.setToolTip("Stops the Measurement")                                                                     #Gibt den Geschwindigkeitswert im cmd aus
                        self.NavWin.buttonStart.setText("Stop")
                        self.NavWin.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")
                else:
                        self.buttonStart.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setText("Start")
                        self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.NavWin.buttonStart.setToolTip("Starts the Measurement")                                                                    #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setText("Start")
                        self.NavWin.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.buttonUnchecked()
                        try:
                                self.Manfred.killFred()
                        except:
                                print("Thread not running")
                
        def stopAll2(self):                                                                                                                             #wird zweimal ausgeführt, da bei einem stateChange in der ButtonGroup immer zwei Werte geändert werden (eine box wird unchecked eine wird gechecked)
                global FullRangeDeviceX
                global FullRangeDeviceY
                self.buttonStart.setChecked(0)
                self.buttonStart.setToolTip("Starts the Measurement")                                                                                   #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                self.buttonStart.setText("Start")
                self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.NavWin.buttonStart.setChecked(0)
                self.NavWin.buttonStart.setToolTip("Starts the Measurement")                                                                            #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                self.NavWin.buttonStart.setText("Start")
                self.NavWin.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                checkedBits = self.cbg2.checkedId()
                self.NavWinBits(checkedBits)
                bitvalOld2 = self.bitval2
                if checkedBits == 0:
                        self.bitval2 = 63
                        self.cb30.setChecked(True)                                                                                                      #Setzt eine CheckBox
                        self.cb31.setChecked(False)                                                                  
                        self.cb32.setChecked(False)                                                                 
                        self.cb33.setChecked(False)                                                                   
                        self.cb34.setChecked(False)                                                                
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(False)
                elif checkedBits == 1:
                        self.bitval2 = 127
                        self.cb30.setChecked(False)                                                                  
                        self.cb31.setChecked(True)                                                                     
                        self.cb32.setChecked(False)                                                                   
                        self.cb33.setChecked(False)                                                             
                        self.cb34.setChecked(False)                                                        
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(False)
                elif checkedBits == 2:
                        self.bitval2 = 255
                        self.cb30.setChecked(False)                                                               
                        self.cb31.setChecked(False)                                                               
                        self.cb32.setChecked(True)                                                               
                        self.cb33.setChecked(False)                                                        
                        self.cb34.setChecked(False)                                                              
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(False)
                elif checkedBits == 3:
                        self.bitval2 = 511
                        self.cb30.setChecked(False)                                                                 
                        self.cb31.setChecked(False)                                                             
                        self.cb32.setChecked(False)                                                              
                        self.cb33.setChecked(True)                                                                   
                        self.cb34.setChecked(False)                                                                 
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(False)
                elif checkedBits == 4:
                        self.bitval2 = 1023
                        self.cb30.setChecked(False)                                                                  
                        self.cb31.setChecked(False)                                                                 
                        self.cb32.setChecked(False)                                                                 
                        self.cb33.setChecked(False)                                                               
                        self.cb34.setChecked(True)                                                                 
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(False)
                elif checkedBits == 5:
                        self.bitval2 = 2047
                        self.cb30.setChecked(False)                                                                  
                        self.cb31.setChecked(False)                                                                    
                        self.cb32.setChecked(False)                                                                  
                        self.cb33.setChecked(False)                                                                 
                        self.cb34.setChecked(False)                                                                  
                        self.cb35.setChecked(True)
                        self.cb36.setChecked(False)
                elif checkedBits == 6:
                        self.bitval2 = 4095
                        self.cb30.setChecked(False)                                                                   
                        self.cb31.setChecked(False)                                                                 
                        self.cb32.setChecked(False)                                                                
                        self.cb33.setChecked(False)                                                                  
                        self.cb34.setChecked(False)                                                                  
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(True)
                """        
                NewValXStart = int((self.slideXStart.value()/bitvalOld2)*self.bitval2)
                NewValYStart = int((self.slideYStart.value()/bitvalOld2)*self.bitval2)
                NewValXStop = int((self.slideXStop.value()/bitvalOld2)*self.bitval2)
                NewValYStop = int((self.slideYStop.value()/bitvalOld2)*self.bitval2)
                self.spinXStart.setMaximum(FullRangeDeviceX/1000)
                self.spinXStop.setMaximum(FullRangeDeviceX/1000)
                self.spinYStart.setMaximum(FullRangeDeviceY/1000)
                self.spinYStop.setMaximum(FullRangeDeviceY/1000)
                self.spinXStart.setSingleStep(round((FullRangeDeviceX/1000)/self.bitval2,3))
                self.spinXStop.setSingleStep(round((FullRangeDeviceX/1000)/self.bitval2,3))
                self.spinYStart.setSingleStep(round((FullRangeDeviceY/1000)/self.bitval2,3))
                self.spinYStop.setSingleStep(round((FullRangeDeviceY/1000)/self.bitval2,3))
                self.slideXStart.setMaximum(self.bitval2)
                self.slideXStop.setMaximum(self.bitval2)
                self.slideYStart.setMaximum(self.bitval2)
                self.slideYStop.setMaximum(self.bitval2)
                self.slideXStart.setValue(int(NewValXStart))
                self.slideXStop.setValue(int(NewValXStop))
                self.slideYStart.setValue(int(NewValYStart))
                self.slideYStop.setValue(int(NewValYStop))
                """
                self.stopAll3()
        
        def buttonUnchecked(self, val):
                if val == 1:
                        self.buttonStart.setToolTip("Start the Measurement")
                        self.buttonStart.setChecked(False)
                        self.buttonStart.setText("Start")
                        self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.NavWin.UncheckButton()
                        """
                        self.NavWin.buttonStart.setToolTip("Start the Measurement")
                        self.NavWin.buttonStart.setChecked(False)
                        self.NavWin.buttonStart.setText("Start")
                        self.NavWin.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        """
                        self.progress1.setValue(100)
                        try:
                                if APDWindowOn == 1:
                                        self.APDWin.StartMeasure()
                        except:
                                pass

                        try:
                                if TempWindowOn == 1:
                                        self.TempSens.StartMeasure()
                        except:
                                pass

        def buttonChecked(self):
                self.buttonStart.setToolTip("Stop the Measurement")
                self.buttonStart.setText("Stop")
                self.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")
                self.buttonStart.setChecked(True)
                self.NavWin.buttonStart.setToolTip("Stop the Measurement")
                self.NavWin.buttonStart.setText("Stop")
                self.NavWin.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")
                self.NavWin.buttonStart.setChecked(True)

        def StartMeasurement(self, down):
                print("!_________________________________!")
                print(down)
                
                print("Messung gestartet")

                global PlotStyle
                global PlotName
                global FileName
                global FilePath
                global TTL1IN
                global TTL1OUT
                global TTL2IN
                global TTL2OUT
                global Wire1
                global Wire2

                integrationtime = self.spinIntTime2.value()
                xstart = self.spinXStart.value()
                #xstop = self.slideXStop.value()
                ystart = self.spinYStart.value()
                #ystop = self.slideYStop.value()
                XOffset = int(xstart / (100/4096))
                YOffset = int(ystart / (100/4096))
                xDim = self.NavWin.SpinX.value()
                yDim = self.NavWin.SpinY.value()
                Volts = self.NavWin.Volts.currentText()
                Volts = round(xDim/10, 1)
                print("Measurement Dims: " + str(xDim) + " x " + str(yDim) + "\t" + str(Volts) + " V")
                print("Measurement Offset: " + str(xstart) + " x " + str(ystart) + "\t" + str(XOffset) + " x " + str(YOffset))
                bits = self.cbg2.checkedId()
                plot = self.Plot1.isChecked()
                colors = PlotStyle
                plotname = PlotName
                filename = FileName
                filepath = FilePath
                slope = self.Slope1.isChecked()
                subgrid = self.Subgrid1.isChecked()
                delaytime = self.delay.value()
                SetXSlope = self.XSlope
                SetYSlope = self.YSlope
                xstartsub = self.slideXStart2.value()
                xstopsub = self.slideXStop2.value()
                ystartsub = self.slideYStart2.value()
                ystopsub = self.slideYStop2.value()
                xstep = self.slideXStep.value() 
                ystep = self.slideYStep.value()
                steptime = self.spinStepTime.value()
                sendTTL = self.groupboxSendTTL3.isChecked()
                getTTL = self.TTLgetPoint2.isChecked()
                channeltimeing = self.channeltimeing.isChecked()
                DoStacks = self.Stack1.isChecked()
                stacks = self.StackCount.value()
                stackstep = self.ZStepsize.value()
                direct = self.ZDirection.currentIndex()
                ZStart = self.ZStartSpin.value()

                #TTL definition                
                QuelleTTL = self.TTLroot.currentIndex()
                if QuelleTTL == 0:
                        TTLOUT = TTL1OUT
                        TTLIN = TTL1IN
                        if Wire1 == 1:
                                OneWire = 1
                        else:
                                OneWire = 0
                else:
                        TTLOUT = TTL2OUT
                        TTLIN = TTL2IN
                        if Wire2 == 1:
                                OneWire = 1
                        else:
                                OneWire = 0
                
                #Channel definition
                channel = [self.cbch21.isChecked(), self.cbch22.isChecked(), self.cbch23.isChecked(), self.cbch24.isChecked(), self.cbch25.isChecked(), self.cbch26.isChecked(), self.cbch27.isChecked(), self.cbch28.isChecked()]
                if channel[0] == True:
                        channel[0] = 1
                else:
                        channel[0] = 0
                if channel[1] == True:
                        channel[1] = 1
                else:
                        channel[1] = 0  
                if channel[2] == True:
                        channel[2] = 1
                else:
                        channel[2] = 0  
                if channel[3] == True:
                        channel[3] = 1
                else:
                        channel[3] = 0  
                if channel[4] == True:
                        channel[4] = 1
                else:
                        channel[4] = 0   
                if channel[5] == True:
                        channel[5] = 1
                else:
                        channel[5] = 0   
                if channel[6] == True:
                        channel[6] = 1
                else:
                        channel[6] = 0   
                if channel[7] == True:
                        channel[7] = 1
                else:
                        channel[7] = 0 


                #Start the Measurement-Thread        
                if down:
                        self.buttonStart.setToolTip("Stops the Measurement")                                                                            #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setText("Stop")
                        self.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")
                        self.NavWin.buttonStart.setToolTip("Stops the Measurement")                                                                     #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setText("Stop")
                        self.NavWin.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")

                        try:
                                self.APDWin.StopMeasure()
                        except:
                                pass
                        try:
                                self.TempSens.StopMeasure()
                        except:
                                pass

                        q = Queue()
                        q2 = Queue()

                        if bits == 0:
                                bitval = 63 
                        elif bits == 1:
                                bitval = 127                                                                                                            #Gibt die Verstärkung im cmd aus
                        elif bits == 2:         
                                bitval = 255                                                                                                            #Gibt die Verstärkung im cmd aus
                        elif bits == 3:
                                bitval = 511                                                                                                            #Gibt die Verstärkung im cmd aus
                        elif bits == 4:
                                bitval = 1023                                                                                                           #Gibt die Verstärkung im cmd aus
                        elif bits == 5:
                                bitval = 2047                                                                                                           #Gibt die Verstärkung im cmd aus
                        elif bits == 6:
                                bitval = 4095
                        xstartResize = 0
                        ystartResize = 0
                        xstopResize = bitval
                        ystopResize = bitval
                        print("Bits: " + str(bits) + " - " + str(bitval))
                        self.ResizeLivePlot(xstartResize, xstopResize, ystartResize, ystopResize, bits)

                        self.Manfred = Measurement(q, integrationtime, channel, xDim, yDim, XOffset, YOffset, delaytime, bits, slope, subgrid, plot, SetXSlope, SetYSlope, xstartsub, xstopsub, ystartsub, ystopsub, xstep, ystep, steptime, sendTTL, getTTL, TTLOUT, TTLIN, OneWire, channeltimeing, DoStacks, stacks, stackstep, direct, ZStart, colors, plotname, filename, filepath)                                 #Übergibt die Werte an den Thread
                        self.Manfred.progress_value.connect(self.buttonUnchecked)
                        self.Manfred.progress_bar.connect(self.updateProgressBar1)
                        
                        self.ManfredsStomach = Calculator(q, q2, integrationtime, xstartResize, xstopResize, ystartResize, ystopResize, bits, slope, subgrid, SetXSlope, SetYSlope, xstartsub, xstopsub, ystartsub, ystopsub, xstep, ystep, channeltimeing)
                        self.ManfredsStomach.progress_Filename.connect(self.updateLivePlotName)
                        self.ManfredsStomach.progress_value.connect(self.updateLivePlot)

                        self.ManfradsSender = CalcPlot1(q2)
                        #self.ManfradsSender.progress_value.connect(self.updateLivePlot)
                        
                        self.Manfred.start()                                                                                                            #Startet den Thread
                        self.ManfredsStomach.start()
                        self.ManfradsSender.start()
                        
                else:
                        print ("Measurement off")
                        self.buttonStart.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setText("Start")                                                                                               #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.NavWin.buttonStart.setToolTip("Starts the Measurement")                                                                    #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setText("Start")                                                                                        #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.Manfred.killFredHard()
                        self.ManfredsStomach.killFred()
                        self.buttonUnchecked(1)

        def updateLivePlot(self, zNew, zNew2):
                self.PlotWin.NewLine(zNew, zNew2)
                
        def updateLivePlotName(self, Date):
                self.PlotWin.Date(Date)

        def updateProgTime(self):
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoVoltage
                global DeviceVoltage
                global PointSpeed

                XDistance = (PiezoDistanceX * (DeviceVoltage/PiezoVoltage))
                YDistance = (PiezoDistanceY * (DeviceVoltage/PiezoVoltage))
                
                TTLTime = 2                                                                                                                             #Expected return Time for a TTL Signal
                SendTime = 0.1                                                                                                                          #Waittime between rising and falling
                if APDBSOn == 1:
                        APDTime = 0.035 + (self.spinIntTime2.value()*0.005)
                elif APDArduinoOn == 1:
                        APDTime = (PointSpeed + self.spinIntTime2.value()) / 1000
                else:
                        APDTime = (PointSpeed + self.spinIntTime2.value()) / 1000
            
                #xstart = self.slideXStart.value()
                #xstop = self.slideXStop.value()
                #ystart = self.slideYStart.value()
                #ystop = self.slideYStop.value()
                delaytime = self.delay.value()

                #print("SliderVal XStart: " + str(xstart))
                #print("SliderVal YStart: " + str(ystart))
                #print("SliderVal XStop: " + str(xstop))
                #print("SliderVal YStop: " + str(ystop))
                
                bits = self.cbg2.checkedId()
                if bits == 0:
                        bits = 64
                        NormalWindowTime = 66.7566
                elif bits == 1:
                        bits = 128
                        NormalWindowTime = 185.1226                                                                                                     #Gibt die Verstärkung im cmd aus
                elif bits == 2:         
                        bits = 256
                        NormalWindowTime = 532.1455                                                                                                     #Gibt die Verstärkung im cmd aus
                elif bits == 3:
                        bits = 512
                        NormalWindowTime = 1823.6051                                                                                                    #Gibt die Verstärkung im cmd aus
                elif bits == 4:
                        bits = 1024
                        NormalWindowTime = 7397.4880                                                                                                    #Gibt die Verstärkung im cmd aus
                elif bits == 5:
                        bits = 2048
                        NormalWindowTime = 29360.1280                                                                                                   #Gibt die Verstärkung im cmd aus
                elif bits == 6:
                        bits = 4096
                        NormalWindowTime = 117440.5120

                #NormalWindowTime = (((xstop - xstart) * (ystop - ystart) * delaytime) + ((ystop - ystart) * 0.2) + ((xstop - xstart) * (ystop - ystart) * APDTime))
                #NormalWindowTime = ((bits * bits * delaytime) + (bits * 0.2) + ((xstop - xstart) * bits * APDTime))

                subgrid = self.Subgrid1.isChecked()
                
                xstartsub = self.slideXStart2.value()
                xstopsub = self.slideXStop2.value()
                ystartsub = self.slideYStart2.value()
                ystopsub = self.slideYStop2.value()
                xstep = self.slideXStep.value() 
                ystep = self.slideYStep.value()
                steptime = self.spinStepTime.value()
                
                sendTTL = self.groupboxSendTTL3.isChecked()
                getTTL = self.TTLgetPoint2.isChecked()

                stack = self.Stack1.isChecked()
                stacks = self.StackCount.value()
                
                if getTTL == True:
                    #SubgridTime = (((xstopsub - xstartsub)/xstep) * ((ystopsub - ystartsub)/ystep) * (TTLTime + SendTime))
                    SubgridTime = ((bits/xstep) * (bits/ystep) * (TTLTime + SendTime))
                elif sendTTL == True:
                    #SubgridTime = (((xstopsub - xstartsub)/xstep) * ((ystopsub - ystartsub)/ystep) * (steptime + SendTime))
                    SubgridTime = ((bits/xstep) * (bits/ystep) * (steptime + SendTime))
                else:
                    #SubgridTime = (((xstopsub - xstartsub)/xstep) * ((ystopsub - ystartsub)/ystep) * steptime)
                    SubgridTime = ((bits/xstep) * (bits/ystep) * steptime)

                
                if subgrid == True:
                    ExTime = NormalWindowTime + SubgridTime
                else:
                    ExTime = NormalWindowTime

                if stack == True:
                    ExTime = ExTime * stacks

                pixelsizeX = round(XDistance/bits, 2)
                pixelsizeY = round(YDistance/bits, 2)

                XDist = round((self.spinXStop.value() - self.spinXStart.value()), 3)
                YDist = round((self.spinYStop.value() - self.spinYStart.value()), 3)

                print("NormalTime: " + str(ExTime))

                TimeMins = ExTime // 60
                TimeSecs1 = ExTime % 60
                TimeSecs = TimeSecs1 // 1
                TimeMilsecs = round(((TimeSecs1 % 1) * 1000), 2)
                self.labelProgTime.setText("Expected Time:\t" + str(int(TimeMins)) + " min  \t" + str(int(TimeSecs)) + " s\t" + str(int(TimeMilsecs)) + " ms\nPixelsize:\t\t" + str(pixelsizeX) + " x " + str(pixelsizeY) + " nm" + " s\nWindowsize:\t" + str(XDist) + " x " + str(YDist) + " [\u03BCm]")                                                                  #Setzt ein Label 

        def updateProgressBar1(self, val):
                self.progress1.setValue(val)

        #Tab3
        def slideXstart2(self):
                global FullRangeDeviceX
                NewVal = round((self.slideXStart2.value()*(FullRangeDeviceX/1000)/self.bitval3),3)
                if NewVal != self.spinXStart2.value():
                        self.StartX2 = (self.slideXStart2.value() / 100)                                                                                #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStart2.setValue(NewVal)                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStop2.setMinimum(self.slideXStart2.value())
                        self.spinXStop2.setMinimum(NewVal)
                        self.slideXStep.setMaximum(self.slideXStop2.value() - self.slideXStart2.value())
                        self.spinXStep.setMaximum(round(self.slideXStop2.value()*((FullRangeDeviceX/1000)/self.bitval3),3)-round(self.slideXStart2.value()*((FullRangeDeviceX/1000)/self.bitval3),3))
                        self.CalcPoints()
                        self.updateProgTime()
        
        def spinXstart2(self):
                global FullRangeDeviceX
                NewVal = int(round(self.spinXStart2.value()/((FullRangeDeviceX/1000)/self.bitval3),0))
                if NewVal != self.slideXStart2.value():
                        self.slideXStart2.setValue(int(NewVal))                                                                                         #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStop2.setMinimum(int(round(self.spinXStart2.value()/((FullRangeDeviceX/1000)/self.bitval3),0)))
                        self.spinXStop2.setMinimum(self.spinXStart2.value()) 
                        self.spinXStop2.setMinimum(self.spinXStart2.value())
                        self.slideXStep.setMaximum(self.slideXStop2.value() - self.slideXStart2.value()) 
                        self.spinXStep.setMaximum(int(round(self.slideXStop2.value()*(FullRangeDeviceX/self.bitval3),3))-int(round(self.slideXStart2.value()*(FullRangeDeviceX/self.bitval3),3)))
                        self.StartX2 = (self.spinXStart2.value() / 100)
                        self.CalcPoints()
                        self.updateProgTime()

        def slideYstart2(self):                 
                global FullRangeDeviceY
                NewVal = round((self.slideYStart2.value()*(FullRangeDeviceY/1000)/self.bitval3),3)
                if NewVal != self.spinYStart2.value():
                        self.StartY2 = (self.slideYStart2.value() / 100)                                                                                #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStart2.setValue(NewVal)                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStop2.setMinimum(self.slideYStart2.value())
                        self.spinYStop2.setMinimum(NewVal)
                        self.slideYStep.setMaximum(self.slideYStop2.value() - self.slideYStart2.value())
                        self.spinYStep.setMaximum(int(round(self.slideYStop2.value()*(FullRangeDeviceY/self.bitval3),3))-int(round(self.slideYStart2.value()*(FullRangeDeviceY/self.bitval3),3)))
                        self.CalcPoints()
                        self.updateProgTime()
        
        def spinYstart2(self):
                global FullRangeDeviceY
                NewVal = int(round(self.spinYStart2.value()/((FullRangeDeviceY/1000)/self.bitval3),0))
                if NewVal != self.slideYStart2.value():
                        self.slideYStart2.setValue(int(NewVal))                                                                                         #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStop2.setMinimum(int(round(self.spinYStart2.value()/((FullRangeDeviceY/1000)/self.bitval3),0)))
                        self.spinYStop2.setMinimum(self.spinYStart2.value()) 
                        self.spinYStop2.setMinimum(self.spinYStart2.value())
                        self.slideYStep.setMaximum(self.slideYStop2.value() - self.slideYStart2.value()) 
                        self.spinYStep.setMaximum(int(round(self.slideYStop2.value()*(FullRangeDeviceY/self.bitval3),3))-int(round(self.slideYStart2.value()*(FullRangeDeviceY/self.bitval3),3)))
                        self.StartY2 = (self.spinYStart2.value() / 100)
                        self.CalcPoints()
                        self.updateProgTime()
        
        def slideXstop2(self):                 
                global FullRangeDeviceX
                NewVal = round((self.slideXStop2.value()*(FullRangeDeviceX/1000)/self.bitval3),3)
                if NewVal != self.spinXStop2.value():
                        self.StopX2 = (self.slideXStop2.value() / 100)                                                                                  #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStop2.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStep.setMaximum(self.slideXStop2.value() - self.slideXStart2.value())
                        self.spinXStep.setMaximum(round(self.slideXStop2.value()*((FullRangeDeviceX/1000)/self.bitval3),3)-round(self.slideXStart2.value()*((FullRangeDeviceX/1000)/self.bitval3),3))
                        self.CalcPoints()
                        self.updateProgTime()                                                                                                           #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                
        def spinXstop2(self):
                global FullRangeDeviceX
                NewVal = int(round(self.spinXStop2.value()/((FullRangeDeviceX/1000)/self.bitval3),0))
                if NewVal != self.spinXStop2.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StopX2 = (self.spinXStop2.value() / 100) 
                        self.slideXStop2.setValue(int(NewVal))                                                                                          #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStep.setMaximum(self.slideXStop2.value() - self.slideXStart2.value())
                        self.spinXStep.setMaximum(round(self.slideXStop2.value()*((FullRangeDeviceX/1000)/self.bitval3),3)-round(self.slideXStart2.value()*((FullRangeDeviceX/1000)/self.bitval3),3))
                        self.CalcPoints()
                        self.updateProgTime()
        
        def slideYstop2(self):                 
                global FullRangeDeviceY
                NewVal = round((self.slideYStop2.value()*(FullRangeDeviceY/1000)/self.bitval3),3)
                if NewVal != self.spinYStop2.value():
                        self.StopY2 = (self.slideYStop2.value() / 100)                                                                                  #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStop2.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStep.setMaximum(self.slideYStop2.value() - self.slideYStart2.value())
                        self.spinYStep.setMaximum(int(round(self.slideYStop2.value()*(FullRangeDeviceY/self.bitval3),3))-int(round(self.slideYStart2.value()*(FullRangeDeviceY/self.bitval3),3)))
                        self.CalcPoints()
                        self.updateProgTime()                                                                                                           #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                
        def spinYstop2(self):
                global FullRangeDeviceY
                NewVal = int(round(self.spinYStop2.value()/((FullRangeDeviceY/1000)/self.bitval3),0))
                if NewVal != self.spinYStop2.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StopY2 = (self.spinYStop2.value() / 100) 
                        self.slideYStop2.setValue(int(NewVal))                                                                                          #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStep.setMaximum(self.slideYStop2.value() - self.slideYStart2.value())
                        self.spinYStep.setMaximum(int(round(self.slideYStop2.value()*(FullRangeDeviceY/self.bitval3),3))-int(round(self.slideYStart2.value()*(FullRangeDeviceY/self.bitval3),3)))
                        self.CalcPoints()
                        self.updateProgTime()
                
        def slideXstep(self):
                global FullRangeDeviceX
                NewVal = round(self.slideXStep.value()*((FullRangeDeviceX/1000)/self.bitval3),3)
                if NewVal != self.spinXStep.value():                                                                                                    #Gibt den Wert des Sliders im cmd aus
                        self.StepX = int(self.slideXStep.value()/100)                                                                                   #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStep.setValue(NewVal)      
                        self.CalcPoints()                                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.updateProgTime()
                
        def spinXstep(self):                                                                                                                            #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                global FullRangeDeviceX
                NewVal = int(round(self.spinXStep.value()/((FullRangeDeviceX/1000)/self.bitval3),3))
                if NewVal != self.slideXStep.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StepX = (NewVal / 100)                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideXStep.setValue(int(NewVal))  
                        self.CalcPoints()                                                                                                               #Setzt den Wert des Sliders auf den Wert der Zahlenauswahlbox
                        self.updateProgTime()
                    
        def slideYstep(self):
                global FullRangeDeviceY
                NewVal = round(self.slideYStep.value()*((FullRangeDeviceY/1000)/self.bitval3),3)
                if NewVal != self.spinYStep.value():                                                                                                    #Gibt den Wert des Sliders im cmd aus
                        self.StepY = (self.slideYStep.value()/100)                                                                                      #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStep.setValue(NewVal)      
                        self.CalcPoints()                                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.updateProgTime()
                
        def spinYstep(self):                                                                                                                            #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                global FullRangeDeviceY
                NewVal = int(round(self.spinYStep.value()/((FullRangeDeviceY/1000)/self.bitval3),3))
                if NewVal != self.slideYStep.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StepY = int(NewVal / 100)                                                                                                  #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideYStep.setValue(int(NewVal))  
                        self.CalcPoints()                                                                                                               #Setzt den Wert des Sliders auf den Wert der Zahlenauswahlbox
                        self.updateProgTime()

        def spinsteptime(self):                                                                                                                         #Gibt den Wert der Zahlauswahlbox im cmd aus
                self.StepTime = (self.spinStepTime.value() / 100)   
                self.CalcPoints()                                                                                                                       #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.updateProgTime()


        def savesettingsScanSync(self):
                name = self.nameSync.text()
                if len(name) == 0:
                        name = time.strftime("%d.%m.%Y %H:%M:%S")
                bits = self.cbg3.checkedId()
                xstart = self.slideXStart2.value()
                xstop = self.slideXStop2.value()
                ystart = self.slideYStart2.value()
                ystop = self.slideYStop2.value()
                xstep = self.slideXStep.value()
                ystep = self.slideYStep.value()
                steptime = self.spinStepTime.value()
                sendTTL = self.groupboxSendTTL3.isChecked()
                getTTL = self.TTLgetPoint2.isChecked()
                channel = self.channeltimeing.isChecked()
                ttl = self.TTLroot2.currentIndex()
                
                SyncSet.execute("INSERT INTO settingsScanSync (name, bits, xstart, xstop, ystart, ystop, xstep, ystep, steptime, sendTTL, getTTL, ttl, channel) VALUES (\"" + name + "\", " + str(bits) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(xstep) + ", " + str(ystep) + ", " + str(steptime) + ", " + str(sendTTL) + ", " + str(getTTL) + ", " + str(ttl) + ", " + str(channel) + ")")
                SyncSet.execute("SELECT * FROM settingsScanSync")
                #print(SyncSet.fetchall())
                connSync.commit()
                self.namesSync.addItem(name)
                
        def usesettingsScanSync(self):
                set = self.namesSync.currentText()
                SyncSet.execute(("SELECT * FROM settingsScanSync WHERE name = \"") + set + ("\""))
                for dsatzSync in SyncSet:
                        name = dsatzSync[0]
                        bits = dsatzSync[1]
                        xstart = dsatzSync[2]
                        xstop = dsatzSync[3]
                        ystart = dsatzSync[4]
                        ystop = dsatzSync[5]
                        xstep = dsatzSync[6]
                        ystep = dsatzSync[7]
                        steptime = dsatzSync[8]
                        sendTTL = dsatzSync[9]
                        getTTL = dsatzSync[10]
                        ttl = dsatzSync[11]
                        channel = dsatzSync[12]
                        #print(str(name) + ", " + str(bits) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(xstep) + ", " + str(ystep) + ", " + str(steptime) + ", " + str(sendTTL) + ", " + str(getTTL))
                
                if bits == 0:
                        self.cb30.setChecked(True)
                if bits == 1:
                        self.cb31.setChecked(True)
                elif bits == 2:
                        self.cb32.setChecked(True)
                elif bits == 3:
                        self.cb33.setChecked(True)
                elif bits == 4:
                        self.cb34.setChecked(True)
                elif bits == 5:
                        self.cb35.setChecked(True)
                elif bits == 6:
                        self.cb36.setChecked(True)
                elif bits == -1:
                        self.cb30.setChecked(False)
                        self.cb31.setChecked(False)
                        self.cb32.setChecked(False)
                        self.cb33.setChecked(False)
                        self.cb34.setChecked(False)
                        self.cb35.setChecked(False)
                        self.cb36.setChecked(False)

                        
                self.slideXStart2.setValue(int(xstart))
                self.slideXStop2.setValue(int(xstop))
                self.slideYStart2.setValue(int(ystart))
                self.slideYStop2.setValue(int(ystop))
                self.slideXStep.setValue(int(xstep))
                self.slideYStep.setValue(int(ystep))
                self.spinStepTime.setValue(float(steptime))
                
                self.groupboxSendTTL3.setChecked(sendTTL)
                self.TTLgetPoint2.setChecked(getTTL)
                self.TTLroot2.setCurrentIndex(ttl)
                self.channeltimeing.setChecked(channel)

                connSync.commit()
                
        def CalcPoints(self):
                XStop = self.spinXStop2.value()
                XStart = self.spinXStart2.value()
                XStep = self.spinXStep.value()
                
                YStop = self.spinYStop2.value()
                YStart = self.spinYStart2.value()
                YStep = self.spinYStep.value()
                
                XPoints = round(((XStop-XStart) / XStep)+1,0)

                print("XPos: (" + str(XStop) + "-" + str(XStart) + ") / " + str(XStep) + " = " + str(XPoints))

                try:
                        XPoints = round(((XStop-XStart) / XStep)+1,0)
                        YPoints = round(((YStop-YStart) / YStep)+1,0)
                        Points = (XPoints * YPoints)
                        self.labelPoints.setText("Number of Subgridpoints: " + str(Points))
                except:
                        pass
                
        def stopAll3(self):  
                global FullRangeDeviceX
                global FullRangeDeviceY                                                                                                                 #wird zweimal ausgeführt, da bei einem stateChange in der ButtonGroup immer zwei Werte geändert werden (eine box wird unchecked eine wird gechecked)
                checkedBits = self.cbg3.checkedId()
                 
                if checkedBits == 0:                                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                        self.bitval3 = 64
                elif checkedBits == 1:
                        self.bitval3 = 128
                elif checkedBits == 2:
                        self.bitval3 = 256
                elif checkedBits == 3:
                        self.bitval3 = 512
                elif checkedBits == 4:
                        self.bitval3 = 1024
                elif checkedBits == 5:
                        self.bitval3 = 2048
                elif checkedBits == 6:
                        self.bitval3 = 4096

                SpinSingleStepX = round(((FullRangeDeviceX/1000)/(self.bitval3-1)),3)
                SpinSingleStepY = round(((FullRangeDeviceY/1000)/(self.bitval3-1)),3)
                SpinXStep = round((self.slideXStep.value() * SpinSingleStepX),3)
                SpinYStep = round((self.slideYStep.value() * SpinSingleStepY),3)
                
                NewValX = round(self.spinXStep.value()/((FullRangeDeviceX/1000)/(self.bitval3-1)),3)
                if NewValX != self.slideXStep.value():                                                                                                  #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideXStep.setValue(int(NewValX)) 
                NewValY = round(self.spinYStep.value()/((FullRangeDeviceY/1000)/(self.bitval3-1)),3)
                if NewValY != self.slideYStep.value():                                                                                                  #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideYStep.setValue(int(NewValY))
                NewValXStart = round(self.spinXStart2.value()/((FullRangeDeviceX/1000)/(self.bitval3-1)),3)
                NewValYStart = round(self.spinYStart2.value()/((FullRangeDeviceY/1000)/(self.bitval3-1)),3)
                NewValXStop = round(self.spinXStop2.value()/((FullRangeDeviceX/1000)/(self.bitval3-1)),3)
                NewValYStop = round(self.spinYStop2.value()/((FullRangeDeviceY/1000)/(self.bitval3-1)),3)
                NewValXStopSpin = NewValXStop * ((FullRangeDeviceX/1000)/(self.bitval3-1))
                NewValYStopSpin = NewValYStop * ((FullRangeDeviceY/1000)/(self.bitval3-1))
                       
                self.slideXStart2.setMaximum(self.bitval3-1)
                self.slideXStop2.setTickInterval(self.bitval3)                                                                                          #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStart2.setMaximum(self.bitval3-1)
                self.slideXStop2.setTickInterval(self.bitval3)                                                                                          #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStop2.setMaximum(self.bitval3-1)
                self.slideXStop2.setTickInterval(self.bitval3)                                                                                          #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStop2.setMaximum(self.bitval3-1)
                self.slideXStop2.setTickInterval(self.bitval3)                                                                                          #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideXStep.setMaximum(self.bitval3-1)
                self.slideXStop2.setTickInterval(self.bitval3)                                                                                          #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideYStep.setMaximum(self.bitval3-1)
                self.slideXStop2.setTickInterval(self.bitval3)
                
                self.spinYStep.setSingleStep(SpinSingleStepY) 
                self.spinXStep.setSingleStep(SpinSingleStepX)
                self.spinYStep.setMinimum(round(((FullRangeDeviceY/1000)/(self.bitval3-1)),3)) 
                self.spinXStep.setMinimum(round(((FullRangeDeviceX/1000)/(self.bitval3-1)),3))
                self.spinXStep.setMaximum(int(FullRangeDeviceX/1000))
                self.spinYStep.setMaximum(int(FullRangeDeviceY/1000))
                
                self.slideXStart2.setValue(int(NewValXStart))
                self.slideYStart2.setValue(int(NewValYStart))
                self.slideXStop2.setValue(int(NewValXStop))
                self.slideYStop2.setValue(int(NewValYStop))

                self.spinXStop2.setValue(NewValXStopSpin)
                self.spinYStop2.setValue(NewValYStopSpin)
                
                self.spinXStep.setValue(SpinXStep)
                self.spinYStep.setValue(SpinYStep)
                
                

        #Tab4 - Z-Stack
        def StartZChange(self, down):
                if down:
                        ZStart = self.ZStartSpin.value()
                        dacZ.set_voltage(ZStart) 
                        self.buttonSetZ.setToolTip("Stops the Process")                                                                                 #Setzt eine Buttonbeschreibung bei MouseOver
                else:
                        self.buttonSetZ.setToolTip("Sets the Stage to the Value")                                                                       #Setzt eine Buttonbeschreibung bei MouseOver
                        dacZ.set_voltage(2048) 


        def slideZChange(self):
                ZStart = self.ZStartSlide.value()
                self.ZStartSpin.setValue(ZStart)
                self.StartZChange(self.buttonSetZ.isChecked())
                self.UpdateLabelDistance()

        def spinZChange(self):
                ZStart = self.ZStartSpin.value()
                self.ZStartSlide.setValue(int(ZStart))
                self.StartZChange(self.buttonSetZ.isChecked())
                self.UpdateLabelDistance()

        def StackCountChange(self):                                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                StackCount = self.StackCount.value()
                self.UpdateLabelDistance()
                
        def StackStepChange(self):                                                                                                                      #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                StepSize = self.ZStepsize.value()                                                                                                       #setzt eine Spinbox
                self.UpdateLabelDistance()
                
        def DirectChange(self):                                                                                                                         #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                Direction = self.ZDirection.currentIndex()
                self.UpdateLabelDistance()
                
        def UpdateLabelDistance(self):
                global PiezoDistanceZ
                global PiezoVoltag
                global DeviceVoltage

                MaxStackSize = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)
                StackCount = self.StackCount.value()                                                                                                    #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                StepSize = self.ZStepsize.value()
                ZVal = self.ZStartSlide.value()
                StackSize = round(((StackCount - 1) * StepSize), 2)

                StackStart = ZVal * (MaxStackSize/4096)

                if self.ZDirection.currentIndex() == 0:
                        MaxStack = MaxStackSize - StackStart
                        if (StackSize*1000)<=MaxStack:
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStack/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]")
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_green.png")
                                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                        else:  
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStack/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]" + "\t\tOut of Range") 
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_red.png")
                                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                elif self.ZDirection.currentIndex() == 1:
                        if (StackSize*1000)<=StackStart:
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((StackStart/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]")
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_green.png")
                                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                        else:  
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((StackStart/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]" + "\t\tOut of Range") 
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_red.png")
                                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                elif self.ZDirection.currentIndex() == 2:
                        UpLimit = MaxStackSize - StackStart
                        DownLimit = StackStart
                        if ((StackSize / 2) * 1000) <= UpLimit and ((StackSize / 2) * 1000) <= DownLimit:
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStackSize/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]")
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_green.png")
                                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                        else:  
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStackSize/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]" + "\t\tOut of Range") 
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_red.png")
                                pixmap_mini = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                
        def savesettingsScanStack(self):
                name = self.nameStack.text()
                if len(name) == 0:
                        name = time.strftime("%d.%m.%Y %H:%M:%S")
                stacks = self.StackCount.value()
                stackstep = self.ZStepsize.value()
                direct = self.ZDirection.currentIndex()
                ZStart = self.ZStartSpin.value()

                StackSet.execute("INSERT INTO settingsScanStack (name, stacks, stackstep, direct, zstart) VALUES (\"" + name + "\", " + str(stacks) + ", " + str(stackstep) + ", " + str(direct) + ", " + str(ZStart) + ")")
                StackSet.execute("SELECT * FROM settingsScanStack")
                #print(StackSet.fetchall())
                connStack.commit()
                self.namesStack.addItem(name)
                
        def usesettingsScanStack(self):
                set = self.namesStack.currentText()
                StackSet.execute(("SELECT * FROM settingsScanStack WHERE name = \"") + set + ("\""))
                for dsatzStack in StackSet:
                        name = dsatzStack[0]
                        stacks = dsatzStack[1]
                        stackstep = dsatzStack[2]
                        direct = dsatzStack[3]
                        zstart = dsatzStack[4]
                        #print(str(name) + ", " + str(xslope) + ", " + str(yslope))
                        
                self.StackCount.setValue(int(stacks))
                self.ZStepsize.setValue(float(stackstep))
                self.ZDirection.setCurrentIndex(int(direct))
                self.ZStartSpin.setValue(int(zstart))
                
                connStack.commit()



        #Tab5 - Slope Compensation
        def AutoSlope(self, down):
                if down:
                        self.buttonAutoSlope.setToolTip("Stop the AutoSlope")                                                                           #Setzt eine Buttonbeschreibung bei MouseOver
                        self.buttonAutoSlope.setStyleSheet("color: black; background-color: rgb(255,0,0)")
                        
                        self.Reading = SearchSlope()
                        self.Reading.progress_Slope.connect(self.setSlope)
                        self.Reading.start()
                else:
                        try:
                                self.Reading.kill()
                        except:
                                pass
                        self.buttonAutoSlope.setToolTip("Start the AutoSlope")                                                                          #Setzt eine Buttonbeschreibung bei MouseOver
                        self.buttonAutoSlope.setChecked(False)
                        self.buttonAutoSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")

        def setSlope(self, SlopeXNew, SlopeYNew):
                print("New Slope: " + str(SlopeXNew) + " - " + str(SlopeYNew))
                SlopeXNew = SlopeXNew -2000
                SlopeYNew = SlopeYNew -2000
                self.slideXSlope.setValue(SlopeXNew)
                self.slideYSlope.setValue(SlopeYNew)
                self.XSlope = SlopeXNew
                self.YSlope = SlopeYNew
                self.Slope1.setChecked(True)
                self.buttonAutoSlope.setToolTip("Start the AutoSlope")
                self.buttonAutoSlope.setChecked(False)
                self.buttonAutoSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")

        def SlopeStartX(self, down):                                                                                                                    #Setzt das Messfenster
                if down:
                        dacX.set_voltage(4095)
                        dacY.set_voltage(int(4095/2))                   
                        self.XSlope = self.slideXSlope.value()
                        dacZ.set_voltage(int(self.XSlope + 2000))
                        self.buttonXSlope.setToolTip("Set Slope")                                                                                       #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                else:
                        print("Slope already Set")
                        self.buttonXSlope.setToolTip("Starts Slopesetup")                                                                               #Setzt den MouseOver-ToolTip des Motor-Startbuttons um

        def SlopeStartY(self, down):                                                                                                                    #Setzt das Messfenster
                if down:
                        dacX.set_voltage(int(4095/2))
                        dacY.set_voltage(4095)                  
                        self.YSlope = self.slideYSlope.value()
                        dacZ.set_voltage(int(self.YSlope + 2000))
                        self.buttonYSlope.setToolTip("Set Slope")                                                                                       #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                else:
                        print("Slope already Set")
                        self.buttonYSlope.setToolTip("Starts Slopesetup")                                                                               #Setzt den MouseOver-ToolTip des Motor-Startbuttons um

        def slideXslope(self):                                                                                                                          #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.spinXSlope.setValue(self.slideXSlope.value())                                                                                      #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                self.SlopeStartX(self.buttonXSlope.isChecked())                                                                                         #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
        
        def spinXslope(self):                                                                                                                           #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.slideXSlope.setValue(int(self.spinXSlope.value()))                                                                                 #Setzt den Wert des Sliders auf den Wert der Zahlenauswahlbox
                self.SlopeStartX(self.buttonXSlope.isChecked())                                                                                         #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden

        def slideYslope(self):                                                                                                                          #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.spinYSlope.setValue(self.slideYSlope.value())                                                                                      #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                self.SlopeStartY(self.buttonYSlope.isChecked())                                                                                         #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
        
        def spinYslope(self):                                                                                                                           #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.slideYSlope.setValue(int(self.spinYSlope.value()))                                                                                 #Setzt den Wert des Sliders auf den Wert der Zahlenauswahlbox
                self.SlopeStartY(self.buttonYSlope.isChecked())                                                                                         #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden


        def savesettingsScanSlope(self):
                name = self.nameSlope.text()
                if len(name) == 0:
                        name = time.strftime("%d.%m.%Y %H:%M:%S")
                xslope = self.slideXSlope.value()
                yslope = self.slideYSlope.value()

                SlopeSet.execute("INSERT INTO settingsScanSlope (name, xslope, yslope) VALUES (\"" + name + "\", " + str(xslope) + ", " + str(yslope) + ")")
                SlopeSet.execute("SELECT * FROM settingsScanSlope")
                #print(SlopeSet.fetchall())
                connSlope.commit()
                self.namesSlope.addItem(name)
                
        def usesettingsScanSlope(self):
                set = self.namesSlope.currentText()
                SlopeSet.execute(("SELECT * FROM settingsScanSlope WHERE name = \"") + set + ("\""))
                for dsatzSlope in SlopeSet:
                        name = dsatzSlope[0]
                        xslope = dsatzSlope[1]
                        yslope = dsatzSlope[2]
                        #print(str(name) + ", " + str(xslope) + ", " + str(yslope))
                        
                self.slideXSlope.setValue(int(xslope))
                self.spinXSlope.setValue(xslope)
                self.slideYSlope.setValue(int(yslope))
                self.spinYSlope.setValue(yslope)
                self.XSlope = xslope
                self.YSlope = yslope
                
                connSlope.commit()

        """
        #Tab6
        def SaveAsPath(self):
                self.SavePath = str(QFileDialog.getExistingDirectory(self, 'Select directory'))
                self.labelSave.setText(self.SavePath)

        def OpenPlotFile(self):
                global TXTFilePath
                
                self.FilePath2 = ""
                self.ComboRow.clear()
                self.FilePath1 = str(QFileDialog.getOpenFileName(self, "Open File", "/home/pi/Desktop/Data", "Textfile (*.txt)"))
                lengthFilePath1 = len(self.FilePath1) - 22
                self.FilePath2 = self.FilePath1[2:lengthFilePath1]
                self.labelPath.setText(self.FilePath2)

                lengthFilePath2 = len(self.FilePath1) - 26
                self.NewFilePath = self.FilePath1[2:lengthFilePath2]
                
                DataStart = self.FileStart.value()

                try:
                        TXTFilePath = self.FilePath2
                except:
                        pass
                try:
                        with open(self.FilePath2,'r') as csvfile:
                                plots = list(csv.reader(csvfile, delimiter='\t'))
                                        
                                self.XCol = 1
                                self.YCol = 2

                                if self.groupboxHeadlines.isChecked() == False:
                                        HeaderLines = 0
                                        Header = plots[HeaderLines]
                                        while Header != []:
                                                Header = plots[HeaderLines]
                                                HeaderLines = HeaderLines + 1

                                        DataStartNew = HeaderLines + 1
                                        self.FileStart.setValue(DataStartNew)
                                        DataStart = DataStartNew
                                        
                                
                                i = 0
                                
                                while i <= (len(plots[DataStart-1])-1):
                                        NewItem = plots[DataStart-1][i]
                                        if NewItem != "X" and NewItem != "Y" and NewItem != "x" and NewItem != "y":
                                                self.ComboRow.addItem(NewItem)
                                        elif NewItem == "X" or NewItem == "x":
                                                self.XCol = i
                                                self.ComboRow.addItem(NewItem)
                                        elif NewItem == "Y" or NewItem == "y":
                                                self.YCol = i
                                                self.ComboRow.addItem(NewItem)
                                        i = i + 1
                                                
                                PlotsLength = len(plots)-1

                                xstart = int(plots[DataStart][self.XCol])
                                ystart = int(plots[DataStart][self.YCol])
                                xstop = int(plots[PlotsLength][self.XCol])
                                ystop = int(plots[PlotsLength][self.YCol])

                                self.xlen = xstop - xstart
                                self.ylen = ystop - ystart
                except:
                        DataStart = DataStart + 1
                        self.FileStart.setValue(DataStart)
                        try:
                                with open(self.FilePath2,'r') as csvfile:
                                        plots = list(csv.reader(csvfile, delimiter='\t'))
                                                
                                        self.XCol = 1
                                        self.YCol = 2
                                        
                                        if self.groupboxHeadlines.isChecked() == False:
                                                HeaderLines = 0
                                                Header = plots[HeaderLines]
                                                while Header != []:
                                                        Header = plots[HeaderLines]
                                                        HeaderLines = HeaderLines + 1

                                                DataStartNew = HeaderLines + 1
                                                self.FileStart.setValue(DataStartNew)
                                                DataStart = DataStartNew
                                        
                                        i = 0
                                        while i <= (len(plots[DataStart-1])-1):
                                                NewItem = plots[DataStart-1][i]
                                                if NewItem != "X" and NewItem != "Y" and NewItem != "x" and NewItem != "y":
                                                        self.ComboRow.addItem(NewItem)
                                                elif NewItem == "X" or NewItem == "x":
                                                        self.XCol = i
                                                        self.ComboRow.addItem(NewItem)
                                                elif NewItem == "Y" or NewItem == "y":
                                                        self.YCol = i
                                                        self.ComboRow.addItem(NewItem)
                                                i = i + 1
                                                        
                                        PlotsLength = len(plots)-1

                                        xstart = int(plots[DataStart][self.XCol])
                                        ystart = int(plots[DataStart][self.YCol])
                                        xstop = int(plots[PlotsLength][self.XCol])
                                        ystop = int(plots[PlotsLength][self.YCol])

                                        self.xlen = xstop - xstart
                                        self.ylen = ystop - ystart
                        except:
                                pass
                self.UpdatePlotLabels()

        def UpdateZAxis(self):
                global CHA
                global CHB
                global L2
                global L3
                global CH1
                global CH2
                global CH3
                global CH4

                CHA_rule = CHA + " [Counts]"
                CHB_rule = CHB + " [Counts]"
                L2_rule = L2 + " [Counts]"
                L3_rule = L3 + " [Counts]"
                CH1_rule = CH1 + " [V]"
                CH2_rule = CH2 + " [V]"
                CH3_rule = CH3 + " [V]"
                CH4_rule = CH4 + " [V]"
                
                if self.ZAxis.text() == "" or self.ZAxis.text() != CHA_rule or self.ZAxis.text() != CHB_rule or self.ZAxis.text() != L2_rule or self.ZAxis.text() != L3_rule or self.ZAxis.text() != CH1_rule or self.ZAxis.text() != CH2_rule or self.ZAxis.text() != CH3_rule or self.ZAxis.text() != CH4_rule:
                        self.UsedAxis = self.ComboRow.currentText()
                        if self.UsedAxis == CHA:
                                Axistext = self.UsedAxis + " [Counts]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == CHB:
                                Axistext = self.UsedAxis + " [Counts]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == L2:
                                Axistext = self.UsedAxis + " [Counts]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == L3:
                                Axistext = self.UsedAxis + " [Counts]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == CH1:
                                Axistext = self.UsedAxis + " [V]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == CH2:
                                Axistext = self.UsedAxis + " [V]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == CH3:
                                Axistext = self.UsedAxis + " [V]"
                                self.ZAxis.setText(Axistext)
                        elif self.UsedAxis == CH4:
                                Axistext = self.UsedAxis + " [V]"
                                self.ZAxis.setText(Axistext)
                        else:
                                Axistext = ""
                                self.ZAxis.setText(Axistext)
                        
        def RangeTrue(self):
                if self.Range.isChecked():
                        self.XAxis.setText("X-Position [\u03BCm]")
                        self.YAxis.setText("Y-Position [\u03BCm]")
                else:
                        self.XAxis.setText("X-Position [Bit]")
                        self.YAxis.setText("Y-Position [Bit]")

        def UpdatePlotLabel(self):
                global TXTFilePath
                TXTFilePath = self.FilePath2
                DataStart = self.FileStart.value()
                self.ComboRow.clear()
                try:
                        with open(self.FilePath2,'r') as csvfile:
                                plots = list(csv.reader(csvfile, delimiter='\t'))
                                        
                                self.XCol = 1
                                self.YCol = 2
                                
                                if self.groupboxHeadlines.isChecked() == False:
                                        HeaderLines = 0
                                        Header = plots[HeaderLines]
                                        while Header != []:
                                                Header = plots[HeaderLines]
                                                HeaderLines = HeaderLines + 1

                                        DataStartNew = HeaderLines + 1
                                        self.FileStart.setValue(DataStartNew)
                                        DataStart = DataStartNew
                                
                                i = 0
                                while i <= (len(plots[DataStart-1])-1):
                                        NewItem = plots[DataStart-1][i]
                                        if NewItem != "X" and NewItem != "Y" and NewItem != "x" and NewItem != "y":
                                                self.ComboRow.addItem(NewItem)
                                        elif NewItem == "X" or NewItem == "x":
                                                self.XCol = i
                                                self.ComboRow.addItem(NewItem)
                                        elif NewItem == "Y" or NewItem == "y":
                                                self.YCol = i
                                                self.ComboRow.addItem(NewItem)
                                        i = i + 1
                                                
                                PlotsLength = len(plots)-1

                                xstart = int(plots[DataStart][self.XCol])
                                ystart = int(plots[DataStart][self.YCol])
                                xstop = int(plots[PlotsLength][self.XCol])
                                ystop = int(plots[PlotsLength][self.YCol])

                                self.xlen = xstop - xstart
                                self.ylen = ystop - ystart
                except:
                        DataStart = DataStart + 1
                        self.FileStart.setValue(DataStart)
                        try:
                                with open(self.FilePath2,'r') as csvfile:
                                        plots = list(csv.reader(csvfile, delimiter='\t'))
                                                
                                        self.XCol = 1
                                        self.YCol = 2
                                        
                                        if self.groupboxHeadlines.isChecked() == False:
                                                HeaderLines = 0
                                                Header = plots[HeaderLines]
                                                while Header != []:
                                                        Header = plots[HeaderLines]
                                                        HeaderLines = HeaderLines + 1

                                                DataStartNew = HeaderLines + 1
                                                self.FileStart.setValue(DataStartNew)
                                                DataStart = DataStartNew
                                        
                                        i = 0
                                        while i <= (len(plots[DataStart-1])-1):
                                                NewItem = plots[DataStart-1][i]
                                                if NewItem != "X" and NewItem != "Y" and NewItem != "x" and NewItem != "y":
                                                        self.ComboRow.addItem(NewItem)
                                                elif NewItem == "X" or NewItem == "x":
                                                        self.XCol = i
                                                        self.ComboRow.addItem(NewItem)
                                                elif NewItem == "Y" or NewItem == "y":
                                                        self.YCol = i
                                                        self.ComboRow.addItem(NewItem)
                                                i = i + 1
                                                        
                                        PlotsLength = len(plots)-1

                                        xstart = int(plots[DataStart][self.XCol])
                                        ystart = int(plots[DataStart][self.YCol])
                                        xstop = int(plots[PlotsLength][self.XCol])
                                        ystop = int(plots[PlotsLength][self.YCol])

                                        self.xlen = xstop - xstart
                                        self.ylen = ystop - ystart
                        except:
                                #print("No File selected")
                                pass
                                
                self.UpdatePlotLabels()

        def UpdatePlotLabels(self):
                if self.groupboxZoom.isChecked() == False:
                        self.labelPlotSize.setText("Plotsize: " + str(self.xlen) + " x " + str(self.ylen))
                else:
                        self.xlen = 0
                        self.ylen = 0
                        self.XStopValue.setMinimum(self.XStartValue.value())
                        self.YStopValue.setMinimum(self.YStartValue.value())
                        self.xlen = self.XStopValue.value() - self.XStartValue.value()
                        self.ylen = self.YStopValue.value() - self.YStartValue.value()
                        self.labelPlotSize.setText("Plotsize: " + str(self.xlen) + " x " + str(self.ylen))

        def PlotFile(self):
                if self.FilePath2 != "":
                #try:
                        FilePath = self.FilePath2
                        DataStart = self.FileStart.value()
                        Color = self.cbgStyle.checkedId()
                        Plotname = self.Plotname.text()
                        XCol = self.XCol
                        YCol = self.YCol
                        PlotCol = self.ComboRow.currentIndex()
                        
                        XAxis = self.XAxis.text()
                        YAxis = self.YAxis.text()
                        ZAxis = self.ZAxis.text()
                        InvertX = self.InvertXAxis.isChecked()
                        InvertY = self.InvertYAxis.isChecked()

                        Zoom = self.groupboxZoom.isChecked()
                        XStart = self.XStartValue.value()
                        XStop = self.XStopValue.value()
                        YStart = self.YStartValue.value()
                        YStop = self.YStopValue.value()

                        ScaleBar = self.groupboxScaleBar.isChecked()
                        Fontsize = self.ScaleBarFontsize.value()
                        Fontcolor = self.FontColor.currentText()
                        FontWeight = self.ScaleBarFontweight.currentText()
                        ScaleBarSize = self.ScaleBarSize.value()
                        ScaleBarSizeVertical = self.ScaleBarSizeVertical.value()
                        ScaleBarPosition = self.ScaleBarPosition.currentText()
                        ScaleBarOffset = self.ScaleBarOffset.value()
                        Range = self.Range.isChecked()
                        
                        if self.Filename.text() != "" and self.SavePath != "":
                                Filename = self.SavePath + "/" + self.Filename.text() + self.SaveAs.currentText()
                        elif self.Filename.text() != "":
                                Filename = "/home/pi/Desktop/Data/" + self.Filename.text() + self.SaveAs.currentText()
                        elif self.SavePath != "":
                                Filename = self.SavePath + "/" + time.strftime("%d-%m-%Y_%H-%M-%S") + self.SaveAs.currentText()
                        else:
                                Filename = self.NewFilePath + self.SaveAs.currentText()
                        
                        UseLimits = self.groupboxColorBar.isChecked()
                        LowerLimit = self.ColorBarMin.value()
                        UpperLimit = self.ColorBarMax.value()

                        Plotstyle = self.ComboStyle.currentIndex()
                        if Plotstyle == 0:
                                self.PlotThread = Plotter(115, 175, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                                self.PlotThread.start()
                                #HydraPlot.PlotMesh(115, 175, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                        elif Plotstyle == 1:
                                HydraPlot.PlotCont(FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                        elif Plotstyle == 2:
                                HydraPlot.PlotMeshCont(FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                        elif Plotstyle == 3:
                                HydraPlot.Plot3D(FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                        elif Plotstyle == 4:
                                HydraPlot.PlotContour3D(FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                        elif Plotstyle == 5:
                                HydraPlot.PlotContourFill3D(FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)
                        elif Plotstyle == 6:
                                HydraPlot.PlotScatter(FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit)

                #except:
                #        print("Wrong Path")
                #        self.showdialogPath()

        def showdialogPath(self):                                                                                                           #Funktion für die PopUp-Nachricht bei nichtausgewählter Amplifiereinstallung (Tab3)
                msg = QMessageBox()                                                                                                     #Setzt die MessageBox
                msg.setIcon(QMessageBox.Warning)                                                                                        #Setzt das Icon auf ein StandardIcon
                msg.setText("No Path selected")                                                                                         #Setzt den Text der MessageBox
                msg.setInformativeText("Please select a File")                                                                          #Setzt den Text für weitere Informationen
                msg.setWindowTitle("Error")                                                                                             #Setzt den Text in der Titel-Leiste des Fensters
                msg.setStandardButtons(QMessageBox.Ok)                                                                                  #Setzt einen Okay-Button
                                
                retval = msg.exec_()
        """
        #Alle Tabs - Ende Funktion
        def UpdateTTLNames(self):
                self.TTLroot.setItemText(0, NameTTL1)
                self.TTLroot.setItemText(1, NameTTL2)
                self.TTLroot2.setItemText(0, NameTTL1)
                self.TTLroot2.setItemText(1, NameTTL2)
                #self.TTLroot.Clear()
                #self.TTLroot.addItem(NameTTL1)
                #self.TTLroot.addItem(NameTTL2)

        def UpdateChannelNames(self):
                self.cbch11.setText(CH1)                                                                                                                #Setzt eine CheckBox
                self.cbch11.setToolTip("Sets the Input to " + CH1)                                                                                      #Setzt eine CheckBox-Beschreibung bei MouseOver
                self.cbch12.setText(CH2)                                                              
                self.cbch12.setToolTip("Sets the Input to " + CH2)                                 
                self.cbch13.setText(CH3)                                                         
                self.cbch13.setToolTip("Sets the Input to " + CH3)                                 
                self.cbch14.setText(CH4)                                                         
                self.cbch14.setToolTip("Sets the Input to " + CH4)                                
                self.cbch15.setText(CHA)                                                         
                self.cbch15.setToolTip("Sets the Input to " + CHA)                                   
                self.cbch16.setText(CHB)                                                           
                self.cbch16.setToolTip("Sets the Input to " + CHB)                                  
                self.cbch17.setText(L2)                                                           
                self.cbch17.setToolTip("Sets the Input to " + L2)                              
                self.cbch18.setText(L3)                                                         
                self.cbch18.setToolTip("Sets the Input to " + L3)                                  

                self.cbch21.setText(CH1)                                                           
                self.cbch21.setToolTip("Sets the Input to " + CH1)                          
                self.cbch22.setText(CH2)                                                       
                self.cbch22.setToolTip("Sets the Input to " + CH2)                           
                self.cbch23.setText(CH3)                                                      
                self.cbch23.setToolTip("Sets the Input to " + CH3)                             
                self.cbch24.setText(CH4)                                                          
                self.cbch24.setToolTip("Sets the Input to " + CH4)                               
                self.cbch25.setText(CHA)                                                        
                self.cbch25.setToolTip("Sets the Input to " + CHA)                              
                self.cbch26.setText(CHB)                                                        
                self.cbch26.setToolTip("Sets the Input to " + CHB)                                   
                self.cbch27.setText(L2)                                                              
                self.cbch27.setToolTip("Sets the Input to " + L2)                               
                self.cbch28.setText(L3)                                                         
                self.cbch28.setToolTip("Sets the Input to " + L3)                               

        def show_devset(self):
                self.devset = DeviceSettings()
                self.devset.show()                     

        def Hydra(self):
                self.H = HydraPopup()
                self.H.show()
                self.HY = HydraClose()     
                self.HY.progress_value.connect(self.HYconnect)
                self.HY.start()

        def HYconnect(self, val):
                if val == 1:
                        self.ende()

        def ende(self):                                                                                                                                 #Die Ende-Funktion beendet alle Prozesse
                global LEDPin
                
                try:
                        connMeasure.commit()                                                           
                        connMeasure.close()
                except:
                        connMeasure.close()                                                                                                   

                try:
                        connSync.commit()                                                           
                        connSync.close()
                except:
                        connSync.close()

                try:
                        connStack.commit()                                                           
                        connStack.close()
                except:
                        connStack.close()

                try:
                        connSlope.commit()                                                           
                        connSlope.close()
                except:
                        connSlope.close()

                try:
                        connDev.commit()                                                           
                        connDev.close()
                except:
                        connDev.close()

                try:
                        connPlot.commit()                                                           
                        connPlot.close()
                except:
                        connPlot.close()

                try:
                        connTTL.commit()                                                           
                        connTTL.close()
                except:
                        connTTL.close()

                try:
                        self.Txt_out.close()
                        self.Txt_sub.close()
                except:
                        print("No file opened")
                        
                try:
                        self.Manfred.killFred()                                                                                                         #Beendet den Thread, wenn der Button unchecked gesetzt wird                                                                                                                             #Beendet das Fenster
                except:
                        print("Thread not running")

                try:
                        self.Monty.killFred()                                                                                                           #Beendet den Thread, wenn der Button unchecked gesetzt wird                                                                                                                             #Beendet das Fenster
                except:
                        print("Thread not running")

                try:
                        self.FylingCircus.killFred()                                                                                                    #Beendet den Thread, wenn der Button unchecked gesetzt wird                                                                                                                             #Beendet das Fenster
                except:
                        print("Thread not running")

                try:
                        dacX.set_voltage(0)
                        dacY.set_voltage(0)
                        dacZ.set_voltage(0)
                except:
                        print("No DAC connected")
                
                try:
                        adc.stop_adc()
                except:
                        print("No ADC connected")
                        
                try:
                        plt.close()
                except:
                        print("No plot selected")

                try:
                        GPIO.output(14, 0)
                except:
                        pass

                try:
                        GPIO.output(15, 0)
                except:
                        pass
                
                try:
                        GPIO.output(17, 0)
                except:
                        pass
                
                try:
                        GPIO.output(18, 0)
                except:
                        pass

                try:
                        GPIO.output(22, 0)
                except:
                        pass

                try:
                        GPIO.output(27, 0)
                except:
                        pass

                GPIO.output(LEDPin, GPIO.LOW)
                GPIO.cleanup()
                Fenster.quitall(self)
                print("Programm beendet")

                sys.exit()                                                                                                                              #Beendet das Fenster



class SearchSlope(QThread):
        progress_Slope = pyqtSignal(int, int)
        
        def __init__(self, parent=None):
                QThread.__init__(self, parent)
                self.i = 0   
                self.APD1 = 0
                self.APD2 = 0
                self.Integration = 1
                                
                GPIO.output(LEDPin, GPIO.HIGH)
                time.sleep(0.5)

                self.Voltage = round(10,1)
                print("Voltage: " + str(self.Voltage))
                Poti.write_range(self.Voltage)

                self.XOffset = 0
                self.YOffset = 0
                print("Offset: " + str(self.XOffset) + "x" + str(self.YOffset))
                dacOffset.setAllVoltage(self.XOffset, self.YOffset, 0, 0)
                
        def run(self):
                global APDon
                
                dacX.set_voltage(4095)
                dacY.set_voltage(int(4095/2))
                i = 1000
                MaxValAPD1 = 0
                PosAPD1 = 2048
                MaxValAPD2 = 0
                PosAPD2 = 2048
                while i <= 3000:
                        dacZ.set_voltage(i)
                        self.APD1, self.APD2 = APDs.captureDual(self.Integration)
                        if self.APD1 > MaxValAPD1:
                                MaxValAPD1 = self.APD1
                                PosAPD1 = i
                        if self.APD2 > MaxValAPD2:
                                MaxValAPD2 = self.APD2
                                PosAPD2 = i
                        i += 1

                if PosAPD1 != PosAPD2:
                        if MaxValAPD1 >= MaxValAPD2:
                                self.XMax = PosAPD1
                        else:
                                self.XMax = PosAPD2
                else:
                        self.XMax = PosAPD1

                time.sleep(1)

                dacX.set_voltage(int(4095/2))
                dacY.set_voltage(4095)
                i = 1000
                MaxValAPD1 = 0
                PosAPD1 = 2048
                MaxValAPD2 = 0
                PosAPD2 = 2048
                while i <= 3000:
                        dacZ.set_voltage(i)
                        self.APD1, self.APD2 = APDs.captureDual(self.Integration)
                        if self.APD1 > MaxValAPD1:
                                MaxValAPD1 = self.APD1
                                PosAPD1 = i
                        if self.APD2 > MaxValAPD2:
                                MaxValAPD2 = self.APD2
                                PosAPD2 = i
                        i += 1

                if PosAPD1 != PosAPD2:
                        if MaxValAPD1 >= MaxValAPD2:
                                self.YMax = PosAPD1
                        else:
                                self.YMax = PosAPD2
                else:
                        self.YMax = PosAPD1

                self.progress_Slope.emit(self.XMax, self.YMax)
                dacZ.set_voltage(2048)
                GPIO.output(LEDPin, GPIO.LOW)
                                
        def kill(self):
                self.i = 1
                GPIO.output(LEDPin, GPIO.LOW)

#Die dritte Klasse ist ein zweiter Thread, also ein paraleler Prozess auf einem anderen Prozessorkern
class Plotter(QThread):
        progress_value = pyqtSignal(list, list)
        
        def __init__(self, a, b, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit, parent=None):
                QThread.__init__(self, parent)
                self.i = 0
                self.a = a
                self.b = b
                self.FilePath = FilePath
                self.DataStart = DataStart
                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = PlotCol
                self.Color = Color
                self.Plotname = Plotname
                self.Filename = Filename
                self.Range = Range
                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                self.FontWeight = FontWeight
                self.ScaleBarSize = ScaleBarSize
                self.ScaleBarSizeVertical = ScaleBarSizeVertical
                self.ScaleBarPosition = ScaleBarPosition
                self.ScaleBarOffset = ScaleBarOffset
                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY
                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop
                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit

        def run(self):
                #Endless Loop to calculate the Data
                while self.i == 0:
                        HydraPlot.PlotMesh(self.a, self.b, self.FilePath, self.DataStart, self.XCol, self.YCol, self.PlotCol, self.Color, self.Plotname, self.Filename, self.Range, self.ScaleBar, self.Fontsize, self.Fontcolor, self.FontWeight, self.ScaleBarSize, self.ScaleBarSizeVertical, self.ScaleBarPosition, self.ScaleBarOffset, self.XAxis, self.YAxis, self.ZAxis,self.InvertX, self.InvertY, self.Zoom, self.XStart, self.XStop, self.YStart, self.YStop, self.UseLimits, self.LowerLimit, self.UpperLimit)
                        self.i = 1

        def killFred(self):                                                                                                                             #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                self.i = 1

                
class CalcPlot1(QThread):
        progress_value = pyqtSignal(list, list)
        
        def __init__(self, q2, parent=None):
                QThread.__init__(self, parent)
                self.i = 0
                self.SenderQueue = q2

        def run(self):
                #Endless Loop to calculate the Data
                while self.i == 0:
                        self.data = self.SenderQueue.get()


        def killFred(self):                                                                                                                             #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                self.i = 1


                
class Calculator(QThread):
        #progress_value = pyqtSignal(list, list)
        progress_Filename = pyqtSignal(str)
        progress_value = pyqtSignal(list, list)
        
        def __init__(self, q, q2, integrationtime, xstart, xstop, ystart, ystop, bits, slope, subgrid, SetXSlope, SetYSlope, xstartsub, xstopsub, ystartsub, ystopsub, xstep, ystep, channeltimeing, parent=None):
                QThread.__init__(self, parent)
                global Version
                
                self.Integrationtime =  integrationtime
                XStartValue = xstart                                                                                                                    #Die Variablen werden in nichtlokale Variablen umgewandelt
                XStopValue = xstop                                                                                                                      #Die Variablen werden in nichtlokale Variablen umgewandelt
                YStartValue = ystart                                                                                                                    #Die Variablen werden in nichtlokale Variablen umgewandelt
                YStopValue = ystop
                XSlopeUpper = SetXSlope                                                                                                                 #Die Variablen werden in nichtlokale Variablen umgewandelt
                YSlopeUpper = SetYSlope
                XStartSub = xstartsub                                                                                                                   #Die Variablen werden in nichtlokale Variablen umgewandelt
                XStopSub = xstopsub                                                                                                                     #Die Variablen werden in nichtlokale Variablen umgewandelt
                YStartSub = ystartsub                                                                                                                   #Die Variablen werden in nichtlokale Variablen umgewandelt
                YStopSub = ystopsub
                XStep = xstep                                                                                                                           #Die Variablen werden in nichtlokale Variablen umgewandelt
                YStep = ystep             

                self.BitsValue = bits
                Slope = slope
                Subgrid = subgrid
                ChannelTimeing = channeltimeing

                #Globalvariables
                global CH1
                global CH2
                global CH3
                global CH4
                global CHA
                global CHB
                global L2
                global L3
                global DHTon
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoVoltage
                global DeviceVoltage

                PiezoX = PiezoDistanceX * (DeviceVoltage/PiezoVoltage)
                PiezoY = PiezoDistanceY * (DeviceVoltage/PiezoVoltage)

                #Queue
                self.CalcQueue = q                                                                                                                      #Queue übergibt Werte aus einem anderen Thread und arbeitet diese der Reihe nach ab
                self.SenderQueue = q2
                
                #Controllvariables
                self.i = 0

                #Data-File
                if bits == 0:
                        self.BitsValue = 64 
                elif bits == 1:
                        self.BitsValue = 128                                                                                                            #Gibt die Verstärkung im cmd aus
                elif bits == 2:         
                        self.BitsValue = 256                                                                                                            #Gibt die Verstärkung im cmd aus
                elif bits == 3:
                        self.BitsValue = 512                                                                                                            #Gibt die Verstärkung im cmd aus
                elif bits == 4:
                        self.BitsValue = 1024                                                                                                           #Gibt die Verstärkung im cmd aus
                elif bits == 5:
                        self.BitsValue = 2048                                                                                                           #Gibt die Verstärkung im cmd aus
                elif bits == 6:
                        self.BitsValue = 4096

                self.DateTime = time.strftime("%d-%m-%Y_%H-%M-%S")                                                                                      #Bestimmt das Datum und die Uhrzeit zu beginn der Messung
                self.DateTime2 = time.strftime("/home/pi/Desktop/Data/NewMeasurement_%d-%m-%Y_%H-%M-%S.txt")                                            #Setzt den Dateiname der txt-Datei
                self.DateTime3 = time.strftime("/home/pi/Desktop/Data/NewMeasurement_%d-%m-%Y_%H-%M-%S.png")

                self.progress_Filename.emit(self.DateTime)

                self.Txt_Messfile = open(self.DateTime2, "w")
                self.Txt_Messfile.write("Created with HydraScan " + str(Version) + "\n")
                self.Txt_Messfile.write("Start: " + str(XStartValue) + " X " + str(YStartValue) + "\n")                                                 #Schreibt die Messschranke in die txt-Datei
                self.Txt_Messfile.write("Stop: " + str(XStopValue) + " X " + str(YStopValue) + "\n")                                                    #Schreibt die Messschranke in die txt-Datei

                if Slope == True:
                        self.Txt_Messfile.write("X Slope: " + str(XSlopeUpper) + "\tY Slope: " + str(YSlopeUpper) + "\n")

                if DHTon == 1:
                        global DHTPin
                        try:
                                humidity, temperature = Adafruit_DHT.read_retry(TempSens, DHTPin)
                                self.Txt_Messfile.write("Temperature: " + str(temperature) + " *C\tHumidity: " + str(humidity) + " %\n")
                        except:
                                pass
                else:
                        pass

                       
                if Subgrid == True and ChannelTimeing == True:
                        self.Txt_Messfile.write("Subgrid-Start: " + str(XStartSub) + " X " + str(YStartSub) + "\n")                                     #Schreibt die Messschranke in die txt-Datei
                        self.Txt_Messfile.write("Subgrid-Stop: " + str(XStopSub) + " X " + str(YStopSub) + "\n")                                        #Schreibt die Messschranke in die txt-Datei
                        self.Txt_Messfile.write("Stepsize X: " + str(XStep) + "\tStepsize Z: " + str(YStep) + "\n")                                     #Schreibt die Messschranke in die txt-Datei

                self.Txt_Messfile.write("Measurement with:\t" + str(self.BitsValue) + " Pixel\n")                                                       #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Messfile.write("X-Range:\t" + str(PiezoX) + " nm\t" + "Y-Range:\t" + str(PiezoY) + " nm\n")                                    #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Messfile.write("Date: " + self.DateTime + "\n")                                                                                #Schreibt das Datum und die Uhrzeit in die txt-Datei
                self.Txt_Messfile.write("\n")                                   
                self.Txt_Messfile.write("Count\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")
                
                self.zNewCH1 = list()
                self.zNewCH2 = list()
                self.zNewCH3 = list()
                self.zNewCH4 = list()
                self.zNewL = list()
                self.zNewS = list()
                self.zNewL1 = list()
                self.zNewL2 = list()

        def run(self):
                #Endless Loop to calculate the Data
                global APDArduinoOn
                global APDBSOn
                
                while self.i == 0:
                        self.counter1 = 0
                        self.counter2 = 0
                        self.counter3 = 0
                        self.counter4 = 0
                        self.counter5 = 0
                        self.counter6 = 0
                        self.counter7 = 0
                        self.counter8 = 0
                        self.data = self.CalcQueue.get()                                                                                                #Get Data from the Queue
                        if APDBSOn == 1:
                                if self.data == -1:
                                        self.killFred()
                                elif self.data["value5"] != 0:
                                        self.get_uptime()
                                        self.counter1 = round((self.counter1/self.Integrationtime),2)
                                        self.counter2 = round((self.counter2/self.Integrationtime),2)
                                        self.counter5 = round((self.counter5/self.Integrationtime),2)
                                        self.counter6 = round((self.counter6/self.Integrationtime),2)
                                        self.Txt_Messfile.write(str(self.data["Counter"]) + "\t" + str(self.data["X"]) + "\t" + str(self.data["Y"]) + "\t" + str(self.data["Z"]) + "\t" + str(self.data["value1"]) + "\t" + str(self.data["value2"]) + "\t" + str(self.data["value3"]) + "\t" + str(self.data["value4"]) + "\t" + str(self.counter1) + "\t" + str(self.counter2) + "\t" + str(self.counter6) + "\t" + str(self.counter5) + "\n")
                                else:
                                        self.Txt_Messfile.write(str(self.data["Counter"]) + "\t" + str(self.data["X"]) + "\t" + str(self.data["Y"]) + "\t" + str(self.data["Z"]) + "\t" + str(self.data["value1"]) + "\t" + str(self.data["value2"]) + "\t" + str(self.data["value3"]) + "\t" + str(self.data["value4"]) + "\t" + str(self.counter1) + "\t" + str(self.counter2) + "\t" + str(self.counter6) + "\t" + str(self.counter5) + "\n")
                                self.data["value5"] = self.counter1
                                self.data["value6"] = self.counter2
                                self.data["value7"] = self.counter5
                                self.data["value8"] = self.counter6
                        elif APDArduinoOn == 1:
                                if self.data == -1:
                                        self.killFred()
                                else:
                                        self.counter1 = self.data["value5"]
                                        self.counter2 = self.data["value6"]
                                        self.counter5 = self.data["value7"]
                                        self.counter6 = self.data["value8"]
                                        self.Txt_Messfile.write(str(self.data["Counter"]) + "\t" + str(self.data["X"]) + "\t" + str(self.data["Y"]) + "\t" + str(self.data["Z"]) + "\t" + str(self.data["value1"]) + "\t" + str(self.data["value2"]) + "\t" + str(self.data["value3"]) + "\t" + str(self.data["value4"]) + "\t" + str(self.counter1) + "\t" + str(self.counter2) + "\t" + str(self.counter6) + "\t" + str(self.counter5) + "\n")
                        else:
                                if self.data == -1:
                                        self.killFred()
                                else:
                                        print(self.data["value5"])
                                        self.counter1 = self.data["value5"]
                                        self.counter2 = self.data["value6"]
                                        self.counter5 = self.data["value7"]
                                        self.counter6 = self.data["value8"]
                                        self.Txt_Messfile.write(str(self.data["Counter"]) + "\t" + str(self.data["X"]) + "\t" + str(self.data["Y"]) + "\t" + str(self.data["Z"]) + "\t" + str(self.data["value1"]) + "\t" + str(self.data["value2"]) + "\t" + str(self.data["value3"]) + "\t" + str(self.data["value4"]) + "\t" + str(self.counter1) + "\t" + str(self.counter2) + "\t" + str(self.counter6) + "\t" + str(self.counter5) + "\n")

                        try:
                                self.zNewL.append(self.counter1)
                                self.zNewS.append(self.counter2)
                                self.zNewL1.append(self.counter5)
                                self.zNewL2.append(self.counter6)

                                self.zNewCH1.append(self.data["value1"])
                                self.zNewCH2.append(self.data["value2"])
                                self.zNewCH3.append(self.data["value3"])
                                self.zNewCH4.append(self.data["value4"])
                        except:
                                pass
                        
                        #"""
                        try:
                                count = int(self.data["Counter"])
                                Rest = (count%self.BitsValue)

                                if Rest == 0:
                                        self.progress_value.emit(self.zNewL, self.zNewS)
                                        self.progress_Filename.emit(self.DateTime)
                                        self.zNewL = list()
                                        self.zNewS = list()
                        except:
                                pass
                        #"""
                self.progress_Filename.emit(self.DateTime)
                        
        #Tested but slow way to calculate the Data
        def get_count(self):
                #starttime = time.time()
                
                #Controlvariable
                i = 35

                #Countervariables
                #counter1 = 0
                #self.counter2 = 0
                #self.counter3 = 0
                #self.counter4 = 0
                #self.counter5 = 0
                #self.counter6 = 0
                #self.counter7 = 0
                #self.counter8 = 0
                statusnew1 = 0
                statusnew2 = 0
                statusnew3 = 0
                statusnew4 = 0
                statusnew5 = 0
                statusnew6 = 0
                statusnew7 = 0
                statusnew8 = 0
                statusold1 = 0
                statusold2 = 0
                statusold3 = 0
                statusold4 = 0
                statusold5 = 0
                statusold6 = 0
                statusold7 = 0
                statusold8 = 0

                #Loop to calcualte every Point of the Trace
                while i <= len(self.data["value5"])-1:
                        if self.data["value5"][i] == 128:
                                statusnew1 = 1
                        elif self.data["value5"][i] == 64:
                                statusnew2 = 2
                        elif self.data["value5"][i] == 32:
                                statusnew3 = 3
                        elif self.data["value5"][i] == 16:
                                statusnew4 = 4
                        elif self.data["value5"][i] == 8:
                                statusnew5 = 5
                        elif self.data["value5"][i] == 4:
                                statusnew6 = 6
                        elif self.data["value5"][i] == 2:
                                statusnew7 = 7
                        elif self.data["value5"][i] == 1:
                                statusnew8 = 8
                        elif self.data["value5"][i] == 192:
                                statusnew1 = 1
                                statusnew2 = 2
                        else:
                                statusnew1 = 0
                                statusnew2 = 0
                                statusnew3 = 0
                                statusnew4 = 0
                                statusnew5 = 0
                                statusnew6 = 0
                                statusnew7 = 0
                                statusnew8 = 0

                        if statusold1 == 0 and statusnew1 == 1:
                                self.counter1 = self.counter1 + 1
                        if statusold2 == 0 and statusnew2 == 2:
                                self.counter2 = self.counter2 + 1
                        if statusold3 == 0 and statusnew3 == 3:
                                self.counter3 = self.counter3 + 1
                        if statusold4 == 0 and statusnew4 == 4:
                                self.counter4 = self.counter4 + 1
                        if statusold5 == 0 and statusnew5 == 5:
                                self.counter5 = self.counter5 + 1
                        if statusold6 == 0 and statusnew6 == 6:
                                self.counter6 = self.counter6 + 1
                        if statusold7 == 0 and statusnew7 == 7:
                                self.counter7 = self.counter7 + 1
                        if statusold8 == 0 and statusnew8 == 8:
                                self.counter8 = self.counter8 + 1
                                        
                        statusold1 = statusnew1
                        statusold2 = statusnew2
                        statusold3 = statusnew3
                        statusold4 = statusnew4
                        statusold5 = statusnew5
                        statusold6 = statusnew6
                        statusold7 = statusnew7
                        statusold8 = statusnew8
                        i = i + 1

                #Processing the calculated Data
                #print("Counter CH1: " + str(self.counter1))
                #print("Counter CH2: " + str(self.counter2))

                #Save Data to txt-File
                #self.Txt_Messfile.write(str(self.data["Counter"]) + "\t" + str(self.data["X"]) + "\t" + str(self.data["Y"]) + "\t" + str(self.data["Z"]) + "\t" + str(self.data["value1"]) + "\t" + str(self.data["value2"]) + "\t" + str(self.data["value3"]) + "\t" + str(self.data["value4"]) + "\t" + str(round((self.counter1/self.Integrationtime),2)) + "\t" + str(round((self.counter2/self.Integrationtime),2)) + "\t" + str(round((self.counter6/self.Integrationtime),2)) + "\t" + str(round((self.counter5/self.Integrationtime),2)) + "\n")
                #stoptime = time.time()
                #runtime = stoptime - starttime
                #print(runtime)

        #Untested but fast way to calculate the Data
        def get_uptime(self):
                #starttime = time.time()
                #Controlvariable
                i = 35

                #Countervariables
                #CH1 = 0
                #CH2 = 0
                #L5 = 0
                #L4 = 0
                #L3 = 0
                #L2 = 0
                #L1 = 0
                #L0 = 0

                #Loop to calcualte every Point of the Trace
                while i <= len(self.data["value5"])-1:
                        self.counter1 += (int(self.data["value5"][i]) // 128)
                        Rest = (int(self.data["value5"][i]) % 128)
                        self.counter2 += (Rest // 64)
                        Rest = (Rest % 64)
                        self.counter3 += (Rest // 32)
                        Rest = (Rest % 32)
                        self.counter4 += (Rest // 16)
                        Rest = (Rest % 16)
                        self.counter5 += (Rest // 8)
                        Rest = (Rest % 8)
                        self.counter6 += (Rest // 4)
                        Rest = (Rest % 4)
                        self.counter7 += (Rest // 2)
                        Rest = (Rest % 2)
                        self.counter8 += (Rest // 1)
                        Rest = (Rest % 1)  
                        i += 1

                #Processing the calculated Data
                #print("Counts CH1: " + str(self.counter1))
                #print("Counts CH2: " + str(self.counter2))

                #self.Txt_Messfile.write(str(self.data["Counter"]) + "\t" + str(self.data["X"]) + "\t" + str(self.data["Y"]) + "\t" + str(self.data["Z"]) + "\t" + str(self.data["value1"]) + "\t" + str(self.data["value2"]) + "\t" + str(self.data["value3"]) + "\t" + str(self.data["value4"]) + "\t" + str(round((self.counter1/self.Integrationtime),2)) + "\t" + str(round((self.counter2/self.Integrationtime),2)) + "\t" + str(round((self.counter6/self.Integrationtime),2)) + "\t" + str(round((self.counter5/self.Integrationtime),2)) + "\n")
                
                #stoptime = time.time()
                #runtime = stoptime - starttime
                #print(runtime)

        def killFred(self):                                                                                                                             #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                self.i = 1                                                                                                                              #Die Kontrollvariable wird auf 1 gesetzt, um die Schleife in der run()-Methode zu beenden
                self.Txt_Messfile.close()
                time.sleep(0.2)                                                                                                                         #Wartet eine Sekunde
                print("Calculator beendet")


class Positioning(QThread):
        progress_value1 = pyqtSignal(float)
        progress_value2 = pyqtSignal(float)
        progress_value3 = pyqtSignal(float)
        progress_value4 = pyqtSignal(float)
        progress_value5 = pyqtSignal(float)
        progress_value6 = pyqtSignal(float)
        progress_value7 = pyqtSignal(float)
        progress_value8 = pyqtSignal(float)

        def __init__(self, integrationtime, CH1, CH2, CH3, CH4, CHA, CHB, L2, L3, parent=None):
                QThread.__init__(self, parent)
                self.CH1 = CH1
                self.CH2 = CH2
                self.CH3 = CH3
                self.CH4 = CH4
                self.CHA = CHA
                self.CHB = CHB
                self.L2 = L2
                self.L3 = L3

                if self.CHA == True or self.CHB == True or self.L2 == True or self.L3 == True:
                        self.Logic = 1
                else:
                        self.Logic = 0

                self.IntegrationTime = integrationtime

                self.i = 0                                                                                                                              #Kontrollvariable
                self.counter = 1
                self.value1 = 0
                self.value2 = 0
                self.value3 = 0
                self.value4 = 0
                self.value5 = 0
                self.value6 = 0
                self.value7 = 0
                self.value8 = 0
                
        def run(self):
                print(self.Logic)
                if self.Logic == 1:
                        if APDArduinoOn == 1:
                                APDs = ArduinoLogic()
                        elif APDBSOn == 1:
                                APDs = APDLogic(5000,self.IntegrationTime) 
                
                while self.i == 0:                                                                                                                      #Überprüft, ob der Messinterval innerhalb der Messgrenzen liegt
                        if self.i == 1:
                                self.killFred()
                                return
                        
                        if self.CH1 == True:
                                self.value1 = adc.read_adc(0, gain=GAIN)
                                #self.value1 = 1
                                self.progress_value1.emit((self.value1/32767)*6.144)
                        if self.CH2 == True:
                                self.value2 = adc.read_adc(1, gain=GAIN)
                                #self.value2 = 2
                                self.progress_value2.emit((self.value2/32767)*6.144)
                        if self.CH3 == True:
                                self.value3 = adc.read_adc(2, gain=GAIN)
                                #self.value3 = 3
                                self.progress_value3.emit((self.value3/32767)*6.144)
                        if self.CH4 == True:
                                self.value4 = adc.read_adc(3, gain=GAIN)
                                #self.value4 = 4
                                self.progress_value4.emit((self.value4/32767)*6.144)
                        if self.Logic:
                                if APDBSOn == 1:
                                        self.value5, self.value6 , self.value7, self.value8 = APDs.capture_and_calc()
                                        if self.CHA == True:
                                                self.progress_value5.emit(self.value5)
                                        if self.CHB == True:
                                                self.progress_value6.emit(self.value6)
                                        if self.L2 == True:
                                                self.progress_value7.emit(self.value7)
                                        if self.L3 == True:
                                                self.progress_value8.emit(self.value8)
                                elif APDArduinoOn == 1:
                                        self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                        self.value7 = 0
                                        self.value8 = 0
                                        if self.CHA == True:
                                                self.progress_value5.emit(self.value5)
                                        if self.CHB == True:
                                                self.progress_value6.emit(self.value6)
                                        if self.L2 == True:
                                                self.progress_value7.emit(self.value7)
                                        if self.L3 == True:
                                                self.progress_value8.emit(self.value8)
                        else:   
                                self.value5 = 0 
                                self.value6 = 0
                                self.value7 = 0
                                self.value8 = 0

                self.killFred()

        def killFred(self):                                                                                                                             #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                self.i = 1
                if self.Logic == 1:
                        APDs.closeDevice()
                try:
                        adc.stop_adc()
                except:
                        pass
                print("Fred beendet")


#Die dritte Klasse ist ein zweiter Thread, also ein paraleler Prozess auf einem anderen Prozessorkern
class Pointmeasurement(QThread):
        progress_value = pyqtSignal(int)
        progress_value1 = pyqtSignal(float)
        progress_value2 = pyqtSignal(float)
        progress_value3 = pyqtSignal(float)
        progress_value4 = pyqtSignal(float)
        progress_value5 = pyqtSignal(float)
        progress_value6 = pyqtSignal(float)
        progress_value7 = pyqtSignal(float)
        progress_value8 = pyqtSignal(float)

        def __init__(self, integrationtime, CH1, CH2, CH3, CH4, CHA, CHB, L2, L3, TTLsendPoint, TTLgetPoint, PointDelay, XPoint, YPoint, ZPoint, BitsPoint, parent=None):
                QThread.__init__(self, parent)
                global LEDPin
                self.LEDPin = LEDPin
                GPIO.add_event_detect(TTL1IN, GPIO.RISING, callback=self.EventHandler_rising, bouncetime = 5)

                self.IntegrationTime = integrationtime
                
                self.CH1 = CH1
                self.CH2 = CH2
                self.CH3 = CH3
                self.CH4 = CH4
                self.CHA = CHA
                self.CHB = CHB
                self.L2 = L2
                self.L3 = L3

                if self.CHA == True or self.CHB == True or self.L2 == True or self.L3 == True:
                        self.Logic = 1
                else:
                        self.Logic = 0

                self.TTLsendPoint = TTLsendPoint
                self.TTLgetPoint = TTLgetPoint
                self.PointDelay = PointDelay

                self.XPoint = XPoint
                self.YPoint = YPoint
                self.ZPoint = ZPoint
                self.BitsPoint = BitsPoint
                
                self.i = 0                                                                                                                              #Kontrollvariable
                self.counter = 1
                self.value1 = 0
                self.value2 = 0
                self.value3 = 0
                self.value4 = 0
                self.value5 = 0
                self.value6 = 0
                self.value7 = 0
                self.value8 = 0
                self.TTL = 0
                
                GPIO.output(LEDPin, GPIO.HIGH)
                time.sleep(0.5)
                

        def EventHandler_rising(self, pin):
                self.TTL = 1
                
        def run(self):
                global CH1
                global CH2
                global CH3
                global CH4
                global CHA
                global CHB
                global L2
                global L3
                global DHTon
                global APDBSOn
                global APDArduinoOn
                if self.Logic == 1:
                        if APDArduinoOn == 1:
                                APDs = ArduinoLogic()
                        elif APDBSOn == 1:
                                APDs = APDLogic(5000,self.IntegrationTime) 
                
                #Datafile
                self.DateTime = time.strftime("%d.%m.%Y %H:%M:%S")                                                                                      #Bestimmt das Datum und die Uhrzeit zu beginn der Messung
                self.DateTime2 = time.strftime("/home/pi/Desktop/Data/PointMeasurement_%d-%m-%Y_%H-%M-%S.txt")                                          #Setzt den Dateiname der txt-Datei
                self.DateTime4 = time.strftime("/home/pi/Desktop/Data/PointMeasurement_%d-%m-%Y_%H-%M-%S.png")                                          #Setzt den Dateiname der png-Datei
                self.DateTime5 = time.strftime("PointMeasurement %d.%m.%Y %H:%M:%S")

                self.Txt_Point = open(self.DateTime2, "w")                                                                                              #Erstellt und öffnet eine neue Datei im Schreibmodus

                self.Txt_Point.write("Pointmeasurement for " + str(self.PointDelay) + " Seconds\n")                                                     #Schreibt die Messschranke in die txt-Datei

                if self.TTLsendPoint == True:
                        if self.TTLgetPoint == True:
                                self.Txt_Point.write("TTL sent and recived\n")
                        else:
                                self.Txt_Point.write("TTL sent\n")
                
                self.Txt_Point.write("Measurement with " + str(self.BitsPoint) + " Pixel\n")                                                            #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Point.write("Date: " + self.DateTime + "\n")                                                                                   #Schreibt das Datum und die Uhrzeit in die txt-Datei
                
                if DHTon == 1:
                        global DHTPin
                        try:
                                humidity, temperature = Adafruit_DHT.read_retry(TempSens, DHTPin)
                                self.Txt_Point.write("Temperature: " + str(temperature) + " *C\tHumidity: " + str(humidity) + " %\n")
                        except:
                                pass
                else:
                        pass
                
                self.Txt_Point.write("\n")
                self.Txt_Point.write("Time[s]\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")

                #Measurement
                if self.TTLsendPoint == True:
                        GPIO.output(TTL1OUT, GPIO.HIGH)
                        time.sleep(0.01)
                        GPIO.output(TTL1OUT, GPIO.LOW)
                        if self.TTLgetPoint == True:
                                while self.TTL == 0 and self.i == 0:
                                        if self.CH1 == True:
                                                self.value1 = adc.read_adc(0, gain=GAIN)
                                                self.progress_value1.emit((self.value1/32767)*6.144)
                                        if self.CH2 == True:
                                                self.value2 = adc.read_adc(1, gain=GAIN)
                                                self.progress_value2.emit((self.value2/32767)*6.144)
                                        if self.CH3 == True:
                                                self.value3 = adc.read_adc(2, gain=GAIN)
                                                self.progress_value3.emit((self.value3/32767)*6.144)
                                        if self.CH4 == True:
                                                self.value4 = adc.read_adc(3, gain=GAIN)
                                                self.progress_value4.emit((self.value4/32767)*6.144)
                                        if self.Logic:
                                                if APDBSOn == 1:
                                                        self.value5, self.value6 , self.value7, self.value8 = APDs.capture_and_calc()
                                                        if self.CHA == True:
                                                                self.progress_value5.emit(self.value5)
                                                        if self.CHB == True:
                                                                self.progress_value6.emit(self.value6)
                                                        if self.L2 == True:
                                                                self.progress_value7.emit(self.value7)
                                                        if self.L3 == True:
                                                                self.progress_value8.emit(self.value8)
                                                elif APDArduinoOn == 1:
                                                        self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                        self.value7 = 0
                                                        self.value8 = 0
                                                        if self.CHA == True:
                                                                self.progress_value5.emit(self.value5)
                                                        if self.CHB == True:
                                                                self.progress_value6.emit(self.value6)
                                                        if self.L2 == True:
                                                                self.progress_value7.emit(self.value7)
                                                        if self.L3 == True:
                                                                self.progress_value8.emit(self.value8)
                                        else:   
                                                self.value5 = 0 
                                                self.value6 = 0
                                                self.value7 = 0
                                                self.value8 = 0
                                        self.Txt_Point.write(str(self.counter) + "\t" + str(self.XPoint) + "\t" + str(self.YPoint) + "\t" + str(self.ZPoint) + "\t" + str(self.value1) + "\t" + str(self.value2) + "\t" + str(self.value3) + "\t" + str(self.value4) + "\t" + str(self.value5) + "\t" + str(self.value6) + "\t" + str(self.value7) + "\t" + str(self.value8) + "\n")               #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab
                                        self.counter = self.counter + 1

                        else:
                                StartTime = time.time()
                                CurrentTime = StartTime
                                while CurrentTime <= (StartTime + self.PointDelay) and self.i == 0: 
                                        if self.CH1 == True:
                                                self.value1 = adc.read_adc(0, gain=GAIN)
                                                self.progress_value1.emit((self.value1/32767)*6.144)
                                        if self.CH2 == True:
                                                self.value2 = adc.read_adc(1, gain=GAIN)
                                                self.progress_value2.emit((self.value2/32767)*6.144)
                                        if self.CH3 == True:
                                                self.value3 = adc.read_adc(2, gain=GAIN)
                                                self.progress_value3.emit((self.value3/32767)*6.144)
                                        if self.CH4 == True:
                                                self.value4 = adc.read_adc(3, gain=GAIN)
                                                self.progress_value4.emit((self.value4/32767)*6.144)
                                        if self.Logic:
                                                if APDBSOn == 1:
                                                        self.value5, self.value6 , self.value7, self.value8 = APDs.capture_and_calc()
                                                        if self.CHA == True:
                                                                self.progress_value5.emit(self.value5)
                                                        if self.CHB == True:
                                                                self.progress_value6.emit(self.value6)
                                                        if self.L2 == True:
                                                                self.progress_value7.emit(self.value7)
                                                        if self.L3 == True:
                                                                self.progress_value8.emit(self.value8)
                                                elif APDArduinoOn == 1:
                                                        self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                        self.value7 = 0
                                                        self.value8 = 0
                                                        if self.CHA == True:
                                                                self.progress_value5.emit(self.value5)
                                                        if self.CHB == True:
                                                                self.progress_value6.emit(self.value6)
                                                        if self.L2 == True:
                                                                self.progress_value7.emit(self.value7)
                                                        if self.L3 == True:
                                                                self.progress_value8.emit(self.value8)
                                        else:   
                                                self.value5 = 0 
                                                self.value6 = 0
                                                self.value7 = 0
                                                self.value8 = 0
                                        self.Txt_Point.write(str(self.counter) + "\t" + str(self.XPoint) + "\t" + str(self.YPoint) + "\t" + str(self.ZPoint) + "\t" + str(self.value1) + "\t" + str(self.value2) + "\t" + str(self.value3) + "\t" + str(self.value4) + "\t" + str(self.value5) + "\t" + str(self.value6) + "\t" + str(self.value7) + "\t" + str(self.value8) + "\n")               #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab
                                        self.counter = self.counter + 1
                                        CurrentTime = time.time()
                else:
                        while self.i ==  0: 
                                if self.CH1 == True:
                                        self.value1 = adc.read_adc(0, gain=GAIN)
                                        self.progress_value1.emit((self.value1/32767)*6.144)
                                if self.CH2 == True:
                                        self.value2 = adc.read_adc(1, gain=GAIN)
                                        self.progress_value2.emit((self.value2/32767)*6.144)
                                if self.CH3 == True:
                                        self.value3 = adc.read_adc(2, gain=GAIN)
                                        self.progress_value3.emit((self.value3/32767)*6.144)
                                if self.CH4 == True:
                                        self.value4 = adc.read_adc(3, gain=GAIN)
                                        self.progress_value4.emit((self.value4/32767)*6.144)
                                if self.Logic:
                                        if APDBSOn == 1:
                                                self.value5, self.value6 , self.value7, self.value8 = APDs.capture_and_calc()
                                                if self.CHA == True:
                                                        self.progress_value5.emit(self.value5)
                                                if self.CHB == True:
                                                        self.progress_value6.emit(self.value6)
                                                if self.L2 == True:
                                                        self.progress_value7.emit(self.value7)
                                                if self.L3 == True:
                                                        self.progress_value8.emit(self.value8)
                                        elif APDArduinoOn == 1:
                                                self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                self.value7 = 0
                                                self.value8 = 0
                                                if self.CHA == True:
                                                        self.progress_value5.emit(self.value5)
                                                if self.CHB == True:
                                                        self.progress_value6.emit(self.value6)
                                                if self.L2 == True:
                                                        self.progress_value7.emit(self.value7)
                                                if self.L3 == True:
                                                        self.progress_value8.emit(self.value8)
                                else:   
                                        self.value5 = 0 
                                        self.value6 = 0
                                        self.value7 = 0
                                        self.value8 = 0
                                self.Txt_Point.write(str(self.counter) + "\t" + str(self.XPoint) + "\t" + str(self.YPoint) + "\t" + str(self.ZPoint) + "\t" + str(self.value1) + "\t" + str(self.value2) + "\t" + str(self.value3) + "\t" + str(self.value4) + "\t" + str(self.value5) + "\t" + str(self.value6) + "\t" + str(self.value7) + "\t" + str(self.value8) + "\n")               #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab
                                self.counter = self.counter + 1
                self.killFred()

        def killFred(self):                                                                                                                             #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                self.i = 1
                try:
                        adc.stop_adc()
                except:
                        pass
                if self.Logic == 1:
                        APDs.closeDevice()
                GPIO.remove_event_detect(TTL1IN)
                print("Fred beendet")
                time.sleep(0.2)
                self.Txt_Point.close()
                self.progress_value.emit(1)
                time.sleep(0.5)
                GPIO.output(LEDPin, GPIO.LOW)

        
#Die dritte Klasse ist ein zweiter Thread, also ein paraleler Prozess auf einem anderen Prozessorkern
class Measurement(QThread):
        progress_value = pyqtSignal(int)
        progress_bar = pyqtSignal(int)

        def __init__(self, q, integrationtime, channel, xDim, yDim, xoff, yoff, delaytime, bits, slope, subgrid, plot, SetXSlope, SetYSlope, xstartsub, xstopsub, ystartsub, ystopsub, xstep, ystep, steptime, sendTTL, getTTL, TTLOUT, TTLIN, OneWire, channeltimeing, DoStacks, stacks, stackstep, direct, ZStart, colors, plotname, filename, filepath, parent=None):
                QThread.__init__(self, parent)
                self.CalcQueue = q

                global PiezoDistanceZ
                global CH1
                global CH2
                global CH3
                global CH4
                global CHA
                global CHB
                global L2
                global L3
                global DHTon
                global LEDPin


                print("Fred beginnt")

                
                #Establishing TTL
                self.TTLOUT = TTLOUT
                self.TTLIN = TTLIN
                self.OneWire = OneWire
                if self.OneWire == 1:
                        self.TTLIN = self.TTLOUT

                self.LEDPin = LEDPin

                self.IntegrationTime = integrationtime
                self.Channel = channel
                self.XSlopeUpper = SetXSlope                                                                                                            #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YSlopeUpper = SetYSlope
                self.DelayTime = delaytime
                #print("------------ Delay -------------  " + str(self.DelayTime))
                self.XStartSub = xstartsub                                                                                                              #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.XStopSub = xstopsub                                                                                                                #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YStartSub = ystartsub                                                                                                              #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YStopSub = ystopsub
                self.XStep = xstep                                                                                                                      #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YStep = ystep                                                                                                                      #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.StepTime = steptime

                self.BitsValue = bits
                self.Slope1 = slope
                self.Subgrid1 = subgrid
                self.Plot1 = plot
                self.Filename = filename
                self.Filepath = filepath
                self.colors = colors
                self.Plotname = plotname
                self.sendTTL = sendTTL
                self.getTTL = getTTL
                self.ChannelTimeing = channeltimeing
                self.ScanPos = []

                self.PiezoDistanceZ = PiezoDistanceZ
                self.Stack1 = DoStacks
                self.Stacks = stacks
                self.StackStep = stackstep
                self.Direct = direct
                self.ZStartValue = ZStart
                self.StackRun = 1

                if self.Stack1 == False:
                        self.Stacks = 1
                        self.StackStep = 0
                        self.Direct = 0
                if self.Direct == 2:
                        self.ZStartValue = (self.ZStartValue + (((self.Stacks - 1) / 2) * int((self.StackStep * 1000) * (4096/self.PiezoDistanceZ))))
                        self.Direct = 1


                if self.Channel[0] == 1:
                        self.ChannelText = CH1
                elif self.Channel[1] == 1:
                        self.ChannelText = CH2
                elif self.Channel[2] == 1:
                        self.ChannelText = CH3
                elif self.Channel[3] == 1:
                        self.ChannelText = CH4
                elif self.Channel[4] == 1:
                        self.ChannelText = CHA
                elif self.Channel[5] == 1:
                        self.ChannelText = CHB
                elif self.Channel[6] == 1:
                        self.ChannelText = L2
                elif self.Channel[7] == 1:
                        self.ChannelText = L3

                self.Logic = False
                if self.Channel[4] == 1 or self.Channel[5] == 1 or self.Channel[6] == 1 or self.Channel[7] == 1:
                        self.Logic = True
                        
                if bits == 0:
                        self.BitsValue = 64 
                elif bits == 1:
                        self.BitsValue = 128                                                                                                            #Gibt die Verstärkung im cmd aus
                elif bits == 2:         
                        self.BitsValue = 256                                                                                                            #Gibt die Verstärkung im cmd aus
                elif bits == 3:
                        self.BitsValue = 512                                                                                                            #Gibt die Verstärkung im cmd aus
                elif bits == 4:
                        self.BitsValue = 1024                                                                                                           #Gibt die Verstärkung im cmd aus
                elif bits == 5:
                        self.BitsValue = 2048                                                                                                           #Gibt die Verstärkung im cmd aus
                elif bits == 6:
                        self.BitsValue = 4096

                self.XStartValue = 0                                                                                                                    #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.XStopValue = self.BitsValue-1                                                                                                      #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YStartValue = 0                                                                                                                    #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YStopValue = self.BitsValue-1

                if self.Slope1 == False:
                        self.XSlopeUpper = 0
                        self.YSlopeUpper = 0


                if self.Subgrid1 == False:
                        self.XStartSub = self.XStartValue                                                                                               #Die Variablen werden in nichtlokale Variablen umgewandelt
                        self.XStopSub = self.XStopValue                                                                                                 #Die Variablen werden in nichtlokale Variablen umgewandelt
                        self.YStartSub = self.YStartValue                                                                                               #Die Variablen werden in nichtlokale Variablen umgewandelt
                        self.YStopSub = self.YStopValue
                        self.XStep = 1                                                                                                                  #Die Variablen werden in nichtlokale Variablen umgewandelt
                        self.YStep = 1                                                                                                                  #Die Variablen werden in nichtlokale Variablen umgewandelt
                        self.StepTime = 0
                        self.sendTTL = 0
                        self.getTTL = 0
                else:
                        self.scanpositions = []
                        yscanpos = self.YStartSub
                        xscanpos = self.XStartSub
                        while yscanpos <= self.YStopSub:                                                                                                #Überprüft, ob der Messwert oberhalb der oberen Messgrenze liegt
                                while xscanpos <= self.XStopSub:                                        
                                        self.scanpositions = (xscanpos, yscanpos)
                                        self.ScanPos.append(self.scanpositions)
                                        xscanpos = xscanpos + self.XStep
                                yscanpos = yscanpos + self.YStep
                                xscanpos = self.XStartSub


                self.length = ((self.XStopValue - self.XStartValue + 1) * (self.YStopValue - self.YStartValue + 1))
                

                #print("Start: ", self.XStartValue, " X ", self.YStartValue)                                                                            #Gibt die Messschranke im cmd aus
                #print("Stop: ", self.XStopValue, " X ", self.YStopValue)                                                                               #Gibt die Messschranke im cmd aus
                #print("Plot: ", self.Plot1)                                                                                                            #Gibt das Messinterval im cmd aus
                
                #print("Measurement with ", str(self.BitsValue), " Pixel")                                                                              #Gibt die Verstärkung im cmd aus
                
                self.DateTime = time.strftime("%d.%m.%Y %H:%M:%S")                                                                                      #Bestimmt das Datum und die Uhrzeit zu beginn der Messung
                self.DateTime2 = time.strftime("/home/pi/Desktop/Data/Measurement_%d-%m-%Y_%H-%M-%S.txt")                                               #Setzt den Dateiname der txt-Datei
                self.DateTime4 = time.strftime("/home/pi/Desktop/Data/Measurement_%d-%m-%Y_%H-%M-%S.png")                                               #Setzt den Dateiname der png-Datei
                self.DateTime5 = time.strftime("Measurement %d.%m.%Y %H:%M:%S")
                self.DateTimeSub = time.strftime("/home/pi/Desktop/Data/Measurement_%d-%m-%Y_%H-%M-%S_Subgid.txt")                                      #Setzt den Dateiname der txt-Datei

                if self.Subgrid1 == True:
                        self.Txt_TTL = open(self.DateTimeSub, "w")
                        self.Txt_TTL.write("Start: " + str(self.XStartValue) + " X " + str(self.YStartValue) + "\n")                                    #Schreibt die Messschranke in die txt-Datei
                        self.Txt_TTL.write("Stop: " + str(self.XStopValue) + " X " + str(self.YStopValue) + "\n")                                       #Schreibt die Messschranke in die txt-Datei
                        self.Txt_TTL.write("Stepsize X: " + str(self.XStep) + "\tStepsize Z: " + str(self.YStep) + "\n")
                        self.Txt_TTL.write("Subgrid-Start: " + str(self.XStartSub) + " X " + str(self.YStartSub) + "\n")                                #Schreibt die Messschranke in die txt-Datei
                        self.Txt_TTL.write("Subgrid-Stop: " + str(self.XStopSub) + " X " + str(self.YStopSub) + "\n") 
                        self.Txt_TTL.write("Measurement with " + str(self.BitsValue) + " Pixel\n")                                                      #Schreibt die Verstärkung in die txt-Datei
                        self.Txt_TTL.write("Date: " + self.DateTime + "\n")                                                                             #Schreibt das Datum und die Uhrzeit in die txt-Datei
                        self.Txt_TTL.write("\n")
                        self.Txt_TTL.write("Count\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")

                if self.Subgrid1 == True and self.ChannelTimeing == True:
                        self.Txt_sub = open(self.DateTimeSub, "w")
                        self.Txt_sub.write("Start: " + str(self.XStartValue) + " X " + str(self.YStartValue) + "\n")                                    #Schreibt die Messschranke in die txt-Datei
                        self.Txt_sub.write("Stop: " + str(self.XStopValue) + " X " + str(self.YStopValue) + "\n")                                       #Schreibt die Messschranke in die txt-Datei
                        self.Txt_sub.write("Stepsize X: " + str(self.XStep) + "\tStepsize Z: " + str(self.YStep) + "\n")

                        if self.Slope1 == True:
                                self.Txt_sub.write("X Slope: " + str(self.XSlopeUpper) + "\tY Slope: " + str(self.YSlopeUpper) + "\n")

                        self.Txt_sub.write("Subgrid-Start: " + str(self.XStartSub) + " X " + str(self.YStartSub) + "\n")                                #Schreibt die Messschranke in die txt-Datei
                        self.Txt_sub.write("Subgrid-Stop: " + str(self.XStopSub) + " X " + str(self.YStopSub) + "\n")                                   #Schreibt die Messschranke in die txt-Datei
                        if self.sendTTL == True:
                                if self.getTTL == True:
                                        self.Txt_sub.write("TTL sent and recived\n")
                                else:
                                        self.Txt_sub.write("TTL sent\n")
                
                        self.Txt_sub.write("Measurement with " + str(self.BitsValue) + " Pixel\n")                                                      #Schreibt die Verstärkung in die txt-Datei
                        self.Txt_sub.write("Date: " + self.DateTime + "\n")                                                                             #Schreibt das Datum und die Uhrzeit in die txt-Datei
                        self.Txt_sub.write("\n")
                        self.Txt_sub.write("Count\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")

                self.i = 0                                                                                                                              #Kontrollvariable
                
                self.counter = 1
                self.counter2 = 1
                self.XRun = self.XStartValue
                self.YRun = self.YStartValue
                self.ZRun = self.ZStartValue
                print("ZRun: " + str(self.ZRun))
                self.value1 = 0
                self.value2 = 0
                self.value3 = 0
                self.value4 = 0
                self.value5 = 0
                self.value6 = 0
                self.value7 = 0
                self.value8 = 0
                self.TTL = 0
                
                GPIO.output(LEDPin, GPIO.HIGH)
                time.sleep(0.5)

                self.Voltage = round(xDim/10,1)
                print("Voltage: " + str(self.Voltage))
                Poti.write_range(self.Voltage)

                self.XOffset = xoff
                self.YOffset = yoff
                print("Offset: " + str(self.XOffset) + "x" + str(self.YOffset))
                dacOffset.setAllVoltage(self.XOffset, self.YOffset, 0, 0)


                time.sleep(2)

        def EventHandler_rising(self, pin):
                self.TTL = 1
                
        def run(self):
                global PiezoDistanceZ
                global APDArduinoOn
                global APDBSOn
                global FocusZ

                #APDread --------------------------------------------
                if self.Logic == True:
                        if APDArduinoOn == 1:
                                APDs = ArduinoLogic()
                        elif APDBSOn == 1:
                                APDs = APDLogic(5000,self.IntegrationTime) 
                
                self.starttime = time.time()
                
                self.z1 = []
                self.z2 = []
                self.z3 = []
                self.z4 = []
                self.z5 = []
                self.z6 = []
                self.z7 = []
                self.z8 = []
                z1part = []
                z2part = []
                z3part = []
                z4part = []
                z5part = []
                z6part = []
                z7part = []
                z8part = []
                
                self.counterIntern = 1
                self.counterSubgrid = 0
                self.StackZPos = self.ZStartValue
                while self.i == 0:
                        while self.StackRun <= self.Stacks:
                                ZPosition = self.StackZPos
                                while self.YRun <= self.YStopValue:                                                                                     #Überprüft, ob der Messwert oberhalb der oberen Messgrenze liegt
                                        while self.XRun <= self.XStopValue:
                                                #starttime = time.time()
                                                if self.Stack1 == False:
                                                        if self.Slope1 == True:
                                                                XSlopePos = (self.XSlopeUpper - (self.XRun * ((self.XSlopeUpper*2)/self.BitsValue)))
                                                                YSlopePos = (self.YSlopeUpper - (self.YRun * ((self.YSlopeUpper*2)/self.BitsValue)))
                                                                SlopePos = (XSlopePos + YSlopePos)
                                                                SlopeVal = ((((SlopePos + 2000) / 4000) * self.BitsValue))
                                                                ZPosition = int(SlopeVal * (4095 / self.BitsValue))
                                                        else:
                                                                ZPosition = FocusZ
                                                        
                                                #print("ZPosition: " + str(ZPosition))
                                                dacZ.set_voltage(ZPosition)                       
                                                dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                                dacY.set_voltage(int(self.YRun * (4095 / self.BitsValue)))
                                                
                                                ScanPosition = (self.XRun, self.YRun)
                                                if ScanPosition in self.ScanPos:
                                                        self.counterSubgrid = self.counterSubgrid + 1
                                                        if self.sendTTL == True:
                                                                if self.OneWire == 1 and self.counter != 0:
                                                                        GPIO.setup(self.TTLOUT, GPIO.OUT, initial=GPIO.HIGH)
                                                                        self.Txt_TTL.write(str(self.counterIntern) + "." + str(0) + "\t" + str(self.XRun) + "\t" + str(self.YRun) + "\n")                #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab                          
                                                                else:
                                                                        GPIO.output(self.TTLOUT, GPIO.HIGH)
                                                                        self.Txt_TTL.write(str(self.counterIntern) + "." + str(0) + "\t" + str(self.XRun) + "\t" + str(self.YRun) + "\n")                #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab                          
                                                                time.sleep(0.005)
                                                                GPIO.output(self.TTLOUT, GPIO.LOW)
                                                                
                                                                if self.OneWire == 1 and self.counter != 0:
                                                                        GPIO.setup(self.TTLIN, GPIO.IN)
                                                                        
                                                                if self.getTTL == True:
                                                                        self.TTL = 0
                                                                        GPIO.add_event_detect(self.TTLIN, GPIO.RISING, callback=self.EventHandler_rising, bouncetime = 5)
                                                                        #print(str(self.TTLIN) + " Event added")
                                                                        if self.ChannelTimeing == True:
                                                                                while self.TTL == 0: 
                                                                                        if self.Channel[0] == 1:
                                                                                                self.value1 = adc.read_adc(0, gain=GAIN)
                                                                                                #self.value1 = 1
                                                                                        if self.Channel[1] == 1:
                                                                                                self.value2 = adc.read_adc(1, gain=GAIN)
                                                                                                #self.value2 = 2
                                                                                        if self.Channel[2] == 1:
                                                                                                self.value3 = adc.read_adc(2, gain=GAIN)
                                                                                                #self.value3 = 3
                                                                                        if self.Channel[3] == 1:
                                                                                                self.value4 = adc.read_adc(3, gain=GAIN)
                                                                                                #self.value4 = 4
                                                                                        if self.Logic:
                                                                                                print("1")
                                                                                                if APDBSOn == 1:
                                                                                                        self.value5, self.value6 , self.value7, self.value8 = APDs.capture_and_calc()
                                                                                                        self.value5 = self.value5/self.IntegrationTime 
                                                                                                        self.value6 = self.value6/self.IntegrationTime
                                                                                                        self.value7 = self.value7/self.IntegrationTime
                                                                                                        self.value8 = self.value8/self.IntegrationTime
                                                                                                elif APDArduinoOn == 1:
                                                                                                        self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                                                        self.value7 = 0
                                                                                                        self.value8 = 0
                                                                                                else:                                                                     
                                                                                                        self.value5 = 0 
                                                                                                        self.value6 = 0
                                                                                                        #self.value5 = random.randint(5, 100)
                                                                                                        #self.value6 = random.randint(5, 100)  
                                                                                                        self.value7 = 0  
                                                                                                        self.value8 = 0     

                                                                                        self.Txt_sub.write(str(self.counter) + "." + str(self.counter2) + "\t" + str(self.XRun) + "\t" + str(self.YRun) + "\t" + str(SlopeVal) + "\t" + str(self.value1) + "\t" + str(self.value2) + "\t" + str(self.value3) + "\t" + str(self.value4) + "\t" + str(self.value5) + "\t" + str(self.value6) + "\t" + str(self.value7) + "\t" + str(self.value8) + "\n")                #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab                          
                                                                                        self.counter2 = self.counter2 + 1
                                                                                        CurrentTime = time.time()
                                                                        else:
                                                                                while self.TTL == 0:
                                                                                        pass
                                                                        GPIO.remove_event_detect(self.TTLIN)
                                                                elif self.ChannelTimeing == True:
                                                                        StartTime = time.time()
                                                                        CurrentTime = StartTime
                                                                        while CurrentTime <= (StartTime + self.StepTime): 
                                                                                if self.Channel[0] == 1:
                                                                                        self.value1 = adc.read_adc(0, gain=GAIN)
                                                                                        #self.value1 = 1
                                                                                if self.Channel[1] == 1:
                                                                                        self.value2 = adc.read_adc(1, gain=GAIN)
                                                                                        #self.value2 = 2
                                                                                if self.Channel[2] == 1:
                                                                                        self.value3 = adc.read_adc(2, gain=GAIN)
                                                                                        #self.value3 = 3
                                                                                if self.Channel[3] == 1:
                                                                                        self.value4 = adc.read_adc(3, gain=GAIN)
                                                                                        #self.value4 = 4
                                                                                if self.Logic:
                                                                                        print("2")
                                                                                        if APDBSOn == 1:
                                                                                                self.value5, self.value6 , self.value7, self.value8 = APDs.capture_and_calc()
                                                                                                self.value5 = self.value5/self.IntegrationTime 
                                                                                                self.value6 = self.value6/self.IntegrationTime
                                                                                                self.value7 = self.value7/self.IntegrationTime
                                                                                                self.value8 = self.value8/self.IntegrationTime
                                                                                        elif APDArduinoOn == 1:
                                                                                                self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                                                self.value7 = 0
                                                                                                self.value8 = 0
                                                                                        else:                                          
                                                                                                self.value5 = 0 
                                                                                                self.value6 = 0
                                                                                                #self.value5 = random.randint(5, 100)
                                                                                                #self.value6 = random.randint(5, 100) 
                                                                                                self.value7 = 0  
                                                                                                self.value8 = 0                       
                                                                                self.Txt_sub.write(str(self.counter) + "." + str(self.counter2) + "\t" + str(self.XRun) + "\t" + str(self.YRun) + "\t" + str(SlopeVal) + "\t" + str(self.value1) + "\t" + str(self.value2) + "\t" + str(self.value3) + "\t" + str(self.value4) + "\t" + str(self.value5) + "\t" + str(self.value6) + "\t" + str(self.value7) + "\t" + str(self.value8) + "\n")                #Schreibt den Messwert und die Messzeit in die txt-Datei, getrennt durch ein Tab                          
                                                                                self.counter2 = self.counter2 + 1
                                                                                CurrentTime = time.time()
                                                                else:
                                                                        StartTime = time.time()
                                                                        CurrentTime = StartTime
                                                                        while CurrentTime <= (StartTime + self.StepTime): 
                                                                                CurrentTime = time.time()
                                                                self.counter2 = 1
                                                        else:
                                                                time.sleep(self.StepTime)

                                                #midtime1 = time.time()
                                                if self.Channel[0] == 1:
                                                        self.value1 = adc.read_adc(0, gain=GAIN)
                                                        z1part.append((self.value1/32767)*6.144)
                                                if self.Channel[1] == 1:
                                                        self.value2 = adc.read_adc(1, gain=GAIN)
                                                        z2part.append((self.value2/32767)*6.144)
                                                if self.Channel[2] == 1:
                                                        self.value3 = adc.read_adc(2, gain=GAIN)
                                                        z3part.append((self.value3/32767)*6.144)
                                                if self.Channel[3] == 1:
                                                        self.value4 = adc.read_adc(3, gain=GAIN)
                                                        z4part.append((self.value4/32767)*6.144)
                                                if self.Logic:
                                                        if APDBSOn == 1:
                                                                self.value5 = APDs.captureData()
                                                                #self.value5, self.value6 , self.value7, self.value8 = APDs.captureData()
                                                                #z5part.append((self.value5/self.IntegrationTime))                
                                                                z5part.append(5)
                                                                #z6part.append((self.value6/self.IntegrationTime))             
                                                                z6part.append(6)
                                                                #z7part.append((self.value7/self.IntegrationTime))             
                                                                z7part.append(7)
                                                                #z8part.append((self.value8/self.IntegrationTime))
                                                                z8part.append(8)
                                                        elif APDArduinoOn == 1:
                                                                self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                self.value7 = 0
                                                                self.value8 = 0
                                                                z5part.append(self.value5)
                                                                z6part.append(self.value6)
                                                                z7part.append(self.value7)
                                                                z8part.append(self.value8)
                                                        else:                                          
                                                                #self.value5 = 0 
                                                                #self.value6 = 0
                                                                self.value5 = random.randint(5, 100)
                                                                self.value6 = random.randint(5, 100) 
                                                                self.value7 = 0  
                                                                self.value8 = 0
                                                #midtime2 = time.time()

                                                SlopeVal = round(ZPosition, 2)

                                                #Data to Calculator-Thread ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                self.data = {
                                                        "Counter":self.counter,
                                                        "X":self.XRun-self.XStartValue,
                                                        "Y":self.YRun-self.YStartValue,
                                                        "Z":ZPosition,
                                                        "value1":self.value1,
                                                        "value2":self.value2,
                                                        "value3":self.value3,
                                                        "value4":self.value4,
                                                        "value5":self.value5,
                                                        "value6":self.value6,
                                                        "value7":self.value7,
                                                        "value8":self.value8
                                                        } 
                                                self.CalcQueue.put(self.data)
                                                #midtime3 = time.time()
                                                
                                                progress = int((self.counterIntern) * (100 / (self.length*self.Stacks)))
                                                self.progress_bar.emit(progress)
                                                self.XRun = self.XRun + 1
                                                self.counter = self.counter + 1
                                                self.counterIntern = self.counterIntern + 1

                                                #endtime = time.time()
                                                #print("Steptime: " + str(endtime - starttime))
                                                #print("Time till Measurement: " + str(midtime1 - starttime))
                                                #print("Time till Data recieved: " + str(midtime2 - midtime1))
                                                #print("Time till Data calculated: " + str(midtime3 - midtime2))
                                                #print("Time till End: " + str(endtime - midtime3))
                                                time.sleep(self.DelayTime)                                                                              #Setzt die Wartezeit zwischen den Spalten

                                        self.YRun = self.YRun + 1
                                        self.XRun = self.XStartValue
                                        dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                        self.z1.append(z1part)
                                        z1part = []
                                        self.z2.append(z2part)
                                        z2part = []
                                        self.z3.append(z3part)
                                        z3part = []
                                        self.z4.append(z4part)
                                        z4part = []
                                        self.z4.append(z4part)
                                        z4part = []
                                        self.z5.append(z5part)
                                        z5part = []
                                        self.z6.append(z6part)
                                        z6part = []
                                        self.z7.append(z7part)
                                        z7part = []
                                        self.z8.append(z8part)
                                        z8part = []
                                        self.POS = []
                                self.counter = 1
                                self.YRun = self.YStartValue
                                self.StackRun = self.StackRun + 1
                                
                                if self.Direct == 0:
                                        self.StackZPos = int(self.StackZPos + ((self.StackStep * 1000) * (4096/self.PiezoDistanceZ)))
                                elif self.Direct == 1:
                                        self.StackZPos = int(self.StackZPos - ((self.StackStep * 1000) * (4096/self.PiezoDistanceZ)))

                                if self.StackZPos <= 0:
                                        self.StackZPos = 0
                                elif self.StackZPos >=4095:
                                        self.StackZPos = 4095

                        self.progress_bar.emit(100)
                        self.data = -1
                        self.CalcQueue.put(self.data)

                        self.stoptime = time.time()
                        self.runtime = self.stoptime - self.starttime
                        print(self.runtime)
                        """
                        self.PlotOn = PlotOn
                        try:
                                if self.Plot1 == True:
                                        Channels = self.Channel
                                        Ch1 = self.z1
                                        Ch2 = self.z2
                                        Ch3 = self.z3
                                        Ch4 = self.z4
                                        Ch5 = self.z5
                                        Ch6 = self.z6
                                        Ch7 = self.z7
                                        Ch8 = self.z8
                                        YStart = self.YStartValue
                                        YStop = self.YStopValue
                                        XStart = self.XStartValue
                                        XStop = self.XStopValue
                                        Colors = self.colors
                                        Plotname = self.Plotname
                                        Filename = self.DateTime4
                                        if self.Channel[4] == 1:
                                                self.plotData(Ch5)
                                        elif self.Channel[5] == 1:
                                                self.plotData(Ch6)
                                        else:
                                                self.LifeOfBrian = PlotData(Channels,Ch1,Ch2,Ch3,Ch4,Ch5,Ch6,Ch7,Ch8,XStart,XStop,YStart,YStop,Colors,Plotname,Filename)            
                        except:
                                print("Plot not possible")
                        """
                        self.i = 1
                        self.killFred()

        def killFred(self):    
                self.i = 1                                                                                                                              #Beendet den Schreibmodus und schließt die txt-Datei
                try:
                        self.Txt_sub.close()                                                                                                            #Beendet den Schreibmodus und schließt die txt-Datei
                except:
                        print("No Subgrid")                                                                                                             #Beendet den Schreibmodus und schließt die txt-Datei
                try:
                        self.Txt_TTL.close()                                                                                                            #Beendet den Schreibmodus und schließt die txt-Datei
                except:
                        print("No Subgrid")             

                zpart = []
                self.POS = []
                try:
                        adc.stop_adc()
                except:
                        pass
                try:
                        GPIO.remove_event_detect(self.TTLIN)
                except:
                        pass
                try:
                        dacX.set_voltage(0)
                        dacY.set_voltage(0)
                        dacZ.set_voltage(2047)
                except:
                        pass
                try:
                        APDs.closeDevice()
                except:
                        pass

                try:
                        self.Voltage = 10
                        Poti.write_range(self.Voltage)
                except:
                        pass
                
                try:
                        dacOffset.setAllVoltage(0, 0, 0, 0)
                except:
                        pass
                self.progress_bar.emit(100) 
                self.progress_value.emit(1)
                time.sleep(0.5)
                GPIO.output(LEDPin, GPIO.LOW)
                print("Fred beendet")                                                                                                                   #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen

        def killFredHard(self):
                self.i = 1                                                                                                                              #Beendet den Schreibmodus und schließt die txt-Datei
                try:
                        self.Txt_sub.close()                                                                                                            #Beendet den Schreibmodus und schließt die txt-Datei
                except:
                        print("No Subgrid")             

                zpart = []
                self.POS = []
                try:
                        adc.stop_adc()
                except:
                        pass
                GPIO.remove_event_detect(self.TTLIN)
                dacX.set_voltage(0)
                dacY.set_voltage(0)
                dacZ.set_voltage(2047)
                dacOffset.setAllVoltage(0, 0, 0, 0)
                Poti.write_range(self.Voltage)
                self.progress_bar.emit(100) 
                self.progress_value.emit(1) 
                GPIO.output(LEDPin, GPIO.LOW)
                self.terminate()
                print("Fred beendet")  
                
                
        def plotData(self, CH):
                if self.Plot1 == True:
                        #Plot
                        dx, dy = 1, 1                                                                                                                   #Schrittweite
                        y, x = np.mgrid[slice(self.YStartValue, self.YStopValue+1, dy), slice(self.XStartValue, self.XStopValue+1, dx)]                 #Setzt das 2D-Grid mit der bestimmten Schrittweite und Start und Endwert

                        if self.colors == 1:
                                cmap = plt.get_cmap('Spectral_r')                                                                                       #Spektralfarben
                        elif self.colors == 2:
                                cmap = plt.get_cmap('gray_r')                                                                                           #Graustufen
                        elif self.colors == 3:
                                cmap = plt.get_cmap('bone')                                                                                             #Blau zu Grün
                        elif self.colors == 4:
                                cmap = plt.get_cmap('Wistia')                                                                                           #Gelb zu Rot
                        elif self.colors == 5:
                                cmap = plt.get_cmap('copper')                                                                                           #Lila zu Gelb
                        elif self.colors == 6:
                                cmap = plt.get_cmap('gist_heat')                                                                                        #Graustufen
                        elif self.colors == 7:
                                cmap = plt.get_cmap('winter')                                                                                           #Blau zu Grün
                        elif self.colors == 8:
                                cmap = plt.get_cmap('spring')                                                                                           #Gelb zu Rot
                        elif self.colors == 9:
                                cmap = plt.get_cmap('summer')                                                                                           #Lila zu Gelb
                        elif self.colors == 10:
                                cmap = plt.get_cmap('autumn')                                                                                           #Graustufen
                        elif self.colors == 11:
                                cmap = plt.get_cmap('hot_r')                                                                                            #Blau zu Grün
                        elif self.colors == 12:
                                cmap = plt.get_cmap('cool')                                                                                             #Lila zu Gelb
                        elif self.colors == 13:
                                cmap = plt.get_cmap('gist_ncar')                                                                                        #Graustufen
                        elif self.colors == 14:
                                cmap = plt.get_cmap('nipy_spectral')                                                                                    #Blau zu Grün
                        elif self.colors == 15:
                                cmap = plt.get_cmap('Reds')                                                                                             #Lila zu Gelb


                        levels = MaxNLocator(nbins=100).tick_values(0, 100)                                                                             #characterizes the bar right
                        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  


                        fig, ax1  = plt.subplots()                                                                                                      #Adds the plot to the figure

                        im1 = ax1.pcolormesh(x, y, CH, cmap=cmap, norm=norm)
            
                        fig.colorbar(im1, ax=ax1)
                        ax1.set_title(self.Plotname)

                        ax1.invert_yaxis()                                                                                                              #invertiert die y-Achse
                        ax1.xaxis.tick_top()                                                                                                            #setzt die x-Achse nach oben

                        try:
                                plt.savefig(self.DateTime4)
                        except:
                                print("Saving Plot not possible")

                        try:
                                
                                plt.show()                                                                                                              #Plot
                        except:
                                print("Plot not posible")
                        PlotOn = 1
                else:
                        print("No plot selected")

        def plotData2(self):
                if self.Plot1 == True:
                        #Plot
                        
                        dx, dy = 1, 1                                                                                                                   #Schrittweite
                        y, x = np.mgrid[slice(self.YStartValue, self.YStopValue+1, dy), slice(self.XStartValue, self.XStopValue+1, dx)]                 #Setzt das 2D-Grid mit der bestimmten Schrittweite und Start und Endwert

                        # pick the desired colormap
                        if self.colors == 1:
                                cmap = plt.get_cmap('Spectral_r')                                                                                       #Spektralfarben
                        elif self.colors == 2:
                                cmap = plt.get_cmap('gray_r')                                                                                           #Graustufen
                        elif self.colors == 3:
                                cmap = plt.get_cmap('bone')                                                                                             #Blau zu Grün
                        elif self.colors == 4:
                                cmap = plt.get_cmap('Wistia')                                                                                           #Gelb zu Rot
                        elif self.colors == 5:
                                cmap = plt.get_cmap('copper')                                                                                           #Lila zu Gelb
                        elif self.colors == 6:
                                cmap = plt.get_cmap('gist_heat')                                                                                        #Graustufen
                        elif self.colors == 7:
                                cmap = plt.get_cmap('winter')                                                                                           #Blau zu Grün
                        elif self.colors == 8:
                                cmap = plt.get_cmap('spring')                                                                                           #Gelb zu Rot
                        elif self.colors == 9:
                                cmap = plt.get_cmap('summer')                                                                                           #Lila zu Gelb
                        elif self.colors == 10:
                                cmap = plt.get_cmap('autumn')                                                                                           #Graustufen
                        elif self.colors == 11:
                                cmap = plt.get_cmap('hot_r')                                                                                            #Blau zu Grün
                        elif self.colors == 12:
                                cmap = plt.get_cmap('cool')                                                                                             #Lila zu Gelb
                        elif self.colors == 13:
                                cmap = plt.get_cmap('gist_ncar')                                                                                        #Graustufen
                        elif self.colors == 14:
                                cmap = plt.get_cmap('nipy_spectral')                                                                                    #Blau zu Grün
                        elif self.colors == 15:
                                cmap = plt.get_cmap('Reds')                                                                                             #Lila zu Gelb


                        levels = MaxNLocator(nbins=50).tick_values(0, 5.4)                                                                              #characterizes the bar right
                        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                        fig, ax  = plt.subplots()
                                                
                        self.data=[]
                        plotnumber = 0
                        if len(self.z1[0]) != 0:
                                #im0 = ax[plotnumber].pcolormesh(x, y, self.z1, cmap=cmap, norm=norm)
                                self.data.append([x, y, self.z1])
                                plotnumber = plotnumber + 1
                        elif len(self.z2[0]) != 0:
                                #im[plotnumber] = ax[plotnumber].pcolormesh(x, y, self.z2, cmap=cmap, norm=norm)
                                self.data.append([x, y, self.z2])
                                plotnumber = plotnumber + 1
                        elif len(self.z3[0]) != 0:
                                #im[plotnumber] = ax[plotnumber].pcolormesh(x, y, self.z3, cmap=cmap, norm=norm)
                                self.data.append([x, y, self.z3])
                                plotnumber = plotnumber + 1     
                        elif len(self.z4[0]) != 0:    
                                #im[plotnumber] = ax[plotnumber].pcolormesh(x, y, self.z4, cmap=cmap, norm=norm)
                                self.data.append([x, y, self.z4])
                                plotnumber = plotnumber + 1
                        elif len(self.z5[0]) != 0:
                                #im[plotnumber] = ax[plotnumber].pcolormesh(x, y, self.z5, cmap=cmap, norm=norm)
                                self.data.append([x, y, self.z5])
                                plotnumber = plotnumber + 1
                        else:
                                print("No Data aqiured")
            
                        i = 0
                        while i <= plotnumber:
                                pc = ax.pcolormesh(self.data[i,0], self.data[i,1], self.data[i,2], cmap=cmap, norm=norm)
                                i = i + 1

                        fig.colorbar(pc, ax=ax)
                        ax.set_title(self.Plotname)

                        ax.invert_yaxis()                                                                                                               #invertiert die y-Achse
                        ax.xaxis.tick_top()                                                                                                             #setzt die x-Achse nach oben

                        try:
                                plt.savefig(self.DateTime4)
                        except:
                                print("Saving Plot not possible")

                        try:
                                
                                plt.show()                                                                                                              #Plot
                        except:
                                print("Plot not posible")
                        PlotOn = 1
                else:
                        print("No plot selected")


        def plotData3(self):
                if self.Plot1 == True:
                        #Plot
                        
                        dx, dy = 1, 1                                                                                                                   #Schrittweite
                        y, x = np.mgrid[slice(self.YStartValue, self.YStopValue+1, dy), slice(self.XStartValue, self.XStopValue+1, dx)]                 #Setzt das 2D-Grid mit der bestimmten Schrittweite und Start und Endwert

                        # pick the desired colormap
                        if self.colors == 1:
                                cmap = plt.get_cmap('Spectral_r')                                                                                       #Spektralfarben
                        elif self.colors == 2:
                                cmap = plt.get_cmap('gray_r')                                                                                           #Graustufen
                        elif self.colors == 3:
                                cmap = plt.get_cmap('bone')                                                                                             #Blau zu Grün
                        elif self.colors == 4:
                                cmap = plt.get_cmap('Wistia')                                                                                           #Gelb zu Rot
                        elif self.colors == 5:
                                cmap = plt.get_cmap('copper')                                                                                           #Lila zu Gelb
                        elif self.colors == 6:
                                cmap = plt.get_cmap('gist_heat')                                                                                        #Graustufen
                        elif self.colors == 7:
                                cmap = plt.get_cmap('winter')                                                                                           #Blau zu Grün
                        elif self.colors == 8:
                                cmap = plt.get_cmap('spring')                                                                                           #Gelb zu Rot
                        elif self.colors == 9:
                                cmap = plt.get_cmap('summer')                                                                                           #Lila zu Gelb
                        elif self.colors == 10:
                                cmap = plt.get_cmap('autumn')                                                                                           #Graustufen
                        elif self.colors == 11:
                                cmap = plt.get_cmap('hot_r')                                                                                            #Blau zu Grün
                        elif self.colors == 12:
                                cmap = plt.get_cmap('cool')                                                                                             #Lila zu Gelb
                        elif self.colors == 13:
                                cmap = plt.get_cmap('gist_ncar')                                                                                        #Graustufen
                        elif self.colors == 14:
                                cmap = plt.get_cmap('nipy_spectral')                                                                                    #Blau zu Grün
                        elif self.colors == 15:
                                cmap = plt.get_cmap('Reds')                                                                                             #Lila zu Gelb


                        levels = MaxNLocator(nbins=50).tick_values(0, 5.4)                                                                              #characterizes the bar right
                        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                        plots = 0
                        if self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 1:    #11111
                                fig, ((ax0,ax1),(ax2,ax3),(ax4,ax5))  = plt.subplots()
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 0:  #11110
                                fig, ((ax0,ax1),(ax2,ax3))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 1:  #11101
                                fig, ((ax0,ax1),(ax2,ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 1:  #11011
                                fig, ((ax0,ax1),(ax3,ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 1:  #10111
                                fig, ((ax0,ax2),(ax3,ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 1:  #01111
                                fig, ((ax1,ax2),(ax3,ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 0:  #11100
                                fig, ((ax0,ax1),(ax2))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 0:  #11010
                                fig, ((ax0,ax1),(ax3))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 0:  #10110
                                fig, ((ax0,ax2),(ax3))  = plt.subplots(2,2)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 0:  #01110
                                fig, ((ax1,ax2),(ax3))  = plt.subplots(2,2)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 1:  #01101
                                fig, ((ax1,ax2),(ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 1:  #01011
                                fig, ((ax1,ax2),(ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 1:  #00111
                                fig, ((ax2,ax3),(ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 1:  #10011
                                fig, ((ax0,ax3),(ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 1:  #11001
                                fig, ((ax0,ax1),(ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 1:  #10101
                                fig, ((ax0,ax2),(ax4))  = plt.subplots(2,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 0:  #11000
                                fig, (ax0,ax1)  = plt.subplots(1,2)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 0:  #10100
                                fig, (ax0,ax2)  = plt.subplots(2,1)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 0:  #10010
                                fig, (ax0,ax3)  = plt.subplots(2,1)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 1:  #10001
                                fig, (ax0,ax4)  = plt.subplots(2,1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 1:  #01001
                                fig, (ax1,ax4)  = plt.subplots(2,1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 1:  #00101
                                fig, (ax2,ax4)  = plt.subplots(2,1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 1:  #00011
                                fig, (ax3,ax4)  = plt.subplots(2,1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 1 and self.Channel[4] == 0:  #00110
                                fig, (ax2,ax3)  = plt.subplots(2,1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 0:  #01100
                                fig, (ax1,ax2)  = plt.subplots(2,1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 0:  #01010
                                fig, (ax1,ax3)  = plt.subplots(2,1)
                        elif self.Channel[0] == 1 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 0:  #10000
                                fig, ax0  = plt.subplots(1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 1 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 0:  #01000
                                fig, ax1  = plt.subplots(1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 1 and self.Channel[3] == 0 and self.Channel[4] == 0:  #00100
                                fig, ax2  = plt.subplots(1)     
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 1 and self.Channel[4] == 0:  #00010
                                fig, ax3  = plt.subplots(1)
                        elif self.Channel[0] == 0 and self.Channel[1] == 0 and self.Channel[2] == 0 and self.Channel[3] == 0 and self.Channel[4] == 1:  #00001
                                fig, ax4  = plt.subplots(1)

                        plotnumber = 0
                        if len(self.z1[0]) != 0:
                                im0 = ax0.pcolormesh(x, y, self.z1, cmap=cmap, norm=norm)
                                ax0.set_title('Plot 1')
                                ax0.invert_yaxis()                                                                                                      #invertiert die y-Achse
                                ax0.xaxis.tick_top()
                                fig.colorbar(im0, ax=ax0)
                                plotnumber = plotnumber + 1
                        if len(self.z2[0]) != 0:
                                im1 = ax1.pcolormesh(x, y, self.z2, cmap=cmap, norm=norm)
                                ax1.set_title('Plot 2')
                                ax1.invert_yaxis()                                                                                                      #invertiert die y-Achse
                                ax1.xaxis.tick_top()
                                fig.colorbar(im1, ax=ax1)
                                plotnumber = plotnumber + 1
                        if len(self.z3[0]) != 0:
                                im2 = ax2.pcolormesh(x, y, self.z3, cmap=cmap, norm=norm)
                                ax2.set_title('Plot 2')
                                ax2.invert_yaxis()                                                                                                      #invertiert die y-Achse
                                ax2.xaxis.tick_top()
                                fig.colorbar(im2, ax=ax2)
                                plotnumber = plotnumber + 1     
                        if len(self.z4[0]) != 0:    
                                im3 = ax3.pcolormesh(x, y, self.z4, cmap=cmap, norm=norm)
                                ax3.set_title('Plot 2')
                                ax3.invert_yaxis()                                                                                                      #invertiert die y-Achse
                                ax3.xaxis.tick_top()
                                fig.colorbar(im3, ax=ax3)
                                plotnumber = plotnumber + 1
                        if len(self.z5[0]) != 0:
                                im4 = ax4.pcolormesh(x, y, self.z5, cmap=cmap, norm=norm)
                                ax4.set_title('Plot 2')
                                ax4.invert_yaxis()                                                                                                      #invertiert die y-Achse
                                ax4.xaxis.tick_top()
                                fig.colorbar(im4, ax=ax4)
                                plotnumber = plotnumber + 1
           

                        try:
                                plt.savefig(self.DateTime4)
                        except:
                                print("Saving Plot not possible")

                        try:
                                plt.show()                                                                                                              #Plot
                        except:
                                print("Plot not posible")
                        PlotOn = 1
                else:
                        print("No plot selected")
"""
class ProcessData(QThread):
        def __init__(self, q, parent=None):
                QThread.__init__(self, parent)
                self.q = q
                #self.X = X
                #self.Y = Y
                #self.AnalogChannels = AnalogChannels
                #self.BSData = BSData
                
                self.run(self.q)
                
        def run(self, self.q):
                #self.openFile
                running == True
                while running == True:
                        if not self.q.empty():
                                val = self.q.get()
                                print(val)
                                if val == False:
                                        running = False
                        

        def openFile(self):
                
                self.Txt_out = open(self.DateTime2, "w")                                                                                                #Erstellt und öffnet eine neue Datei im Schreibmodus

                self.Txt_out.write("Start: " + str(self.XStartValue) + " X " + str(self.YStartValue) + "\n")                                            #Schreibt die Messschranke in die txt-Datei
                self.Txt_out.write("Stop: " + str(self.XStopValue) + " X " + str(self.YStopValue) + "\n")                                               #Schreibt die Messschranke in die txt-Datei

                if len(self.Plotname) == 0:
                        self.Plotname = (time.strftime("Measurement %d.%m.%Y %H:%M:%S - "))

                if self.Slope1 == True:
                        self.Txt_out.write("X Slope: " + str(self.XSlopeUpper) + "\tY Slope: " + str(self.YSlopeUpper) + "\n")

                if DHTon == 1:
                        global DHTPin
                        try:
                                humidity, temperature = Adafruit_DHT.read_retry(TempSens, DHTPin)
                                self.Txt_out.write("Temperature: " + str(temperature) + " *C\tHumidity: " + str(humidity) + " %\n")
                        except:
                                pass
                else:
                        pass

                       
                if self.Subgrid1 == True and self.ChannelTimeing == True:
                        self.Txt_out.write("Subgrid-Start: " + str(self.XStartSub) + " X " + str(self.YStartSub) + "\n")                                #Schreibt die Messschranke in die txt-Datei
                        self.Txt_out.write("Subgrid-Stop: " + str(self.XStopSub) + " X " + str(self.YStopSub) + "\n")                                   #Schreibt die Messschranke in die txt-Datei
                        self.Txt_out.write("Stepsize X: " + str(self.XStep) + "\tStepsize Z: " + str(self.YStep) + "\n")                                #Schreibt die Messschranke in die txt-Datei

                        self.Txt_sub = open(self.DateTimeSub, "w")
                        self.Txt_sub.write("Start: " + str(self.XStartValue) + " X " + str(self.YStartValue) + "\n")                                    #Schreibt die Messschranke in die txt-Datei
                        self.Txt_sub.write("Stop: " + str(self.XStopValue) + " X " + str(self.YStopValue) + "\n")                                       #Schreibt die Messschranke in die txt-Datei
                        self.Txt_sub.write("Stepsize X: " + str(self.XStep) + "\tStepsize Z: " + str(self.YStep) + "\n")

                        if self.Slope1 == True:
                                self.Txt_sub.write("X Slope: " + str(self.XSlopeUpper) + "\tY Slope: " + str(self.YSlopeUpper) + "\n")
                    
                        self.Txt_sub.write("Subgrid-Start: " + str(self.XStartSub) + " X " + str(self.YStartSub) + "\n")                                #Schreibt die Messschranke in die txt-Datei
                        self.Txt_sub.write("Subgrid-Stop: " + str(self.XStopSub) + " X " + str(self.YStopSub) + "\n")                                   #Schreibt die Messschranke in die txt-Datei
                        if self.sendTTL == True:
                                if self.getTTL == True:
                                        self.Txt_sub.write("TTL sent and recived\n")
                                        self.Txt_out.write("TTL sent and recived\n")
                                else:
                                        self.Txt_sub.write("TTL sent\n")
                                        self.Txt_out.write("TTL sent\n")
                
                        self.Txt_sub.write("Measurement with " + str(self.BitsValue) + " Pixel\n")                                                      #Schreibt die Verstärkung in die txt-Datei
                        self.Txt_sub.write("Date: " + self.DateTime + "\n")                                                                             #Schreibt das Datum und die Uhrzeit in die txt-Datei
                        self.Txt_sub.write("\n")
                        self.Txt_sub.write("Count\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")

        
                #try:
                #       plt.close('all')
                #except:
                #       print("No old Plot")

                self.Txt_out.write("Measurement with " + str(self.BitsValue) + " Pixel\n")                                                              #Schreibt die Verstärkung in die txt-Datei
        
                self.Txt_out.write("Date: " + self.DateTime + "\n")                                                                                     #Schreibt das Datum und die Uhrzeit in die txt-Datei
                self.Txt_out.write("\n")
                self.Txt_out.write("Count\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")



        def Calc_Logic(self):      
                i = 0
                counter1 = 0
                counter2 = 0
                counter3 = 0
                counter4 = 0
                counter5 = 0
                counter6 = 0
                counter7 = 0
                counter8 = 0
                statusnew1 = 0
                statusnew2 = 0
                statusnew3 = 0
                statusnew4 = 0
                statusnew5 = 0
                statusnew6 = 0
                statusnew7 = 0
                statusnew8 = 0
                statusold1 = 0
                statusold2 = 0
                statusold3 = 0
                statusold4 = 0
                statusold5 = 0
                statusold6 = 0
                statusold7 = 0
                statusold8 = 0
                    
                while i <= len(self.BSData)-1:
                        
                    if self.BSData[i] == 128:
                        statusnew1 = 1
                    elif self.BSData[i] == 64:
                        statusnew2 = 2
                    elif self.BSData[i] == 32:
                        statusnew3 = 3
                    elif self.BSData[i] == 16:
                        statusnew4 = 4
                    elif self.BSData[i] == 8:
                        statusnew5 = 5
                    elif self.BSData[i] == 4:
                        statusnew6 = 6
                    elif self.BSData[i] == 2:
                        statusnew7 = 7
                    elif self.BSData[i] == 1:
                        statusnew8 = 8
                    elif self.BSData[i] == 192:
                        statusnew1 = 1
                        statusnew2 = 2
                    else:
                        statusnew1 = 0
                        statusnew2 = 0
                        statusnew3 = 0
                        statusnew4 = 0
                        statusnew5 = 0
                        statusnew6 = 0
                        statusnew7 = 0
                        statusnew8 = 0

                    if statusold1 == 0 and statusnew1 == 1:
                        counter1 = counter1 + 1
                    if statusold2 == 0 and statusnew2 == 2:
                        counter2 = counter2 + 1
                    if statusold3 == 0 and statusnew3 == 3:
                        counter3 = counter3 + 1
                    if statusold4 == 0 and statusnew4 == 4:
                        counter4 = counter4 + 1
                    if statusold5 == 0 and statusnew5 == 5:
                        counter5 = counter5 + 1
                    if statusold6 == 0 and statusnew6 == 6:
                        counter6 = counter6 + 1
                    if statusold7 == 0 and statusnew7 == 7:
                        counter7 = counter7 + 1
                    if statusold8 == 0 and statusnew8 == 8:
                        counter8 = counter8 + 1
                    statusold1 = statusnew1
                    statusold2 = statusnew2
                    statusold3 = statusnew3
                    statusold4 = statusnew4
                    statusold5 = statusnew5
                    statusold6 = statusnew6
                    statusold7 = statusnew7
                    statusold8 = statusnew8
                    i = i + 1

                #print("Counts CH1 " + str(counter1))
                #print("Counts CH2 " + str(counter2))
                #print("Counts L5 " + str(counter3))
                #print("Counts L4 " + str(counter4))
                #print("Counts L3 " + str(counter5))
                #print("Counts L2 " + str(counter6))
                #print("Counts L1 " + str(counter7))
                #print("Counts L0 " + str(counter8))
                #self.stoptime = time.time()
                #self.runtime = self.stoptime - self.starttime
                #self.midtime1 = self.stoptime - self.midtime
                #self.midtime2 = self.midtime - self.starttime
                #print("Gesamt: " + str(self.runtime))
                #print("Receive Data: " + str(self.midtime2))
                #print("Process Data: " + str(self.midtime1))
                return counter1, counter2, counter5, counter6

                self.killBrian()

        def killBrian(self):                                                                   
                pass
"""

#Die dritte Klasse ist ein zweiter Thread, also ein paraleler Prozess auf einem anderen Prozessorkern
class PlotData(QThread):
        def __init__(self, Channels, CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, XStart, XStop, YStart, YStop, Colors, Plotname, Filename, parent=None):
                QThread.__init__(self, parent)
                self.Channels = Channels
                self.CH1 = CH1
                self.CH2 = CH2
                self.CH3 = CH3
                self.CH4 = CH4
                self.CH5 = CH5
                self.CH6 = CH6
                self.CH7 = CH7
                self.CH8 = CH8
                self.YStartValue = YStart
                self.YStopValue = YStop
                self.XStartValue = XStart
                self.XStopValue = XStop
                self.colors = Colors
                self.Plotname = Plotname
                self.DateTime4 = Filename

                """
                print(self.Channels)
                print(self.CH1)
                print(self.CH2)
                print(self.CH3)
                print(self.CH4)
                print(self.CH5)
                print(self.CH6)
                print(self.CH7)
                print(self.CH8)
                print(self.colors)
                print(self.Plotname)
                print(self.DateTime4)
                """
                self.run()
                
        def run(self):  
                #Grid Setup
                dx, dy = 1, 1                                                                                                                           #Schrittweite
                y, x = np.mgrid[slice(self.YStartValue, self.YStopValue+1, dy), slice(self.XStartValue, self.XStopValue+1, dx)]                         #Setzt das 2D-Grid mit der bestimmten Schrittweite und Start und Endwert

                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                     #Lila zu Gelb
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                #Graustufen
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                            #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                                     #Lila zu Gelb

                levels = MaxNLocator(nbins=50).tick_values(0, 5.4)                                                                                      #characterizes the bar right
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                #Figure Setup
                fig, ax1  = plt.subplots()                                                                                                              #Adds the plot to the figure

                if len(self.CH1[0]) != 0:
                        im1 = ax1.pcolormesh(x, y, self.CH1, cmap=cmap, norm=norm)              
                elif len(self.CH2[0]) != 0:
                        im1 = ax1.pcolormesh(x, y, self.CH2, cmap=cmap, norm=norm)
                elif len(self.CH3[0]) != 0:
                        im1 = ax1.pcolormesh(x, y, self.CH3, cmap=cmap, norm=norm)
                elif len(self.CH4[0]) != 0:    
                        im1 = ax1.pcolormesh(x, y, self.CH4, cmap=cmap, norm=norm)
                elif len(self.CH5[0]) != 0:
                        im1 = ax1.pcolormesh(x, y, self.CH5, cmap=cmap, norm=norm)
                elif len(self.CH6[0]) != 0:
                        im1 = ax1.pcolormesh(x, y, self.CH6, cmap=cmap, norm=norm)
                else:
                        print("No Data accuired")
    
                fig.colorbar(im1, ax=ax1)
                ax1.set_title(self.Plotname)

                ax1.invert_yaxis()                                                                                                                      #invertiert die y-Achse
                ax1.xaxis.tick_top()                                                                                                                    #setzt die x-Achse nach oben

                #Plot and Save
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                      #Plot
                except:
                        print("Plot not posible")

                self.killBrian()

        def killBrian(self):                                                                                                                            #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen
                time.sleep(0.2)                                                                   
                print("Brian dead")


#Exception Catcher
def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        print("Not an Error just some more Work to do! ;-)")
        time.sleep(3)
        QtWidgets.QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


def main():
        global StyleName
        global StyleColor
        #try:
        app = QApplication(sys.argv)   
        app.setStyle(StyleName)
        if StyleColor == "dark" and StyleName != "windowsvista":
                palette = QtGui.QPalette()
                palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
                palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
                palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
                palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
                palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
                         
                #palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
                #palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0,250,0).lighter())
                palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(34,139,34).lighter())
                palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
                app.setPalette(palette)
        elif StyleColor == "dark" and StyleName == "windowsvista":
                palette = QtGui.QPalette()
                palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
                palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
                palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
                palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
                palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
                palette.setColor(QtGui.QPalette.Button, QtGui.QColor(153,153,153))
                palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.black)
                palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
                #palette.setColor(QtGui.QPalette.TabWidget, QtCore.Qt.red)
                         
                #palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
                #palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0,250,0).lighter())
                palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(34,139,34).lighter())
                palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
                app.setPalette(palette)

        w = Fenster()

        #sys.excepthook = excepthook

        sys.exit(app.exec_())                                                                                                                           #Programm endet wenn Fenster endet


        """except KeyboardInterrupt:
                print("Own KeyboardInterrupt")                                                                                                          #Programm endet wenn Fenster endet

        except:
                GPIO.cleanup()
                print("Cleanup6")

        finally:
                try:
                        connMeasure.commit()                                                           
                        connMeasure.close()
                except:
                        connMeasure.close()                                                                                                             #Die Ende-Funktion beendet alle Prozesse

                try:
                        connSync.commit()                                                           
                        connSync.close()
                except:
                        connSync.close()
                                                                                                                                                        #Die Ende-Funktion beendet alle Prozesse
                try:
                        connStack.commit()                                                           
                        connStack.close()
                except:
                        connStack.close()
                                                                                                                                                        #Die Ende-Funktion beendet alle Prozesse
                try:
                        connSlope.commit()                                                           
                        connSlope.close()
                except:
                        connSlope.close()
                                                                                                                                                        #Die Ende-Funktion beendet alle Prozesse
                try:
                        connDev.commit()                                                           
                        connDev.close()
                except:
                        connDev.close()
                                                                                                                                                        #Die Ende-Funktion beendet alle Prozesse
                try:
                        connPlot.commit()                                                           
                        connPlot.close()
                except:
                        connPlot.close()
                                                                                                                                                        #Die Ende-Funktion beendet alle Prozesse
                try:
                        connTTL.commit()                                                           
                        connTTL.close()
                except:
                        connTTL.close()
                        
                try:
                        self.Txt_out.close()
                        self.Txt_sub.close()
                except:
                        pass
                        
                try:
                        self.Manfred.killFred()                                                                                                         #Beendet den Thread, wenn der Button unchecked gesetzt wird                                                                                                                             #Beendet das Fenster
                except:
                        pass

                try:
                        self.Monty.killFred()                                                                                                           #Beendet den Thread, wenn der Button unchecked gesetzt wird                                                                                                                             #Beendet das Fenster
                except:
                        pass

                try:
                        self.FylingCircus.killFred()                                                                                                    #Beendet den Thread, wenn der Button unchecked gesetzt wird                                                                                                                             #Beendet das Fenster
                except:
                        pass

                try:
                        dacX.set_voltage(0)
                        dacY.set_voltage(0)
                        dacZ.set_voltage(0)
                except:
                        pass
                
                try:
                        adc.stop_adc()
                except:
                        pass
                        
                try:
                        plt.close()
                except:
                        pass

                try:
                        GPIO.output(14, 0)
                except:
                        pass

                try:
                        GPIO.output(15, 0)
                except:
                        pass
                
                try:
                        GPIO.output(17, 0)
                except:
                        pass
                
                try:
                        GPIO.output(18, 0)
                except:
                        pass

                try:
                        GPIO.output(22, 0)
                except:
                        pass

                try:
                        GPIO.output(27, 0)
                except:
                        pass

                #w.quitall()
                
                print("Everything is over!")
                GPIO.cleanup()
                print("Cleanup7")"""

        
if __name__ == '__main__':
        main()                                                                                                                                          #Programm endet wenn Fenster endet

"""except KeyboardInterrupt:
        print("Own KeyboardInterrupt")

except:
        print("A big Exception occurred")

finally:
        print("Catch it if you can")
        GPIO.cleanup()
        print("Cleanup8")
"""
