#HydraScan 1.45.2 - Gaia

"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 1: Setup -----------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


#Info ---------------------------------------------------------------
Version = "1.45.2"
VersionName = "Gaia"
print("Version: HydraScan " + str(Version) + " - " + str(VersionName))
Updates = "Auto Update\n\tLive Plot APD\n\tInvert XY\n\tSymPhoTime\n\tCode cleaning\n\tminor fixes"
NumberUpdates = 6
print("Updates: " + Updates)
Copyright = "Property of HydraSpex UG"
print("Copyright: " + Copyright)
Contact = "info@hydraspex.com"
print("Contact: " + Contact)
Cite = "Available soon!"
print("If HydraScan contributes to publisch a work please cite: " + Cite + "\n\n")


#Global Variables ---------------------------------------------------
#Style
WindowPosX = 50
WindowPosY = 100
WindowWidth = 1200
WindowHeight = 800
StyleName = "Fusion"            #'Fusion', 'Windows', 'windowsvista'(['bb10dark', 'bb10bright', 'cleanlooks', 'gtk2', 'cde', 'motif', 'plastique', 'qt5ct-style', 'Windows', 'Fusion'])
#StyleName = "Windows"
#StyleName = "windowsvista"
#StyleName = "qt5ct-style"
StyleColor = "dark"             #'light', 'dark'
#StyleColor = "light"
Font = "Arial"
FontSize = 10
CurrentPage = 0

#Device
PiezoDistanceX = 100000                                                                                                                                 #Nanometers
PiezoDistanceY = 100000                                                                                                                                 #Nanometers
PiezoDistanceZ = 100000                                                                                                                                  #Nanometers
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
StartValX = 2048
StartValY = 2048
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

#Path & Meta Data
PlotStyle = 1
FileName = "Measurement"
FileNamePoint = "Pointmeasurement"
FileNameSub = "Subgridmeasurement"
SubPoints = "SubgridPoints"
MainPath = "/home/pi/Desktop/Data"
FilePath = "/home/pi/Desktop/Data/"
TXTFilePath = "/home/pi/Desktop/Data/"
Meta = 0
LaserWL = ""
LaserPower = ""
Filter = ""
Sample = ""

#TTL
TTL1OUT = 23
TTL1IN = 18
Wire1 = False
TTL2OUT = 24
TTL2IN = 25
Wire2 = False
LEDPin = 26
SymPho1 = 14
SymPho2 = 15



#Library import -------------------------------------------------------
#Python Imports
try:
        import requests
        import os
        import sys
        import shutil
        import zipfile
        import io
        import warnings
        import subprocess
        warnings.filterwarnings('ignore')
        import threading
        from threading import Thread
        sys.setrecursionlimit(1000000)
        import traceback
        import time
        import shlex
        #print("Operating System: " + str(os.name))
        if os.name == "nt":
                FontSize = 8
        import sqlite3
        import math
        from shutil import copyfile
        from queue import Queue
except:
        print("Python imports failed")

#Auto-Updater  -----------------------------------------------------------
#GitSetup
__version__ = Version
REPO = "HydraSpex/HydraScan" 
BACKUP_DIR = "HydraScan_old"

# DATEIEN, DIE ERHALTEN BLEIBEN MÜSSEN
# Hier trägst du deine Datenbanken oder Config-Dateien ein
KEEP_FILES = ["settings.db", "user_prefs.json", "database.sqlite"]
KEEP_EXTENSIONS = [".db", ".sqlite"]

#Auto-Updater
def update_full_repo():
        print(f"--- Full Update Check (Current version: v{__version__}) ---")
        
        api_url = f"https://api.github.com/repos/{REPO}/releases/latest"
        
        try:
                response = requests.get(api_url, timeout=15)
                if response.status_code == 200:
                        latest_release = response.json()
                        latest_version = latest_release['tag_name'].replace("v", "")
                        #print(f"Version im Repo v{latest_version}")
                        
                        if latest_version > __version__:
                                print(f"New Version v{latest_version} found!")
                                zip_url = latest_release['zipball_url']
                                
                                # 1. ZIP in den Arbeitsspeicher laden
                                print("Repository-Archiv Download...")
                                zip_response = requests.get(zip_url, timeout=30)
                                
                                if zip_response.status_code == 200:
                                        if os.path.exists(BACKUP_DIR):
                                                shutil.rmtree(BACKUP_DIR)
                                
                                        os.makedirs(BACKUP_DIR)
                                        
                                        current_files = os.listdir('.')
                                        for item in current_files:
                                                # Überspringe den Backup-Ordner und das Update-Skript selbst
                                                if item in [BACKUP_DIR, ".git", ".env"]:
                                                        continue

                                                # PRÜFUNG: Ist es eine schützenswerte Datei?
                                                ext = os.path.splitext(item)[1]
                                                if item in KEEP_FILES or ext in KEEP_EXTENSIONS:
                                                        print(f"Behalte lokale Daten: {item}")
                                                        # Diese Datei bleibt einfach im Hauptordner liegen!
                                                        continue

                                                shutil.move(item, os.path.join(BACKUP_DIR, item))
                                        
                                        print(f"Redirected old Version to '{BACKUP_DIR}'.")

                                        with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
                                                top_dir = z.namelist()[0].split('/')[0]
                                                z.extractall()
                                                
                                                extracted_dir = top_dir
                                                for file_name in os.listdir(extracted_dir):
                                                        source = os.path.join(extracted_dir, file_name)
                                                
                                                        # VORSICHT: Falls das ZIP eine leere Standard-DB enthält, 
                                                        # darf diese die User-DB nicht überschreiben!
                                                        if os.path.exists(file_name) and (file_name in KEEP_FILES or os.path.splitext(file_name)[1] in KEEP_EXTENSIONS):
                                                                print(f"Überspringe Überschreiben von User-Daten: {file_name}")
                                                                continue
                                                        
                                                shutil.move(source, file_name)

                                        print("Installing new Software...")
                                        try:    
                                                install_requirements()
                                        except:
                                                print("Installation failed")
                                        print("Installation done.")

                                        print("Update finished. Restart the Software to use the newest Version.\n\n")
                                        sys.exit()
                                else:
                                        print("Download failed.")
                        else:
                                print("Current Version ist the newest Version.\n\n")
                else:
                        print("API-Error at Release-Info request.")
                
        except Exception as e:
                print(f"Critical Update-Error: {e}\n\n")

def install_requirements():
        if os.path.exists("requirements.txt"):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

try:    
        update_full_repo()
except:
        print("Update failed")


#Error-Logger -----------------------------------------------------------
#try:
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import platform # Um Systeminfos mitzusenden
from dotenv import load_dotenv
import logging
#except:
#        print("Error-Logger Imports failed")

# Konfiguration des Loggings
LOG_FILE = "error.log"
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG, # Speichert alles ab 'DEBUG' aufwärts
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'), # In Datei schreiben
        logging.StreamHandler(sys.stdout)               # Auch in der Konsole anzeigen
    ]
)

logger = logging.getLogger(__name__)



#GUI Imports -----------------------------------------------------------
try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtGui import *
        from PyQt5 import *
        from PyQt5.QtCore import *
except:
        print("PyQt imports failed")

#Tempsensor imports -----------------------------------------------------------
try:
        import Adafruit_DHT # type: ignore
        TempSens = Adafruit_DHT.DHT22
        DHTPin = 22
        DHTon = 1
        TempWindowOn = 0
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

#Raspberry imports and settings -----------------------------------------------------------
try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIOon = 1
except:
        print("GPIO import failed")                                                                                                     #Create virtual GPIOs to catch errors
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
                
                def setup(self, val, mode, initial=0):
                        print("No GPIO " + str(val) + " - " + str(mode) + " - " + str(initial))
                        pass

                def output(self, val, val1):
                        print("No GPIO " + str(val) + " - " + str(val1))

                def add_event_detect(self, val=0, val2=0, callback=None, bouncetime=0):
                        if callback != None:
                                self.callback

                def callback(self):
                        print("Test")

                def remove_event_detect(self, val):
                        pass

        GPIO = GPIO_Virtual()
        GPIOon = 0


#DAC & Poti imports -----------------------------------------------------------
try:
	from MCP4728_lib import MCP4728
	dacOffset = MCP4728()
	dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
	NoOffset = 0
except:
        print("Offset imports failed")                                                                                                  #Create virtual DACs to catch errors
        class Offset_Virtual():
                def __init__(self):
                        pass

                def setAllVoltage(self, val1, val2, val3, val4):
                        pass
                        #print("No Offset DAC: " + str(val1) + " - " + str(val2) + " - " + str(val3) + " - " + str(val4))

                def setOneVoltage(self, CH, volt):
                        pass
                        #print("No Offset DAC: Channel " + str(CH) + " - " + str(volt))

        dacOffset = Offset_Virtual()
        dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
        NoOffset = 1

try:
	from MCP4151_0 import MCP4151_0
	Poti = MCP4151_0()
	Poti.write_range(PotiStartVal)
	NoPoti = 0
except:
        print("Poti imports failed")                                                                                                    #Create virtual DACs to catch errors
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
        print("DAC imports failed")                                                                                                     #Create virtual DACs to catch errors
        class DAC_Virtual():
                def __init__(self, name="Test"):
                        self.name = name
                        pass

                def set_voltage(self, val, persist = False):
                        #print(self.name + ": " + str(val))
                        pass
                        #print(self.__class__)
                        #pass

        class DAC_Virtual2():
                def __init__(self, name="Test"):
                        self.name = name
                        pass

                def set_voltage(self, val, persist = False):
                        #print(self.name + ": " + str(val))
                        pass
                        #print(self.__class__)
                        #pass

        dacZ = DAC_Virtual2("DAC Z")
        dacX = DAC_Virtual2("DAC X")
        dacY = DAC_Virtual2("DAC Y")
        dacZ.set_voltage(FocusZ)
        dacX.set_voltage(0)
        dacY.set_voltage(0)
        NoDAC = 1

#ADC imports -----------------------------------------------------------
try:
        import Adafruit_ADS1x15
        adc = Adafruit_ADS1x15.ADS1115()
        GAIN = 2/3
        NoADC = 0
except:
        print("ADC imports failed")                                                                                                     #Create virtual ADCs to catch errors
        GAIN = 2/3
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

#Matplotlib imports -----------------------------------------------------------
try:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        import matplotlib
        matplotlib.use('Qt5Agg')
        import matplotlib.pyplot as plt
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

#Scipy import -----------------------------------------------------------
try:
        from scipy.interpolate import RectBivariateSpline
        from scipy.interpolate import interp2d
except:
        print("scipy imports failed")

#Plotimports -----------------------------------------------------------
try:
        import HydraPlotLib
        import HydraPlot
except:
        print("HydraPlot imports failed")

#Maximum Detection -----------------------------------------------------------
try:
        import MaxDetectLib
except:
        print("MaxDetectLib import Failed")

#Logic imports   -----------------------------------------------------------
APDon = 0
APDWindowOn = 0
APDArduinoOn = 0
APDArduinoI2C = 0
APDArduinoSPI = 0
APDBSOn = 0
RandCount = 0
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
                from APDArduinoLibSPI import ArduinoLogic # type: ignore
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
                print("No APDs")
                APDon = 0
                APDWindowOn = 0
                APDArduinoOn = 0
                APDArduinoI2C = 0
                APDArduinoSPI = 0
                APDBSOn = 0
                print("ADP imports failed")                                                                             #Create virtual ADCs to catch errors
                class ADP_Virtual():
                        def __init__(self):
                                pass

                        def captureDual(self, val):
                                global RandCount
                                print("No APD: " + str(val) + " - RandCount: " + str(RandCount))
                                a = random.uniform(0, (100*val))
                                b = random.uniform(0, (100*val))
                                if RandCount%500 == 0:
                                        a = 200*val 
                                if val == 0:
                                        a = 300
                                RandCount = RandCount + 1
                                return a, b

                        def capture1(self, ms):
                                global RandCount
                                print("No APD - Single1: " + str(ms) + " - RandCount: " + str(RandCount))
                                a = random.uniform(0, (100*ms))
                                if RandCount%500 == 0:
                                        a = 200*ms 
                                if ms == 0:
                                        a = 300
                                RandCount = RandCount + 1
                                return a

                        def capture2(self, ms):
                                global RandCount
                                print("No APD - Single1: " + str(ms))
                                b = random.uniform(0, (100*ms))
                                return b
                        
                        def closeDevice(self):
                                pass

                APDs = ADP_Virtual()
                count1, count2 = APDs.captureDual(1)

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
        channel0 integer,
        channel1 integer,
        channel2 integer,
        channel3 integer,
        channel4 integer,
        channel5 integer,
        channel6 integer,
        channel7 integer,
        xstart real,
        xstop real,
        ystart real,
        ystop real,
        slope integer,
        subgrid integer,
        sympho integer,
        stack integer,
        plot integer)""")
        print("Datenbank 1 wurde angelegt")
except:
        print("Datenbank 1 abgerufen")
try:
        connMeasure.commit()
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
        manuelauto integer,
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
        connSync.commit()
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
        connStack.commit()
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
        connSlope.commit()
except:
        print("database 4 failed")

#File Settings
try:
        connFile = sqlite3.connect("settingsFile.db")
        FileSet = connFile.cursor()
except:
        print("no database 5 connection")
try:
        FileSet.execute("""
        CREATE TABLE settingsFile (
        ID integer,
        filename text,
        filepoint text,
        filesub text,
        subpoints text,
        filepath text,
        mainpath text,
        meta integer,
        laserWL text,
        laserPower text,
        filter text,
        sample text)""")
        print("Datenbank 5 wurde angelegt")
        FileSet.execute("INSERT INTO settingsFile (ID, filename, filepoint, filesub, subpoints, filepath, mainpath, meta, laserWL, laserPower, filter, sample) VALUES (" + str(1) + ", " + "\"" + FileName  + "\"" + ", " + "\"" + FileNamePoint  + "\"" + ", " + "\"" + FileNameSub  + "\"" + ", " + "\"" + SubPoints  + "\"" + ", " + "\"" + FilePath  + "\"" + ", " + "\"" + MainPath  + "\"" + ", " + str(Meta) + ", " + "\"" + LaserWL  + "\"" + ", " + "\"" + LaserPower  + "\"" + ", " + "\"" + Filter  + "\"" + ", " + "\"" + Sample  + "\"" + ")")
        print("Settings saved")
except:
        print("Datenbank 5 abgerufen")
try:
        FileSet.execute("SELECT * FROM settingsFile WHERE ID = 1")
        for dsatzFile in FileSet:
                filename = dsatzFile[1]
                filepoint = dsatzFile[2]
                filesub = dsatzFile[3]
                subpoints = dsatzFile[4]
                filepath = dsatzFile[5]
                mainpath = dsatzFile[6]
                meta = dsatzFile[7]
                wl = dsatzFile[8]
                power = dsatzFile[9]
                filter = dsatzFile[10]
                sample = dsatzFile[11]
        FileName = filename
        FileNamePoint = filepoint
        FileNameSub = filesub
        SubPoints = subpoints
        FilePath = filepath
        MainPath = mainpath
        Meta = meta
        LaserWL = wl
        LaserPower = power
        Filter = filter
        Sample = sample
except:
        print("read database 5 failed")
try:
        connFile.commit()
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
        PiezoDistanceX = piezodistanceX                                                                                         #Nanometers
        PiezoDistanceY = piezodistanceY                                                                                         #Nanometers
        PiezoDistanceZ = piezodistanceZ                                                                                         #Nanometers
        PiezoVoltage = piezovoltage                                                                                             #Volts
        CHA = ChA                                                                                                               #Channel A
        CHB = ChB                                                                                                               #Channel B
        L2 = l2                                                                                                                 #Channel L2
        L3 = l3                                                                                                                 #Channel L3
        CH1 = Ch1                                                                                                               #Channel 1
        CH2 = Ch2                                                                                                               #Channel 2
        CH3 = Ch3                                                                                                               #Channel 3
        CH4 = Ch4                                                                                                               #Channel 4
        
        #Device
        PiezoDistanceX = piezodistanceX                                                                                                                                 #Nanometers
        PiezoDistanceY = piezodistanceY                                                                                                                                 #Nanometers
        PiezoDistanceZ = piezodistanceZ                                                                                                                                  #Nanometers
        PiezoVoltage = piezovoltage                                                                                                                                       #Volts
        DeviceVoltageLow = -10    #ProblemHier Weiter                                                                                                                                   #Volts
        #DeviceVoltageLow = -5                                                                                                                                        #Volts
        #DeviceVoltageLow = 0                                                                                                                                   #Volts
        DeviceVoltageHigh = 10                                                                                                                                  #Volts
        #DeviceVoltageHigh = 5                                                                                                                                  #Volts
        DeviceVoltage = DeviceVoltageHigh - DeviceVoltageLow                                                                                                    #Volts
        if PiezoVoltage <= DeviceVoltage:
                PotiStartVal = PiezoVoltage
        else:
                PotiStartVal = DeviceVoltage
        FullRangeDeviceX = PiezoDistanceX * (DeviceVoltage / PiezoVoltage)                                                                                      #Nanometers
        FullRangeDeviceY = PiezoDistanceY * (DeviceVoltage / PiezoVoltage)                                                                                      #Nanometers
        FullRangeDeviceZ = PiezoDistanceZ * (DeviceVoltage / PiezoVoltage)                                                                                      #Nanometers  
                
        print("New Distance set: " + str(FullRangeDeviceX))
except:
        pass
        print("No new Distance set: " + str(FullRangeDeviceX))
try:
        connDev.commit()                                                                                                        #never forget this, if you want the changes to be saved:
except:
        print("database 6 failed")

print("New FullRangeDeviceX: " + str(FullRangeDeviceX))
print("New PiezoDistanceX: " + str(PiezoDistanceX))
print("New DeviceVoltage: " + str(DeviceVoltage))
print("New FullRangeDeviceX: " + str(FullRangeDeviceX))

#TTL Settings
TTLOUT1 = {"Name" : "SymPho1", "Pin" : 14, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT2 = {"Name" : "SymPho2", "Pin" : 15, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT3 = {"Name" : "TTL 3", "Pin" : 23, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT4 = {"Name" : "TTL 4", "Pin" : 24, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT5 = {"Name" : "TTL 5", "Pin" : 18, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT6 = {"Name" : "TTL 6", "Pin" : 25, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT7 = {"Name" : "Shutter 1", "Pin" : 27, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT8 = {"Name" : "Shutter 2", "Pin" : 22, "Polarity" : 0, "Mode" : 1, "Initial" : 0}
TTLOUT_Wires = [False, False, False, False]
ShutterMode = [0, 0, 0, 0]
Shutter2Threashold = 35000

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
        polarity1 integer,
        mode1 integer,
        initial1 integer,
        name2 text,
        polarity2 integer,
        mode2 integer,
        initial2 integer,
        name3 text,
        polarity3 integer,
        mode3 integer,
        initial3 integer,
        name4 text,
        polarity4 integer,
        mode4 integer,
        initial4 integer,
        name5 text,
        polarity5 integer,
        mode5 integer,
        initial5 integer,
        name6 text,
        polarity6 integer,
        mode6 integer,
        initial6 integer,
        name7 text,
        polarity7 integer,
        mode7 integer,
        initial7 integer,
        name8 text,
        polarity8 integer,
        mode8 integer,
        initial8 integer,
        wire1 integer,
        wire2 integer,
        wire3 integer,
        wire4 integer,
        Shutter1 integer,
        Shutter2 integer,
        Shutter1TTLSync integer,
        Shutter2TTLSync integer,
        Shutter2Threashold integer)""")

        print("Datenbank 7 wurde angelegt")
        TTLSet.execute("INSERT INTO settingsScanTTL (ID, name1, polarity1, mode1, initial1, name2, polarity2, mode2, initial2, name3, polarity3, mode3, initial3, name4, polarity4, mode4, initial4, name5, polarity5, mode5, initial5, name6, polarity6, mode6, initial6, name7, polarity7, mode7, initial7, name8, polarity8, mode8, initial8, wire1, wire2, wire3, wire4, Shutter1, Shutter2, Shutter1TTLSync, Shutter2TTLSync, Shutter2Threashold) VALUES (" 
                        + str(1) + ", " + "\"" + TTLOUT1["Name"]  + "\"" + ", " + str(TTLOUT1["Polarity"]) + ", " + str(TTLOUT1["Mode"]) + ", " + str(TTLOUT1["Initial"]) + ", "
                        + "\"" + TTLOUT2["Name"]  + "\"" + ", " + str(TTLOUT2["Polarity"]) + ", " + str(TTLOUT2["Mode"]) + ", " + str(TTLOUT2["Initial"]) + ", "
                        + "\"" + TTLOUT3["Name"]  + "\"" + ", " + str(TTLOUT3["Polarity"]) + ", " + str(TTLOUT3["Mode"]) + ", " + str(TTLOUT3["Initial"]) + ", "
                        + "\"" + TTLOUT4["Name"]  + "\"" + ", " + str(TTLOUT4["Polarity"]) + ", " + str(TTLOUT4["Mode"]) + ", " + str(TTLOUT4["Initial"]) + ", "
                        + "\"" + TTLOUT5["Name"]  + "\"" + ", " + str(TTLOUT5["Polarity"]) + ", " + str(TTLOUT5["Mode"]) + ", " + str(TTLOUT5["Initial"]) + ", "
                        + "\"" + TTLOUT6["Name"]  + "\"" + ", " + str(TTLOUT6["Polarity"]) + ", " + str(TTLOUT6["Mode"]) + ", " + str(TTLOUT6["Initial"]) + ", "
                        + "\"" + TTLOUT7["Name"]  + "\"" + ", " + str(TTLOUT7["Polarity"]) + ", " + str(TTLOUT7["Mode"]) + ", " + str(TTLOUT7["Initial"]) + ", "
                        + "\"" + TTLOUT8["Name"]  + "\"" + ", " + str(TTLOUT8["Polarity"]) + ", " + str(TTLOUT8["Mode"]) + ", " + str(TTLOUT8["Initial"]) + ", "
                        + str(TTLOUT_Wires[0]) + ", " + str(TTLOUT_Wires[1]) + ", " + str(TTLOUT_Wires[2]) + ", " + str(TTLOUT_Wires[3]) + ", "
                        + str(ShutterMode[0]) + ", " + str(ShutterMode[1]) + ", " + str(ShutterMode[2]) + ", " + str(ShutterMode[3]) + ", " + str(Shutter2Threashold)
                        + ")")
        print("Settings saved")
except:
        print("Datenbank 7 abgerufen")
try:
        TTLSet.execute("SELECT * FROM settingsScanTTL WHERE ID = 1")
        for dsatzTTL in TTLSet:
                TTLOUT1["Name"] = dsatzTTL[1]
                TTLOUT1["Polarity"] = dsatzTTL[2]
                TTLOUT1["Mode"] = dsatzTTL[3]
                TTLOUT1["Initial"] = dsatzTTL[4]   
                TTLOUT2["Name"] = dsatzTTL[5]
                TTLOUT2["Polarity"] = dsatzTTL[6]
                TTLOUT2["Mode"] = dsatzTTL[7]
                TTLOUT2["Initial"] = dsatzTTL[8] 
                TTLOUT3["Name"] = dsatzTTL[9]
                TTLOUT3["Polarity"] = dsatzTTL[10]
                TTLOUT3["Mode"] = dsatzTTL[11]
                TTLOUT3["Initial"] = dsatzTTL[12] 
                TTLOUT4["Name"] = dsatzTTL[13]
                TTLOUT4["Polarity"] = dsatzTTL[14]
                TTLOUT4["Mode"] = dsatzTTL[15]
                TTLOUT4["Initial"] = dsatzTTL[16] 
                TTLOUT5["Name"] = dsatzTTL[17]
                TTLOUT5["Polarity"] = dsatzTTL[18]
                TTLOUT5["Mode"] = dsatzTTL[19]
                TTLOUT5["Initial"] = dsatzTTL[20] 
                TTLOUT6["Name"] = dsatzTTL[21]
                TTLOUT6["Polarity"] = dsatzTTL[22]
                TTLOUT6["Mode"] = dsatzTTL[23]
                TTLOUT6["Initial"] = dsatzTTL[24] 
                TTLOUT7["Name"] = dsatzTTL[25]
                TTLOUT7["Polarity"] = dsatzTTL[26]
                TTLOUT7["Mode"] = dsatzTTL[27]
                TTLOUT7["Initial"] = dsatzTTL[28] 
                TTLOUT8["Name"] = dsatzTTL[29]
                TTLOUT8["Polarity"] = dsatzTTL[30]
                TTLOUT8["Mode"] = dsatzTTL[31]
                TTLOUT8["Initial"] = dsatzTTL[32]  
                TTLOUT_Wires[0] = dsatzTTL[33]
                TTLOUT_Wires[1] = dsatzTTL[34]
                TTLOUT_Wires[2] = dsatzTTL[35]
                TTLOUT_Wires[3] = dsatzTTL[36]   
                ShutterMode[0] = dsatzTTL[37]   
                ShutterMode[1] = dsatzTTL[38]    
                ShutterMode[2] = dsatzTTL[39]    
                ShutterMode[3] = dsatzTTL[40] 
                Shutter2Threashold = dsatzTTL[41]    
        #NameTTL1 = name1
        #NameTTL2 = name2
        #Wire1 = wire1
        #Wire2 = wire2
except:
        pass
try:
        connTTL.commit()                                                                                                        #never forget this, if you want the changes to be saved:
except:
        print("database 7 failed")

try:
        GPIO.setup(TTLOUT1["Pin"], TTLOUT1["Mode"], initial=TTLOUT1["Initial"])
        GPIO.setup(TTLOUT2["Pin"], TTLOUT2["Mode"], initial=TTLOUT2["Initial"])
        GPIO.setup(TTLOUT3["Pin"], TTLOUT3["Mode"], initial=TTLOUT3["Initial"])
        GPIO.setup(TTLOUT4["Pin"], TTLOUT4["Mode"], initial=TTLOUT4["Initial"])
        GPIO.setup(TTLOUT5["Pin"], TTLOUT5["Mode"], initial=TTLOUT5["Initial"])
        GPIO.setup(TTLOUT6["Pin"], TTLOUT6["Mode"], initial=TTLOUT6["Initial"])
        GPIO.setup(TTLOUT7["Pin"], TTLOUT7["Mode"], initial=TTLOUT7["Initial"])
        GPIO.setup(TTLOUT8["Pin"], TTLOUT8["Mode"], initial=TTLOUT8["Initial"])

except:
        print("TTL failed")

#Directory build or check --------------------------------------------
try:
        os.makedirs(FilePath)
        print("Data folder created")
except:
        pass
try:
        os.makedirs('/Files')
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Settings.png", "/Files/Settings.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/About.png", "/Files/About.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Help.png", "/Files/Help.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/HydraScan_free.png", "/Files/HydraScan_free.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Hydra_logo_klein.png", "/Files/Hydra_logo_klein.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/ShowTemp.png", "/Files/ShowTemp.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/temperature.png", "/Files/temperature.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Temp_high.png", "/Files/Temp_high.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Temp_low.png", "/Files/Temp_low.png")
        print("Data folder created")
except:
        pass
try:
        copyfile("/home/pi/Desktop/HydraScan/Files/Temp_normal.png", "/Files/Temp_normal.png")
        print("Data folder created")
except:
        pass

#Plot Variables  --------------------------------------------
xstart = 0
ystart = 0
xstop = 255
ystop = 255
upperLimit1 = 100
lowerLimit1 = 0
upperLimit2 = 100
lowerLimit2 = 0
InvertXLive1 = False
InvertYLive1 = False
InvertXLive2 = False
InvertYLive2 = False
PlotBits = 256

#404 work not found
CurrentOffsetX = 0
CurrentOffsetY = 0
CurrentPoti = 10
XOffsetStart = 0 
YOffsetStart = 0 
DimensionStart = 100
ZoomedNav = False
zVoltage = 10
zStartX = 0
zStartY = 0
zStopX = 255
zStopY = 255
zBits = 256

data_file = np.loadtxt("/home/pi/Desktop/HydraScan/Files/DickPic.pattern", delimiter='\t', skiprows=0)
HydraLab = data_file[:,3]
zNew = list()
zNew2 = list()
zPart = list()
zPart2 = list()
x = xstart
y = ystart
run = 0
while x <= xstop:
        while y <= ystop:
                zPart.append(HydraLab[run])
                zPart2.append(HydraLab[run])
                y += 1
                run += 1
        y = ystart
        x += 1
        zNew.append(zPart)
        zNew2.append(zPart2)
        zPart = list()
        zPart2 = list()

#zNew = list(map(list, zip(*zNew)))
#print(zNew)
x = xstart
while x <= xstop:
        zNew2[x] = zNew[255-x]
        #print(zNew[255-x])
        x += 1
zNew = zNew2
zNew = list(map(list, zip(*zNew)))
zNewLatestOverview = zNew
#print(zNew)

data_file = np.loadtxt("/home/pi/Desktop/HydraScan/Files/HydraLab_Logo.pattern", delimiter='\t', skiprows=0)
HydraLab = data_file[:,3]
#HydraLab_Logo.pattern
zNew = list()
zNew2 = list()
zPart = list()
zPart2 = list()
x = xstart
y = ystart
run = 0
while x <= xstop:
        while y <= ystop:
                zPart.append(HydraLab[run])
                zPart2.append(HydraLab[run])
                y += 1
                run += 1
        y = ystart
        x += 1
        zNew.append(zPart)
        zNew2.append(zPart2)
        zPart = list()
        zPart2 = list()

#zNew = list(map(list, zip(*zNew)))
#print(zNew)
x = xstart
while x <= xstop:
        zNew2[x] = zNew[255-x]
        #print(zNew[255-x])
        x += 1
zNew = zNew2
zNew = list(map(list, zip(*zNew)))
zNew2 = zNew
#print(zNew)


y, x = np.meshgrid(np.linspace(ystart,ystop,(ystop-ystart+1)), np.linspace(xstart,xstop,(xstop-xstart+1)))
v = np.linspace(xstart,xstop,(xstop-xstart+1))
t = np.sin(v)*np.sin(v)
tt = np.cos(v)*np.cos(v)
N = 256
zNewOld = zNew
coordinatesTTL = list()
NavPlotNum = 0

AnimationPlot1 = False
AnimationPlot2 = False

#WSXM Colormap
CMapMatrixWSXM = np.ones((N, 3))
CMapMatrixWSXM[0:67, 2] = np.linspace(6/255, 6/255, 67)                                                                         #R
CMapMatrixWSXM[67:103, 2] = np.linspace(6/255, 17/255, (103-67))
CMapMatrixWSXM[103:161, 2] = np.linspace(17/255, 57/255, (161-103))
CMapMatrixWSXM[161:223, 2] = np.linspace(57/255, 136/255, (223-161))
CMapMatrixWSXM[223:255, 2] = np.linspace(136/255, 255/255, (255-223))
CMapMatrixWSXM[0:23, 1] = np.linspace(6/255, 7/255, 23)                                                                         #G
CMapMatrixWSXM[23:73, 1] = np.linspace(7/255, 47/255, (73-23))
CMapMatrixWSXM[73:149, 1] = np.linspace(47/255, 159/255, (149-73))
CMapMatrixWSXM[149:208, 1] = np.linspace(159/255, 234/255, (208-149))
CMapMatrixWSXM[208:238, 1] = np.linspace(234/255, 255/255, (238-208))
CMapMatrixWSXM[238:255, 1] = np.linspace(255/255, 255/255, (255-238))
CMapMatrixWSXM[0:35, 0] = np.linspace(4/255, 43/255, 35)                                                                        #B
CMapMatrixWSXM[35:95, 0] = np.linspace(43/255, 179/255, (95-35))
CMapMatrixWSXM[95:170, 0] = np.linspace(179/255, 255/255, (170-95))
CMapMatrixWSXM[170:255, 0] = np.linspace(255/255, 255/255, (255-170))
wsxmCMAP = ListedColormap(CMapMatrixWSXM)
inverseCMapMatrixWSXM = list(reversed(CMapMatrixWSXM))
wsxmCMAP_r = ListedColormap(inverseCMapMatrixWSXM)

#RHK Colormap
CMapMatrixRHK = np.zeros((N, 3))
CMapMatrixRHK[0:N, 1] = np.linspace(1, 0, N)
CMapMatrixRHK[0:N, 0] = np.linspace(1, 1, N)
rhkCMAP_r = ListedColormap(CMapMatrixRHK)
inverseCMapMatrixRHK=list(reversed(CMapMatrixRHK))
rhkCMAP = ListedColormap(inverseCMapMatrixRHK)

#Hydra Colormap
CMapMatrixHydra = np.zeros((N, 3))
CMapMatrixHydra[0:256, 1] = np.linspace(0/255, 255/255, N)
HydraCMAP2 = ListedColormap(CMapMatrixHydra)
inverseCMapMatrixHydra=list(reversed(CMapMatrixHydra))
HydraCMAP2_r = ListedColormap(inverseCMapMatrixHydra)

#Hydra2 Colormap
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

#Banksy Colormap
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

#LED Blinking ------------------------------------------------
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 2: Navigation Window -----------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

#Navigation Window ------------------------------------------------
class NavWin(QWidget):
        progress_valueCheck = pyqtSignal(bool, bool, bool, bool, int, int)
        progress_valueXY = pyqtSignal(int, int, int, int)
        progress_valueButton = pyqtSignal(bool)
        position_valueXY = pyqtSignal(float, float, float, float)
        progress_Focus = pyqtSignal(int)
        progress_valueLineOut = pyqtSignal(float, float, float, float, float, float, float, float)
        
        def __init__(self):
                super().__init__()
                global FullRangeDeviceX
                global FullRangeDeviceY
                global DeviceVoltage
                global PiezoVoltage
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight
                global Font
                global FontSize
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

                self.DimensionStepsX = round((FullRangeDeviceX*((PiezoVoltage/DeviceVoltage)/(DeviceVoltage*2)))/1000,3)
                self.DimensionStepsY = round((FullRangeDeviceY*((PiezoVoltage/DeviceVoltage)/(DeviceVoltage*2)))/1000,3)

                self.XStart = 0
                self.YStart = 0
                self.XStop = 255
                self.YStop = 255     

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
                self.setGeometry(self.WindowPosX,self.WindowPosY,605,595)
                self.setMinimumSize(QSize(500,500))   
                self.setWindowTitle("Quick Navigation")                                                                         #Titelbalken
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
                self.myFig.progress_valueMinMax.connect(self.MinMaxFromPlot)
                self.myFig.progress_valueLine.connect(self.LineValues)
                self.myFig.adjustSize()

                print(FullRangeDeviceX)
                print(FullRangeDeviceY)
                self.SpinX = QDoubleSpinBox(self)
                self.SpinX.setMinimum(0.000)                                                                                    #Setzt ein Minimalwert für die Auswahl
                self.SpinX.setMaximum(round(FullRangeDeviceX/1000,3))                                                           #Setzt ein Maximum für die Auswahl
                self.SpinX.setValue(round(FullRangeDeviceX/1000,3))                                                             #Setzt einen Startwert
                self.SpinX.setSingleStep(self.DimensionStepsX)                                                                  #Setzt die Schritweite
                self.SpinX.setDecimals(3)                                                                                       #Setzt die Dezimalstellen
                self.SpinX.setToolTip("Sets the X-Dimensions [\u03BCm]")                                                        #Setzt einen MousOver ToolTip
                self.SpinX.valueChanged.connect(self.XChanged)                                                                  #Setzt einen Event für den Fall der Wertänderung
                self.labelSpinX = QLabel("X-Dimensions [\u03BCm]", self) 

                self.SpinY = QDoubleSpinBox(self)
                self.SpinY.setMinimum(0.000)
                self.SpinY.setMaximum(round(FullRangeDeviceY/1000,3))
                self.SpinY.setValue(round(FullRangeDeviceY/1000,3))
                self.SpinY.setSingleStep(self.DimensionStepsY)
                self.SpinY.setDecimals(3)
                self.SpinY.setToolTip("Sets the Y-Dimensions [\u03BCm]")
                self.SpinY.valueChanged.connect(self.YChanged)
                self.labelSpinY = QLabel("Y-Dimensions [\u03BCm]", self)

                self.spinMin = QSpinBox(self)
                self.spinMin.setMinimum(0)
                self.spinMin.setMaximum(1000000)
                self.spinMin.setValue(0)
                self.spinMin.setSingleStep(1)
                self.spinMin.setToolTip("Sets the Min Value of the Plot")
                self.spinMin.valueChanged.connect(self.MinMaxChange)
                #self.labelSpinMin = QLabel("Y-Dimensions [\u03BCm]", self)
                
                self.spinMax = QSpinBox(self)
                self.spinMax.setMinimum(0)
                self.spinMax.setMaximum(1000000)
                self.spinMax.setValue(100)
                self.spinMax.setSingleStep(1)
                self.spinMax.setToolTip("Sets the Max Value of the Plot")
                self.spinMax.valueChanged.connect(self.MinMaxChange)
                #self.labelSpinMax = QLabel("Y-Dimensions [\u03BCm]", self)

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
                self.spinIntTime.setMaximum(200)
                self.spinIntTime.setValue(1)
                self.spinIntTime.setToolTip("Set the Integrationtime of the Logic-Channels in Milliseconds")
                self.spinIntTime.valueChanged.connect(self.updateCheck)

                self.buttonStart = QPushButton(text = 'Start')
                self.buttonStart.setCheckable(True)
                self.buttonStart.setToolTip("Starts the Measurement")
                self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonStart.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonStart.clicked[bool].connect(self.updateButton)
                self.buttonStart.setChecked(False)

                self.ButtonFull = QPushButton(text = 'Full Range')
                self.ButtonFull.clicked.connect(self.FullRect)
                self.labelFullSpace = QLabel(" ", self)

                self.ButtonFocus = QPushButton(text = 'Autofocus')
                self.ButtonFocus.setCheckable(True)
                self.ButtonFocus.setToolTip("Starts the Autofocus")
                self.ButtonFocus.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.ButtonFocus.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.ButtonFocus.clicked[bool].connect(self.AutoFocus)
                self.ButtonFocus.setChecked(False)

                self.ButtonOverview = QPushButton(text = 'Load Overview')
                menu = QMenu()
                menu.addAction('Load Lumi', self.LoadLumi)
                menu.addAction('Load Scat', self.LoadScat)
                menu.addAction('Load Latest', self.LoadOverview)
                menu.addAction('Load File Lumi', self.LoadOverviewFile1)
                menu.addAction('Load File Scat', self.LoadOverviewFile2)
                self.ButtonOverview.setMenu(menu)
                self.ButtonOverview.setToolTip("Load latest Overview")
                self.ButtonOverview.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.ButtonOverview.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                #self.ButtonOverview.clicked[bool].connect(self.LoadOverview)

                self.TTLSync = QCheckBox("TTL-Sync", self)
                self.TTLSync.stateChanged.connect(self.updateCheck)

                self.Sympho = QCheckBox("SymPhoTime", self)
                self.Sympho.stateChanged.connect(self.updateCheck)

                self.ZStack = QCheckBox("Z-Stack", self)
                self.ZStack.stateChanged.connect(self.ZStackCheck)

                self.Slope = QCheckBox("Slope", self)
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

                self.groupboxMeasure = QGroupBox(self)
                self.vboxMeasure = QVBoxLayout(self)
                self.vboxMeasure.addWidget(self.TTLSync)
                self.vboxMeasure.addWidget(self.Sympho)
                self.vboxMeasure.addWidget(self.ZStack)
                self.vboxMeasure.addWidget(self.Slope)
                self.vboxMeasure.addWidget(self.labelIntTime)
                self.vboxMeasure.addWidget(self.spinIntTime)
                self.vboxMeasure.addWidget(self.Bits)
                self.vboxMeasure.addWidget(self.Volts)
                self.vboxMeasure.addWidget(self.ButtonFocus)
                self.groupboxMeasure.setLayout(self.vboxMeasure)

                self.groupboxSettings = QGroupBox("Contrast", self)
                self.vboxSettings = QVBoxLayout(self)
                self.vboxSettings.addWidget(self.spinMin)
                self.vboxSettings.addWidget(self.spinMax)
                self.vboxSettings.addWidget(self.ButtonOverview)
                self.groupboxSettings.setLayout(self.vboxSettings)

                self.LAYOUTV.addWidget(self.buttonStart)
                self.LAYOUTV.addWidget(self.groupboxMeasure)
                self.LAYOUTV.addWidget(self.groupboxSettings)

                self.LAYOUTH.addLayout(self.LAYOUTV)
                self.LAYOUTH.addWidget(self.myFig)

                self.LAYOUT_A.addLayout(self.LAYOUTH)
                self.LAYOUT_A.addWidget(self.groupboxDimensions)

                self.setLayout(self.LAYOUT_A)
                self.LoadLumi()

        def LoadLumi(self):
                self.myFig.FromLive(0,zoom=True)

        def LoadScat(self):
                self.myFig.FromLive(1,zoom=True)

        def LoadOverviewFile1(self):
                self.LoadOverviewFile(0)

        def LoadOverviewFile2(self):
                self.LoadOverviewFile(1)

        #Geändert 14.08.2025
        def LoadOverviewFile(self, num):
                global zNewLatestOverview
                global XOffsetStart
                global YOffsetStart
                global DimensionStart
                global ZoomedNav
                global FullRangeDeviceX

                self.OverviewPathRaw = str(QFileDialog.getOpenFileName(self, "Open File", "/home/pi/Desktop/Data", "Textfile (*.txt)"))
                lengthFilePath1 = len(self.OverviewPathRaw) - 22
                self.OverviewPath = self.OverviewPathRaw[2:lengthFilePath1]
                lengthFilePath2 = len(self.OverviewPathRaw) - 26
                self.NewFilePath = self.OverviewPathRaw[2:lengthFilePath2]
                #DataStart = 0

                f = open(self.OverviewPath, "r")
                Line = f.readline()
                Line = f.readline()
                Line = f.readline()
                Line = f.readline()
                Offset = str(f.readline())
                Line = f.readline()
                Range = str(f.readline())
                f.close()

                x = Range.find(":")
                Range = Range[x+2:]
                x = Range.find(".")
                Range = Range[:x]

                RangeInt = int(Range)

                x = Offset.find(":")
                Offset = Offset[x+2:]
                x = Offset.find(".")
                OffsetX = Offset[:x+2]
                OffsetX = float(OffsetX)

                x = Offset.find(":")
                Offset = Offset[x+2:]
                x = Offset.find(".")
                OffsetY = Offset[:x+2]
                OffsetY = float(OffsetY)
                
                #print("OffsetX: " + str(OffsetX))
                #print("OffsetY: " + str(OffsetY))

                if RangeInt != FullRangeDeviceX:
                        YesNo = self.button_clicked(RangeInt/1000)
                        if YesNo == True:
                                XStart = int((OffsetX/FullRangeDeviceX)*255)
                                XStop = int(XStart + ((RangeInt/FullRangeDeviceX)*255))
                                YStart = int((OffsetY/FullRangeDeviceX)*255)
                                YStop = int(YStart + ((RangeInt/FullRangeDeviceX)*255))
                                #self.myFig.SetRect(XStart, YStart, XStop, YStop)
                                #print("Start/Stop: " + str(XStart) + " - " + str(YStart) + " / " + str(XStop) + " - " + str(YStop))
                                self.progress_valueXY.emit(XStart, YStart, XStop, YStop)
                                #self.position_valueXY.emit(XStart, YStart, XStart, YStart)
                                #self.SpinX.setValue(round(RangeInt/1000,3))  
                                #self.SpinY.setValue(round(RangeInt/1000,3)) 
                                XOffsetStart = OffsetX/1000
                                YOffsetStart = OffsetY/1000
                                DimensionStart = RangeInt/1000
                                ZoomedNav = True
                                zoom = True
                        else:
                                return
                else:
                        XOffsetStart = 0
                        YOffsetStart = 0
                        DimensionStart = FullRangeDeviceX/1000          
                        ZoomedNav = False
                        zoom = False
                
                #print("Lul: " + str(ZoomedNav) + " - Offset: " + str(XOffsetStart) + " x " + str(YOffsetStart) + " - Dim: " + str(DimensionStart))
                
                data_file = np.loadtxt(self.OverviewPath, delimiter='\t', skiprows=10)
                LumiRaw = data_file[:,8]
                ScatRaw = data_file[:,9]
                pixel = int(math.sqrt(len(LumiRaw)))
                
                if num == 0:
                        data = LumiRaw
                else:
                        data = ScatRaw

                print("Pixel: " + str(pixel))
                zNew = list()
                zPart = list()
                x = 0
                y = 0
                run = 0
                while x <= (pixel-1):
                        print("x: " + str(x))
                        while y <= (pixel-1):
                                #print("xy: " + str(x) + " x " + str(y))
                                zPart.append(data[run])
                                run += 1
                                y += 1
                        y = 0
                        x += 1
                        zNew.append(zPart)
                        zPart = list()
                zNew2 = zNew

                print("length zNew: " + str(len(zNew)))
                print("length zNew2: " + str(len(zNew2)))
                #x = 0
                #while x <= (pixel-1):
                #        print(x)
                #        zNew[x] = zNew2[(pixel-1)-x]
                #        x += 1
                zNew = list(map(list, zip(*zNew)))
                zNewLatestOverview = zNew

                self.myFig.LoadOverviewFile(zoom)
                if RangeInt == FullRangeDeviceX:
                        self.FullRect()

        def button_clicked(self, Range):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Obacht!!!")
                dlg.setText("Achtung die gewählte Datei beinhaltet keine Übersichtsmessung.\n\nDimensionen: " + str(Range) + " \u03BCm x " + str(Range) + " \u03BCm\n\nTrotzdem übernehmen?")
                dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dlg.setIcon(QMessageBox.Question)
                button = dlg.exec()

                if button == QMessageBox.Yes:
                        return True
                else:
                        return False

        def LoadOverview(self):
                self.FullRect()
                self.myFig.LoadOverview(False)

        def WindowClose(self):
                try:
                        self.myFig.close()
                except:
                        pass
                self.close()

        def MinMaxFromPlot(self, Min, Max):
                print("MinMaxFromPlot")
                self.spinMin.setValue(Min)
                self.spinMax.setValue(Max)

        def MinMaxChange(self):
                print("MinMaxChange")
                NewMin = self.spinMin.value()
                NewMax = self.spinMax.value()
                self.myFig.MinMaxChange(NewMin, NewMax)

        def UpdateFromPlot(self, past, zoom, Min, Max):
                global coordinatesTTL
                global DimensionStart
                
                print("MinMaxChange")
                coordinatesTTL = list()
                self.myFig.FromLive(past, zoom = zoom)
                self.MinMaxFromPlot(Min, Max)
                self.SpinX.setValue(int(DimensionStart))

        def UpdateFromTTL(self, past, coordinates):
                self.myFig.FromLive(past, fromTTL = True, coordinates=coordinates)

        def SaveFig(self):
                self.myFig.FromLive(0, fromTTL = True, coordinatesNew = False, save=True)
                self.myFig.FromLive(1, fromTTL = True, coordinatesNew = False, save=True)

        def AddCoordinates(self, AddX, AddY):
                global coordinatesTTL
                global NavPlotNum
                global zNew
                global zNew2
                global zNewold

                self.AddX = AddX
                self.AddY = AddY

                past = NavPlotNum
                if past == 0:
                        data = zNew
                else:
                        data = zNew2

                data = zNewOld

                localMax = 0
                MaxPosX = AddX
                MaxPosY = AddY
                Surroundings = 5
                i = self.AddX - Surroundings
                while i <= self.AddX + Surroundings and i < len(data) and i >= 0:
                        j = self.AddY - Surroundings
                        while j <= self.AddY + Surroundings and j < len(data) and j >= 0:
                                if data[i][j] > localMax:
                                        localMax = data[i][j]
                                        MaxPosX = i
                                        MaxPosY = j
                                j += 1
                        i += 1

                self.coordinatesTTL = coordinatesTTL
                self.coordinatesNew = list()
                i = 0
                while i <= len(self.coordinatesTTL):
                        self.coordinatesLine = list()
                        if i < len(self.coordinatesTTL):
                                self.coordinatesLine.append(self.coordinatesTTL[i][0])
                                self.coordinatesLine.append(self.coordinatesTTL[i][1])
                        else:
                                self.coordinatesLine.append(MaxPosX)
                                self.coordinatesLine.append(MaxPosY)
                        self.coordinatesNew.append(self.coordinatesLine)
                        i += 1
                x = self.coordinatesNew
                self.coordinatesTTL = np.array([np.array(xi) for xi in x])
                coordinatesTTL = self.coordinatesTTL
                
                self.myFig.FromLive(past, fromTTL = True, coordinates=self.coordinatesTTL, coordinatesNew = False)

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
                self.SpinX.setValue(Volts*10)
                self.SpinY.setValue(Volts*10)

        def UncheckButton(self):
                self.buttonStart.setToolTip("Start the Measurement")
                self.buttonStart.setChecked(False)
                self.buttonStart.setText("Start")
                self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")

        def PositionFromMainMid(self, MidX, MidY, Range):
                #print("Mittelpunkt: " + str(MidX) + "x" + str(MidY) + "  - Range: " + str(Range))
                pass

        def PositionFromMain(self, XStart, YStart, XStop, YStop):
                self.XStart = XStart
                self.YStart = YStart
                self.XStop = XStop
                self.YStop = YStop
                XDim = round(((self.XStop-self.XStart)*(FullRangeDeviceX/self.BitVal))/1000,0)
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
                global FullRangeDeviceX
                X = self.SpinX.value()
                Y = self.SpinY.value()
                if X != Y and X != FullRangeDeviceX/1000:
                        Y = X
                if Y != self.YOld1:
                        self.SpinY.setValue(Y)
                        self.NewDimSpin()
                        self.XOld1 = X
                        self.YOld1 = Y

        def YChanged(self):
                global FullRangeDeviceY
                X = self.SpinX.value()
                Y = self.SpinY.value()
                if Y != X and Y != FullRangeDeviceY/1000:
                        X = Y
                if X != self.XOld1:
                        self.SpinX.setValue(X)
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
                DimX = (self.XStop-self.XStart)
                DimY = (self.YStop-self.YStart)
                #print("X Pos: " + str(self.XStart) + " x " + str(self.XStop))
                #print("Y Pos: " + str(self.YStart) + " x " + str(self.YStop))
                #print("Divs: " + str(DimX) + " x " + str(DimY))
                if DimX>DimY:
                        Dim = DimX
                else:
                        Dim = DimY
                self.XStop = self.XStart + Dim
                self.YStop = self.YStart + Dim
                self.progress_valueXY.emit(self.XStart, self.YStart, self.XStop, self.YStop)

        def LineValues(self, X1, Y1, X2, Y2, X1raw, Y1raw, X2raw, Y2raw):
                global XOffsetStart
                global YOffsetStart
                global DimensionStart
                global ZoomedNav
                global FullRangeDeviceX
                global FullRangeDeviceY

                PlotPosX1 = X1
                PlotPosY1 = Y1
                PlotPosX2 = X2
                PlotPosY2 = Y2
                #print("PlotPosX: " + str(PlotPosX))
                print("Plot Pos: " + str(PlotPosX1) + " x " + str(PlotPosY1))
                print("Plot Pos raw: " + str(X1raw) + " x " + str(Y1raw))
                #print(str(ZoomedNav) + " - Offset: " + str(XOffsetStart) + " x " + str(YOffsetStart) + " - Dim: " + str(DimensionStart))
                if ZoomedNav == True:
                        PosX1 = XOffsetStart + (DimensionStart/(FullRangeDeviceX/1000))*X1
                        PosY1 = YOffsetStart + (DimensionStart/(FullRangeDeviceY/1000))*Y1
                        PosX2 = XOffsetStart + (DimensionStart/(FullRangeDeviceX/1000))*X2
                        PosY2 = YOffsetStart + (DimensionStart/(FullRangeDeviceY/1000))*Y2
                else:
                        PosX1 = X1
                        PosY1 = Y1
                        PosX2 = X2
                        PosY2 = Y2
                self.progress_valueLineOut.emit(PosX1, PosY1, PosX2, PosY2, X1raw, Y1raw, X2raw, Y2raw)
                #self.progress_valueLineOut.emit(X1, Y1, X2, Y2)

        def PosFromPlot(self, X, Y):
                global XOffsetStart
                global YOffsetStart
                global DimensionStart
                global ZoomedNav
                global FullRangeDeviceX
                global FullRangeDeviceY

                PlotPosX = X
                PlotPosY = Y
                #print("PlotPosX: " + str(PlotPosX))
                #print("Plot Pos" + str(PlotPosX) + " x " + str(PlotPosY))
                #print(str(ZoomedNav) + " - Offset: " + str(XOffsetStart) + " x " + str(YOffsetStart) + " - Dim: " + str(DimensionStart))
                if ZoomedNav == True:
                        PosX = XOffsetStart + (DimensionStart/(FullRangeDeviceX/1000))*X
                        PosY = YOffsetStart + (DimensionStart/(FullRangeDeviceY/1000))*Y
                else:
                        PosX = X
                        PosY = Y

                #print("New Pos" + str(PosX) + " x " + str(PosY))
                self.position_valueXY.emit(PosX, PosY, PlotPosX, PlotPosY)

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
                val2 = self.Sympho.isChecked()
                val3 = self.ZStack.isChecked()
                val4 = self.Slope.isChecked()
                val5 = self.spinIntTime.value()
                val6 = self.Bits.currentIndex()
                self.progress_valueCheck.emit(val1, val2, val3, val4, val5, val6)
                self.myFig.UpdateBits(val6)

        def updateXY(self):
                val1 = self.TTLSync.isChecked()
                val2 = self.Sympho.isChecked()
                val3 = self.ZStack.isChecked()
                val4 = self.Slope.isChecked()
                self.progress_valueXY.emit(val1, val2, val3, val4)

        def updateButton(self):
                global zStartX
                global zStartY
                global zStopX
                global zStopY

                val1 = self.buttonStart.isChecked()
                self.progress_valueButton.emit(val1)
                if val1 == True:
                        zStartX = self.XStart
                        zStartY = self.YStart
                        zStopX = self.XStop
                        zStopY = self.YStop

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

        def AutoFocus(self, down):                                                                                      #Setzt das Messfenster
                if down:
                        global FocusZ
                        self.FocusZ = FocusZ

                        self.ButtonFocus.setToolTip("Stop the Autofocus")
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

                FocusZ = FocusNew
                self.progress_Focus.emit(FocusNew)
                self.ButtonFocus.setToolTip("Start the Autofocus")
                self.ButtonFocus.setChecked(False)
                self.ButtonFocus.setStyleSheet("color: black; background-color: rgb(0,255,0)")

#Auto Focus ------------------------------------------------
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
                #print("Voltage: " + str(self.Voltage))
                Poti.write_range(self.Voltage)

                self.XOffset = 0
                self.YOffset = 0
                #print("Offset: " + str(self.XOffset) + "x" + str(self.YOffset))
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

#Navigation Plot ------------------------------------------------
class NavPlot(FigureCanvas):
        progress_valueXYrect = pyqtSignal(int, int, int, int)
        progress_valueXYpos = pyqtSignal(float,float)
        progress_valueMinMax = pyqtSignal(int,int)
        progress_valueLine = pyqtSignal(float, float, float, float, float, float, float, float)
        
        def __init__(self):  
                global xstart
                global ystart
                global xstop
                global ystop
                global upperLimit1
                global lowerLimit1
                global HydraCMAP2
                global HydraCMAP2_r
                global HydraCMAP
                global HydraCMAP_r
                global InvertXLive1
                global InvertYLive1

                self.zoom = False
                self.HydraCMAP = HydraCMAP2
                self.HydraCMAP_r = HydraCMAP2_r
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
                self.X = 0
                self.Y = 0
                #PosFromLine
                self.Line = False
                self.LineVals = [[0,0],[0,0]]
                self.lineOn = False
                self.MarkerOn = False
                
                while self.y <= self.ystop:
                        while self.x <= self.xstop:
                                self.zPart.append(0)
                                self.x += 1
                        self.x = self.xstart
                        self.y += 1
                        self.zNew.append(self.zPart)
                        self.zPart = list()
                
                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))

                self.cmap = self.HydraCMAP
                self.fig, self.ax1  = plt.subplots()
                plt.axis('off')
                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax1.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                self.ax1.set_aspect('equal')
                #Jonas
                if InvertYLive1 == True:
                        self.ax1.invert_yaxis()
                if InvertXLive1 == True:
                        self.ax1.invert_xaxis()

                FigureCanvas.__init__(self, self.fig)
                cid1 = self.fig.canvas.mpl_connect('button_press_event', self.on_press2)

                self.RS = RectangleSelector(self.ax1, self.line_select_callback,
                        useblit=False, button=[1,3], 
                        minspanx=5, minspany=5, spancoords='pixels', state_modifier_keys=dict(square='square'),
                        interactive=True)

                self.iteration = 0

        def LoadOverview(self, zoom):
                self.FromLive(-1, zoom = zoom)

        def LoadOverviewFile(self, zoom):
                self.FromLive(-2, zoom = zoom)

        def MinMaxChange(self, NewMin, NewMax):
                self.NewMin = NewMin
                self.NewMax = NewMax
                if self.NewMax > self.NewMin:
                        self.quad1.set_clim(self.NewMin, self.NewMax)
                        self.fig.canvas.draw()

        def FromLive(self, past, zoom = False, fromTTL = False, coordinates = 0, coordinatesNew = True, save=False, oldPlot = False, NewLims = True):
                global zNew
                global zNew2
                global zNewOld
                global zNewLatestOverview
                global DimensionStart
                global CurrentOffsetX
                global CurrentOffsetY
                global CurrentPoti
                global XOffsetStart
                global YOffsetStart
                global upperLimit1
                global lowerLimit1
                global upperLimit2
                global lowerLimit2
                global zVoltage
                global zStartX
                global zStartY
                global zStopX
                global zStopY
                global zBits
                global HydraCMAP2
                global HydraCMAP2_r
                global coordinatesTTL
                global NavPlotNum
                global FilePath
                global SubPoints
                global ZoomedNav
                global InvertXLive1
                global InvertYLive1
                global FullRangeDeviceX
                print("FromLive")

                NavPlotNum = past
                self.past = NavPlotNum
                self.zoom = zoom
                self.HydraCMAP = HydraCMAP2
                self.HydraCMAP_r = HydraCMAP2_r

                self.Bits = zBits
                if self.Bits == 0:
                        self.Bits = 64
                elif self.Bits == 1:
                        self.Bits = 128
                elif self.Bits == 2:
                        self.Bits = 256
                elif self.Bits == 3:
                        self.Bits = 512
                elif self.Bits == 4:
                        self.Bits = 1024
                elif self.Bits == 5:
                        self.Bits = 2048
                elif self.Bits == 6:
                        self.Bits = 4096
                self.Volts = zVoltage
                self.xstart = 0
                self.ystart = 0
                self.xstop = 255
                self.ystop = 255
                self.xstartNew = zStartX
                self.ystartNew = zStartY
                self.xstopNew = zStopX
                self.ystopNew = zStopY
                self.BitsNewX = self.xstopNew - self.xstartNew + 1

                if NavPlotNum == 0:
                        self.zNew = zNew
                if NavPlotNum == 1:
                        self.zNew = zNew2
                if NavPlotNum == -1:
                        self.zNew = zNewLatestOverview
                        self.Bits = len(self.zNew[0])
                        DimensionStart = (FullRangeDeviceX/1000)
                        CurrentOffsetX = 0
                        CurrentOffsetY = 0
                        CurrentPoti = 10
                        XOffsetStart = 0 
                        YOffsetStart = 0 
                        ZoomedNav = True
                        zoom = True
                if NavPlotNum == -2:
                        self.zNew = zNewLatestOverview
                        self.Bits = len(self.zNew[0])
                        CurrentOffsetX = XOffsetStart
                        CurrentOffsetY = YOffsetStart
                        CurrentPoti = round(DimensionStart/10,1)

                if zoom == True:
                        ZoomedNav = True
                        self.xstartNew = 0
                        self.ystartNew = 0
                        self.xstopNew = 255
                        self.ystopNew = 255
                        #self.BitsNewX = self.Bits
                        self.BitsNewX = 256
                else:
                        ZoomedNav = False
                        if DimensionStart == (FullRangeDeviceX/1000):
                                zNewLatestOverview = self.zNew


                #Größe definieren
                Size = self.Bits
                NewSize = self.BitsNewX
                Faktor = self.BitsNewX/self.Bits
                #print("Bits: " + str(Size) + " - NewSize: " + str(NewSize) + " - Faktor: " + str(Faktor))

                #Output berechnen
                if fromTTL == True:
                        if coordinatesNew == True:
                                coordinates = coordinates * Faktor
                                i = 0
                                while i < len(coordinates):
                                        coordinates[i][1] = coordinates[i][1] + self.xstartNew
                                        coordinates[i][0] = coordinates[i][0] + self.ystartNew
                                        i += 1
                                np.around(coordinates, decimals=0)
                        else:
                                coordinates = coordinatesTTL

                        if len(coordinates) != 0:
                                struct_a = np.core.records.fromarrays(
                                coordinates.transpose(), names="x, y", formats="i8, i8"
                                )
                                struct_a.sort(order="y")

                                i = 0
                                coordinatesSorted = list()
                                while i < len(struct_a):
                                        coordinatesLine = list()
                                        coordinatesLine.append(struct_a[i][0])
                                        coordinatesLine.append(struct_a[i][1])
                                        coordinatesSorted.append(coordinatesLine)
                                        i += 1
                                x = coordinatesSorted
                                coordinates = np.array([np.array(xi) for xi in x])

                x = self.zNew
                val = np.array([np.array(xi) for xi in x])
                Z = val
                x = np.linspace(0, self.Bits-1, self.Bits)
                y = np.linspace(0, self.Bits-1, self.Bits)
                x2 = np.linspace(0, self.Bits-1, self.BitsNewX)
                y2 = np.linspace(0, self.Bits-1, self.BitsNewX)
                f = interp2d(x, y, Z, kind='cubic')
                Z2 = f(y2, x2)
                zout = Z2

                if oldPlot == False and NewLims == True:
                        maxVal = list()
                        minVal = list()
                        i = 0
                        while i < len(zout):
                                maxVal.append(max(zout[i]))
                                minVal.append(min(zout[i]))
                                i += 1
                        self.upperLimit = max(maxVal)
                        self.lowerLimit = min(minVal)

                        self.progress_valueMinMax.emit(int(self.lowerLimit), int(self.upperLimit))
                else:
                        self.upperLimit = self.NavWin.spinMax.value()
                        self.lowerLimit = self.NavWin.spinMin.value()

                y = 0
                while y < 256:
                        x = 0
                        while x < 256:
                                yNew = y-self.ystartNew
                                xNew = x-self.xstartNew
                                if yNew >= 0 and yNew < len(zout) and xNew >= 0 and xNew < len(zout):
                                        zNewOld[x][y] = zout[xNew][yNew]
                                x += 1        
                        y += 1
                self.zNew = zNewOld

                self.ax1.clear()
                print("LowerLim: " + str(self.lowerLimit))
                print("Upperlim: " + str(self.upperLimit))
                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))
                self.RS.set_visible(False)
                self.RS.update()

                self.quad1 = self.ax1.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)

                self.ax1.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                self.ax1.set_aspect('equal')

                if InvertYLive1 == True:
                        self.ax1.invert_yaxis()
                if InvertXLive1 == True:
                        self.ax1.invert_xaxis()

                if fromTTL == True:
                        if len(coordinates) != 0:
                                self.ax1.plot(coordinates[:, 0], coordinates[:, 1], color='white', marker='x', markersize=15, linestyle='none')
                                
                                i = 0
                                while i < len(coordinates):
                                        label = f"{i+1}"
                                        self.ax1.annotate(label, # this is the text
                                                        (coordinates[i][0], coordinates[i][1]), # these are the coordinates to position the label
                                                        textcoords="offset points", # how to position the text
                                                        xytext=(0,10), # distance from text to points (x,y)
                                                        ha='center')
                                        i += 1
                                coordinatesTTL = coordinates

                plt.axis('off')
                self.ax1.axis('off')
                self.fig.canvas.draw()
                cid1 = self.fig.canvas.mpl_connect('button_press_event', self.on_press2)

                self.RS = RectangleSelector(self.ax1, self.line_select_callback,
                        useblit=False, button=[1,3], 
                        minspanx=5, minspany=5, spancoords='pixels', state_modifier_keys=dict(square='square'),
                        interactive=True)

                if save == True:
                        Date = self.DateTime = time.strftime("%d-%m-%Y_%H-%M-%S")
                        self.Filename = FilePath + SubPoints + "_" + str(NavPlotNum) + "_" + Date + ".png"
                        self.fig.savefig(self.Filename)

                return self.quad1
        
        def RemoveLineMarker(self):
                print("Remove Marker 2")
                print(self.MarkerOn)
                print(self.lineOn)
                
                if self.MarkerOn == True:
                        m = self.MarkerPos.pop(0)
                        m.remove()
                        self.MarkerOn = False
                if self.lineOn == True:
                        l = self.lineplot.pop(0)
                        l.remove()
                        self.lineOn = False
                self.fig.canvas.draw()

        def PositionMarker(self, X, Y, On):
                global XOffsetStart
                global YOffsetStart
                global DimensionStart
                global FullRangeDeviceX
                global FullRangeDeviceY

                if self.MarkerOn == True:
                        m = self.MarkerPos.pop(0)
                        m.remove()
                        self.MarkerOn = False

                try:
                        print("PositionMarker: " + str(X) + " x " + str(Y))
                        self.FromLive(self.past, zoom = self.zoom, oldPlot = True, NewLims = False)
                except:
                        pass
                if On == True:
                        if X != self.X or Y != self.Y:
                                #work
                                if self.zoom == True:
                                        print("DimStart: " + str(DimensionStart) + "  - Offset: " + str(XOffsetStart) + " x " + str(YOffsetStart))
                                        self.X = int((((X*(100/4095)) - XOffsetStart) / DimensionStart) * 255)
                                        self.Y = int((((Y*(100/4095)) - YOffsetStart) / DimensionStart) * 255)
                                else:
                                        XNew = int((X/4095)*255)
                                        YNew = int((Y/4095)*255)
                                        #print("PosNew: " + str(XNew) + " x " + str(YNew))
                                        self.X = XNew
                                        self.Y = YNew


                                #print("PosMarker: " + str(X) + " - " + str(Y) + " - " + str(On))
                                print("PosMarkerOld: " + str(self.X) + " - " + str(self.Y))
                                #print("PosPlot: " + str(self.past) + " - " + str(self.zoom))
                                self.MarkerPos = self.ax1.plot(self.X, self.Y, color='white', marker='x', markersize=15, linestyle='none')
                                #PosFromLine
                                #label = "Pos"
                                #try:
                                #        self.anno.remove()
                                #except:
                                #        pass
                                #self.anno = self.ax1.annotate(label, # this is the text
                                #                (self.X, self.Y), # these are the coordinates to position the label
                                #                textcoords="offset points", # how to position the text
                                #                xytext=(0,10), # distance from text to points (x,y)
                                #                ha='center')
                                self.MarkerOn = True
                                self.fig.canvas.draw()


        def UpdateBits(self, Bits):
                global HydraCMAP
                global HydraCMAP_r
                
                self.HydraCMAP = HydraCMAP
                self.HydraCMAP_r = HydraCMAP_r
                self.Bits = 255
                self.xstart = 0
                self.ystart = 0
                self.xstop = 255
                self.ystop = 255
                self.upperLimit = 10
                self.lowerLimit = 0
                self.zNew = list()
                self.zPart = list()
                self.x = self.xstart
                self.y = self.ystart

        def SetRect(self, XStart, YStart, XStop, YStop):
                #print("SetRect: (" + str(XStart) + " x " + str(XStop) + ") - (" + str(YStart) + " x " + str(YStop) + ")")

                #self.RS.extents = (XStart, YStart, XStop, YStop)
                self.RS.extents = (XStart,XStop,YStart,YStop)
                self.RS.update()

        def FullRect(self, Bits):
                ext = (0,Bits,0,Bits)
                self.RS.draw_shape(ext)
                self.RS._corner_handles.set_data(*self.RS.corners)
                self.RS._edge_handles.set_data(*self.RS.edge_centers)
                self.RS._center_handle.set_data(*self.RS.center)
                self.RS.update()
                
        def clear(self, XStart, YStart, XStop, YStop):
                self.RS.extents = (XStart,XStop,YStart,YStop)
                self.RS.set_visible(False)
                self.RS.update()

        def line_select_callback(self, eclick, erelease):
                global FullRangeDeviceX
                global FullRangeDeviceY

                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
                #print("XPos =" + str(x1) + "x" + str(y1))
                #print("YPos =" + str(x2) + "x" + str(y2))
                xDim = x2 - x1
                yDim = y2 - y1
                if xDim >= yDim:
                        Dim = xDim
                else:
                        Dim = yDim
                #print("Dim: " + str(Dim))
                Dim = (((round((Dim/255)*(FullRangeDeviceX/1000),0)//5)*5)/(FullRangeDeviceX/1000))*255                 #Unsicher
                x2 = x1 + Dim
                y2 = y1 + Dim
                #print("XPos =" + str(x1) + "x" + str(y1))
                #print("YPos =" + str(x2) + "x" + str(y2))
                #print("DimNew: " + str(Dim))
                #print("DimV: " + str(((round((Dim/255)*100,0)//5)*5)))

                self.RS.extents = (x1,x2,y1,y2)
                self.RS.update()
                self.progress_valueXYrect.emit(int(round(x1,0)), int(round(y1,0)), int(round(x2,0)), int(round(y2,0)))

        def toggle_selector(self, event):
                if event.key in ['Q', 'q'] and self.RS1.active:
                        self.RS.set_active(False)
                if event.key in ['A', 'a'] and not self.RS1.active:
                        self.RS.set_active(True)

        def on_press(self, event):
                self.RS.set_visible(True)
                self.XStart = event.xdata
                self.YStart = event.ydata
                self.RS.update()

        def on_release(self, event):
                self.XStop = event.xdata
                self.YStop = event.ydata
                self.RS.update()

        def on_press2(self, pos):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage

                if pos.button == 1:
                        if pos.xdata != None and pos.ydata != None:
                                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)
                                X = round((int(round(pos.xdata,0)) * (self.DimensionStepsX/255)),3)
                                Y = round((int(round(pos.ydata,0)) * (self.DimensionStepsY/255)),3)
                                #XDim = X + self.DimensionStepX
                                self.progress_valueXYpos.emit(X, Y)
                                #print("on_press2 true: " + str(X) + " x " + str(Y) + " - " + str(self.DimensionStepsX))
                if pos.button == 3:
                        if self.Line == False:
                                self.LineVals[0][0] = pos.xdata
                                self.LineVals[0][1] = pos.ydata
                                self.Line = True
                                self.DrawLine(new = False)
                        else:
                                self.LineVals[1][0] = pos.xdata
                                self.LineVals[1][1] = pos.ydata
                                self.Line = False
                                self.DrawLine(new = True)

        def DrawLine(self, new = False):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage

                if new == True:
                        self.lineOn = True
                        self.lineplot = self.ax1.plot([self.LineVals[0][0],self.LineVals[1][0]],[self.LineVals[0][1],self.LineVals[1][1]], 'blue')
                        
                        self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                        self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)

                        print("DimensionStepsX: " + str(self.DimensionStepsX))
                        print("X1: " + str(self.LineVals[0][0]))
                        print("Y1: " + str(self.LineVals[0][1]))
                        print("X2: " + str(self.LineVals[1][0]))
                        print("Y2: " + str(self.LineVals[1][1]))

                        X1 = round((int(round(self.LineVals[0][0],0)) * (self.DimensionStepsX/255)),3)
                        Y1 = round((int(round(self.LineVals[0][1],0)) * (self.DimensionStepsY/255)),3)
                        X2 = round((int(round(self.LineVals[1][0],0)) * (self.DimensionStepsX/255)),3)
                        Y2 = round((int(round(self.LineVals[1][1],0)) * (self.DimensionStepsY/255)),3)
                        
                        self.progress_valueLine.emit(X1, Y1, X2, Y2, self.LineVals[0][0], self.LineVals[0][1], self.LineVals[1][0], self.LineVals[1][1])

                else:
                        if self.lineOn == True:
                                l = self.lineplot.pop(0)
                                l.remove()
                                self.lineOn = False

                

"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 3: Live Plot Window ------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

#Live Plot Window ------------------------------------------------
class PlotWindow(QWidget):
        progress_valueRect = pyqtSignal(int, int, int, int)
        progress_valuePos = pyqtSignal(int, int)
        progress_Refresh = pyqtSignal(int, int, int, int)

        def __init__(self):
                super().__init__()
                global CH1
                global CH2
                global CH3
                global CH4
                global CHA
                global CHB
                global L2
                global L3
                global Font
                global FontSize
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

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

                # Create a Layout
                self.LAYOUT_A = QHBoxLayout()

                self.ButtonSave = QPushButton(text = 'Save Plots')
                self.ButtonSave.setFixedSize(230, 30)
                self.ButtonSave.clicked.connect(self.SavePlots)
                self.ButtonSave.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.ButtonRefresh1 = QPushButton(text = 'Refresh Navigation')
                self.ButtonRefresh1.setFixedSize(210, 30)
                self.ButtonRefresh1.clicked.connect(self.RefreshNav)
                self.ButtonRefresh1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.ButtonRefreshZoomed1 = QPushButton(text = 'Refresh Zoomed')
                self.ButtonRefreshZoomed1.setFixedSize(210, 30)
                self.ButtonRefreshZoomed1.clicked.connect(self.RefreshNavZoomed)
                self.ButtonRefreshZoomed1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.ButtonRefresh2 = QPushButton(text = 'Refresh Navigation')
                self.ButtonRefresh2.setFixedSize(210, 30)
                self.ButtonRefresh2.clicked.connect(self.RefreshNav2)
                self.ButtonRefresh2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                self.ButtonRefreshZoomed2 = QPushButton(text = 'Refresh Zoomed')
                self.ButtonRefreshZoomed2.setFixedSize(210, 30)
                self.ButtonRefreshZoomed2.clicked.connect(self.RefreshNavZoomed2)
                self.ButtonRefreshZoomed2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.ButtonAutoScale1 = QPushButton(text = 'Auto Scale')
                self.ButtonAutoScale1.setCheckable(True)
                self.ButtonAutoScale1.setFixedSize(210, 30)
                self.ButtonAutoScale1.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.ButtonAutoScale1.setChecked(True)
                self.ButtonAutoScale1.setVisible(False)

                self.ButtonAutoScale2 = QPushButton(text = 'Auto Scale')
                self.ButtonAutoScale2.setCheckable(True)
                self.ButtonAutoScale2.setFixedSize(210, 30)
                self.ButtonAutoScale2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.ButtonAutoScale2.setChecked(True)
                self.ButtonAutoScale2.setVisible(False)

                self.InvertCMAPLive1 = QCheckBox("Invert Color", self)
                #self.InvertCMAPLive1.stateChanged.connect(self.InvertCMAP1)
                self.InvertXAxisLive1 = QCheckBox("Invert X", self)
                self.InvertXAxisLive1.stateChanged.connect(self.InvertXChanged1)
                self.InvertYAxisLive1 = QCheckBox("Invert Y", self)
                #self.InvertYAxisLive1.setChecked(True)
                self.InvertYAxisLive1.stateChanged.connect(self.InvertYChanged1)

                self.InvertCMAPLive2 = QCheckBox("Invert Color", self)
                #self.InvertCMAPLive2.stateChanged.connect(self.InvertCMAP2)
                self.InvertXAxisLive2 = QCheckBox("Invert X", self)
                self.InvertXAxisLive2.stateChanged.connect(self.InvertXChanged2)
                self.InvertYAxisLive2 = QCheckBox("Invert Y", self)
                #self.InvertYAxisLive2.setChecked(True)
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
                
                self.RangeUpper1 = QSpinBox(self)
                self.RangeUpper1.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeUpper1.setMaximum(1000000)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeUpper1.setValue(100)                                                                                                  #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeUpper1.valueChanged.connect(self.UpperRange1)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeUpper1.setToolTip("Sets the upper Range")
                self.labelRangeUpper1 = QLabel("Upper Range", self)

                self.RangeLower1 = QSpinBox(self)
                self.RangeLower1.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeLower1.setMaximum(1000000)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeLower1.setValue(0)                                                                                                  #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeLower1.valueChanged.connect(self.LowerRange1)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeLower1.setToolTip("Sets the lower Range")
                self.labelRangeLower1 = QLabel("Lower Range", self)

                self.RangeUpper2 = QSpinBox(self)
                self.RangeUpper2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeUpper2.setMaximum(1000000)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeUpper2.setValue(100)                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.RangeUpper2.valueChanged.connect(self.UpperRange2)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.RangeUpper2.setToolTip("Sets the upper Range")
                self.labelRangeUpper2 = QLabel("Upper Range", self)

                self.RangeLower2 = QSpinBox(self)
                self.RangeLower2.setMinimum(0)                                                                                                          #Setzt ein Minimalwert für die Auswahl
                self.RangeLower2.setMaximum(1000000)                                                                                                        #Setzt ein Maximum für die Auswahl
                self.RangeLower2.setValue(0)                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
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
                self.selector1 = SelectFromCollection(1, self.myFig1.ax, self.myFig1.quad1)
                self.selector2 = SelectFromCollection(2, self.myFig2.ax, self.myFig2.quad2)
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
                self.vboxManipulateLumi.addWidget(self.InvertCMAPLive1)
                self.vboxManipulateLumiInvert = QHBoxLayout(self)
                self.vboxManipulateLumiInvert.addWidget(self.InvertXAxisLive1)
                self.vboxManipulateLumiInvert.addWidget(self.InvertYAxisLive1)
                self.vboxManipulateLumi.addLayout(self.vboxManipulateLumiInvert)
                self.vboxManipulateLumi.addStretch(2)
                self.vboxManipulateLumi.addWidget(self.groupboxRange1)
                self.vboxManipulateLumi.addStretch(2)
                #self.vboxManipulateLumi.addWidget(self.ButtonAutoScale1)
                self.vboxManipulateLumi.addWidget(self.ButtonRefreshZoomed1)
                self.vboxManipulateLumi.addWidget(self.ButtonRefresh1)
                self.groupboxManipulateLumi.setLayout(self.vboxManipulateLumi)
                self.groupboxManipulateLumi.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

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
                #self.vboxManipulateScat.addWidget(self.ButtonAutoScale2)
                self.vboxManipulateScat.addWidget(self.ButtonRefreshZoomed2)
                self.vboxManipulateScat.addWidget(self.ButtonRefresh2)
                self.groupboxManipulateScat.setLayout(self.vboxManipulateScat)
                self.groupboxManipulateScat.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
                self.groupboxLumi = QGroupBox(self.CheckedChannel1, self) 
                self.vboxLumi = QGridLayout(self)
                self.vboxLumi.addWidget(self.myFig1, 0, 0)
                self.vboxLumi.addWidget(self.myFig3, 1, 0)
                self.vboxLumi.addWidget(self.labelFigureStretch1)
                self.vboxLumi.setRowStretch(0, 3)
                self.vboxLumi.setRowStretch(1, 1)
                self.groupboxLumi.setLayout(self.vboxLumi)
                self.groupboxLumi.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

                self.groupboxScat = QGroupBox(self.CheckedChannel2, self)            
                self.vboxScat = QGridLayout(self)
                self.vboxScat.addWidget(self.myFig2, 0, 0)
                self.vboxScat.addWidget(self.myFig4, 1, 0)
                self.vboxScat.addWidget(self.labelFigureStretch2)
                self.vboxScat.setRowStretch(0, 3)
                self.vboxScat.setRowStretch(1, 1)
                self.groupboxScat.setLayout(self.vboxScat)
                self.groupboxScat.setFont(QFont(self.Fontstyle, 15, QFont.Bold))

                self.groupboxChannelSettings = QGroupBox(self)
                self.LayoutChannelSettings = QVBoxLayout(self)
                self.LayoutChannelSettings.addWidget(self.ButtonSave)
                self.LayoutChannelSettings.addWidget(self.groupboxManipulateLumi)
                self.LayoutChannelSettings.addWidget(self.groupboxManipulateScat)
                self.groupboxChannelSettings.setLayout(self.LayoutChannelSettings)
                self.groupboxChannelSettings.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.groupboxChannelSettings.setFixedSize(250, 1000)

                self.LAYOUT_A.addWidget(self.groupboxChannelSettings)
                self.LAYOUT_A.addWidget(self.groupboxLumi)
                self.LAYOUT_A.addWidget(self.groupboxScat)

                #self.ch1Live1.currentTextChanged.connect(self.ChannelSelect)
                #self.ch2Live1.currentTextChanged.connect(self.ChannelSelect)
                #self.PlotColors1.currentTextChanged.connect(self.PlotsytleChanged1)
                #self.PlotColors2.currentTextChanged.connect(self.PlotsytleChanged2)

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

        def WindowClose(self):
                try:
                        self.myFig1.close()
                except:
                        pass
                try:
                        self.myFig2.close()
                except:
                        pass
                try:
                        self.myFig3.close()
                except:
                        pass
                try:
                        self.myFig4.close()
                except:
                        pass
                self.close()

        def UpdateChannelNames(self):
                global CH1
                global CH2
                global CH3
                global CH4
                global CHA
                global CHB
                global L2
                global L3

                self.ch1Live1.setItemText(0, CH1) 
                self.ch1Live1.setItemText(1, CH2) 
                self.ch1Live1.setItemText(2, CH3) 
                self.ch1Live1.setItemText(3, CH4) 
                self.ch1Live1.setItemText(4, CHA) 
                self.ch1Live1.setItemText(5, CHB) 
                self.ch1Live1.setItemText(6, L2)
                self.ch1Live1.setItemText(7, L3)

                self.ch2Live1.setItemText(0, CH1) 
                self.ch2Live1.setItemText(1, CH2) 
                self.ch2Live1.setItemText(2, CH3) 
                self.ch2Live1.setItemText(3, CH4) 
                self.ch2Live1.setItemText(4, CHA) 
                self.ch2Live1.setItemText(5, CHB) 
                self.ch2Live1.setItemText(6, L2)
                self.ch2Live1.setItemText(7, L3)

                self.ChannelSelect()

        def RefreshNav(self):
                Min = self.RangeLower1.value()
                Max = self.RangeUpper1.value()
                past = 0
                zoom = 0
                self.progress_Refresh.emit(past, zoom, Min, Max)

        def RefreshNavZoomed(self):
                Min = self.RangeLower1.value()
                Max = self.RangeUpper1.value()
                past = 0
                zoom = 1
                self.progress_Refresh.emit(past, zoom, Min, Max)

        def RefreshNav2(self):
                Min = self.RangeLower2.value()
                Max = self.RangeUpper2.value()
                past = 1
                zoom = 0
                self.progress_Refresh.emit(past, zoom, Min, Max)

        def RefreshNavZoomed2(self):
                Min = self.RangeLower2.value()
                Max = self.RangeUpper2.value()
                past = 1
                zoom = 1
                self.progress_Refresh.emit(past, zoom, Min, Max)

        def updateRectLumi(self, val1, val2, val3, val4):
                self.progress_valueRect.emit(val1, val2, val3, val4)
                self.myFig2.HideRectangle()

        def updateRectScat(self, val1, val2, val3, val4):
                self.progress_valueRect.emit(val1, val2, val3, val4)
                self.myFig1.HideRectangle()

        def updatePosition(self, val1, val2):
                self.progress_valuePos.emit(val1, val2)

        def EnteredRect(self, val):
                self.myFig1.HideRectangle()
                self.myFig2.HideRectangle()

        def NewLine2(self, zNew, zNew2, t, tt):
                #print(zNew2)
                self.myFig1.CalcNewLine1(zNew)
                self.myFig3.CalcNewLine1(t)
                self.myFig2.CalcNewLine1(zNew2)
                self.myFig4.CalcNewLine1(tt)
                #print("Plot sent 2")

        def NewLine(self, Lumi, Scat):
                self.CalcNewValues1(Lumi)
                self.CalcNewValues2(Scat)

        def Date(self, Date):
                self.myFig1.UpdateFilename(Date)
                self.myFig2.UpdateFilename(Date)

        def printer(self, i):
                #print(i)
                #print(self.ch1Live1.currentText())
                pass

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
                if down:
                        self.ButtonLive.setText("Stop LivePlot")
                else:
                        self.ButtonLive.setText("Start LivePlot")

        def SavePlots(self):
                #self.myFig1.SaveFile()
                #self.myFig2.SaveFile()
                #print("Resume")
                self.myFig1.resume()

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
                #self.selector1 = SelectFromCollection(1, self.myFig1.ax, self.myFig1.quad1)
                #self.selector2 = SelectFromCollection(2, self.myFig2.ax, self.myFig2.quad2)
                #self.selector1.progress_values.connect(self.LineAnalysis1)
                #self.selector2.progress_values.connect(self.LineAnalysis2)
                #self.selector1.progress_valuesPoint.connect(self.PointAnalysis1)
                #self.selector2.progress_valuesPoint.connect(self.PointAnalysis2)

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
                if value > lowerLimit1:
                        #print("RangeChange")
                        upperLimit1 = value
                        self.myFig1.RangeChangeAnimate(upperLimit1, lowerLimit1)
                        self.myFig3.RangeChangeAnimate(upperLimit1, lowerLimit1)

        def UpperRange2(self):
                global upperLimit2
                global lowerLimit2
                value = self.RangeUpper2.value()
                if value > lowerLimit2:
                        upperLimit2 = value
                        self.myFig2.RangeChangeAnimate(upperLimit2, lowerLimit2)
                        self.myFig4.RangeChangeAnimate(upperLimit2, lowerLimit2)

        def LowerRange1(self):
                global upperLimit1
                global lowerLimit1
                value = self.RangeLower1.value()
                if upperLimit1 > value:
                        lowerLimit1 = value
                        self.myFig1.RangeChangeAnimate(upperLimit1, lowerLimit1)
                        self.myFig3.RangeChangeAnimate(upperLimit1, lowerLimit1)

        def LowerRange2(self):
                global upperLimit2
                global lowerLimit2
                value = self.RangeLower2.value()
                if upperLimit2 > value:
                        lowerLimit2 = value
                        self.myFig2.RangeChangeAnimate(upperLimit2, lowerLimit2)
                        self.myFig4.RangeChangeAnimate(upperLimit2, lowerLimit2)

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
                #print(InvertXLive1)
                self.myFig1.InvertX(InvertXLive1)

        def InvertYChanged1(self):
                global InvertYLive1
                InvertYLive1 = self.InvertYAxisLive1.isChecked()
                #print(InvertYLive1)
                self.myFig1.InvertY(InvertYLive1)

        def InvertXChanged2(self):
                global InvertXLive2
                InvertXLive2 = self.InvertXAxisLive2.isChecked()
                self.myFig2.InvertX(InvertXLive2)

        def InvertYChanged2(self):
                global InvertYLive2
                InvertYLive2 = self.InvertYAxisLive2.isChecked()
                self.myFig2.InvertY(InvertYLive2)

        def closeEvent(self, event):
                pass

        def CalcNewValues1(self, Lumi):
                self.zNew = Lumi
                self.t = Lumi
                self.myFig1.CalcNewLine1(self.zNew)
                self.myFig3.CalcNewLine1(self.t)

        def NewMaxMin(self, plotnum, max, min):
                max = max + 2
                if min > 2:
                        min = min - 2
                else:
                        min = 0
                if plotnum == 0:
                        #print("Max 0")
                        self.myFig1.RangeChange(max, min)
                        self.myFig3.RangeChange(max, min)
                        self.RangeLower1.setValue(min)
                        self.RangeUpper1.setValue(max)
                        #WorkMax
                elif plotnum == 1:
                        #print("Max 1")
                        self.myFig2.RangeChange(max, min)
                        self.myFig4.RangeChange(max, min)
                        self.RangeLower2.setValue(min)
                        self.RangeUpper2.setValue(max)

        def CalcNewValues2(self, Scat):
                self.zNew2 = Scat
                self.tt = Scat
                self.myFig2.CalcNewLine1(self.zNew2)
                self.myFig4.CalcNewLine1(self.tt)

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

#Rectangle Selecter
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
                self.lasso = LassoSelector(ax, onselect=self.onselect, button = 1)
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
                #print("pos")
                #print(pos)
                X = int(pos.xdata)
                Y = int(pos.ydata)
                Z = int(round(ValueSource[X][Y],0))
                self.progress_valuesPoint.emit(X,Y,Z)

        def onselect(self, verts):
                global zNew
                global zNew2
                if self.ID == 1:
                        ValueSource = zNew
                else:
                        ValueSource = zNew2
                path = Path(verts)
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
                                        pass
                                elif X == XOld and (Y != YOld-1 or Y != YOld+1):
                                        YNew = YOld
                                        while YNew > Y:
                                                YNew -= 1
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
                                                value = ValueSource[X][YNew]
                                                self.data = {
                                                        "Counter":counter,
                                                        "X":X,
                                                        "Y":YNew,
                                                        "value":value}
                                                self.dataStorage.append(self.data)
                                                counter += 1
                                elif Y == YOld and (X != XOld-1 or X != XOld+1):
                                        XNew = XOld
                                        while XNew > X:
                                                XNew -= 1
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
                                                value = ValueSource[XNew][Y]
                                                self.data = {
                                                        "Counter":counter,
                                                        "X":XNew,
                                                        "Y":Y,
                                                        "value":value}
                                                self.dataStorage.append(self.data)
                                                counter += 1
                                elif (Y != YOld-1 or Y != YOld+1) and (X != XOld-1 or X != XOld+1):
                                        XNew = XOld
                                        YNew = YOld
                                        if X < XOld and Y < YOld:
                                                while XNew > X:
                                                        XNew -= 1
                                                        if YNew > Y:
                                                                YNew -= 1
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
                                                                value = ValueSource[XNew][YNew]
                                                                self.data = {
                                                                        "Counter":counter,
                                                                        "X":XNew,
                                                                        "Y":YNew,
                                                                        "value":value}
                                                                self.dataStorage.append(self.data)
                                                                counter += 1
                                else:
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
                        i = 0
                        while i < len(self.dataStorage):
                                i += 1
                        if len(self.dataStorage) != 1:
                                self.progress_values.emit(self.dataStorage)

        def disconnect(self):
                self.lasso.disconnect_events()
                self.fc[:, -1] = 1
                self.collection.set_facecolors(self.fc)
                self.canvas.draw_idle()

#Meshplot Luminescence ---------------------------------------------
class LumiMeshplot(FigureCanvas, animation.FuncAnimation):
        progress_valueLumi = pyqtSignal(int, int, int, int)
        progress_valuePosition = pyqtSignal(int, int)

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

                self.y, self.x = np.meshgrid(np.linspace(self.ystart,self.ystop,(self.ystop-self.ystart+1)), np.linspace(self.xstart,self.xstop,(self.xstop-self.xstart+1)))

                # The window
                self.cmap = self.HydraCMAP2
                self.fig, self.ax  = plt.subplots() 
                self.quad1 = self.ax.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax.set_xlabel('X [Bits]')
                self.ax.set_ylabel('Y [Bits]')
                self.ax.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                if self.InvertXLive == True:
                        self.ax.invert_xaxis()
                if self.InvertYLive == True:
                        self.ax.invert_yaxis()
                self.ax.set_aspect('equal')

                #self.cb1 = self.fig.colorbar(self.quad1,ax=self.ax)
                #self.cb1.set_label(self.Axistext)

                #FigureCanvas.__init__(self, self.fig)

                self.iteration = 0
                self.runner = 0

                #Start
                FigureCanvas.__init__(self, self.fig)
                self.im = animation.FuncAnimation(fig=self.fig, func=self.animateNewTest, frames=64, interval=64, repeat_delay=0, blit=True, cache_frame_data=False)

                self.pause()
                return

        def pause(self):
                global AnimationPlot1
                AnimationPlot1 = False
                self.im.event_source.stop()
                #print("pause1")
                return
        
        def resume(self):
                global AnimationPlot1
                AnimationPlot1 = True
                self.im.event_source.start()
                #print("resume1")
                return

        def animateNew(self, i):
                global AnimationPlot1
                if AnimationPlot1 == False:
                        self.pause()
                #print("Plot1: " + str(i))
                self.quad1 = self.ax.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                return self.quad1, 

        def animateNewTest(self, i):
                global AnimationPlot1
                if AnimationPlot1 == False:
                        self.pause()

                if (self.runner % 16) == 0:
                        self.ax.clear()

                self.quad1 = self.ax.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)

                if (self.runner % 16) == 0:
                        self.ax.set_xlabel('X [Bits]')
                        self.ax.set_ylabel('Y [Bits]')
                        self.ax.set_facecolor(((53/255),(53/255),(53/255)))
                        self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                        if self.InvertXLive == True:
                                self.ax.invert_xaxis()
                        if self.InvertYLive == True:
                                self.ax.invert_yaxis()
                        self.ax.set_aspect('equal')

                self.runner += 1

                return self.quad1, 


        """
        def animateNew(self, i):
                print(i)
                lim = 300
                j = 0
                while j <= 255:
                        if i > 25 and i < 35:
                                if j > 25 and j < 35:
                                        self.zNew[j][i] = random.randint(200,300)
                                        self.vmaximum = 300
                                else:
                                        self.zNew[j][i] = random.randint(50,200)
                        else:
                                self.zNew[j][i] = random.randint(50,200)
                        j += 1
                self.quad1 = self.ax.pcolormesh(self.x,self.y,self.zNew,cmap=self.cmap, vmin=self.lowerLimit, vmax=lim)
                return self.quad1, 
        """

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
                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
                self.progress_valueLumi.emit(int(round(x1,0)), int(round(y1,0)), int(round(x2,0)), int(round(y2,0)))

        def toggle_selector(self, event):
                #print(' Key pressed.')
                if event.key in ['Q', 'q'] and self.RS.active:
                        self.RS.set_active(False)
                if event.key in ['A', 'a'] and not self.RS.active:
                        self.RS.set_active(True)

        def on_press(self, event):
                self.XStart = event.xdata
                self.YStart = event.ydata

        def on_release(self, event):
                self.X = event.xdata
                self.Y = event.ydata
                self.progress_valuePosition.emit(self.X, self.Y)

        def HideRectangle(self):
                #print("Hide RS1")
                #self.RS1.set_visible(False)
                #self.RS1.update()
                pass

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
                self.fig.canvas.draw()
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
                self.fig.canvas.draw()

        def UpdateFilename(self, Date):
                global FilePath
                global FileName
                self.Filename = FilePath + FileName + "_" + Date + ".png"

        def InvertX(self, InvertXLive1):
                self.InvertXLive = InvertXLive1
                self.ax.invert_xaxis()
                self.fig.canvas.draw()
                self.resume()
                self.pause()

        def InvertY(self, InvertYLive1):
                self.InvertYLive = InvertYLive1
                self.ax.invert_yaxis()
                self.fig.canvas.draw()
                self.resume()
                self.pause()

        def RangeChange(self, up, down):
                #print("Lumi Range" + str(down) + " x " + str(up))
                self.upperLimit = up
                self.lowerLimit = down

        #Work
        def RangeChangeAnimate(self, up, down):
                #print("Range")
                self.upperLimit = up
                self.lowerLimit = down
                self.quad1.set_clim(self.lowerLimit, self.upperLimit)
                self.fig.canvas.draw()

        def ChannelChanged(self, Axistext, Headline):
                #print(Axistext + "\t" + Headline)
                self.Axistext = Axistext
                self.Headline = Headline

        def CalcNewLine(self,AutoScale):
                self.AutoScale = AutoScale

        def CalcNewLine1(self,a):
                self.zNew = a
                i = 0
                self.animateNew(i)

#Meshplot Scattering ------------------------------------------------------------------
class ScatMeshplot(FigureCanvas):
        progress_valueScat = pyqtSignal(int, int, int, int)
        progress_valuePosition = pyqtSignal(int, int)
        
        def __init__(self):
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
                
                self.runner = 0

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
                self.cmap = self.HydraCMAP2
                self.fig, self.ax  = plt.subplots() 
                self.quad2 = self.ax.pcolormesh(self.x, self.y, self.zNew2, cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                self.ax.set_xlabel('X [Bits]')
                self.ax.set_ylabel('Y [Bits]')
                self.ax.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                if self.InvertXLive == True:
                        self.ax.invert_xaxis()
                if self.InvertYLive == True:
                        self.ax.invert_yaxis()
                self.ax.set_aspect('equal')
                #self.cb2 = self.fig.colorbar(self.quad2,ax=self.ax)
                #self.cb2.set_label(self.Axistext)
                #FigureCanvas.__init__(self, self.fig)
                #self.iteration = 0

                #Start
                FigureCanvas.__init__(self, self.fig)
                self.im = animation.FuncAnimation(fig=self.fig, func=self.animateNewTest, frames=64, interval=64, repeat_delay=0, blit=True, cache_frame_data=False)
                self.pause()
                return

        def pause(self):
                global AnimationPlot2
                AnimationPlot2 = False
                self.im.event_source.stop()
                #print("pause2")
                return
        
        def resume(self):
                global AnimationPlot2
                AnimationPlot2 = True
                self.im.event_source.start()
                #print("resume2")
                return

        def animateNew(self, i):
                global AnimationPlot2
                if AnimationPlot2 == False:
                        self.pause()
                #print("Plot2: " + str(i))
                self.quad2 = self.ax.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)
                return self.quad2, 

        def animateNewTest(self, i):
                global AnimationPlot2
                if AnimationPlot2 == False:
                        self.pause()

                if (self.runner % 16) == 0:
                        self.ax.clear()

                self.quad2 = self.ax.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=self.upperLimit)

                if (self.runner % 16) == 0:
                        self.ax.set_xlabel('X [Bits]')
                        self.ax.set_ylabel('Y [Bits]')
                        self.ax.set_facecolor(((53/255),(53/255),(53/255)))
                        self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                        if self.InvertXLive == True:
                                self.ax.invert_xaxis()
                        if self.InvertYLive == True:
                                self.ax.invert_yaxis()
                        self.ax.set_aspect('equal')

                self.runner += 1

                return self.quad2, 
        """
        def animateNew(self, i):
                print(i)
                lim = 300
                j = 0
                while j <= 255:
                        if i > 25 and i < 35:
                                if j > 25 and j < 35:
                                        self.zNew2[j][i] = random.randint(200,300)
                                        self.vmaximum = 300
                                else:
                                        self.zNew2[j][i] = random.randint(50,200)
                        else:
                                self.zNew2[j][i] = random.randint(50,200)
                        j += 1
                self.quad2 = self.ax.pcolormesh(self.x,self.y,self.zNew2,cmap=self.cmap, vmin=self.lowerLimit, vmax=lim)
                return self.quad2, 
        """

        def line_select_callback(self, eclick, erelease):
                x1, y1 = eclick.xdata, eclick.ydata
                x2, y2 = erelease.xdata, erelease.ydata
                self.progress_valueScat.emit(int(round(x1,0)), int(round(y1,0)), int(round(x2,0)), int(round(y2,0)))

        def toggle_selector(self, event):
                if event.key in ['Q', 'q'] and self.RS1.active:
                        self.RS1.set_active(False)
                if event.key in ['A', 'a'] and not self.RS1.active:
                        self.RS1.set_active(True)

        def on_press(self, event):
                self.RS1.set_visible(True)
                self.XStart = event.xdata
                self.YStart = event.ydata

        def on_release(self, event):
                self.XStop = event.xdata
                self.YStop = event.ydata
                if self.XStart == self.XStop and self.YStart == self.YStop:
                        self.progress_valuePosition.emit(self.XStart, self.YStart)

        def HideRectangle(self):
                #print("Hide RS1")
                #self.RS1.set_visible(False)
                #self.RS1.update()
                pass

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
                self.fig.canvas.draw()
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
                self.fig.canvas.draw()

        def UpdateFilename(self, Date):
                global FilePath
                global FileName

                self.Filename = FilePath + FileName + "_" + Date + ".png"

        def ChannelChanged(self, Axistext, Headline):
                self.Axistext = Axistext
                self.Headline = Headline

        def InvertX(self, InvertXLive2):
                self.InvertXLive = InvertXLive2
                self.ax.invert_xaxis()
                self.fig.canvas.draw()
                self.resume()
                self.pause()

        def InvertY(self, InvertYLive2):
                self.InvertYLive = InvertYLive2
                self.ax.invert_yaxis()
                self.fig.canvas.draw()
                self.resume()
                self.pause()        

        def RangeChange(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down

        def RangeChangeAnimate(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down
                self.quad2.set_clim(self.lowerLimit, self.upperLimit)
                self.fig.canvas.draw()

        def CalcNewLine(self,b):
                i = 0
                self.b = b
                while i <= self.xstop:
                        self.bNew = self.b
                        self.zNew2[i][self.iteration] = self.bNew
                        i += 1
                self.iteration += 1
                self.animate()

        def CalcNewLine1(self,b):
                self.zNew2 = b
                i = 0
                self.animateNew(i)

#Lineplot Luminescence ------------------------------------------------------------------
class LumiLineplot(FigureCanvas):
        progress_valuePosition = pyqtSignal(int, int)
        def __init__(self):
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
                self.ax3.grid(True)
                FigureCanvas.__init__(self, self.fig)
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
                self.line1 = self.ax3.plot(x,y,color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax3.set_xlim(0,xHigh)
                if yLow <= 0:
                        self.ax3.set_ylim((yLow),(yHigh+int(round(yHigh/10,0))))
                elif yLow <= 5:
                        self.ax3.set_ylim((yLow-1),(yHigh+int(round(yHigh/10,0))))
                else:
                        self.ax3.set_ylim((yLow-5),(yHigh+int(round(yHigh/10,0))))
                self.ax3.set_xlabel('X [Bits]')
                self.ax3.set_ylabel(self.Axistext)
                self.ax3.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                self.ax3.grid(True)
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
                self.ax3.grid(True)
                self.fig.canvas.draw()
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        def RangeChange(self, up, down):
                self.upperLimit = up
                self.lowerLimit = down

        def ChannelChanged(self, Axistext, Headline):
                #print(Axistext + "\t" + Headline)
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
                self.t = a
                self.animate()

#Lineplot Scattering
class ScatLineplot(FigureCanvas):
        progress_valuePosition = pyqtSignal(int, int)
        def __init__(self):
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
                cmap = plt.get_cmap('Spectral_r') 
                self.fig, self.ax4  = plt.subplots() 
                self.line2, = self.ax4.plot([],[],color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax4.set_xlim(0,self.xstop-self.xstart)
                self.ax4.set_ylim(self.lowerLimit,self.upperLimit)
                self.ax4.set_xlabel('X [Bits]')
                self.ax4.set_ylabel(self.Axistext)
                self.ax4.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                self.ax4.grid(True)
                FigureCanvas.__init__(self, self.fig)
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
                self.line1 = self.ax4.plot(x,y,color=(0,1,0),linestyle='-',linewidth=2,picker=10)
                self.ax4.set_xlim(0,xHigh)
                if yLow <= 0:
                        self.ax4.set_ylim((yLow),(yHigh+int(round(yHigh/10,0))))
                elif yLow <= 5:
                        self.ax4.set_ylim((yLow-1),(yHigh+int(round(yHigh/10,0))))
                else:
                        self.ax4.set_ylim((yLow-5),(yHigh+int(round(yHigh/10,0))))
                self.ax4.set_xlabel('X [Bits]')
                self.ax4.set_ylabel(self.Axistext)
                self.ax4.set_facecolor(((53/255),(53/255),(53/255)))
                self.fig.patch.set_facecolor(((53/255),(53/255),(53/255)))
                self.ax4.grid(True)
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
                self.ax4.grid(True)
                self.fig.canvas.draw()
                cid = self.fig.canvas.mpl_connect('pick_event', self.on_pick)

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

                self.animate()

        def CalcNewLine1(self,b):
                self.tt = b
                self.animate()

"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 4: APD Window ------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

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
                global Font
                global FontSize
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

                self.WindowPosX = WindowPosX + WindowWidth + 5
                self.WindowPosY = WindowPosY + 600 + 35

                self.setWindowTitle("APD Readings")
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/APD2.png"))
                self.setGeometry(self.WindowPosX,self.WindowPosY,300,265)

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
                self.IntTime.setMaximum(200)  
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
                        pixmap_mini = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
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
                        pixmap_mini = pixmap.scaled(80, 80, Qt.KeepAspectRatio)
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
                #print("Start APDs")
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
                        pixmap_mini = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                elif self.APD1Val == 0 and self.APD2Val == 0:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2.png")
                        pixmap_mini = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                else:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/APD2_red.png")
                        pixmap_mini = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

        def UpdateAPD1(self, val):
                self.APD1Val = (val/self.Integration)
                self.labelAPD1.setText("APD 1:\t" + str(round(self.APD1Val,2)) + " khz\n\t" + str(val) + " counts")
                self.labelAPD1.adjustSize()
                self.UpdateAmpel()

        def UpdateAPD2(self, val):
                self.APD2Val = (val/self.Integration)
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

#APD Reader --------------------------------------------------------------
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

"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 5: Temperature Window ----------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

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
                global Font
                global FontSize
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

                self.WindowPosX = WindowPosX + WindowWidth + 10 + 300
                self.WindowPosY = WindowPosY + 600 + 35

                self.setWindowTitle("Temperature")
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/ShowTemp.png"))
                self.setGeometry(self.WindowPosX,self.WindowPosY,300,265)
                

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
                        pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()

                        #Start Reading
                        self.StartMeasure() 
                else:
                        self.labelValid = QLabel(("No Sensor connected"), self)
                        self.labelValid.move(30, 25)
                        
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/temperature.png")
                        pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
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
                        pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                elif val >= 28:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Temp_high.png")
                        pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                        self.labelTest.setPixmap(pixmap_mini)
                        self.labelTest.show()
                else:
                        pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Temp_normal.png")
                        pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
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

#Temperature Reader ----------------------------------------------------
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 6: Settings Windows ------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

#File Settings Window ------------------------------------------------------
class FileSettings(QWidget):
        progress_save = pyqtSignal(int)

        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight
                global Font
                global FontSize
                global MainPath
                global FilePath
                global FileName
                global FileNamePoint
                global FileNameSub
                global SubPoints
                global Meta
                global LaserWL
                global LaserPower
                global Filter
                global Sample

                self.filepath = MainPath
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50
                
                self.setWindowTitle("File Settings")
                self.setGeometry(self.WindowPosX,self.WindowPosY,420,420)
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Settings.png"))
                
                #File-Widgets setzen                                                                     #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.buttonPath = QPushButton("Filepath", self)
                self.Filename = QLineEdit(self)
                self.FilenameSub = QLineEdit(self)
                self.FilenameSubPoints = QLineEdit(self)
                self.FilenamePoint = QLineEdit(self)
                self.labelPath = QLabel(MainPath, self)
                self.labelFile = QLabel("Filename Measurement", self)
                self.labelFileSub = QLabel("Filename Subgrid", self)
                self.labelFileSubPoints = QLabel("Filename Subgrid-Points", self)
                self.labelFilePoint = QLabel("Filename Point", self)

                self.buttonPath.setToolTip("Set the Filepath")
                self.buttonPath.clicked.connect(self.OpenPath)

                self.Filename.setToolTip("Sets the Filename for the normal Measurement")
                self.Filename.setText(FileName)
                self.FilenameSub.setToolTip("Sets the Filename for the TTL-Sync Measurement")
                self.FilenameSub.setText(FileNameSub)
                self.FilenameSubPoints.setToolTip("Sets the Filename for the TTL-Sync Measurement")
                self.FilenameSubPoints.setText(SubPoints)
                self.FilenamePoint.setToolTip("Sets the Filename for the Pointmeasurement")
                self.FilenamePoint.setText(FileNamePoint)

                #Meta-Widgets setzen
                self.labelMeta = QLabel("The Meta-Data will be writen on the top of the collected Data in the Data File", self)
                self.LaserWL = QLineEdit(self)
                self.LaserWL.setText(LaserWL)
                self.LaserWL.setToolTip("Describe Laser Wavelength you are using in nm")
                self.labelLaserWL = QLabel("Laser Wavelength", self)
                self.LaserPower = QLineEdit(self)
                self.LaserPower.setText(LaserPower)
                self.LaserPower.setToolTip("Describe Laser Power you are using in mW")
                self.labelLaserPower = QLabel("Laser Power", self)
                self.LaserFilter = QLineEdit(self)
                self.LaserFilter.setText(Filter)
                self.LaserFilter.setToolTip("Describe Filters you are using")
                self.labelLaserFilter = QLabel("Filter", self)
                self.Sample = QLineEdit(self)
                self.Sample.setText(Sample)
                self.Sample.setToolTip("Describe the Sample in few words")
                self.labelSample = QLabel("Sample", self)

                #Ende
                self.end = QPushButton("Save + Quit", self)                                                                                             #setzt einen Ende-Button
                self.end.setToolTip("Save the Changes and Quit the Window")
                self.end.clicked.connect(self.SaveAndClose)

                #Layout
                self.layoutV1 = QVBoxLayout(self)

                self.groupboxFileSet = QGroupBox("Filesettings", self)
                self.layoutGBF1 = QHBoxLayout(self)
                self.layoutGBF1.addWidget(self.Filename)
                self.layoutGBF1.addWidget(self.labelFile)
                self.layoutGBF2 = QHBoxLayout(self)
                self.layoutGBF2.addWidget(self.FilenameSub)
                self.layoutGBF2.addWidget(self.labelFileSub)
                self.layoutGBF3 = QHBoxLayout(self)
                self.layoutGBF3.addWidget(self.FilenameSubPoints)
                self.layoutGBF3.addWidget(self.labelFileSubPoints)
                self.layoutGBF4 = QHBoxLayout(self)
                self.layoutGBF4.addWidget(self.FilenamePoint)
                self.layoutGBF4.addWidget(self.labelFilePoint)
                self.layoutGBF5 = QHBoxLayout(self)
                self.layoutGBF5.addWidget(self.buttonPath)
                self.layoutGBF5.addWidget(self.labelPath)
                self.layoutGBF6 = QVBoxLayout(self)
                self.layoutGBF6.addLayout(self.layoutGBF1)
                self.layoutGBF6.addLayout(self.layoutGBF2)
                self.layoutGBF6.addLayout(self.layoutGBF3)
                self.layoutGBF6.addLayout(self.layoutGBF4)
                self.layoutGBF6.addLayout(self.layoutGBF5)
                self.groupboxFileSet.setLayout(self.layoutGBF6)

                self.groupboxMeta = QGroupBox("Meta Data", self)
                self.groupboxMeta.setCheckable(True)
                if Meta == 0:
                        self.groupboxMeta.setChecked(False)
                else:
                        self.groupboxMeta.setChecked(True)
                self.layoutGBM1 = QHBoxLayout(self)
                self.layoutGBM1.addWidget(self.LaserWL)
                self.layoutGBM1.addWidget(self.labelLaserWL)
                self.layoutGBM2 = QHBoxLayout(self)
                self.layoutGBM2.addWidget(self.LaserPower)
                self.layoutGBM2.addWidget(self.labelLaserPower)
                self.layoutGBM3 = QHBoxLayout(self)
                self.layoutGBM3.addWidget(self.LaserFilter)
                self.layoutGBM3.addWidget(self.labelLaserFilter)
                self.layoutGBM4 = QHBoxLayout(self)
                self.layoutGBM4.addWidget(self.Sample)
                self.layoutGBM4.addWidget(self.labelSample)
                self.layoutGBM5 = QVBoxLayout(self)
                self.layoutGBM5.addWidget(self.labelMeta)
                self.layoutGBM5.addLayout(self.layoutGBM1)
                self.layoutGBM5.addLayout(self.layoutGBM2)
                self.layoutGBM5.addLayout(self.layoutGBM3)
                self.layoutGBM5.addLayout(self.layoutGBM4)
                self.groupboxMeta.setLayout(self.layoutGBM5)

                self.layoutEnd = QHBoxLayout(self)
                self.layoutEnd.addStretch(1)
                self.layoutEnd.addWidget(self.end)

                self.layoutV1.addWidget(self.groupboxFileSet)
                self.layoutV1.addWidget(self.groupboxMeta)
                self.layoutV1.addStretch(1)
                self.layoutV1.addLayout(self.layoutEnd)

                self.setLayout(self.layoutV1)

        def usesettings(self):
                global FilePath
                global FileName
                global FileNameSub
                global SubPoints
                global FileNamePoint
                global MainPath
                global Meta
                global LaserWL
                global LaserPower
                global Filter
                global Sample

                FileSet.execute("SELECT * FROM settingsFile WHERE ID = 1")
                for dsatzFile in FileSet:
                        filename = dsatzFile[1]
                        filepoint = dsatzFile[2]
                        filesub = dsatzFile[3]
                        subpoints = dsatzFile[4]
                        filepath = dsatzFile[5]
                        mainpath = dsatzFile[6]
                        meta = dsatzFile[7]
                        wl = dsatzFile[8]
                        power = dsatzFile[9]
                        filter = dsatzFile[10]
                        sample = dsatzFile[11]
                        
                FilePath = filepath
                FileName = filename
                FileNameSub = filesub
                SubPoints = subpoints
                FileNamePoint = filepoint
                MainPath = mainpath
                Meta = meta
                LaserWL = wl
                LaserPower = power
                Filter = filter
                Sample = sample

                self.FilenameSub.setText(FileNameSub)
                self.FilenameSubPoints.setText(SubPoints)
                self.FilenamePoint.setText(FileNamePoint)
                self.Filename.setText(FileName)
                self.labelPath.setText(MainPath)

                if Meta == 1:
                        self.groupboxMeta.setChecked(True)
                else:
                        self.groupboxMeta.setChecked(False)
                self.LaserWL.setText(LaserWL)
                self.LaserPower.setText(LaserPower)
                self.LaserFilter.setText(Filter)
                self.Sample.setText(Sample)

                connFile.commit()

        def closeEvent(self, event):
                connFile.commit()

        def SaveAndClose(self):
                global FilePath
                global FileName
                global FileNameSub
                global SubPoints
                global FileNamePoint
                global MainPath
                global Meta
                global LaserWL
                global LaserPower
                global Filter
                global Sample

                FileName = self.Filename.text()
                FileNameSub = self.FilenameSub.text()
                SubPoints = self.FilenameSubPoints.text()
                FileNamePoint = self.FilenamePoint.text()
                MainPath = self.filepath
                FilePath = MainPath + "/"

                if self.groupboxMeta.isChecked():
                        Meta = 1
                else:
                        Meta = 0
                LaserWL = self.LaserWL.text()
                LaserPower = self.LaserPower.text()
                Filter = self.LaserFilter.text()
                Sample = self.Sample.text()
                
                FileSet.execute("UPDATE settingsFile SET filename=?, filepoint=?, filesub=?, subpoints=?, filepath=?, mainpath=?, meta=?, laserWL=?, laserPower=?, filter=?, sample=? WHERE ID=?", (FileName, FileNamePoint, FileNameSub, SubPoints, FilePath, MainPath, Meta, LaserWL, LaserPower, Filter, Sample, 1))
                FileSet.execute("SELECT * FROM settingsFile")
                connFile.commit()
                self.progress_save.emit(1)
                self.close()

        def OpenPath(self):
                global MainPath
                self.filepath = str(QFileDialog.getExistingDirectory(self, "Open Path", MainPath))
                self.labelPath.setText(self.filepath)

#TTL Settings Window ------------------------------------------------------
class TTLSettings(QWidget):
        progress_save = pyqtSignal(int)
        
        def __init__(self):
                super().__init__()
                self.initMe()

        def initMe(self):
                global TTLOUT1
                global TTLOUT2
                global TTLOUT3
                global TTLOUT4
                global TTLOUT5
                global TTLOUT6
                global TTLOUT7
                global TTLOUT8
                global TTLOUT_Wires
                global ShutterMode
                global WindowPosX
                global WindowPosY
                global WindowWidth
                global WindowHeight
                global Font
                global FontSize

                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

                self.WindowPosX = WindowPosX + 50
                self.WindowPosY = WindowPosY + 50

                self.setWindowTitle("TTL Settings")
                self.setGeometry(self.WindowPosX,self.WindowPosY,620,500)
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/Settings.png"))

                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.NameTTL1 = QLineEdit(self)
                self.NameTTL2 = QLineEdit(self)                                                                                                           #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.NameTTL3 = QLineEdit(self)
                self.NameTTL4 = QLineEdit(self)                                                                                                           #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.NameTTL5 = QLineEdit(self)
                self.NameTTL6 = QLineEdit(self)                                                                                                           #Es ist wichtig die Widgets am Anfang zu definieren, da sonst später aufruffehler auftretten können
                self.NameTTL7 = QLineEdit(self)
                self.NameTTL8 = QLineEdit(self)
                self.NameTTL1.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL2.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL3.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL4.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL5.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL6.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL7.setToolTip("Choose a Name for the TTL connection")
                self.NameTTL8.setToolTip("Choose a Name for the TTL connection")
                self.buttonTestTTL1 = QPushButton("Test TTL 1", self)
                self.buttonTestTTL2 = QPushButton("Test TTL 2", self)
                self.buttonTestTTL3 = QPushButton("Test TTL 3", self)
                self.buttonTestTTL4 = QPushButton("Test TTL 4", self)
                self.buttonTestTTL5 = QPushButton("Test TTL 5", self)
                self.buttonTestTTL6 = QPushButton("Test TTL 6", self)
                self.buttonTestTTL7 = QPushButton("Test TTL 7", self)
                self.buttonTestTTL8 = QPushButton("Test TTL 8", self)
                self.buttonTestTTL1.setObjectName('Button 1')
                self.buttonTestTTL2.setObjectName('Button 2')
                self.buttonTestTTL3.setObjectName('Button 3')
                self.buttonTestTTL4.setObjectName('Button 4')
                self.buttonTestTTL5.setObjectName('Button 5')
                self.buttonTestTTL6.setObjectName('Button 6')
                self.buttonTestTTL7.setObjectName('Button 7')
                self.buttonTestTTL8.setObjectName('Button 8')
                self.labelTTL1 = QLabel("Name TTL1:", self)
                self.labelTTL2 = QLabel("Name TTL2:", self)
                self.labelTTL3 = QLabel("Name TTL3:", self)
                self.labelTTL4 = QLabel("Name TTL4:", self)
                self.labelTTL5 = QLabel("Name TTL5:", self)
                self.labelTTL6 = QLabel("Name TTL6:", self)
                self.labelTTL7 = QLabel("Name TTL7:", self)
                self.labelTTL8 = QLabel("Name TTL8:", self)
                self.TTL3Polarity = QCheckBox("Invert Polarity", self)
                self.TTL4Polarity = QCheckBox("Invert Polarity", self)
                self.TTL5Polarity = QCheckBox("Invert Polarity", self)
                self.TTL6Polarity = QCheckBox("Invert Polarity", self)
                self.TTL3Wire = QCheckBox("1-Wire", self)                                                                             #Setzt eine CheckBox
                self.TTL3Wire.setToolTip("Sets the TTL to 1-Wire Communication, the TTL3-BNC will work as In- and Output")
                self.TTL4Wire = QCheckBox("1-Wire", self)                                                                             #Setzt eine CheckBox
                self.TTL4Wire.setToolTip("Sets the TTL to 1-Wire Communication, the TTL4-BNC will work as In- and Output")
                self.TTL5Wire = QCheckBox("1-Wire", self)                                                                             #Setzt eine CheckBox
                self.TTL5Wire.setToolTip("Sets the TTL to 1-Wire Communication, the TTL5-BNC will work as In- and Output")
                self.TTL6Wire = QCheckBox("1-Wire", self)                                                                             #Setzt eine CheckBox
                self.TTL6Wire.setToolTip("Sets the TTL to 1-Wire Communication, the TTL6-BNC will work as In- and Output")
                self.buttonTestTTL1.setToolTip("Send a TTL Signal")
                self.buttonTestTTL1.clicked.connect(self.TestTTL)
                self.buttonTestTTL2.setToolTip("Send a TTL Signal")
                self.buttonTestTTL2.clicked.connect(self.TestTTL)
                self.buttonTestTTL3.setToolTip("Send a TTL Signal")
                self.buttonTestTTL3.clicked.connect(self.TestTTL)
                self.buttonTestTTL4.setToolTip("Send a TTL Signal")
                self.buttonTestTTL4.clicked.connect(self.TestTTL)
                self.buttonTestTTL5.setToolTip("Send a TTL Signal")
                self.buttonTestTTL5.clicked.connect(self.TestTTL)
                self.buttonTestTTL6.setToolTip("Send a TTL Signal")
                self.buttonTestTTL6.clicked.connect(self.TestTTL)
                self.buttonTestTTL7.setToolTip("Send a TTL Signal")
                self.buttonTestTTL7.clicked.connect(self.TestTTL)
                self.buttonTestTTL8.setToolTip("Send a TTL Signal")
                self.buttonTestTTL8.clicked.connect(self.TestTTL)
                
                self.Shutter1 = QComboBox(self)
                self.Shutter1.addItem("Stay activated")
                self.Shutter1.addItem("Pulse at Start and Stop")
                self.Shutter1.addItem("Stay activated while Line")
                self.Shutter1.addItem("Pulse at Linestart and Linestop")
                self.Shutter1.setCurrentIndex(ShutterMode[0])
                self.Shutter1.setToolTip("Choose a Shutter Mode for the normal Measurements")

                self.Shutter1TTLSync = QComboBox(self)
                self.Shutter1TTLSync.addItem("Same as normal Measurement")
                self.Shutter1TTLSync.addItem("Activated at every Position")
                self.Shutter1TTLSync.addItem("Pulse at every Position")
                self.Shutter1TTLSync.setCurrentIndex(ShutterMode[2])
                self.Shutter1TTLSync.setToolTip("Choose a Shutter Mode for the TTLSyncing Mode")
                self.labelShutter1TTLSync = QLabel("TTLSync Mode:", self)

                self.Shutter2 = QComboBox(self)
                self.Shutter2.addItem("Stay activated")
                self.Shutter2.addItem("Pulse at Start and Stop")
                self.Shutter2.addItem("Stay activated while Line")
                self.Shutter2.addItem("Pulse at Linestart and Linestop")
                self.Shutter2.addItem("Detector Security Shutter")
                self.Shutter2.setCurrentIndex(ShutterMode[1])

                self.Shutter2TTLSync = QComboBox(self)
                self.Shutter2TTLSync.addItem("Same as normal Measurement")
                self.Shutter2TTLSync.addItem("Activated at every Position")
                self.Shutter2TTLSync.addItem("Pulse at every Position")
                self.Shutter2TTLSync.setCurrentIndex(ShutterMode[3])
                self.labelShutter2TTLSync = QLabel("TTLSync Mode:", self)

                self.Shutter2Threashold = QSpinBox(self)
                self.Shutter2Threashold.setMinimum(0)
                self.Shutter2Threashold.setMaximum(10000000)                                                                                           #Setzt ein Maximum für die Auswahl
                self.Shutter2Threashold.setValue(35000)                      
                self.Shutter2Threashold.setToolTip("Sets Threashold for Detector Security Shutter. Shutter activates, if Detector readings excede the Threashold.") 

                if self.Shutter2.currentIndex() != 4:
                        self.Shutter2TTLSync.setVisible(True)
                        self.labelShutter2TTLSync.setText("TTLSync Mode:")
                        self.Shutter2Threashold.setVisible(False)
                else:
                        self.Shutter2TTLSync.setVisible(False)
                        self.labelShutter2TTLSync.setText("Threashold:")
                        self.Shutter2Threashold.setVisible(True)
                
                self.Shutter2.currentIndexChanged.connect(self.Shutter2Changed)

                self.TTL3Wire.setChecked(TTLOUT_Wires[0])
                self.TTL4Wire.setChecked(TTLOUT_Wires[1])
                self.TTL5Wire.setChecked(TTLOUT_Wires[2])
                self.TTL6Wire.setChecked(TTLOUT_Wires[3])
                self.TTL3Polarity.setChecked(TTLOUT3["Polarity"])
                self.TTL4Polarity.setChecked(TTLOUT4["Polarity"])
                self.TTL5Polarity.setChecked(TTLOUT5["Polarity"])
                self.TTL6Polarity.setChecked(TTLOUT6["Polarity"])

                self.NameTTL1.setText(TTLOUT1["Name"])
                self.NameTTL2.setText(TTLOUT2["Name"]) 
                self.NameTTL3.setText(TTLOUT3["Name"])
                self.NameTTL4.setText(TTLOUT4["Name"]) 
                self.NameTTL5.setText(TTLOUT5["Name"])
                self.NameTTL6.setText(TTLOUT6["Name"]) 
                self.NameTTL7.setText(TTLOUT7["Name"])
                self.NameTTL8.setText(TTLOUT8["Name"]) 

                self.labelTTL1.move(30,32)
                self.labelTTL2.move(30,72)
                self.labelTTL3.move(30,112)
                self.labelTTL4.move(30,152)
                self.labelTTL5.move(30,192)
                self.labelTTL6.move(30,232)
                self.labelTTL7.move(30,272)
                self.labelTTL8.move(30,352)
                self.NameTTL1.move(130,30)
                self.NameTTL2.move(130,70)
                self.NameTTL3.move(130,110)
                self.NameTTL4.move(130,150)
                self.NameTTL5.move(130,190)
                self.NameTTL6.move(130,230)
                self.NameTTL7.move(130,270)
                self.NameTTL8.move(130,350)
                self.buttonTestTTL1.move(280,30)
                self.buttonTestTTL2.move(280,70)
                self.buttonTestTTL3.move(280,110)
                self.buttonTestTTL4.move(280,150)
                self.buttonTestTTL5.move(280,190)
                self.buttonTestTTL6.move(280,230)
                self.buttonTestTTL7.move(280,270)
                self.buttonTestTTL8.move(280,350)
                self.labelShutter1TTLSync.move(282,312)
                self.labelShutter2TTLSync.move(282,392)
                self.TTL3Wire.move(390,112)
                self.TTL4Wire.move(390,152)
                self.TTL5Wire.move(390,192)
                self.TTL6Wire.move(390,232)
                self.TTL3Polarity.move(470,112)
                self.TTL4Polarity.move(470,152)
                self.TTL5Polarity.move(470,192)
                self.TTL6Polarity.move(470,232)
                self.Shutter1.move(390,270)
                self.Shutter1TTLSync.move(390,310)
                self.Shutter2.move(390,350)
                self.Shutter2TTLSync.move(390,390)
                self.Shutter2Threashold.move(390,390)


                #Ende
                self.end = QPushButton("Save + Quit", self)                                                                                             #setzt einen Ende-Button
                self.end.setToolTip("Save the Changes and Quit the Window")                                                                             #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end.move(520,450)
                self.end.clicked.connect(self.SaveAndClose) 
                
        def Shutter2Changed(self):
                if self.Shutter2.currentIndex() != 4:
                        self.Shutter2TTLSync.setVisible(True)
                        self.labelShutter2TTLSync.setText("TTLSync Mode:")
                        self.Shutter2Threashold.setVisible(False)
                else:
                        self.Shutter2TTLSync.setVisible(False)
                        self.labelShutter2TTLSync.setText("Threashold:")
                        self.Shutter2Threashold.setVisible(True)

        def TestTTL(self):
                global TTLOUT1
                global TTLOUT2
                global TTLOUT3
                global TTLOUT4
                global TTLOUT5
                global TTLOUT6
                global TTLOUT7
                global TTLOUT8
                
                clicked = self.sender()
                if clicked.objectName() == "Button 1":
                        TTLOUT = TTLOUT1["Pin"]
                elif clicked.objectName() == "Button 2":
                        TTLOUT = TTLOUT2["Pin"]
                elif clicked.objectName() == "Button 3":
                        TTLOUT = TTLOUT3["Pin"]
                elif clicked.objectName() == "Button 4":
                        TTLOUT = TTLOUT4["Pin"]
                elif clicked.objectName() == "Button 5":
                        TTLOUT = TTLOUT5["Pin"]
                elif clicked.objectName() == "Button 6":
                        TTLOUT = TTLOUT6["Pin"]
                elif clicked.objectName() == "Button 7":
                        TTLOUT = TTLOUT7["Pin"]
                elif clicked.objectName() == "Button 8":
                        TTLOUT = TTLOUT8["Pin"]

                GPIO.output(TTLOUT, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(TTLOUT, GPIO.LOW)


        def EventHandler_rising1(self):
                self.TTL = 1

        def closeEvent(self, event):
                connTTL.commit()

        def SaveAndClose(self):
                global TTLOUT1
                global TTLOUT2
                global TTLOUT3
                global TTLOUT4
                global TTLOUT5
                global TTLOUT6
                global TTLOUT7
                global TTLOUT8
                global TTLOUT_Wires
                global ShutterMode
                global Shutter2Threashold

                TTLOUT1["Name"] = self.NameTTL1.text()
                TTLOUT2["Name"] = self.NameTTL2.text()
                TTLOUT3["Name"] = self.NameTTL3.text()
                TTLOUT4["Name"] = self.NameTTL4.text()
                TTLOUT5["Name"] = self.NameTTL5.text()
                TTLOUT6["Name"] = self.NameTTL6.text()
                TTLOUT7["Name"] = self.NameTTL7.text()
                TTLOUT8["Name"] = self.NameTTL8.text()
                
                if self.TTL3Polarity.isChecked():
                        TTLOUT3["Polarity"] = 1
                else:
                        TTLOUT3["Polarity"] = 0
                if self.TTL4Polarity.isChecked():
                        TTLOUT4["Polarity"] = 1
                else:
                        TTLOUT4["Polarity"] = 0
                if self.TTL5Polarity.isChecked():
                        TTLOUT5["Polarity"] = 1
                else:
                        TTLOUT5["Polarity"] = 0
                if self.TTL6Polarity.isChecked():
                        TTLOUT6["Polarity"] = 1
                else:
                        TTLOUT6["Polarity"] = 0

                TTLOUT_Wires[0] = self.TTL3Wire.isChecked()
                TTLOUT_Wires[1] = self.TTL4Wire.isChecked()
                TTLOUT_Wires[2] = self.TTL5Wire.isChecked()
                TTLOUT_Wires[3] = self.TTL6Wire.isChecked()
                ShutterMode[0] = self.Shutter1.currentIndex()
                ShutterMode[1] = self.Shutter2.currentIndex()
                ShutterMode[2] = self.Shutter1TTLSync.currentIndex()
                ShutterMode[3] = self.Shutter2TTLSync.currentIndex()
                Shutter2Threashold = self.Shutter2Threashold.value()

                TTLSet.execute("UPDATE settingsScanTTL SET name1=?, polarity1=?, mode1=?, initial1=?, name2=?, polarity2=?, mode2=?, initial2=?, name3=?, polarity3=?, mode3=?, initial3=?, name4=?, polarity4=?, mode4=?, initial4=?, name5=?, polarity5=?, mode5=?, initial5=?, name6=?, polarity6=?, mode6=?, initial6=?, name7=?, polarity7=?, mode7=?, initial7=?, name8=?, polarity8=?, mode8=?, initial8=?, wire1=?, wire2=?, wire3=?, wire4=?, Shutter1=?, Shutter2=?, Shutter1TTLSync=?, Shutter2TTLSync=?, Shutter2Threashold=? WHERE ID=?", 
                                (TTLOUT1["Name"], TTLOUT1["Polarity"], TTLOUT1["Mode"], TTLOUT1["Initial"]
                                , TTLOUT2["Name"], TTLOUT2["Polarity"], TTLOUT2["Mode"], TTLOUT2["Initial"]
                                , TTLOUT3["Name"], TTLOUT3["Polarity"], TTLOUT3["Mode"], TTLOUT3["Initial"]
                                , TTLOUT4["Name"], TTLOUT4["Polarity"], TTLOUT4["Mode"], TTLOUT4["Initial"]
                                , TTLOUT5["Name"], TTLOUT5["Polarity"], TTLOUT5["Mode"], TTLOUT5["Initial"]
                                , TTLOUT6["Name"], TTLOUT6["Polarity"], TTLOUT6["Mode"], TTLOUT6["Initial"]
                                , TTLOUT7["Name"], TTLOUT7["Polarity"], TTLOUT7["Mode"], TTLOUT7["Initial"]
                                , TTLOUT8["Name"], TTLOUT8["Polarity"], TTLOUT8["Mode"], TTLOUT8["Initial"]
                                , TTLOUT_Wires[0], TTLOUT_Wires[1], TTLOUT_Wires[2], TTLOUT_Wires[3]
                                , ShutterMode[0], ShutterMode[1], ShutterMode[2], ShutterMode[3], Shutter2Threashold
                                , 1))
                TTLSet.execute("SELECT * FROM settingsScanTTL")
                connTTL.commit()
                self.progress_save.emit(1)
                self.close()

#Device Settings Window ------------------------------------------------------
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
                global Font
                global FontSize
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

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
                self.PiezodistanceX.setValue(PiezoDistanceX)                 

                self.PiezodistanceY.setMinimum(0)                                                                                                      #Setzt ein Minimalwert für die Auswahl
                self.PiezodistanceY.setMaximum(1000000) 
                self.PiezodistanceY.setToolTip("Set the Maximum Y-Range of the Piezotable in Nanometers")
                self.PiezodistanceY.setValue(PiezoDistanceY)
                
                self.PiezodistanceZ.setMinimum(0)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.PiezodistanceZ.setMaximum(1000000) 
                self.PiezodistanceZ.setToolTip("Set the Maximum Z-Range of the Piezotable in Nanometers")
                self.PiezodistanceZ.setValue(PiezoDistanceZ)  

                self.Piezovoltage.setMinimum(0.00)                                                                                                      #Setzt ein Minimalwert für die Auswahl
                self.Piezovoltage.setMaximum(25.00)                                                                                                     #Setzt ein Maximum für die Auswahl
                self.Piezovoltage.setValue(PiezoVoltage)                                                                                                #Setzt einen Startwert
                self.Piezovoltage.setSingleStep(0.01)
                self.Piezovoltage.setDecimals(2)                         
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
                self.end = QPushButton("Save + Quit Application", self)                                                                                             #setzt einen Ende-Button
                self.end.setToolTip("Save the Changes and Quit the Window")                                                                             #Setzt eine Buttonbeschreibung bei MouseOver    
                self.end.move(285,670)
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
                connDev.commit()

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
                connDev.commit()
                self.progress_save.emit(1)
                self.close()

#About Window ------------------------------------------------------
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
                global Font
                global FontSize

                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

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

#Help Window ------------------------------------------------------
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
                global Font
                global FontSize
                
                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))

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

#HydraPopup Window ------------------------------------------------------
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

#HydraClose ------------------------------------------------------
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



"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 7: Main Windows ------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""



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
                global Font
                global FontSize

                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))
                self.setGeometry(WindowPosX, WindowPosY, WindowWidth, WindowHeight)                                                                     #Fensergröße und Position
                self.setMinimumSize(QSize(1000,900))                                                                                                    #Setzt einen Minimalwert für das Fenster, kleiner kann es nicht gezogen werden
                self.setWindowTitle("HydraScan " + str(Version))                                                                                        #Titelbalken
                self.setWindowIcon(QIcon("/home/pi/Desktop/HydraScan/Files/HydraScan_free.png")) 


                self.table_widget = MyTables(self)                                                                              
                self.setCentralWidget(self.table_widget)                                                                                                #Icon oben links

                self.statusBar().showMessage("Property of University Tübingen")                                                                         #Setzt im StatusBar des Fensters den Text

                mainMenu = self.menuBar()
                setMenu = mainMenu.addMenu("Settings")
                helpMenu = mainMenu.addMenu("Help")
                mainMenu.setFont(QFont(self.Fontstyle, self.Fontsize)) 
                setMenu.setFont(QFont(self.Fontstyle, self.Fontsize)) 
                helpMenu.setFont(QFont(self.Fontstyle, self.Fontsize)) 

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

                FileSettings = QAction("File Settings", self)
                FileSettings.setShortcut("Ctrl+P")
                FileSettings.setStatusTip("Define the Files")
                FileSettings.triggered.connect(self.show_pltset)
                setMenu.addAction(FileSettings)

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

                self.show()                                                                                                                             #Die Show funktion zeigt das MainWindow an

        def closeEvent(self, event):
                self.quitall()
                GPIO.cleanup()
                self.Hydra()

        def show_NavWin(self):
                self.table_widget.show_NavWin()

        def show_apd(self):
                global APDWindowOn
                #self.APDWin = APDWindow()
                #self.APDWin.show()
                #APDWindowOn = 1

        def show_temp(self):
                global TempWindowOn
                self.TempSens = TempWindow()
                self.TempSens.show()
                TempWindowOn = 1

        def show_plot(self):
                self.PlotWin = PlotWindow()
                self.PlotWin.show()

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
                except:
                        pass
                try:
                        self.table_widget.close_NavWin()
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
                self.table_widget.PlotWin.UpdateChannelNames()
                self.Hydra()

        def UpdateTabsTTL(self):
                self.table_widget.UpdateTTLNames()

        def show_pltset(self):
                self.pltset = FileSettings()
                self.pltset.progress_save.connect(self.UpdateTabsFile)
                self.pltset.show()

        def UpdateTabsFile(self):
                self.table_widget.UpdateFilePath()

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

        def HYende(self): 
                global StartValX
                global StartValY
                global FocusZ                                                                                                                              #Die Ende-Funktion beendet alle Prozesse
                self.quitall()
                
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
                        connFile.commit()                                                           
                        connFile.close()
                except:
                        connFile.close()
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
                        dacX.set_voltage(0, persist=True)
                        dacY.set_voltage(0, persist=True)
                        dacZ.set_voltage(FocusZ, persist=True)
                        dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
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
                print("Programm beendet")
                sys.exit()                                                                                                                              #Beendet das Fenster

#Table Window ---------------------------------------------------------
class MyTables(QWidget):     
        def __init__(self, parent):
                super(QWidget, self).__init__(parent)

                global APDon
                global DHTon
                global StyleColor
                global StyleName
                global Font
                global FontSize

                self.Fontstyle = Font
                self.Fontsize = FontSize
                self.setFont(QFont(self.Fontstyle, self.Fontsize))
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
                self.XOldPos = 0
                self.YOldPos = 0
                self.PositionX = 0
                self.PositionY = 0
                self.PlotPosX = 0
                self.PlotPosY = 0
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
                #für weiter Tabs hier eine neue Zeile einfügen

                #Tabs zum Widget hinzufügen
                self.tabs.addTab(self.tab1, "Positioning")
                self.tabs.addTab(self.tab2, "Measurement")
                self.tabs.addTab(self.tab3, "TTL Sync")
                self.tabs.addTab(self.tab4, "Z-Stack")
                self.tabs.addTab(self.tab5, "Slope Compensation")
                self.tabs.setCurrentIndex(1)
                #für weiter Tabs hier eine neue Zeile einfügen

                #Darkmode ist essenziell
                if StyleColor == "dark" and StyleName == "windowsvista":
                        self.tabs.setStyleSheet("color: black;"
                                                "background-color: rgb(153,153,153);")

#------------------------ Tab1 -----------------------------
                global CHA
                global CHB
                global L2
                global L3
                global CH1
                global CH2
                global CH3
                global CH4
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
                global PointSpeed
                global MainPath
                global TTLOUT3
                global TTLOUT4
                global TTLOUT5
                global TTLOUT6
                
                #Widgets setzen                                                                                                                         #Es ist wichtig die Widgets am anfang zu definieren, da sonst später aufruffehler auftretten können
                self.buttonPos = QPushButton("Move to", self)                                                                                 #setzt einen Button                                                                             
                self.buttonPoint = QPushButton("Point Measurement", self)
                self.buttonShutter = QPushButton("Open Shutter", self)
                self.PointDelay = QDoubleSpinBox(self)      
                self.PointCount = QSpinBox(self)                                                                                              #setzt eine Spinbox
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
                self.labelPointCount = QLabel("Number of Signals", self)              
                #self.labelSendTTL1 = QLabel("Send TTL Signal\nto Device", self)  
                #self.labelGetTTL1 = QLabel("Wait for TTL\nDevice to answer", self)          
                self.labelStretch1Tab1 = QLabel("", self)
                self.labelStretch2Tab1 = QLabel("", self) 
                self.labelIntTime1 = QLabel("Integration [ms]", self)
                self.spinIntTime1 = QSpinBox(self) 

                #PosFromLine
                self.AnzahlPositionen = 0
                self.NummerPositionen = 0
                self.LinePositions = [[10,10],[20,20],[30,30],[40,40],[50,50]]
                self.labelPositions = QLabel("Position " + str(self.NummerPositionen) + "/" + str(self.AnzahlPositionen), self)
                self.buttonLine = QPushButton("Next Position", self)
                self.buttonPrevious = QPushButton("Previous Position", self)
                self.buttonRemove = QPushButton("Remove Marker", self)
                self.labelLineDivs = QLabel("Linedivider", self)
                self.LineDivs = QSpinBox(self)
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
                self.buttonPos.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonPos.clicked[bool].connect(self.clickedPos)                                                                                   #ruft die clickedPos-Funktion auf, wenn der Button betätigt wird und gibt einen true Wert an die Funktion, wenn der Button unten bleibt und einen false Wert, wenn er wieder oben ist
                self.buttonPos.setFixedSize(160, 25)
                
                self.buttonPoint.setCheckable(True)
                self.buttonPoint.setToolTip("Start the Measurement at the Point")
                self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonPoint.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonPoint.clicked[bool].connect(self.clickedPoint)               
                self.buttonPoint.setFixedSize(160, 25)

                self.buttonLine.setCheckable(False)
                self.buttonLine.setToolTip("Move to next Position")
                self.buttonLine.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonLine.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonLine.clicked[bool].connect(self.NextLine)               
                self.buttonLine.setFixedSize(130, 25)
                
                self.buttonPrevious.setCheckable(False)
                self.buttonPrevious.setToolTip("Move to previous Position")
                self.buttonPrevious.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonPrevious.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonPrevious.clicked[bool].connect(self.PrevLine)               
                self.buttonPrevious.setFixedSize(130, 25)

                self.buttonRemove.setCheckable(False)
                self.buttonRemove.setToolTip("Remove all Markers from Plot")
                self.buttonRemove.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonRemove.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonRemove.clicked[bool].connect(self.RemoveMarker)              
                self.buttonRemove.setFixedSize(130, 25)

                self.buttonShutter.setCheckable(True)
                self.buttonShutter.setToolTip("Open the selected Shutter")
                self.buttonShutter.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                self.buttonShutter.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                self.buttonShutter.clicked[bool].connect(self.ShutterAction)              
                self.buttonShutter.setFixedSize(160, 25)

                #ComboBox definieren
                #self.TTLroot.setFixedSize(130, 25)
                self.TTLroot.addItem(TTLOUT3["Name"])
                self.TTLroot.addItem(TTLOUT4["Name"])
                self.TTLroot.addItem(TTLOUT5["Name"])
                self.TTLroot.addItem(TTLOUT6["Name"])

                #Shutter
                self.ShutterRoot1 = QComboBox(self)
                self.ShutterRoot1.addItem(TTLOUT7["Name"])
                self.ShutterRoot1.addItem(TTLOUT8["Name"])
                self.ShutterRoot1.addItem("Both Shutters")
                self.ShutterRoot1.addItem("None")
                

                #Slider definieren
                self.slideX.setMinimum(0)                                                                                                               #Setzt ein Minimalwert für die Auswahl
                self.slideX.setMaximum(4095)                                                                                                             #Setzt ein Maximum für die Auswahl
                self.slideX.setValue(0)                                                                                                                 #Setzt einen Startwert
                self.slideX.setTickPosition(QSlider.TicksBelow)                                                                                         #Setzt Rastpunkte unter dem Slider
                self.slideX.setTickInterval(4096)                                                                                                        #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideX.sliderReleased.connect(self.positionX)                                                                                        #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideX.setToolTip("Sets the X-Position")                                                                                           #Setzt eine Buttonbeschreibung bei MouseOver

                self.slideY.setMinimum(0)                                                                                                               #Setzt ein Minimalwert für die Auswahl
                self.slideY.setMaximum(4095)                                                                                                             #Setzt ein Maximum für die Auswahl
                self.slideY.setValue(0)                                                                                                                 #Setzt einen Startwert
                self.slideY.setTickPosition(QSlider.TicksBelow)                                                                                         #Setzt Rastpunkte unter dem Slider
                self.slideY.setTickInterval(4096)                                                                                                        #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                self.slideY.sliderReleased.connect(self.positionY)                                                                                        #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.slideY.setToolTip("Sets the Y-Position")                                                                                           #Setzt eine Buttonbeschreibung bei MouseOver

                #Spinbox definieren
                self.LineDivs.setMinimum(2)
                self.LineDivs.setMaximum(100)                                                                                           #Setzt ein Maximum für die Auswahl
                self.LineDivs.setValue(2)                                                                                                                 #Setzt einen Startwert
                self.LineDivs.valueChanged.connect(self.LineDivsPos)
                self.LineDivs.setToolTip("Sets number of Positions in a Line") 

                self.spinX.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.spinX.setMaximum(FullRangeDeviceX/1000)                                                                                            #Setzt ein Maximum für die Auswahl
                self.spinX.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.spinX.editingFinished.connect(self.spinboxX)                                                                                          #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinX.setSingleStep(round((FullRangeDeviceX/1000)/4096,3))
                self.spinX.setDecimals(3)
                self.spinX.setToolTip("Sets the X-Position")                                                                                            #Setzt eine Buttonbeschreibung bei MouseOver
                
                self.spinY.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.spinY.setMaximum(FullRangeDeviceY/1000)                                                                                            #Setzt ein Maximum für die Auswahl
                self.spinY.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.spinY.editingFinished.connect(self.spinboxY)                                                                                          #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinY.setSingleStep(round((FullRangeDeviceY/1000)/4096,3))
                self.spinY.setDecimals(3)
                self.spinY.setToolTip("Sets the Y-Position")                                                                                            #Setzt eine Buttonbeschreibung bei MouseOver
                
                self.PointDelay.setMinimum(0.000)                                                                                                       #Setzt ein Minimalwert für die Auswahl
                self.PointDelay.setMaximum(60.000)                                                                                                      #Setzt ein Maximum für die Auswahl
                self.PointDelay.setValue(1.000)                                                                                                         #Setzt einen Startwert
                self.PointDelay.setSingleStep(0.001)
                self.PointDelay.setDecimals(3)
                self.PointDelay.setToolTip("Sets the Measurementtime in Seconds")                                                                       #Setzt eine Buttonbeschreibung bei MouseOver

                self.PointCount.setMinimum(1)
                self.PointCount.setMaximum(10000)
                self.PointCount.setValue(1)
                self.PointCount.setToolTip("Sets the number of TTL Signals sent.") 

                self.spinIntTime1.setMinimum(1)
                self.spinIntTime1.setMaximum(200)
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
                self.cbg1.setExclusive(True)

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
                #self.vboxSendTTL1.addWidget(self.labelSendTTL1)
                self.vboxSendTTL1.addWidget(self.TTLroot)
                self.vboxSendTTL1.addStretch(1)
                self.vboxSendTTL1.addWidget(self.labelPointDelay)
                self.vboxSendTTL1.addWidget(self.PointDelay)
                self.vboxSendTTL1.addWidget(self.labelPointCount)
                self.vboxSendTTL1.addWidget(self.PointCount)
                self.vboxSendTTL1.addStretch(1)
                self.vboxSendTTL1.addWidget(self.TTLgetPoint1)
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

                self.groupboxLine = QGroupBox("Line Measurement", self) 
                self.layoutVLine = QVBoxLayout(self)
                self.layoutVLine.addWidget(self.buttonLine)
                self.layoutVLine.addWidget(self.buttonPrevious)
                self.layoutVLine.addWidget(self.labelPositions)
                self.layoutVLine.addStretch(1)
                self.layoutVLine.addWidget(self.labelLineDivs)
                self.layoutVLine.addWidget(self.LineDivs)
                self.layoutVLine.addWidget(self.buttonRemove)
                self.groupboxLine.setLayout(self.layoutVLine)

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
                self.tab1.layoutV1.addWidget(self.ShutterRoot1)
                self.tab1.layoutV1.addWidget(self.buttonShutter)
                self.tab1.layoutV1.addStretch(3)

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
                self.tab1.layoutGrid.addWidget(self.groupboxLine, 2, 4)
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
                self.delay = QSpinBox(self)                                                                                                   #setzt eine Spinbox
                self.linetime = QSpinBox(self)                                                                                                             #setzt eine Spinbox
                self.labelLinetime = QLabel("Line-Delay [ms]", self)                                                                                                              #setzt eine Spinbox
                self.labelDelay = QLabel("Step-Delay [ms]", self)                                                                                       #setzt ein Label
                self.labelIntTime = QLabel("Integration Time [ms]", self)
                self.spinIntTime2 = QSpinBox(self)
                self.progress1 = QProgressBar(self)
                self.Subgrid1 = QCheckBox("TTL-Sync")
                self.Sympho1 = QCheckBox("SymPhoTime")
                self.Slope1 = QCheckBox("Slope Compensation")
                self.Stack1 = QCheckBox("ZStack")
                self.Plot1 = QCheckBox("Plot Data")

                self.buttonResetZFocus2 = QPushButton("Reset Z", self)
                self.spinZFocus2 = QDoubleSpinBox(self)
                self.labelZFocus2 = QLabel("Z-Position", self)

                self.labelProgTime = QLabel("", self)                                                                                                   #Setzt ein Label 
                self.labelStretch1Tab2 = QLabel("  \n  \n  ", self)
                self.labelStretch2Tab2 = QLabel("", self) 
                self.labelStretch3Tab2 = QLabel("", self) 

                self.labelPath = QLabel(("Filepath: " + str(MainPath)), self)

                #Shutter
                self.ShutterRoot2 = QComboBox(self)
                self.ShutterRoot2.addItem(TTLOUT7["Name"])
                self.ShutterRoot2.addItem(TTLOUT8["Name"])
                self.ShutterRoot2.addItem("Both Shutters")
                self.ShutterRoot2.addItem("None")

                #Save - Settings
                self.nameMeasure = QLineEdit(self)                                                                                                      #Setzt eine Textbox
                self.saveMeasure = QPushButton("Save", self)                                                                                            #Setzt einen Button
                self.namesMeasure = QComboBox(self)                                                                                                     #Setzt eine Auswahlbox
                self.useMeasure = QPushButton("Use", self)                                                                                              #Setzt einen Button

                #Stack
                self.Stack1.setToolTip("Adds a multiple Layers to the Measurement")
                self.Stack1.stateChanged.connect(self.StackSelect)
                self.Stack1.setChecked(False)
                
                #Slopecompensation
                self.Slope1.setToolTip("Adds a Slope Compensation to the Measurement")   
                self.Slope1.stateChanged.connect(self.SlopeSelect)
                self.Slope1.setChecked(False)

                #Subgrid
                self.Subgrid1.setToolTip("Adds a Subgrid to the Measurement and syncronises the selected TTL Device")   
                self.Subgrid1.setChecked(False)
                self.Subgrid1.stateChanged.connect(self.NavWinCheckboxen)
                
                #Sympho
                self.Sympho1.setToolTip("Synchronises the Measurement with the SymPhoTime System")
                self.Sympho1.setChecked(False)
                self.Sympho1.stateChanged.connect(self.NavWinCheckboxen)

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
                self.buttonStart.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))


                self.buttonResetZFocus2.setToolTip("Reset Z-Axis to Startvalue")
                self.buttonResetZFocus2.clicked[bool].connect(self.ResetZFocus)
                self.buttonResetZFocus2.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))
                
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
                print("FullRangeDeviceZ: " + str(PiezoDistanceZ))
                self.spinZFocus2.setMinimum(0)                                                                                                         #Setzt ein Minimalwert für die Auswahl
                self.spinZFocus2.setMaximum(PiezoDistanceZ/1000)                                                                 #Setzt ein Maximum für die Auswahl
                self.spinZFocus2.setValue((PiezoDistanceZ/1000)/2)                                                                       #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinZFocus2.setSingleStep(round(((PiezoDistanceZ/1000)/4095),3))                                                                               #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinZFocus2.setDecimals(3)                                                                                                     #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                #self.slideXStart.valueChanged.connect(self.slideXstart)                                                                                 #ruft beim Ablegen des Sliders die Funktion speedM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinZFocus2.setToolTip("Sets the Z-Startposition")  

                self.spinXStart.setMinimum(round(0*((FullRangeDeviceY/1000)/255),3))                                                                    #Setzt ein Minimalwert für die Auswahl
                self.spinXStart.setMaximum(round(255*((FullRangeDeviceX/1000)/255),3))                                                                  #Setzt ein Maximum für die Auswahl
                self.spinXStart.setValue(round(0*((FullRangeDeviceX/1000)/255),3))                                                                      #Setzt einen Startwert
                self.spinXStart.valueChanged.connect(self.spinXstart)                                                                               #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
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

                self.linetime.setMinimum(0) 
                self.linetime.setMaximum(100)  
                self.linetime.setValue(0) 
                self.linetime.setToolTip("Sets the Waiting Time after each Line in Milliseconds") 

                self.spinIntTime2.setMinimum(1)
                self.spinIntTime2.setMaximum(200)
                self.spinIntTime2.setValue(1)
                self.spinIntTime2.setToolTip("Set the Integrationtime of the Logic-Channels in Milliseconds")
                self.spinIntTime2.valueChanged.connect(self.NavWinIntTime)

                #Label definieren
                XDistance = (PiezoDistanceX * (DeviceVoltage/PiezoVoltage))
                YDistance = (PiezoDistanceY * (DeviceVoltage/PiezoVoltage))
                pixelsizeX = round(XDistance/256, 2)
                pixelsizeY = round(YDistance/256, 2)
                XDist = round(PiezoDistanceX/1000, 3)
                YDist = round(PiezoDistanceY/1000, 3)
                NormalTime = 532.1455
                TimeMins = NormalTime // 60
                TimeSecs1 = NormalTime % 60
                TimeSecs = TimeSecs1 // 1
                TimeMilsecs = round(((TimeSecs1 % 1) * 1000), 2)
                self.labelProgTime.setText("Expected Time:\t" + str(int(TimeMins)) + " min  \t" + str(int(TimeSecs)) + " s\t" + str(int(TimeMilsecs)) + " ms\nPixelsize:\t" + str(pixelsizeX) + " x " + str(pixelsizeY) + " nm" + " s\nWindowsize:\t" + str(XDist) + " x " + str(YDist) + " [\u03BCm]")                                                                  #Setzt ein Label 

                #Checkboxen als ButtonGroup zusammenfassen
                self.cbg2 = QButtonGroup()                                                                                                              #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg2.addButton(self.cb20, 0)                                                                                                       #Erstellt eine ButtonGroup, dadurch sind die hinzugefügten CheckBoxen miteinander verknüpft und die Auswahl ist exklusiv, heißt nur eine Checkbox kann ausewählt sein
                self.cbg2.addButton(self.cb21, 1)                                                                                                       #Fügt die erste Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb22, 2)                                                                                                       #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb23, 3)                                                                                                       #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb24, 4)                                                                                                       #Fügt die zweite Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb25, 5)                                                                                                       #Fügt die dritte Checkbox zur ButtonGroup hinzu
                self.cbg2.addButton(self.cb26, 6)                                                                                                       #Fügt die vierte Checkbox zur ButtonGroup hinzu
                self.cbg2.setExclusive(True)

                #Voreinstellungen Änderung                                                                                                              #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn der Amplifier umgestellt wird
                self.cbg2.buttonClicked.connect(self.stopAll2)                                                                                  #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird
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
                self.layoutCBs.addWidget(self.Sympho1)    
                self.layoutCBs.addStretch(1)       
                self.layoutCBs.addWidget(self.Stack1)                                                                                                   #Setzt das Widget   
                self.layoutCBs.addStretch(1)       
                self.layoutCBs.addWidget(self.Plot1)

                self.layoutDelay = QHBoxLayout(self) 
                self.layoutDelay.addWidget(self.spinIntTime2)
                self.layoutDelay.addWidget(self.labelIntTime)  
                self.layoutDelay.addWidget(self.linetime)                                                                                                            #setzt eine Spinbox
                self.layoutDelay.addWidget(self.labelLinetime)                                                                                                 #Setzt ein horizontales Layout
                self.layoutDelay.addWidget(self.delay)                                                                                                  #Fügt ein Layout hinzu
                self.layoutDelay.addWidget(self.labelDelay)

                self.layoutZ = QHBoxLayout(self)
                self.layoutZ.addWidget(self.spinZFocus2)
                self.layoutZ.addWidget(self.labelZFocus2)
                self.layoutZ.addWidget(self.buttonResetZFocus2)
                self.layoutZ.addWidget(self.ShutterRoot2)

                self.vboxMesSet = QVBoxLayout(self)                                                                                                     #Setzt einen Abstandshalter
                self.vboxMesSet.addLayout(self.layoutCBs)
                self.vboxMesSet.addStretch(1)
                self.vboxMesSet.addLayout(self.layoutDelay)
                self.vboxMesSet.addStretch(1)
                self.vboxMesSet.addLayout(self.layoutZ)
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
                self.tab2.layoutV1.addWidget(self.labelProgTime)
                self.tab2.layoutV1.addWidget(self.labelPath)                                                                                        #Setzt einen Abstandshalter                     

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
                self.LabelSpinCount = QLabel("Number of Points", self)                                                                                             #Setzt eine Textbox
                self.spinTh = QDoubleSpinBox(self)
                self.LabelSpinTh = QLabel("Threshold", self)  
                self.LoadAutoSync1 = QPushButton("Load Plot 1", self) 
                self.LoadAutoSync2 = QPushButton("Load Plot 2", self)  
                self.cbCount = QCheckBox("Use Count", self) 
                self.cbTh = QCheckBox("Use Threshold", self)     
                self.spinAddPosX = QDoubleSpinBox(self)
                self.spinAddPosY = QDoubleSpinBox(self)
                self.AddPos = QPushButton("Add Position", self) 
                self.LabelAdd = QLabel("X-Y Position", self) 

                self.AddPos.clicked.connect(self.AddCoordinate)  

                self.cbCount.setChecked(True)
                self.cbTh.stateChanged.connect(self.ThChange)
                self.cbCount.stateChanged.connect(self.CountChange)

                self.spinAddPosX.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.spinAddPosX.setMaximum(FullRangeDeviceX/1000)                                                                                            #Setzt ein Maximum für die Auswahl
                self.spinAddPosX.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.spinAddPosX.setSingleStep(round((FullRangeDeviceX/1000)/256,3))
                self.spinAddPosX.setDecimals(3)
                self.spinAddPosX.setToolTip("Select the X-Position") 

                self.spinAddPosY.setMinimum(0)                                                                                                                #Setzt ein Minimalwert für die Auswahl
                self.spinAddPosY.setMaximum(FullRangeDeviceY/1000)                                                                                            #Setzt ein Maximum für die Auswahl
                self.spinAddPosY.setValue(0)                                                                                                                  #Setzt einen Startwert
                self.spinAddPosY.setSingleStep(round((FullRangeDeviceY/1000)/256,3))
                self.spinAddPosY.setDecimals(3)
                self.spinAddPosY.setToolTip("Select the Y-Position") 

                self.spinTh.setMinimum(0)                                                                                           #Setzt ein Minimalwert für die Auswahl
                self.spinTh.setMaximum(100000000)                                                                                                          #Setzt ein Maximum für die Auswahl
                self.spinTh.setValue(0)                                                                                                            #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinTh.setSingleStep(0.01)                                                                  #ruft bei Auswahl eines Wertes die Funktion spinboxM1 auf (mit ".valueChanged." kann man immer aktuelle den Wert ablesen)
                self.spinTh.setDecimals(2)

                self.spinCount.setMinimum(0)
                self.spinCount.setMaximum(64000)                                                                                                         #Setzt ein Maximum für die Auswahl
                self.spinCount.setValue(1)

                self.LoadAutoSync1.clicked.connect(self.LoadSync1)
                self.LoadAutoSync2.clicked.connect(self.LoadSync2)

                #TTL
                self.TTLroot2.addItem(TTLOUT3["Name"])
                self.TTLroot2.addItem(TTLOUT4["Name"])
                self.TTLroot2.addItem(TTLOUT5["Name"])
                self.TTLroot2.addItem(TTLOUT6["Name"])

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

                self.cbg3.buttonClicked.connect(self.stopAll3)                                                                                     #Stoppt die Messung und setzt den Start-Butten auf ungeklicked, wenn die unter Messschranke umgestellt wird

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
                self.groupboxSendTTL3.setChecked(True)
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
                self.vboxSave3.addWidget(self.useSync) 
                self.groupboxSave3.setLayout(self.vboxSave3)

                self.groupboxSteps = QGroupBox("Measurement Settings", self) 
                self.groupboxManuel = QGroupBox("Manuel Grid", self)
                self.groupboxManuel.setCheckable(True)
                self.groupboxManuel.setChecked(True)
                self.groupboxManuel.toggled.connect(self.updateManuelGrid)
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
                self.groupboxAuto.toggled.connect(self.updateAutoGrid)
                self.layoutHCount = QVBoxLayout(self)    
                self.layoutVCount1 = QHBoxLayout(self) 
                self.layoutVCount1.addWidget(self.cbCount)
                self.layoutVCount1.addWidget(self.spinCount)                                                                                               #Setzt ein horizontales Layout
                self.layoutVCount1.addWidget(self.LabelSpinCount)
                self.layoutVCount1.addWidget(self.LoadAutoSync1)   
                self.layoutVCount2 = QHBoxLayout(self) 
                self.layoutVCount2.addWidget(self.cbTh)
                self.layoutVCount2.addWidget(self.spinTh)                                                                                               #Setzt ein horizontales Layout
                self.layoutVCount2.addWidget(self.LabelSpinTh)
                self.layoutVCount2.addWidget(self.LoadAutoSync2)
                self.layoutVCount3 = QHBoxLayout(self) 
                self.layoutVCount3.addWidget(self.spinAddPosX)
                self.layoutVCount3.addWidget(self.spinAddPosY)                                                                                         #Setzt ein horizontales Layout
                self.layoutVCount3.addWidget(self.LabelAdd)
                self.layoutVCount3.addWidget(self.AddPos)
                self.layoutHCount.addLayout(self.layoutVCount1)
                self.layoutHCount.addLayout(self.layoutVCount2)
                self.layoutHCount.addLayout(self.layoutVCount3)
                self.groupboxAuto.setLayout(self.layoutHCount)

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
                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
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
                self.vboxSave4.addWidget(self.useStack) 
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
                self.buttonAutoSlope.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                self.buttonXSlope.setCheckable(True)                                                                                                    #Macht den Button chackbar
                self.buttonXSlope.setToolTip("Define the X Slope")                                                                                      #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonXSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonXSlope.clicked[bool].connect(self.SlopeStartX)
                self.buttonXSlope.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                #Button definieren
                self.buttonYSlope.setCheckable(True)                                                                                                    #Macht den Button chackbar
                self.buttonYSlope.setToolTip("Define the Y Slope")                                                                                      #Setzt eine Buttonbeschreibung bei MouseOver
                self.buttonYSlope.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonYSlope.clicked[bool].connect(self.SlopeStartY)
                self.buttonYSlope.setFont(QFont(self.Fontstyle, self.Fontsize, QFont.Bold))

                #Settings
                self.saveSlope.setToolTip("Saves the Settings")                                                                                         #Setzt eine Buttenbeschreibung bei MouseOver
                self.saveSlope.clicked.connect(self.savesettingsScanSlope)                                                                              #Ruft die savesettings-Funktion auf
                self.namesSlope.setToolTip("Old Settings")
                SlopeSet.execute("SELECT name FROM settingsScanSlope")
                for dsatzSlope in SlopeSet:
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
                self.vboxSave5.addWidget(self.useSlope) 
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


#-------------- Tabs zum Widget hinzufügen ------------------
                global Cite
                self.labelCite = QLabel("If HydraScan contributes to publisch a work please cite:\n" + Cite + "\nSee \"About\" for Details", self)                                                                                              #setzt ein Label    
                self.labelCite.setFont(QFont('Arial', 8))

                self.layout.addWidget(self.tabs)                                                                                                        #Fügt die Tabs zum Layout hinzu
                self.layout.addWidget(self.labelCite)
                self.setLayout(self.layout)                                                                                                             #Setzt das Layout als Seiten-Layout             

        """
        -------------------------------------------------------------------------------------------------------------------------------------------------------
        -------------------------------------------------------------------- Section 8: Main Window Functions -------------------------------------------------
        -------------------------------------------------------------------------------------------------------------------------------------------------------
        """

#---------------------- Tab Funktionen ----------------------
        #Navigation Window Functions
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
                XStart = int(round((self.slideXStart.value()/1000)/(self.DimensionStepsX/255)))
                XStop = int(round((self.slideXStop.value()/1000)/(self.DimensionStepsX/255)))
                YStart = int(round((self.slideYStart.value()/1000)/(self.DimensionStepsY/255)))
                YStop = int(round((self.slideYStop.value()/1000)/(self.DimensionStepsY/255)))
                self.NavWin.PositionFromMain(XStart, YStart, XStop, YStop)

                MidX = self.slideX.value()
                MidY = self.slideY.value()
                Range = 50
                #self.NavWin.PositionFromMainMid(MidX, MidY, Range)

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
                if self.Sympho1.isChecked():
                        self.NavWin.Sympho.setChecked(True)
                        self.Plot1.setChecked(False)
                else:
                        self.NavWin.Sympho.setChecked(False)
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
                self.NavWin.progress_valueLineOut.connect(self.PosFromLine)
                self.NavWin.show()

        def RemoveMarker(self):
                print("Remove Marker 1")
                self.AnzahlPositionen = 0
                self.NummerPositionen = 0
                self.labelPositions.setText("Position " + str(self.NummerPositionen) + "/" + str(self.AnzahlPositionen))
                self.NavWin.myFig.RemoveLineMarker()

        def PosFromLine(self, X1, Y1, X2, Y2, X1raw, Y1raw, X2raw, Y2raw):
                print("PosFromLive")
                #print(self.LineDivs.value())
                self.LinePositions = []
                self.LinePositionsRaw = []
                self.AnzahlPositionen = self.LineDivs.value()
                self.NummerPositionen = 0
                i = 0
                while i < self.AnzahlPositionen:
                        X = X1 + i*((X2-X1)/(self.AnzahlPositionen-1))
                        Y = Y1 + i*((Y2-Y1)/(self.AnzahlPositionen-1))
                        Xraw = X1raw + i*((X2raw-X1raw)/(self.AnzahlPositionen-1))
                        Yraw = Y1raw + i*((Y2raw-Y1raw)/(self.AnzahlPositionen-1))
                        #print(X)
                        #print(Y)
                        self.LinePositions.append([X,Y])
                        self.LinePositionsRaw.append([Xraw,Yraw])
                        i += 1
                self.labelPositions.setText("Position " + str(self.NummerPositionen) + "/" + str(self.AnzahlPositionen))
                print(self.LinePositions)
                print(self.LinePositionsRaw)

                #PosFromLine

        def close_NavWin(self):
                self.NavWin.WindowClose()

        def FocusFromNavWin(self, FocusNew):
                self.Slope1.setChecked(False)

        def updateFromNavWinPosition(self, X, Y, PlotPosX, PlotPosY):
                self.PlotPosX = PlotPosX
                self.PlotPosY = PlotPosY
                self.spinX.setValue(X)
                self.spinY.setValue(Y)
                self.spinboxX()
                self.spinboxY()
                self.spinAddPosX.setValue(X)
                self.spinAddPosY.setValue(Y)

        def updateFromNavWinCheck(self, TTL, Sympho, Stack, Slope, IntTime, Bits):
                self.Subgrid1.setChecked(TTL)
                self.Sympho1.setChecked(Sympho)
                self.Stack1.setChecked(Stack)
                self.Slope1.setChecked(Slope)
                self.spinIntTime2.setValue(IntTime)

                if Bits == 0:
                        self.cb10.setChecked(True)
                        self.cb20.setChecked(True)
                        self.cb30.setChecked(True)
                if Bits == 1:                                                                                                    #Setzt eine CheckBox
                        self.cb11.setChecked(True)
                        self.cb21.setChecked(True)
                        self.cb31.setChecked(True)
                if Bits == 2:                                                                                                     #Setzt eine CheckBox
                        self.cb12.setChecked(True)
                        self.cb22.setChecked(True)
                        self.cb32.setChecked(True)
                if Bits == 3:                                                                                                   #Setzt eine CheckBox
                        self.cb13.setChecked(True)
                        self.cb23.setChecked(True)
                        self.cb33.setChecked(True)
                if Bits == 4:                                                                                                    #Setzt eine CheckBox
                        self.cb14.setChecked(True)
                        self.cb24.setChecked(True)
                        self.cb34.setChecked(True) 
                if Bits == 5:                                                                                                     #Setzt eine CheckBox
                        self.cb15.setChecked(True)
                        self.cb25.setChecked(True)
                        self.cb35.setChecked(True)
                if Bits == 6:
                        self.cb16.setChecked(True)
                        self.cb26.setChecked(True)
                        self.cb36.setChecked(True)

        def updateFromNavWinXY(self, XStart, YStart, XStop, YStop):
                global FullRangeDeviceX
                global FullRangeDeviceY
                global PiezoVoltage
                global DeviceVoltage
                global CurrentOffsetX 
                global CurrentOffsetY 
                global CurrentPoti 
                global ZoomedNav
                global XOffsetStart
                global YOffsetStart
                global DimensionStart
                
                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)

                """
                print(self.DimensionStepsX)
                      
                print("Hier arbeiten!!!")
                
                print(XStart)
                print(YStart)
                print(XStop)
                print(YStop)
                
                print(ZoomedNav)
                print(CurrentPoti)
                print(CurrentOffsetX)
                print(CurrentOffsetY)
                
                print("Hier arbeiten!!!")
                
                if ZoomedNav and CurrentPoti == 10:
                """
                XStart = round((XStart*(self.DimensionStepsX/255)),3)
                YStart = round((YStart*(self.DimensionStepsY/255)),3)
                XStop = round((XStop*(self.DimensionStepsX/255)),3)
                YStop = round((YStop*(self.DimensionStepsY/255)),3)
                print("XStart2: " + str(XStart))
                #print("XStars3: " + str((int(XStart*1000))))
                """
                else:
                    print((round(((XStart/255)*((4096/10)*CurrentPoti)),0)/4095))
                    XStart = ((CurrentOffsetX + round(((XStart/255)*((4096/10)*CurrentPoti)),0)/4095))
                    YStart = ((CurrentOffsetY + round(((YStart/255)*((4096/10)*CurrentPoti)),0)/4095))
                    XStop = ((round(((XStop/255)*((4096/10)*CurrentPoti)),0)/4095)*100)
                    YStop = ((round(((YStop/255)*((4096/10)*CurrentPoti)),0)/4095)*100)
                    #XStart = round((XStart*(self.DimensionStepsX/255)),3)
                    #YStart = round((YStart*(self.DimensionStepsY/255)),3)
                    #XStop = round((XStop*(self.DimensionStepsX/255)),3)
                    #YStop = round((YStop*(self.DimensionStepsY/255)),3)
                    print("XStart2: " + str(XStart))
                    #print("XStars3: " + str((int(XStart*1000))))
                    #CurrentPoti = (((XStop - XStart)/4095)*100)
                
                print("After calc")
                print(XStart)
                print(YStart)
                print(XStop)
                print(YStop)
                print(XStop - XStart)
                #print(CurrentPoti)
                
                self.DimensionStepsX = round((FullRangeDeviceX * (PiezoVoltage / DeviceVoltage) / 1000),3)
                self.DimensionStepsY = round((FullRangeDeviceY * (PiezoVoltage / DeviceVoltage) / 1000),3)
                X = round((int(round(XStart,0)) * (self.DimensionStepsX/255)),3)
                Y = round((int(round(YStart,0)) * (self.DimensionStepsY/255)),3)
                XEnd = round((int(round(XStop,0)) * (self.DimensionStepsX/255)),3)
                YEnd = round((int(round(YStop,0)) * (self.DimensionStepsY/255)),3)
                if ZoomedNav and CurrentPoti == 10:
                        PosX = XOffsetStart + (DimensionStart/100)*X
                        PosY = YOffsetStart + (DimensionStart/100)*Y
                        PosXEnd = XOffsetStart + (DimensionStart/100)*XEnd
                        PosYEnd = YOffsetStart + (DimensionStart/100)*YEnd
                else:
                        PosX = X
                        PosY = Y
                        PosXEnd = XEnd
                        PosYEnd = YEnd
                print("NewVals")
                print(PosX)
                print(PosY)
                print(PosXEnd)
                print(PosYEnd)
                print(PosXEnd - PosX)
                """

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

                if self.slideXStart.value() != XStart:
                        #self.slideXStart.setValue(int(PosX))
                        self.slideXStart.setValue(int(XStart*1000))
                if self.slideYStart.value() != YStart:
                        #self.slideYStart.setValue(int(PosY))
                        self.slideYStart.setValue(int(YStart*1000))
                if self.slideXStop.value() != XStop:
                        #self.slideXStop.setValue(int(PosXEnd))
                        self.slideXStop.setValue(int(XStop*1000))
                if self.slideYStop.value() != YStop: 
                        #self.slideYStop.setValue(int(PosYEnd))
                        self.slideYStop.setValue(int(YStop*1000))

        def updateFromNavWinButton(self, check):
                if check:
                        self.buttonStart.setChecked(True)
                else:
                        self.buttonStart.setChecked(False)
                self.StartMeasurement(check)


        #APD Window Functions
        def show_apd(self):
                global APDWindowOn
                #try:
                #        self.APDWin = APDWindow()
                #        self.APDWin.show()
                #        APDWindowOn = 1
                #except:
                #        print("APD Thread failed")


        #Temperature Window Functions
        def show_temp(self):
                global TempWindowOn
                try:
                        self.TempSens = TempWindow()
                        self.TempSens.show()
                        TempWindowOn = 1
                except:
                        print("Temp Thread failed")


        #Plot Window Functions
        def show_plot(self):
                self.PlotWin = PlotWindow()
                self.PlotWin.progress_valueRect.connect(self.updateRect)
                self.PlotWin.progress_valuePos.connect(self.updatePos)
                self.PlotWin.progress_Refresh.connect(self.updateRefresh)
                self.PlotWin.show()

        def updateRefresh(self, past, zoom, Min, Max):
                self.NavWin.UpdateFromPlot(past, zoom, Min, Max)

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
                self.slideXStart.setValue(XStart*1000)
                self.slideYStart.setValue(YStart*1000)
                self.slideXStop.setValue(XStop*1000)
                self.slideYStop.setValue(YStop*1000)

        def updatePos(self, val1, val2):
                self.slideX.setValue(int(val1))
                self.slideY.setValue(int(val2))
                self.positionX()
                self.positionY()

        def ResizeLivePlot(self, NewXStart, NewXStop, NewYStart, NewYStop, bits):
                self.PlotWin.Resize(NewXStart, NewXStop, NewYStart, NewYStop, bits)


        #Tab1 - Funktionen definieren
        def ShutterAction(self, down):
                global TTLOUT7
                global TTLOUT8
                global ShutterMode
                
                Shutters = self.ShutterRoot1.currentIndex()
                
                if down:
                        self.buttonShutter.setText("Close Shutter")
                        self.buttonShutter.setToolTip("Close the selected Shutter")
                        self.buttonShutter.setStyleSheet("color: black; background-color: rgb(255,63,0)")
                        if Shutters == 0 or Shutters == 2:
                                #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                                if ShutterMode[0] == 0 or ShutterMode[0] == 2:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                elif ShutterMode[0] == 1 or ShutterMode[0] == 3:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        if Shutters == 1 or Shutters == 2:
                                #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                                if ShutterMode[1] == 0 or ShutterMode[1] == 2:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                elif ShutterMode[1] == 1 or ShutterMode[1] == 3:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                else:
                        self.buttonShutter.setText("Open Shutter")
                        self.buttonShutter.setToolTip("Open the selected Shutter")
                        self.buttonShutter.setStyleSheet("color: black; background-color: rgb(0,250,0)")
                        if Shutters == 0 or Shutters == 2:
                                if ShutterMode[0] == 0 or ShutterMode[0] == 2:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                elif ShutterMode[0] == 1 or ShutterMode[0] == 3:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        if Shutters == 1 or Shutters == 2:
                                if ShutterMode[1] == 0 or ShutterMode[1] == 2:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                elif ShutterMode[1] == 1 or ShutterMode[1] == 3:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

        def PrevLine(self):
                global FullRangeDeviceX
                global FullRangeDeviceY
                #print("Previous Position")
                if self.NummerPositionen > 1:
                        self.NummerPositionen -= 1
                else:
                        self.NummerPositionen = self.AnzahlPositionen
                        
                self.spinX.setValue(self.LinePositions[self.NummerPositionen-1][0])
                self.spinY.setValue(self.LinePositions[self.NummerPositionen-1][1])
                self.spinboxX()
                self.spinboxY()
                self.labelPositions.setText("Position " + str(self.NummerPositionen) + "/" + str(self.AnzahlPositionen))
                #self.PlotPosX = self.LinePositionsRaw[self.NummerPositionen-1][0]
                #self.PlotPosY = self.LinePositionsRaw[self.NummerPositionen-1][1]
                self.PlotPosX = (self.LinePositionsRaw[self.NummerPositionen-1][0]/255)*(FullRangeDeviceX/1000)                 #Unsicher
                self.PlotPosY = (self.LinePositionsRaw[self.NummerPositionen-1][1]/255)*(FullRangeDeviceY/1000)
                #print("Position im PlotPosXY: " + str(self.PlotPosX) + " x " + str(self.PlotPosY)) 
                #self.spinboxX()
                #self.spinboxY()
                self.clickedPos(self.buttonPos.isChecked()) 


        def NextLine(self):
                global FullRangeDeviceX
                global FullRangeDeviceY
                #print("Next Position")
                if self.NummerPositionen < self.AnzahlPositionen:
                        self.NummerPositionen += 1
                else:
                        self.NummerPositionen = 1
                        
                self.spinX.setValue(self.LinePositions[self.NummerPositionen-1][0])
                self.spinY.setValue(self.LinePositions[self.NummerPositionen-1][1])
                self.spinboxX()
                self.spinboxY()
                self.labelPositions.setText("Position " + str(self.NummerPositionen) + "/" + str(self.AnzahlPositionen))
                #self.PlotPosX = self.LinePositionsRaw[self.NummerPositionen-1][0]
                #self.PlotPosY = self.LinePositionsRaw[self.NummerPositionen-1][1]
                self.PlotPosX = (self.LinePositionsRaw[self.NummerPositionen-1][0]/255)*(FullRangeDeviceX/1000)                 #Unsicher
                self.PlotPosY = (self.LinePositionsRaw[self.NummerPositionen-1][1]/255)*(FullRangeDeviceY/1000)
                print("Position im PlotPosXY: " + str(self.PlotPosX) + " x " + str(self.PlotPosY)) 
                #self.spinboxX()
                #self.spinboxY()
                self.clickedPos(self.buttonPos.isChecked()) 

        def LineDivsPos(self):
                #PosFromLine
                self.LineDivs.value()

        def IntChange(self):
                if self.buttonPos.isChecked():
                        self.clickedPos(False)
                        self.clickedPos(True)  

        def positionX(self):                                                                                                                            #Funktion setzt die Geschwindigkeitsvariable des ersten Motors auf den Wert des Sliders (Tab1)
                global FullRangeDeviceX

                checkedBits = self.cbg1.checkedId()
                checkedBits = 6
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
                NewVal = round((self.slideX.value()*(100/(self.bitval))),3)
                if self.spinX.value() != NewVal:
                        self.spinX.setValue(NewVal)
                        self.spinboxX()
                        self.spinboxY()                                                                                                     #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())             
        
        def spinboxX(self):                                                                                                                             #Funktion setzt die Geschwindigkeitsvariable des ersten Motors auf den Wert der Zahlenauswahlbox (Tab1)
                global FullRangeDeviceX

                checkedBits = self.cbg1.checkedId()
                
                checkedBits = 6
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
                self.PositionX = int(round((self.spinX.value()*1000)/(100/self.bitval)/1000,0))     #Test
                print("spinboxX: " + str(self.PositionX))
                if self.slideX.value() != self.PositionX:
                        self.slideX.setValue(int(self.PositionX)) 
                        
                        self.positionX()                                                                                    #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())                                                                             #Ruft die clickedM1-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden

        def positionY(self):                                                                                                                            #Funktion setzt die Geschwindigkeitsvariable des zweiten Motors auf den Wert des Sliders (Tab1)
                global FullRangeDeviceY 

                checkedBits = self.cbg1.checkedId()
                
                checkedBits = 6
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
                NewVal = round((self.slideY.value()*(100/(self.bitval))),3)         #Test2
                if self.spinY.value() != NewVal:
                        self.spinY.setValue(NewVal)                                                                                                     #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())    

        def spinboxY(self):                                                                                                                             #Funktion setzt die Geschwindigkeitsvariable des zweiten Motors auf den Wert der Zahlenauswahlbox (Tab1)
                global FullRangeDeviceY 

                checkedBits = self.cbg1.checkedId()
                
                checkedBits = 6
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
                self.PositionY = int(round((self.spinY.value()*1000)/(100/self.bitval)/1000,0))
                print("spinboxY: " + str(self.PositionY))
                if self.slideY.value() != self.PositionY:
                        self.slideY.setValue(int(self.PositionY))    
                        
                        self.positionY()                                                                                   #Setzt den Wert der Zahlenauswahlbox auf den Wert des Sliders
                        if self.buttonPos.isChecked():
                                self.clickedPos(self.buttonPos.isChecked())                                                                             #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden

        def clickedPos(self, down): 
                global CurrentOffsetX 
                global CurrentOffsetY 
                global CurrentPoti 
                global ZoomedNav
                global FullRangeDeviceX
                global FullRangeDeviceY
                global TTLOUT7
                global TTLOUT8
                global ShutterMode

                Shutters = self.ShutterRoot1.currentIndex()
                
                #DoWorkHere
                if down:                                                                                                                                #Setzt den MouseOver-ToolTip des Motor-Startbuttons um   
                        if Shutters == 0 or Shutters == 2:
                                #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                                if ShutterMode[0] == 0 or ShutterMode[0] == 2:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                elif ShutterMode[0] == 1 or ShutterMode[0] == 3:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        if Shutters == 1 or Shutters == 2:
                                #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                                if ShutterMode[1] == 0 or ShutterMode[1] == 2:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                elif ShutterMode[1] == 1 or ShutterMode[1] == 3:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                        try:
                                self.APDWin.StopMeasure()
                        except:
                                pass

                        if self.NummerPositionen == 0 and self.AnzahlPositionen != 0:
                                try:
                                        self.NextLine()
                                except:
                                        pass

                        self.buttonPoint.setChecked(0)
                        self.buttonPoint.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPoint.setText("Point Measurement")
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

                        print("Position Slider: " + str(self.PositionX) + " x " + str(self.PositionY)) 
                        #404 work not found
                        OffsetX = int(round(CurrentOffsetX,0))
                        OffsetY = int(round(CurrentOffsetY,0))
                        if ZoomedNav == True:
                                PositionPlotX = self.PlotPosX
                                PositionPlotY = self.PlotPosY
                                PositionPlotFullX = (PositionPlotX/(FullRangeDeviceX/1000))*4095
                                #print("PositionPlotFullX: " + str(PositionPlotFullX))
                                #print("FullRangeDeviceX: " + str(FullRangeDeviceX))
                                #print("PositionPlotFullXNew: " + str((PositionPlotX/(FullRangeDeviceX/1000))*4095))
                                PositionPlotFullY = (PositionPlotY/(FullRangeDeviceX/1000))*4095
                                OffsetX = int(round(CurrentOffsetX,0))
                                OffsetY = int(round(CurrentOffsetY,0))
                                Voltage = CurrentPoti 
                                #print("Position im Plot Full: " + str(PositionPlotFullX) + " x " + str(PositionPlotFullY)) 
                                #print("Offset: " + str(OffsetX) + " x " + str(OffsetY))
                                #print("Voltage: " + str(Voltage))

                                X = int(PositionPlotFullX)
                                Y = int(PositionPlotFullY)
                                Poti.write_range(Voltage)
                                dacOffset.setAllVoltage(OffsetX, OffsetY, 0, 0)
                                
                        else:
                                X = int(self.PositionX*(4095 / self.bitval))
                                Y = int(self.PositionY*(4095 / self.bitval))
                                #print("Position Slider: " + str(self.PositionX) + " x " + str(self.PositionY)) 
                                #print("Position XY: " + str(X) + " x " + str(Y)) 

                        TestOffX = ((OffsetX/4095)*(FullRangeDeviceX/1000))
                        TestOffY = ((OffsetY/4095)*(FullRangeDeviceX/1000))
                        TestX = ((X/4095)*(FullRangeDeviceX/1000))
                        TestY = ((Y/4095)*(FullRangeDeviceX/1000))
                        #print("/nPosition X = OffsetX: " + str(TestOffX) + " ym + DacX: " + str(TestX))
                        #print("/nPosition X = OffsetX: " + str(TestOffY) + " ym + DacX: " + str(TestY))
                        #print("PosX: " + str(self.PositionX) + "  PosY: " + str(self.PositionY))
                        Z = int(self.SlopeVal)
                        #print("DacX: " + str(X) + "  DacY: " + str(Y) + "  DACZ: " + str(Z))
                        dacX.set_voltage(X)
                        dacY.set_voltage(Y)
                        dacZ.set_voltage(Z)
                        #print("X: " + str(X))
                        #print("Y: " + str(Y))
                        
                        #clickedPos1
                        X = int(self.PositionX*(4095 / self.bitval))
                        Y = int(self.PositionY*(4095 / self.bitval))
                        if self.XOldPos != X or self.YOldPos != Y:
                                self.NavWin.myFig.PositionMarker(X,Y,True)
                                self.XOldPos = X
                                self.YOldPos = Y


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
                else:
                        if Shutters == 0 or Shutters == 2:
                                if ShutterMode[0] == 0 or ShutterMode[0] == 2:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                elif ShutterMode[0] == 1 or ShutterMode[0] == 3:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        if Shutters == 1 or Shutters == 2:
                                if ShutterMode[1] == 0 or ShutterMode[1] == 2:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                elif ShutterMode[1] == 1 or ShutterMode[1] == 3:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                        
                        Poti.write_range(10)
                        dacOffset.setAllVoltage(0, 0, 0, 0)
                        self.NavWin.myFig.PositionMarker(0,0,False)
                        try:
                                self.Monty.killFred()
                        except:
                                pass
                        
                        try:
                                if APDWindowOn == 1:
                                        self.APDWin.StartMeasure()
                        except:
                                pass

                        self.buttonPos.setToolTip("Starts the Positioning") 
                        self.buttonPos.setText("Move to")                                                                                     #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
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
                        self.buttonPoint.setText("Point Measurement")
                        self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.flyingcircus = 0

        def clickedPoint(self, down): 
                global FocusZ
                global TTLOUT7
                global TTLOUT8
                global ShutterMode

                Shutters = self.ShutterRoot1.currentIndex()
                                                                                                                                  #Setzt die Position
                if down:                                                                                                                                #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        if Shutters == 0 or Shutters == 2:
                                #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                                if ShutterMode[0] == 0 or ShutterMode[0] == 2:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                elif ShutterMode[0] == 1 or ShutterMode[0] == 3:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        if Shutters == 1 or Shutters == 2:
                                #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                                if ShutterMode[1] == 0 or ShutterMode[1] == 2:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                elif ShutterMode[1] == 1 or ShutterMode[1] == 3:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                        try:
                                self.APDWin.StopMeasure()
                        except:
                                pass

                        self.buttonPoint.setToolTip("Stops the Measurement") 
                        self.buttonPoint.setText("Stop Measurement")                                                                                    #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPoint.setStyleSheet("background-color: rgb(255,63,0)")
                        self.buttonPos.setChecked(0)
                        self.buttonPos.setToolTip("Starts the Positioning") 
                        self.buttonPos.setText("Move to")
                        self.buttonPos.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                        try:
                                self.Monty.killFred()
                                self.monty = 0
                        except:
                                pass

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

                        XPoint = self.PositionX
                        YPoint = self.PositionY
                        ZPoint = self.SlopeVal
                        #print(ZPoint)
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
                        if Shutters == 0 or Shutters == 2:
                                if ShutterMode[0] == 0 or ShutterMode[0] == 2:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                elif ShutterMode[0] == 1 or ShutterMode[0] == 3:
                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        if Shutters == 1 or Shutters == 2:
                                if ShutterMode[1] == 0 or ShutterMode[1] == 2:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                elif ShutterMode[1] == 1 or ShutterMode[1] == 3:
                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        time.sleep(0.1)
                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                        
                        try:
                                self.FlyingCircus.killFred()
                        except:
                                pass
                        
                        try:
                                if APDWindowOn == 1:
                                        self.APDWin.StartMeasure()
                        except:
                                pass
                                
                        self.buttonPoint.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonPoint.setText("Point Measurement")
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
                self.buttonPos.setText("Move to") 
                self.buttonPos.setToolTip("Starts the Positioning")                                                                                     #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                self.buttonPos.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                self.buttonPoint.setText("Point Measurement")
                self.buttonPoint.setToolTip("Starts the Measurement")                                                                                   #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                self.buttonPoint.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                #dacX.set_voltage(0)
                #dacY.set_voltage(0)
                #dacZ.set_voltage(0)
                bitvalOld = self.bitval-1
                checkedBits = self.cbg1.checkedId()
                self.NavWinBits(checkedBits)
                XPosOld = self.slideX.value()
                YPosOld = self.slideY.value()
                if checkedBits == 0:
                        self.bitval = 64
                        self.cb20.setChecked(True)
                        self.cb30.setChecked(True)
                elif checkedBits == 1:
                        self.bitval = 128
                        self.cb21.setChecked(True)
                        self.cb31.setChecked(True)
                elif checkedBits == 2:
                        self.bitval = 256
                        self.cb22.setChecked(True)
                        self.cb32.setChecked(True)
                elif checkedBits == 3:
                        self.bitval = 512
                        self.cb23.setChecked(True)
                        self.cb33.setChecked(True)
                elif checkedBits == 4:
                        self.bitval = 1024
                        self.cb24.setChecked(True)
                        self.cb34.setChecked(True)
                elif checkedBits == 5:
                        self.bitval = 2048
                        self.cb25.setChecked(True)
                        self.cb35.setChecked(True)
                elif checkedBits == 6:
                        self.bitval = 4096
                        self.cb26.setChecked(True)
                        self.cb36.setChecked(True)
                #self.slideX.setMaximum(self.bitval-1)
                #self.slideY.setMaximum(self.bitval-1)
                #self.slideX.setValue(int((XPosOld/bitvalOld)*(self.bitval-1)))
                #self.slideY.setValue(int((YPosOld/bitvalOld)*(self.bitval-1)))
                self.spinX.setMaximum(FullRangeDeviceX/1000)
                self.spinY.setMaximum(FullRangeDeviceY/1000)
                #self.spinX.setSingleStep(round((FullRangeDeviceX/1000)/(self.bitval-1),3))
                #self.spinY.setSingleStep(round((FullRangeDeviceY/1000)/(self.bitval-1),3))


        #Tab2 - Funktion für die Messung
        def ResetZFocus(self):
                global FocusZ
                global PiezoDistanceZ

                value = ((FocusZ/4096)*PiezoDistanceZ)/1000
                self.spinZFocus2.setValue(value)


        def slideXstart(self):                                                                                                                          #Gibt den Wert des Sliders im cmd aus
                global FullRangeDeviceX
                NewVal = round((self.slideXStart.value()/1000),3)
                NewValInt = int(round(NewVal,0))
                if NewVal != self.spinXStart.value():
                        self.StartX = (NewVal / (FullRangeDeviceX/1000))                                                                                                    #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStart.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStop.setMinimum(NewValInt)
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
                        self.StartX = (NewVal / (FullRangeDeviceX/1000))
                        self.updateProgTime()
                        self.PositionToNavWin()

        def slideYstart(self):                                                                                                                          #Gibt den Wert des Sliders im cmd aus
                global FullRangeDeviceY
                NewVal = round((self.slideYStart.value()/1000),3)
                NewValInt = int(round(NewVal,0))
                if NewVal != self.spinYStart.value():
                        self.StartY = (NewVal / (FullRangeDeviceY/1000))                                                                                                    #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStart.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStop.setMinimum(NewValInt)
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
                        self.StartY = (NewVal / (FullRangeDeviceY/1000))
                        self.updateProgTime()
                        self.PositionToNavWin()

        def slideXstop(self,x):                                                                                                                         #Gibt den Wert des Sliders im cmd aus
                global FullRangeDeviceX
                NewVal = round((self.slideXStop.value()/1000),3)
                if NewVal != self.spinXStop.value():
                        self.StopX = (NewVal / (FullRangeDeviceX/1000))                                                                                                     #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStop.setValue(NewVal)                                                                                                 #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.updateProgTime()
                        self.PositionToNavWin()

        def spinXstop(self,x):
                global FullRangeDeviceX
                NewVal = int(self.spinXStop.value()*1000)
                if NewVal != self.slideXStop.value():
                        self.StopX = (NewVal / (FullRangeDeviceX/1000))                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideXStop.setValue(NewVal)
                        self.updateProgTime()
                        self.PositionToNavWin()

        def slideYstop(self,x):
                global FullRangeDeviceY
                NewVal = round((self.slideYStop.value()/1000),3)
                if NewVal != self.spinYStop.value:
                        self.StopY = (NewVal / (FullRangeDeviceY/1000))                                                                                                     #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStop.setValue(NewVal) 
                        self.updateProgTime()
                        self.PositionToNavWin()

        def spinYstop(self,x):                                                                                                                          #Funktion setzt die Geschwindigkeitsvariable des zweiten Motors auf den Wert der Zahlenauswahlbox (Tab1)
                global FullRangeDeviceY
                NewVal = int(self.spinYStop.value()*1000)
                if NewVal != self.slideYStop.value():
                        self.StopY = (NewVal / (FullRangeDeviceY/1000))                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
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
                sympho = self.Sympho1.isChecked()

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
                if plot == True:
                        plot = 1
                else:
                        plot = 0
                if slope == True:
                        slope = 1
                        self.nameSlope.setText(name)
                        self.savesettingsScanSlope()
                else:
                        slope = 0
                if subgrid == True:
                        subgrid = 1
                        self.nameSync.setText(name)
                        self.savesettingsScanSync()
                else:
                        subgrid = 0
                if stack == True:
                        stack = 1
                        self.nameStack.setText(name)
                        self.savesettingsScanStack()
                else:
                        stack = 0
                MeasureSet.execute("INSERT INTO settingsScanMeasure (name, bits, channel0, channel1, channel2, channel3, channel4, channel5, channel6, channel7, xstart, xstop, ystart, ystop, slope, subgrid, sympho, stack, plot) VALUES (\"" + name + "\", " + str(bits) + ", " + str(channel[0]) + ", " + str(channel[1]) + ", " + str(channel[2]) + ", " + str(channel[3]) + ", " + str(channel[4]) + ", " + str(channel[5]) + ", " + str(channel[6]) + ", " + str(channel[7]) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(slope) + ", " + str(subgrid) + ", " + str(sympho) + ", " + str(stack) + ", " + str(plot) + ")")
                MeasureSet.execute("SELECT * FROM settingsScanMeasure")
                connMeasure.commit()
                self.namesMeasure.addItem(name)

        def usesettingsScanMeasure(self):
                set = self.namesMeasure.currentText()
                MeasureSet.execute(("SELECT * FROM settingsScanMeasure WHERE name = \"") + set + ("\""))
                for dsatzMeasure in MeasureSet:
                        name = dsatzMeasure[0]
                        bits = dsatzMeasure[1]
                        channel0 = dsatzMeasure[2]
                        channel1 = dsatzMeasure[3]
                        channel2 = dsatzMeasure[4]
                        channel3 = dsatzMeasure[5]
                        channel4 = dsatzMeasure[6]
                        channel5 = dsatzMeasure[7]
                        channel6 = dsatzMeasure[8]
                        channel7 = dsatzMeasure[9]
                        xstart = dsatzMeasure[10]
                        xstop = dsatzMeasure[11]
                        ystart = dsatzMeasure[12]
                        ystop = dsatzMeasure[13]
                        slope = dsatzMeasure[14]
                        subgrid = dsatzMeasure[15]
                        sympho = dsatzMeasure[16]
                        stack = dsatzMeasure[17]
                        plot = dsatzMeasure[18]

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

                if channel0 == 1:
                        self.cbch21.setChecked(True)
                else:
                        self.cbch21.setChecked(False)
                if channel1 == 1:
                        self.cbch22.setChecked(True)
                else:
                        self.cbch22.setChecked(False)
                if channel2 == 1:
                        self.cbch23.setChecked(True)
                else:
                        self.cbch23.setChecked(False)
                if channel3 == 1:
                        self.cbch24.setChecked(True)
                else:
                        self.cbch24.setChecked(False)
                if channel4 == 1:
                        self.cbch25.setChecked(True)
                else:
                        self.cbch25.setChecked(False)
                if channel5 == 1:
                        self.cbch26.setChecked(True)
                else:
                        self.cbch26.setChecked(False)
                if channel6 == 1:
                        self.cbch27.setChecked(True)
                else:
                        self.cbch27.setChecked(False)
                if channel7 == 1:
                        self.cbch28.setChecked(True)
                else:
                        self.cbch28.setChecked(False)

                self.slideXStart.setValue(int(xstart))
                self.slideXStop.setValue(int(xstop))
                self.slideYStart.setValue(int(ystart))
                self.slideYStop.setValue(int(ystop))
                self.Slope1.setChecked(slope)
                self.Subgrid1.setChecked(subgrid)
                self.Sympho1.setChecked(sympho)
                self.Stack1.setChecked(stack)
                self.Plot1.setChecked(plot)

                if slope == True:
                        self.nameSlope.setText(name)
                        self.usesettingsScanSlope()
                else:
                        slope = 0
                if subgrid == True:
                        self.nameSync.setText(name)
                        self.usesettingsScanSync()
                else:
                        subgrid = 0
                if stack == True:
                        self.nameStack.setText(name)
                        self.usesettingsScanStack()
                else:
                        stack = 0
                connMeasure.commit()

        def clickedStart(self, down):                                                                                                                   #Setzt das Messfenster
                if down:
                        self.StartX = self.slideXStart.value()
                        self.StartY = self.slideYStop.value()
                        self.StopX = self.slideXStart.value()
                        self.StopY = self.slideYStop.value()                                                                           #Gibt den Geschwindigkeitswert im cmd aus
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
                        self.cb10.setChecked(True)
                        self.cb30.setChecked(True)
                elif checkedBits == 1:
                        self.bitval2 = 127                                                             
                        self.cb11.setChecked(True)                                                                  
                        self.cb31.setChecked(True)
                elif checkedBits == 2:
                        self.bitval2 = 255                                                        
                        self.cb12.setChecked(True)                                                              
                        self.cb32.setChecked(True)
                elif checkedBits == 3:
                        self.bitval2 = 511                                                       
                        self.cb13.setChecked(True)                                                             
                        self.cb33.setChecked(True)
                elif checkedBits == 4:
                        self.bitval2 = 1023                                                               
                        self.cb34.setChecked(True)
                elif checkedBits == 5:
                        self.bitval2 = 2047                                                                 
                        self.cb15.setChecked(True)                                                                  
                        self.cb35.setChecked(True)
                elif checkedBits == 6:
                        self.bitval2 = 4095
                        self.cb16.setChecked(True)
                        self.cb36.setChecked(True)
                self.stopAll3()

        def buttonUnchecked(self, val):
                global AnimationPlot1
                global AnimationPlot2
                global zNew
                global zNew2
                global t
                global tt
                if val == 1:
                        AnimationPlot1 = True
                        self.PlotWin.myFig1.resume()
                        AnimationPlot2 = True
                        self.PlotWin.myFig2.resume()
                        time.sleep(1)
                        #self.PlotWin.NewMaxMin(0, 300, 0)
                        #self.PlotWin.NewMaxMin(1, 300, 0)
                        self.PlotWin.NewLine2(zNew, zNew2, t, tt)
                        #print("Plot sent")
                        self.buttonStart.setToolTip("Start the Measurement")
                        self.buttonStart.setChecked(False)
                        self.buttonStart.setText("Start")
                        self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.NavWin.UncheckButton()
                        try:
                            #self.progress1.setValue(100)
                            AnimationPlot1 = False
                            self.PlotWin.myFig1.pause()
                            AnimationPlot2 = False
                            self.PlotWin.myFig2.pause()
                        except:
                            print("Failed1")
                        GPIO.output(LEDPin, GPIO.LOW)
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

        def plane_equation(self, p1, p2, p3):
                # Create two vectors in the plane
                v1 = p2 - p1
                v2 = p3 - p1

                # Calculate the normal vector
                normal = np.cross(v1, v2)

                # Calculate the equation of the plane: a*x + b*y + c*z + d = 0
                a, b, c = normal
                d = -np.dot(normal, p1)
                #d = 0
                #a = a *(-1)
                #b = b *(-1)
                #c = c *(-1)
                #d = d *(-1)

                #print("a b c" + str(a) + " + " + str(b) + " + " +str(c) + " + " + str(d))
                a = a/(-c)
                b = b/(-c)
                d = d/(-c)
                #print("a b c" + str(a) + " + " + str(b) + " + " +str(c) + " + " + str(d))
                return np.array([a, b, c, d])
        
        def calculate_z(self, plane_coeffs, x, y):
                a, b, c, d = plane_coeffs
                z = a*x + b*y + d
                #print("Eq: " + str(z) + " = " + str(a) + "*" + str(x) + " + " + str(b) + "*" + str(y) + " + " + str(d))

                return z

        def StartMeasurement(self, down):
                global PlotStyle
                global FileNameSub
                global FileName
                global FilePath
                global TTL1IN
                global TTL1OUT
                global TTL2IN
                global TTL2OUT
                global Wire1
                global Wire2
                global zVoltage
                global zStartX
                global zStartY
                global zStopX
                global zStopY
                global zBits
                global AnimationPlot1
                global AnimationPlot2
                #Jonas
                global XOffsetStart
                global YOffsetStart
                global DimensionStart
                global FullRangeDeviceX
                global FullRangeDeviceY
                
                #Start the Measurement-Thread        
                if down:
                        GPIO.output(LEDPin, GPIO.HIGH)
                        self.buttonStart.setToolTip("Stops the Measurement")                                                                            #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setText("Stop")
                        self.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")
                        self.NavWin.buttonStart.setToolTip("Stops the Measurement")                                                                     #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setText("Stop")
                        self.NavWin.buttonStart.setStyleSheet("background-color: rgb(255,63,0)")
                else:
                        self.buttonStart.setToolTip("Starts the Measurement")                                                                           #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setText("Start")                                                                                               #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")
                        self.NavWin.buttonStart.setToolTip("Starts the Measurement")                                                                    #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setText("Start")                                                                                        #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                        self.NavWin.buttonStart.setStyleSheet("color: black; background-color: rgb(0,255,0)")

                integrationtime = self.spinIntTime2.value()
                xstart = self.spinXStart.value()
                ystart = self.spinYStart.value()
                XOffsetStart = xstart
                YOffsetStart = ystart
                zstart = self.spinZFocus2.value()
                XOffset = int(xstart / ((FullRangeDeviceX/1000)/4096))                  #Unsicher
                YOffset = int(ystart / ((FullRangeDeviceY/1000)/4096))
                xDim = self.NavWin.SpinX.value()
                DimensionStart = xDim
                yDim = self.NavWin.SpinY.value()
                Volts = self.NavWin.Volts.currentText()
                Volts = round(xDim/10, 1)
                zVoltage = Volts
                bits = self.cbg2.checkedId()
                zBits = bits
                plot = self.Plot1.isChecked()
                colors = PlotStyle
                filenamesub = FileNameSub
                filename = FileName
                filepath = FilePath
                slope = self.Slope1.isChecked()
                subgrid = self.Subgrid1.isChecked()
                sympho = self.Sympho1.isChecked()
                subgridAuto = self.groupboxAuto.isChecked()
                if subgridAuto == True and subgrid == True:
                        self.NavWin.SaveFig()
                delaytime = self.delay.value()
                linetime = self.linetime.value()

                #NewSlope
                SetXSlope = self.XSlope + 2000
                SetYSlope = self.YSlope + 2000
                p1 = np.array([2047, 2047, 2000])
                p2 = np.array([4095, 2047, SetXSlope])
                p3 = np.array([2047, 4095, SetYSlope])
                plane_coeffs = self.plane_equation(p1, p2, p3)

                if Volts < 10:
                        #Positionen berechnen
                        OffsetSlopeX1 = XOffset + ((Volts*10)*(4095/(FullRangeDeviceX/1000)))
                        OffsetSlopeY1 = YOffset
                        OffsetSlopeZ1 = self.calculate_z(plane_coeffs, OffsetSlopeX1, OffsetSlopeY1)
                        OffsetSlopeX2 = XOffset
                        OffsetSlopeY2 = YOffset + ((Volts*10)*(4095/(FullRangeDeviceY/1000)))
                        OffsetSlopeZ2 = self.calculate_z(plane_coeffs, OffsetSlopeX2, OffsetSlopeY2)
                        OffsetSlopeX3 = XOffset
                        OffsetSlopeY3 = YOffset
                        OffsetSlopeZ3 = self.calculate_z(plane_coeffs, OffsetSlopeX3, OffsetSlopeY3)
                        p1 = np.array([0, 4095, self.calculate_z(plane_coeffs, OffsetSlopeX1, OffsetSlopeY1)])
                        p2 = np.array([4095, 0, self.calculate_z(plane_coeffs, OffsetSlopeX2, OffsetSlopeY2)])
                        p3 = np.array([0, 0, self.calculate_z(plane_coeffs, OffsetSlopeX3, OffsetSlopeY3)])
                        plane_coeffs = self.plane_equation(p1, p2, p3)

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
                PlotChannel1 = self.PlotWin.ch1Live1.currentIndex()
                PlotChannel2 = self.PlotWin.ch2Live1.currentIndex()

                #TTL definition                
                QuelleTTL = self.TTLroot2.currentIndex()
                Shutters = self.ShutterRoot2.currentIndex()
                """
                print("TTLRoot " + str(QuelleTTL))
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
                """

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

                #Start the Measurement-Thread        
                if down:
                        #self.stopAll()
                        self.clickedPos(False)
                        time.sleep(0.5)
                        print("WTF")
                        self.clickedPoint(False)
                        time.sleep(0.5)
                        print("WTF2")

                        try:
                                self.APDWin.StopMeasure()
                        except:
                                print("fail apd!")
                        #try:
                        #        self.TempSens.StopMeasure()
                        #except:
                        #        pass
                        print("WTF2")

                        xstartResize = 0
                        ystartResize = 0
                        xstopResize = bitval
                        ystopResize = bitval
                        print("WTF3")
                        
                        if sympho:
                                self.Olaf = SymPhoTimeScan(integrationtime, zstart, xDim, XOffset, YOffset, delaytime, linetime, bits, slope, SetXSlope, SetYSlope, plane_coeffs, Shutters)
                                self.Olaf.progress_value.connect(self.buttonUnchecked)
                                self.Olaf.progress_bar.connect(self.updateProgressBar1)
                                self.Olaf.start()
                        else:
                                self.ResizeLivePlot(xstartResize, xstopResize, ystartResize, ystopResize, bits)
                                #try:
                                if plot == True:
                                        AnimationPlot1 = True
                                        self.PlotWin.myFig1.resume()
                                        self.PlotWin.myFig2.resume()
                                self.Manfred = Measurement(integrationtime, channel, zstart, xDim, yDim, XOffset, YOffset, delaytime, bits, slope, subgrid, subgridAuto, sympho, plot, SetXSlope, SetYSlope, xstartsub, xstopsub, ystartsub, ystopsub, xstep, ystep, steptime, sendTTL, getTTL, QuelleTTL, Shutters, channeltimeing, DoStacks, stacks, stackstep, direct, ZStart, colors, filenamesub, filename, filepath, PlotChannel1, PlotChannel2, plane_coeffs)                                 #Übergibt die Werte an den Thread
                                self.Manfred.progress_value.connect(self.buttonUnchecked)
                                self.Manfred.progress_bar.connect(self.updateProgressBar1)
                                self.Manfred.progress_Filename.connect(self.updateLivePlotName)
                                self.Manfred.progress_values2.connect(self.updateLivePlot2)
                                self.Manfred.progress_Max.connect(self.updateLivePlotMax)
                                self.Manfred.start()
                                """
                                except:
                                        try:
                                                print("BreakManfred")
                                                self.Manfred.breakIt()
                                                self.Manfred.wait()
                                                self.Manfred = None
                                        except:
                                                pass
                                            
                                        print("Error")
                                        AnimationPlot1 = False
                                        self.PlotWin.myFig1.pause()
                                        AnimationPlot2 = False
                                        self.PlotWin.myFig2.pause()
                                        self.buttonUnchecked(1)
                                        GPIO.output(LEDPin, GPIO.LOW)
                                """
                        print("WTF4")
                else:
                        try:
                                print("BreakManfred")
                                self.Manfred.breakIt()
                                self.Manfred.wait()
                                self.Manfred = None
                        except:
                                pass
                        #try:
                        #        print("KillFredHard")
                        #        #self.Manfred.killFredHard()
                        #        self.Manfred.wait()
                        #        del self.Manfred
                        #except:
                        #        pass
                        #try:
                        #        self.Manfred.YRun = bitval
                        #        self.Manfred.XRun = bitval                                                                                                     #Die Variablen werden in nichtlokale Variablen umgewandelt
                        #except:
                        #        pass
                        #try:
                        #        self.Manfred.i = 1
                        #except:
                        #        pass
                        #try:
                        #        print("KillFredHard")
                        #        self.Manfred.killFredHard()
                        #        #self.Manfred.wait()
                        #        del self.Manfred
                        #except:
                        #        pass
                        #try:
                        #        print("terminate Fred")
                        #        self.Manfred.terminate()
                        #except:
                        #        pass
                        try:
                                print("BreakOlaf")
                                self.Olaf.breakIt()
                                self.Olaf.wait()
                                self.Olaf = None
                        except:
                                pass
                        AnimationPlot1 = False
                        self.PlotWin.myFig1.pause()
                        AnimationPlot2 = False
                        self.PlotWin.myFig2.pause()
                        self.buttonUnchecked(1)
                        GPIO.output(LEDPin, GPIO.LOW)

        def updateLivePlot(self, zNew, zNew2):
                if self.Plot1.isChecked():
                        self.PlotWin.NewLine(zNew, zNew2)

        def updateLivePlot2(self, zNew, zNew2, t, tt):
                if self.Plot1.isChecked():
                        self.PlotWin.NewLine2(zNew, zNew2, t, tt)

        def updateLivePlotMax(self, plotnum, max, min):
                if self.Plot1.isChecked():
                        self.PlotWin.NewMaxMin(plotnum, max, min)

        def updateLivePlotName(self, Date):
                if self.Plot1.isChecked():
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

                delaytime = self.delay.value()
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
                    SubgridTime = ((bits/xstep) * (bits/ystep) * (TTLTime + SendTime))
                elif sendTTL == True:
                    SubgridTime = ((bits/xstep) * (bits/ystep) * (steptime + SendTime))
                else:
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
                TimeMins = ExTime // 60
                TimeSecs1 = ExTime % 60
                TimeSecs = TimeSecs1 // 1
                TimeMilsecs = round(((TimeSecs1 % 1) * 1000), 2)
                self.labelProgTime.setText("Expected Time:\t" + str(int(TimeMins)) + " min  \t" + str(int(TimeSecs)) + " s\t" + str(int(TimeMilsecs)) + " ms\nPixelsize:\t" + str(pixelsizeX) + " x " + str(pixelsizeY) + " nm" + " s\nWindowsize:\t" + str(XDist) + " x " + str(YDist) + " [\u03BCm]")                                                                  #Setzt ein Label 

        def updateProgressBar1(self, val):
                try:
                        #pass
                        self.progress1.setValue(val)
                except:
                        print("Failed2")

        #Tab3 - TTL-Sync Functions
        def AddCoordinate(self):
                self.AddX = int(round((self.spinAddPosX.value()*1000)/((FullRangeDeviceX/1000)/self.bitval)/1000,0))
                self.AddY = int(round((self.spinAddPosY.value()*1000)/((FullRangeDeviceY/1000)/self.bitval)/1000,0))
                self.NavWin.AddCoordinates(self.AddX, self.AddY)

        def LoadSync1(self):
                global zNew
                global coordinatesTTL
                data = zNew
                past = 0
                dist = 2

                if self.cbCount.isChecked():
                        num_max = self.spinCount.value()
                        image, im, coordinates, low = MaxDetectLib.Maxima_Detection_NumMax(data, num_max, dist)
                        self.spinCount.setValue(len(coordinates))
                        self.spinTh.setValue(low)
                else:
                        Th = self.spinTh.value()
                        image, im, coordinates, low = MaxDetectLib.Maxima_Detection_Threshold(data, Th, dist)
                        self.spinCount.setValue(len(coordinates))
                        self.spinTh.setValue(low)

                self.labelPoints.setText("Number of Subgridpoints: " + str(len(coordinates)))
                coordinatesTTL = coordinates
                self.NavWin.UpdateFromTTL(past, coordinates)

        def LoadSync2(self):
                global zNew2
                global coordinatesTTL
                data = zNew2
                past = 1
                num_max = self.spinCount.value()
                dist = 2

                if self.cbCount.isChecked():
                        num_max = self.spinCount.value()
                        image, im, coordinates, low = MaxDetectLib.Maxima_Detection_NumMax(data, num_max, dist)
                        self.spinCount.setValue(len(coordinates))
                        self.spinTh.setValue(low)
                else:
                        Th = self.spinTh.value()
                        image, im, coordinates, low = MaxDetectLib.Maxima_Detection_Threshold(data, Th, dist)
                        self.spinCount.setValue(len(coordinates))
                        self.spinTh.setValue(low)

                self.labelPoints.setText("Number of Subgridpoints: " + str(len(coordinates)))
                coordinatesTTL = coordinates
                self.NavWin.UpdateFromTTL(past, coordinates)

        def PlotMax(self, image, image_show, coordinates, low):
                global HydraCMAP2
                global HydraCMAP2_r
                global HydraCMAP
                global HydraCMAP_r

                self.HydraCMAP = HydraCMAP2
                self.HydraCMAP_r = HydraCMAP2_r

		#Show results
                fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True)
                ax = axes.ravel()
                ax[0].imshow(image, cmap=self.HydraCMAP)
                ax[0].axis('off')
                ax[0].set_title('Original')

                name = "Threshold filter: " + str(low)
                ax[1].imshow(image_show, cmap=self.HydraCMAP)
                ax[1].axis('off')
                ax[1].set_title(name)

                name = "LocalMax with " + str(len(coordinates)) + " Maxima"
                ax[2].imshow(image, cmap=self.HydraCMAP)
                ax[2].autoscale(False)
                ax[2].plot(coordinates[:, 1], coordinates[:, 0], color='white', marker='x', markersize=15, linestyle='none')
                ax[2].axis('off')
                ax[2].set_title(name)

                fig.tight_layout()

                plt.show()

        def updateManuelGrid(self, down):
                if down == True:
                        self.groupboxAuto.setChecked(False)

        def updateAutoGrid(self, down):
                if down == True:
                        self.groupboxManuel.setChecked(False)
                else:
                        self.groupboxManuel.setChecked(True)

        def ThChange(self):
                down = self.cbTh.isChecked()
                if down == True:
                        self.cbCount.setChecked(False)
                else:
                        self.cbCount.setChecked(True)

        def CountChange(self):
                down = self.cbCount.isChecked()
                if down == True:        
                        self.cbTh.setChecked(False)
                else:
                        self.cbTh.setChecked(True)

        def slideXstart2(self):
                global FullRangeDeviceX
                NewVal = round((self.slideXStart2.value()*(FullRangeDeviceX/1000)/self.bitval3),3)
                if NewVal != self.spinXStart2.value():
                        self.StartX2 = (self.slideXStart2.value() / (FullRangeDeviceX/1000))                                                                                #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
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
                        self.StartX2 = (self.spinXStart2.value() / (FullRangeDeviceX/1000))
                        self.CalcPoints()
                        self.updateProgTime()

        def slideYstart2(self):                 
                global FullRangeDeviceY
                NewVal = round((self.slideYStart2.value()*(FullRangeDeviceY/1000)/self.bitval3),3)
                if NewVal != self.spinYStart2.value():
                        self.StartY2 = (self.slideYStart2.value() / (FullRangeDeviceY/1000))                                                                                #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
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
                        self.StartY2 = (self.spinYStart2.value() / (FullRangeDeviceY/1000))
                        self.CalcPoints()
                        self.updateProgTime()

        def slideXstop2(self):                 
                global FullRangeDeviceX
                NewVal = round((self.slideXStop2.value()*(FullRangeDeviceX/1000)/self.bitval3),3)
                if NewVal != self.spinXStop2.value():
                        self.StopX2 = (self.slideXStop2.value() / (FullRangeDeviceX/1000))                                                                                  #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStop2.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStep.setMaximum(self.slideXStop2.value() - self.slideXStart2.value())
                        self.spinXStep.setMaximum(round(self.slideXStop2.value()*((FullRangeDeviceX/1000)/self.bitval3),3)-round(self.slideXStart2.value()*((FullRangeDeviceX/1000)/self.bitval3),3))
                        self.CalcPoints()
                        self.updateProgTime()                                                                                                           #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen

        def spinXstop2(self):
                global FullRangeDeviceX
                NewVal = int(round(self.spinXStop2.value()/((FullRangeDeviceX/1000)/self.bitval3),0))
                if NewVal != self.spinXStop2.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StopX2 = (self.spinXStop2.value() / (FullRangeDeviceX/1000)) 
                        self.slideXStop2.setValue(int(NewVal))                                                                                          #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideXStep.setMaximum(self.slideXStop2.value() - self.slideXStart2.value())
                        self.spinXStep.setMaximum(round(self.slideXStop2.value()*((FullRangeDeviceX/1000)/self.bitval3),3)-round(self.slideXStart2.value()*((FullRangeDeviceX/1000)/self.bitval3),3))
                        self.CalcPoints()
                        self.updateProgTime()

        def slideYstop2(self):                 
                global FullRangeDeviceY
                NewVal = round((self.slideYStop2.value()*(FullRangeDeviceY/1000)/self.bitval3),3)
                if NewVal != self.spinYStop2.value():
                        self.StopY2 = (self.slideYStop2.value() / (FullRangeDeviceY/1000))                                                                                  #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStop2.setValue(NewVal)                                                                                                #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStep.setMaximum(self.slideYStop2.value() - self.slideYStart2.value())
                        self.spinYStep.setMaximum(int(round(self.slideYStop2.value()*(FullRangeDeviceY/self.bitval3),3))-int(round(self.slideYStart2.value()*(FullRangeDeviceY/self.bitval3),3)))
                        self.CalcPoints()
                        self.updateProgTime()                                                                                                           #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen

        def spinYstop2(self):
                global FullRangeDeviceY
                NewVal = int(round(self.spinYStop2.value()/((FullRangeDeviceY/1000)/self.bitval3),0))
                if NewVal != self.spinYStop2.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StopY2 = (self.spinYStop2.value() / (FullRangeDeviceY/1000)) 
                        self.slideYStop2.setValue(int(NewVal))                                                                                          #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.slideYStep.setMaximum(self.slideYStop2.value() - self.slideYStart2.value())
                        self.spinYStep.setMaximum(int(round(self.slideYStop2.value()*(FullRangeDeviceY/self.bitval3),3))-int(round(self.slideYStart2.value()*(FullRangeDeviceY/self.bitval3),3)))
                        self.CalcPoints()
                        self.updateProgTime()

        def slideXstep(self):
                global FullRangeDeviceX
                NewVal = round(self.slideXStep.value()*((FullRangeDeviceX/1000)/self.bitval3),3)
                if NewVal != self.spinXStep.value():                                                                                                    #Gibt den Wert des Sliders im cmd aus
                        self.StepX = int(self.slideXStep.value()/(FullRangeDeviceX/1000))                                                                                   #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinXStep.setValue(NewVal)      
                        self.CalcPoints()                                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.updateProgTime()

        def spinXstep(self):                                                                                                                            #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                global FullRangeDeviceX
                NewVal = int(round(self.spinXStep.value()/((FullRangeDeviceX/1000)/self.bitval3),3))
                if NewVal != self.slideXStep.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StepX = (NewVal / (FullRangeDeviceX/1000))                                                                                                     #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideXStep.setValue(int(NewVal))  
                        self.CalcPoints()                                                                                                               #Setzt den Wert des Sliders auf den Wert der Zahlenauswahlbox
                        self.updateProgTime()

        def slideYstep(self):
                global FullRangeDeviceY
                NewVal = round(self.slideYStep.value()*((FullRangeDeviceY/1000)/self.bitval3),3)
                if NewVal != self.spinYStep.value():                                                                                                    #Gibt den Wert des Sliders im cmd aus
                        self.StepY = (self.slideYStep.value()/(FullRangeDeviceY/1000))                                                                                      #Rechnet den Wert des Sliders in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.spinYStep.setValue(NewVal)      
                        self.CalcPoints()                                                                                                               #Ruft die clickedM2-Funktion auf und übergibt den Bool-Wert des checkbaren Buttons, so kann der Motor im Betrieb gesteuert werden
                        self.updateProgTime()

        def spinYstep(self):                                                                                                                            #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                global FullRangeDeviceY
                NewVal = int(round(self.spinYStep.value()/((FullRangeDeviceY/1000)/self.bitval3),3))
                if NewVal != self.slideYStep.value():                                                                                                   #Gibt den Wert der Zahlauswahlbox im cmd aus
                        self.StepY = int(NewVal / (FullRangeDeviceY/1000))                                                                                                  #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                        self.slideYStep.setValue(int(NewVal))  
                        self.CalcPoints()                                                                                                               #Setzt den Wert des Sliders auf den Wert der Zahlenauswahlbox
                        self.updateProgTime()

        def spinsteptime(self):                                                                                                                         #Gibt den Wert der Zahlauswahlbox im cmd aus
                self.StepTime = (self.spinStepTime.value() / (FullRangeDeviceY/1000))   
                self.CalcPoints()                                                                                                                       #Rechnet den Wert der Zahlauswahlbox in eine Geschwindigkeit (Wert zwischen 0 und 1) um und speichert ihn in der Geschwindigkeitsvariablen
                self.updateProgTime()

        def savesettingsScanSync(self):
                name = self.nameSync.text()
                if len(name) == 0:
                        name = time.strftime("%d.%m.%Y %H:%M:%S")
                bits = self.cbg3.checkedId()
                xstart = self.spinXStart2.value()
                xstop = self.spinXStop2.value()
                ystart = self.spinYStart2.value()
                ystop = self.spinYStop2.value()
                if self.groupboxManuel.isChecked():
                        manuelauto = 1
                elif self.groupboxAuto.isChecked():
                        manuelauto = 2
                xstep = self.spinXStep.value()
                ystep = self.spinYStep.value()
                steptime = self.spinStepTime.value()
                sendTTL = self.groupboxSendTTL3.isChecked()
                getTTL = self.TTLgetPoint2.isChecked()
                channel = self.channeltimeing.isChecked()
                ttl = self.TTLroot2.currentIndex()

                SyncSet.execute("INSERT INTO settingsScanSync (name, bits, xstart, xstop, ystart, ystop, manuelauto, xstep, ystep, steptime, sendTTL, getTTL, ttl, channel) VALUES (\"" + name + "\", " + str(bits) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(manuelauto) + ", " + str(xstep) + ", " + str(ystep) + ", " + str(steptime) + ", " + str(sendTTL) + ", " + str(getTTL) + ", " + str(ttl) + ", " + str(channel) + ")")
                SyncSet.execute("SELECT * FROM settingsScanSync")
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
                        manuelauto = dsatzSync[6]
                        xstep = dsatzSync[7]
                        ystep = dsatzSync[8]
                        steptime = dsatzSync[9]
                        sendTTL = dsatzSync[10]
                        getTTL = dsatzSync[11]
                        ttl = dsatzSync[12]
                        channel = dsatzSync[13]
                        #print(str(name) + ", " + str(bits) + ", " + str(xstart) + ", " + str(xstop) + ", " + str(ystart) + ", " + str(ystop) + ", " + str(xstep) + ", " + str(ystep) + ", " + str(steptime) + ", " + str(sendTTL) + ", " + str(getTTL))

                if manuelauto == 1:
                        self.groupboxManuel.setChecked(True)
                        self.groupboxAuto.setChecked(False)
                else:
                        self.groupboxManuel.setChecked(False)
                        self.groupboxAuto.setChecked(True)

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

                self.spinXStart2.setValue(int(xstart))
                self.spinXStop2.setValue(int(xstop))
                self.spinYStart2.setValue(int(ystart))
                self.spinYStop2.setValue(int(ystop))
                self.spinXStep.setValue(int(xstep))
                self.spinYStep.setValue(int(ystep))
                self.spinStepTime.setValue(float(steptime))
                self.groupboxSendTTL3.setChecked(sendTTL)
                self.TTLgetPoint2.setChecked(getTTL)
                self.TTLroot2.setCurrentIndex(ttl)
                self.channeltimeing.setChecked(channel)

                self.stopAll3()
                connSync.commit()

        def CalcPoints(self):
                XStop = self.spinXStop2.value()
                XStart = self.spinXStart2.value()
                XStep = self.spinXStep.value()
                YStop = self.spinYStop2.value()
                YStart = self.spinYStart2.value()
                YStep = self.spinYStep.value()

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
                self.NavWinBits(checkedBits)

                if checkedBits == 0:
                        self.cb10.setChecked(True)
                        self.cb20.setChecked(True)                                                                                                                    #Setzt 11 Rastpunkte also je einen alle 10 Schritte
                        self.bitval3 = 64
                elif checkedBits == 1:
                        self.bitval3 = 128
                        self.cb11.setChecked(True)
                        self.cb21.setChecked(True) 
                elif checkedBits == 2:
                        self.bitval3 = 256
                        self.cb12.setChecked(True)
                        self.cb22.setChecked(True) 
                elif checkedBits == 3:
                        self.bitval3 = 512
                        self.cb13.setChecked(True)
                        self.cb23.setChecked(True) 
                elif checkedBits == 4:
                        self.bitval3 = 1024
                        self.cb14.setChecked(True)
                        self.cb24.setChecked(True) 
                elif checkedBits == 5:
                        self.bitval3 = 2048
                        self.cb15.setChecked(True)
                        self.cb25.setChecked(True) 
                elif checkedBits == 6:
                        self.bitval3 = 4096
                        self.cb16.setChecked(True)
                        self.cb26.setChecked(True) 

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
                                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                        else:  
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStack/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]" + "\t\tOut of Range") 
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_red.png")
                                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                elif self.ZDirection.currentIndex() == 1:
                        if (StackSize*1000)<=StackStart:
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((StackStart/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]")
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_green.png")
                                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                        else:  
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((StackStart/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]" + "\t\tOut of Range") 
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_red.png")
                                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                elif self.ZDirection.currentIndex() == 2:
                        UpLimit = MaxStackSize - StackStart
                        DownLimit = StackStart
                        if ((StackSize / 2) * 1000) <= UpLimit and ((StackSize / 2) * 1000) <= DownLimit:
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStackSize/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]")
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_green.png")
                                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
                                self.labelAmpel.setPixmap(pixmap_mini)
                                self.labelAmpel.show()
                        else:  
                                self.labelStackSize.setText("Maximum Stacksize: " + str(round((MaxStackSize/1000),2)) + " [\u03BCm]\nStacksize: " + str(StackSize) + " [\u03BCm]" + "\t\tOut of Range") 
                                pixmap = QPixmap("/home/pi/Desktop/HydraScan/Files/Ampel_red.png")
                                pixmap_mini = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
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
                print(SlopeXNew)
                print(SlopeYNew)
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
                        #print("Slope already Set")
                        self.buttonXSlope.setToolTip("Starts Slopesetup")                                                                               #Setzt den MouseOver-ToolTip des Motor-Startbuttons um

        def SlopeStartY(self, down):                                                                                                                    #Setzt das Messfenster
                if down:
                        dacX.set_voltage(int(4095/2))
                        dacY.set_voltage(4095)                  
                        self.YSlope = self.slideYSlope.value()
                        dacZ.set_voltage(int(self.YSlope + 2000))
                        self.buttonYSlope.setToolTip("Set Slope")                                                                                       #Setzt den MouseOver-ToolTip des Motor-Startbuttons um
                else:
                        #print("Slope already Set")
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
                xslope = int(self.slideXSlope.value())
                yslope = int(self.slideYSlope.value())

                SlopeSet.execute("INSERT INTO settingsScanSlope (name, xslope, yslope) VALUES (\"" + name + "\", " + str(xslope) + ", " + str(yslope) + ")")
                SlopeSet.execute("SELECT * FROM settingsScanSlope")
                connSlope.commit()
                self.namesSlope.addItem(name)

        def usesettingsScanSlope(self):
                set = self.namesSlope.currentText()
                SlopeSet.execute(("SELECT * FROM settingsScanSlope WHERE name = \"") + set + ("\""))
                for dsatzSlope in SlopeSet:
                        name = dsatzSlope[0]
                        xslope = dsatzSlope[1]
                        yslope = dsatzSlope[2]

                self.slideXSlope.setValue(int(xslope))
                self.spinXSlope.setValue(int(xslope))
                self.slideYSlope.setValue(int(yslope))
                self.spinYSlope.setValue(int(yslope))
                self.XSlope = xslope
                self.YSlope = yslope
                
                connSlope.commit()

        #Alle Tabs - Ende Funktion
        def UpdateFilePath(self):
                global MainPath
                self.labelPath.setText("Filepath: " + str(MainPath))

        def UpdateTTLNames(self):
                self.TTLroot.setItemText(0, TTLOUT3["Name"])
                self.TTLroot.setItemText(1, TTLOUT4["Name"])
                self.TTLroot.setItemText(2, TTLOUT5["Name"])
                self.TTLroot.setItemText(3, TTLOUT6["Name"])
                self.TTLroot2.setItemText(0, TTLOUT3["Name"])
                self.TTLroot2.setItemText(1, TTLOUT4["Name"])
                self.TTLroot2.setItemText(2, TTLOUT5["Name"])
                self.TTLroot2.setItemText(3, TTLOUT6["Name"])
                self.ShutterRoot1.setItemText(0,TTLOUT7["Name"])
                self.ShutterRoot1.setItemText(1,TTLOUT8["Name"])
                self.ShutterRoot2.setItemText(0,TTLOUT7["Name"])
                self.ShutterRoot2.setItemText(1,TTLOUT8["Name"])

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
                global StartValX
                global StartValY
                global FocusZ
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
                        connFile.commit()                                                           
                        connFile.close()
                except:
                        connFile.close()
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
                        dacX.set_voltage(StartValX, persist=True)
                        dacY.set_voltage(StartValY, persist=True)
                        dacZ.set_voltage(FocusZ, persist=True)
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
                try:
                        self.APDWin.WindowClose()
                except:
                        pass
                try:
                        self.TempSens.WindowClose()
                except:
                        pass
                try:
                        self.PlotWin.WindowClose()
                except:
                        pass
                #try:
                self.close_NavWin()
                #except:
                #        pass
                GPIO.output(LEDPin, GPIO.LOW)
                GPIO.cleanup()
                Fenster.quitall(self)
                print("Programm beendet")

                sys.exit()                                                                                                                              #Beendet das Fenster


"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 9: Positioning Subclasses -----------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
#Positioning Subclass is a new Thread that is started in Tab1
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

                self.killFred()

        def killFred(self):
                self.i = 1
                if self.Logic == 1:
                        APDs.closeDevice()
                try:
                        adc.stop_adc()
                except:
                        pass
                print("Fred beendet")

#Pointmeasurement Subclass is a new Thread that is started in Tab1
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
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoDistanceZ
                global DeviceVoltage
                global PiezoVoltage
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
                PiezoX = PiezoDistanceX * (DeviceVoltage/PiezoVoltage)
                PiezoY = PiezoDistanceY * (DeviceVoltage/PiezoVoltage)
                self.XPointYM = ((PiezoX/(self.BitsPoint-1))*XPoint)/1000
                self.YPointYM = ((PiezoY/(self.BitsPoint-1))*YPoint)/1000
                self.ZPointYM = ((PiezoDistanceZ/(4095))*ZPoint)/1000

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
                global FilePath
                global FileNamePoint
                global Meta
                global LaserWL
                global LaserPower
                global Filter
                global Sample

                if self.Logic == 1:
                        if APDArduinoOn == 1:
                                APDs = ArduinoLogic()
                        elif APDBSOn == 1:
                                APDs = APDLogic(5000,self.IntegrationTime) 
                
                #Datafile
                self.DateTime = time.strftime("%d.%m.%Y %H:%M:%S")                                                                                      #Bestimmt das Datum und die Uhrzeit zu beginn der Messung
                self.DateTime2 = time.strftime(FilePath + FileNamePoint + "_%d-%m-%Y_%H-%M-%S.txt")                                          #Setzt den Dateiname der txt-Datei
                self.DateTime4 = time.strftime(FilePath + FileNamePoint + "_%d-%m-%Y_%H-%M-%S.png")                                          #Setzt den Dateiname der png-Datei
                self.DateTime5 = time.strftime(FileNamePoint + " %d.%m.%Y %H:%M:%S")

                self.Txt_Point = open(self.DateTime2, "w")                                                                                              #Erstellt und öffnet eine neue Datei im Schreibmodus

                self.Txt_Point.write("Pointmeasurement for " + str(self.PointDelay) + " Seconds\n")                                                     #Schreibt die Messschranke in die txt-Datei

                if self.TTLsendPoint == True:
                        if self.TTLgetPoint == True:
                                self.Txt_Point.write("TTL sent and recived\n")
                        else:
                                self.Txt_Point.write("TTL sent\n")
                
                self.Txt_Point.write("Measurement with " + str(self.BitsPoint) + " Pixel\n")                                                            #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Point.write("Date: " + self.DateTime + "\n")                                                                   #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Point.write("X-Position: " + str(self.XPointYM) + "\tY-Position: " + str(self.YPointYM) + "\tZ-Position: " + str(self.ZPointYM))                                                                                 #Schreibt das Datum und die Uhrzeit in die txt-Datei
                
                if DHTon == 1:
                        global DHTPin
                        try:
                                humidity, temperature = Adafruit_DHT.read_retry(TempSens, DHTPin)
                                self.Txt_Point.write("Temperature: " + str(temperature) + " *C\tHumidity: " + str(humidity) + " %\n")
                        except:
                                pass
                else:
                        pass

                if Meta == 1:
                        self.Txt_Point.write("\n")
                        self.Txt_Point.write("----------------------- Meta Data -----------------------\n")  
                        if LaserWL:
                                self.Txt_Point.write("Laser Wavelength: " + LaserWL + "\n")  
                        if LaserPower:
                                self.Txt_Point.write("Laser Power: " + LaserPower + "\n")  
                        if Filter:
                                self.Txt_Point.write("Filter: " + Filter + "\n")  
                        if Sample:
                                self.Txt_Point.write("Sample: " + Sample + "\n")  
                        self.Txt_Point.write("---------------------------------------------------------")
                        self.Txt_Point.write("\n")
                
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

        def killFred(self):     
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 10: Measurement Subclasses -----------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

class SymPhoTimeScan(QThread):
        progress_bar = pyqtSignal(int)
        progress_value = pyqtSignal(int)

        def __init__(self, integrationtime, zstart, xDim, xoff, yoff, delaytime, linetime, bits, slope, SetXSlope, SetYSlope, plane_coeffs, Shutters, parent=None):
                QThread.__init__(self, parent)
                global LEDPin
                global PiezoDistanceZ
                global TTLOUT1 
                global TTLOUT2
                #global FocusZ
                
                print("Olaf läuft")

                #Establishing TTL
                self.SymphoOut1 = TTLOUT1["Pin"]
                self.SymphoOut2 = TTLOUT2["Pin"]

                
                self.Shutters = Shutters

                self.IntegrationTime = integrationtime/1000
                self.XSlopeUpper = SetXSlope                                                                                                            #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YSlopeUpper = SetYSlope
                self.plane_coeffs = plane_coeffs
                """print(self.plane_coeffs)
                print("Calc Z (0,0): " + str(self.calculate_z(0, 0)))
                print("Calc Z (256,256): " + str(self.calculate_z(256, 256)))
                print("Calc Z (512,512): " + str(self.calculate_z(512, 512)))
                print("Calc Z (2047,2047): " + str(self.calculate_z(2047, 2047)))
                print("Calc Z (4095,4095): " + str(self.calculate_z(4095, 4095)))
                print("Calc Z (2047,4095): " + str(self.calculate_z(2047, 4095)))
                print("Calc Z (4095,2047): " + str(self.calculate_z(4095, 2047)))"""
                self.LineTime = linetime/1000
                self.BitsValue = bits
                self.Slope1 = slope
                self.FocusZ = int(((zstart*1000)/PiezoDistanceZ)*4096)
                        
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

                self.i = 0
                self.XRun = self.XStartValue
                self.YRun = self.YStartValue
                #self.ZRun = self.ZStartValue
                time.sleep(0.5)

                self.Voltage = round(xDim/10,1)
                Poti.write_range(self.Voltage)

                self.XOffset = xoff
                self.YOffset = yoff
                dacOffset.setAllVoltage(self.XOffset, self.YOffset, 0, 0)

                self.Voltage = 5
                self.XOffset = 2047
                self.YOffset = 2047


                #GPIO.setup(self.SymphoOut1, GPIO.OUT)
                #GPIO.setup(self.SymphoOut2, GPIO.OUT)
                GPIO.output(self.SymphoOut1, GPIO.LOW)
                GPIO.output(self.SymphoOut2, GPIO.LOW)

                self._running = True
                
                time.sleep(2)

        def run(self):
                global StartValX
                global StartValY
                global FocusZ
                global TTLOUT7
                global TTLOUT8
                global ShutterMode

                print("Messung Start")
                if self.Shutters == 0 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                        if ShutterMode[0] == 0:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                        elif ShutterMode[0] == 1:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                if self.Shutters == 1 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                        if ShutterMode[1] == 0:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                        elif ShutterMode[1] == 1:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                dacZ.set_voltage(self.FocusZ)
                while self.i == 0:
                        if not self._running:
                                break
                        GPIO.output(self.SymphoOut1, GPIO.HIGH)
                        while self.YRun <= self.YStopValue:
                                if not self._running:
                                        break

                                print("Line Start")
                                if self.Shutters == 0 or self.Shutters == 2:
                                        if ShutterMode[0] == 2:
                                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                        elif ShutterMode[0] == 3:
                                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                                time.sleep(0.1)
                                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                if self.Shutters == 1 or self.Shutters == 2:
                                        if ShutterMode[1] == 2:
                                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                        elif ShutterMode[1] == 3:
                                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                                time.sleep(0.1)
                                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                                dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                time.sleep(self.LineTime)
                                GPIO.output(self.SymphoOut2, GPIO.HIGH)
                                dacY.set_voltage(int(self.YRun * (4095 / self.BitsValue)))
                                while self.XRun <= self.XStopValue:
                                        if not self._running:
                                                break
                                        if self.Slope1 == True:
                                                #XSlopePos = (self.XSlopeUpper - (self.XRun * ((self.XSlopeUpper*2)/self.BitsValue)))
                                                #YSlopePos = (self.YSlopeUpper - (self.YRun * ((self.YSlopeUpper*2)/self.BitsValue)))
                                                #SlopePos = (XSlopePos + YSlopePos)
                                                #SlopeVal = ((((SlopePos + 2000) / 4000) * self.BitsValue))
                                                #SlopeVal = self.calculate_z(self.XRun, self.YRun)
                                                #ZPosition = int(SlopeVal * (4095 / self.BitsValue))
                                                #print(self.XRun)
                                                ZPosition = int(self.calculate_z(int(self.XRun * (4095 / self.BitsValue)), int(self.YRun * (4095 / self.BitsValue))))
                                        else:
                                                ZPosition = self.FocusZ
                                        dacZ.set_voltage(ZPosition)
                                        dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                        #print("Position: " + str(int(self.XRun * (4095 / self.BitsValue))) + " x " + str(int(self.YRun * (4095 / self.BitsValue))) + " x " + str(ZPosition))
                                        self.XRun = self.XRun + 1
                                        time.sleep(self.IntegrationTime)
                                GPIO.output(self.SymphoOut2, GPIO.LOW)

                                print("Line Stop")
                                if self.Shutters == 0 or self.Shutters == 2:
                                        if ShutterMode[0] == 2:
                                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                        elif ShutterMode[0] == 3:
                                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                                time.sleep(0.1)
                                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                if self.Shutters == 1 or self.Shutters == 2:
                                        if ShutterMode[1] == 2:
                                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                        elif ShutterMode[1] == 3:
                                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                                time.sleep(0.1)
                                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)


                                self.YRun = self.YRun + 1
                                while self.XRun > self.XStartValue:
                                        dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                        self.XRun -= 1
                                self.XRun = self.XStartValue
                                progress = int((self.YRun) * (100 / (self.YStopValue)))
                                self.progress_bar.emit(progress)
                        GPIO.output(self.SymphoOut1, GPIO.LOW)


                        self.i = 1

                print("Messung Stop")
                if self.Shutters == 0 or self.Shutters == 2:
                        if ShutterMode[0] == 0:
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        elif ShutterMode[0] == 1:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                if self.Shutters == 1 or self.Shutters == 2:
                        if ShutterMode[1] == 0:
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                        elif ShutterMode[1] == 1:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                time.sleep(0.5)

                                
                YDown = self.YStopValue
                XDown = self.XStopValue
                XOff = self.XOffset
                YOff = self.YOffset
                print(self.Voltage)
                if self.Voltage >= 9.6:
                        print("Way back!")
                        while XDown > 0:
                                dacOffset.setAllVoltage(XDown, YDown, 0, 0)
                                XDown -= 4
                                time.sleep(0.001)
                        while YDown > 0:
                                dacOffset.setAllVoltage(XDown, YDown, 0, 0)
                                YDown -= 4
                                time.sleep(0.001)
                        print("Way back!")
                else:
                        print("Way back2!")
                        while YDown > 0:
                                dacX.set_voltage(YDown)
                                YDown -= 4
                                time.sleep(0.001)
                        while XDown > 0:
                                dacY.set_voltage(XDown)
                                XDown -= 4
                                time.sleep(0.001)
            
                        print("Way back2.1!")
                        while XOff > 0:
                                dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                                XOff -= 4
                                time.sleep(0.001)
                        while YOff > 0:
                                dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                                YOff -= 4
                                time.sleep(0.001)
                                
                        print("Way back2!")
                
            
                #print("YDown" + str(YDown))
                #print("XDown" + str(XDown))
                #print("XOff" + str(XOff))
                #print("YOff" + str(YOff))
                #print("StartValX" + str(StartValX))
                #print("StartValY" + str(StartValY))
                
                #print("Way back3!")
                while XOff < StartValX:
                        #print("XOff" + str(XOff))
                        dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                        XOff += 4
                        time.sleep(0.001)
                while YOff < StartValY:
                        #print("YOff" + str(YOff))
                        dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                        YOff += 4
                        time.sleep(0.001)

                #print("YDown" + str(YDown))
                #print("XDown" + str(XDown))
                #print("XOff" + str(XOff))
                #print("YOff" + str(YOff))
                #print("StartValX" + str(StartValX))
                #print("StartValY" + str(StartValY))
                dacX.set_voltage(0)
                dacY.set_voltage(0)
                dacZ.set_voltage(FocusZ)
                dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
                
                
                self.progress_bar.emit(100)
                self.progress_value.emit(1)
                print("Olaf gestoppt")

                return
                #self.terminate()

        def breakIt(self):
                self.i = 1
                self._running = False

        def calculate_z(self, x, y):
                a, b, c, d = self.plane_coeffs
                z = a*x + b*y + d
                #print("Eq: " + str(z) + " = " + str(a) + "*" + str(x) + " + " + str(b) + "*" + str(y) + " + " + str(d))

                return z


class Measurement(QThread):
        progress_value = pyqtSignal(int)
        progress_bar = pyqtSignal(int)
        progress_Filename = pyqtSignal(str)
        #progress_values = pyqtSignal(list, list)
        progress_values2 = pyqtSignal(object, object, object, object)
        progress_Max = pyqtSignal(int, object, object)

        def __init__(self, integrationtime, channel, zstart, xDim, yDim, xoff, yoff, delaytime, bits, slope, subgrid, subgridAuto, sympho, plot, SetXSlope, SetYSlope, xstartsub, xstopsub, ystartsub, ystopsub, xstep, ystep, steptime, sendTTL, getTTL, QuelleTTL, Shutters, channeltimeing, DoStacks, stacks, stackstep, direct, ZStart, colors, filenamesub, filename, filepath, PlotChannel1, PlotChannel2, plane_coeffs, parent=None):
                QThread.__init__(self, parent)
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
                global coordinatesTTL
                global Version
                global PiezoDistanceX
                global PiezoDistanceY
                global PiezoDistanceZ
                global PiezoVoltage
                global DeviceVoltage
                global FilePath
                global FileName
                global FileNameSub
                global Meta
                global LaserWL
                global LaserPower
                global Filter
                global Sample
                global CurrentOffsetX 
                global CurrentOffsetY 
                global CurrentPoti 
                global ZoomedNav
                global TTLOUT3
                global TTLOUT4
                global TTLOUT5
                global TTLOUT6
                global TTLOUT_Wires

                print("Integrationtime: " + str(integrationtime))

                PiezoX = PiezoDistanceX * (DeviceVoltage/PiezoVoltage)
                PiezoY = PiezoDistanceY * (DeviceVoltage/PiezoVoltage)

                print("Fred beginnt")

                #Establishing TTL
                self.OneWire = TTLOUT_Wires[0]
                if QuelleTTL == 0:
                        self.TTLOUT = TTLOUT3["Pin"]
                        if TTLOUT_Wires[0] == 1:
                                self.TTLIN = self.TTLOUT
                        else:
                                self.TTLIN = TTLOUT4["Pin"]
                        self.TTLPolarity = TTLOUT3["Polarity"]
                elif QuelleTTL == 1:
                        self.TTLOUT = TTLOUT4["Pin"]
                        if TTLOUT_Wires[1] == 1:
                                self.TTLIN = self.TTLOUT
                        else:
                                self.TTLIN = TTLOUT3["Pin"]
                        self.TTLPolarity = TTLOUT4["Polarity"]
                elif QuelleTTL == 2:
                        self.TTLOUT = TTLOUT5["Pin"]
                        if TTLOUT_Wires[2] == 1:
                                self.TTLIN = self.TTLOUT
                        else:
                                self.TTLIN = TTLOUT6["Pin"]
                        self.TTLPolarity = TTLOUT5["Polarity"]
                else:
                        self.TTLOUT = TTLOUT6["Pin"]
                        if TTLOUT_Wires[3] == 1:
                                self.TTLIN = self.TTLOUT
                        else:
                                self.TTLIN = TTLOUT5["Pin"]
                        self.TTLPolarity = TTLOUT6["Polarity"]
                        
                #print("TTLOUT " + str(self.TTLOUT))
                #print("TTLIN " + str(self.TTLIN))

                self.Shutters = Shutters

                self.LEDPin = LEDPin

                self.IntegrationTime = integrationtime
                self.Channel = channel
                self.XSlopeUpper = SetXSlope                                                                                                            #Die Variablen werden in nichtlokale Variablen umgewandelt
                self.YSlopeUpper = SetYSlope
                self.plane_coeffs = plane_coeffs
                self.DelayTime = delaytime
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
                self.SubgridAuto = subgridAuto
                self.Sympho1 = sympho
                self.coordinatesTTL = coordinatesTTL
                self.Plot1 = plot
                self.PlotChannel1 = PlotChannel1
                self.PlotChannel2 = PlotChannel2
                self.Filename = filename
                self.Filepath = filepath
                self.colors = colors
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
                        print("--------------------------------------------")
                        print(zstart)
                        print(self.PiezoDistanceZ)
                        print(((zstart*1000)/self.PiezoDistanceZ))
                        print(((zstart*1000)/self.PiezoDistanceZ)*4095)
                        print("--------------------------------------------")
                        
                        self.ZStartValue = int(((zstart*1000)/self.PiezoDistanceZ)*4095)
                        self.zstartFocus = int(((zstart*1000)/self.PiezoDistanceZ)*4095)
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
                        self.BitsNum = 2
                elif bits == 1:
                        self.BitsValue = 128   
                        self.BitsNum = 4                                                                                                         #Gibt die Verstärkung im cmd aus
                elif bits == 2:         
                        self.BitsValue = 256   
                        self.BitsNum = 8                                                                                                         #Gibt die Verstärkung im cmd aus
                elif bits == 3:
                        self.BitsValue = 512   
                        self.BitsNum = 16                                                                                                         #Gibt die Verstärkung im cmd aus
                elif bits == 4:
                        self.BitsValue = 1024   
                        self.BitsNum = 32                                                                                                        #Gibt die Verstärkung im cmd aus
                elif bits == 5:
                        self.BitsValue = 2048  
                        self.BitsNum = 64                                                                                                         #Gibt die Verstärkung im cmd aus
                elif bits == 6:
                        self.BitsValue = 4096
                        self.BitsNum = 128

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
                elif self.SubgridAuto == False:
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
                else:
                        Faktor = self.BitsValue/256
                        coordinates = self.coordinatesTTL * Faktor
                        self.scanpositions = []
                        i = 0
                        while i < len(coordinates):                                       
                                self.scanpositions = (int(coordinates[i][0]), int(coordinates[i][1]))
                                self.ScanPos.append(self.scanpositions)
                                i += 1
                self.length = ((self.XStopValue - self.XStartValue + 1) * (self.YStopValue - self.YStartValue + 1))
                
                self.DateTime = time.strftime("%d.%m.%Y %H:%M:%S")                                                                                      #Bestimmt das Datum und die Uhrzeit zu beginn der Messung
                self.DateTime2 = time.strftime(FilePath + FileName + "_%d-%m-%Y_%H-%M-%S.txt")                                               #Setzt den Dateiname der txt-Datei
                self.DateTime4 = time.strftime(FilePath + FileName + "_%d-%m-%Y_%H-%M-%S.png")                                               #Setzt den Dateiname der png-Datei
                self.DateTime5 = time.strftime(FileName + " %d.%m.%Y %H:%M:%S")
                self.DateTimeSub = time.strftime(FilePath + FileNameSub + "_%d-%m-%Y_%H-%M-%S.txt")                                      #Setzt den Dateiname der txt-Datei

                self.progress_Filename.emit(self.DateTime)

                self.Txt_Messfile = open(self.DateTime2, "w")
                self.Txt_Messfile.write("Created with HydraScan " + str(Version) + "\n")
                self.Txt_Messfile.write("Start: " + str(self.XStartValue) + " X " + str(self.YStartValue) + "\n")                                                 #Schreibt die Messschranke in die txt-Datei
                self.Txt_Messfile.write("Stop: " + str(self.XStopValue) + " X " + str(self.YStopValue) + "\n")                                                    #Schreibt die Messschranke in die txt-Datei

                if slope == True:
                        self.Txt_Messfile.write("X Slope: " + str(self.XSlopeUpper) + "\tY Slope: " + str(self.YSlopeUpper) + "\n")
                if DHTon == 1:
                        global DHTPin
                        try:
                                humidity, temperature = Adafruit_DHT.read_retry(TempSens, DHTPin)
                                self.Txt_Messfile.write("Temperature: " + str(temperature) + " *C\tHumidity: " + str(humidity) + " %\n")
                        except:
                                pass
                if self.Subgrid1 == True and self.ChannelTimeing == True:
                        self.Txt_Messfile.write("Subgrid-Start: " + str(self.XStartSub) + " X " + str(self.YStartSub) + "\n")                                     #Schreibt die Messschranke in die txt-Datei
                        self.Txt_Messfile.write("Subgrid-Stop: " + str(self.XStopSub) + " X " + str(self.YStopSub) + "\n")                                        #Schreibt die Messschranke in die txt-Datei
                        self.Txt_Messfile.write("Stepsize X: " + str(self.XStep) + "\tStepsize Z: " + str(self.YStep) + "\n")                                     #Schreibt die Messschranke in die txt-Datei
                if self.Sympho1 == True:
                        global SymPho1
                        global SymPho2
                        self.SymphoOut1 = SymPho1
                        self.SymphoOut2 = SymPho2
                        self.Txt_Messfile.write("\nSymPhoTime is activated\n")

                self.Txt_Messfile.write("Measurement with:\t" + str(self.BitsValue) + " Pixel\n")                                                       #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Messfile.write("X-Offset:\t" + str(round((PiezoX/4095)*xoff,1)) + " nm\t" + "Y-Offset:\t" + str(round((PiezoX/4095)*yoff,1)) + " nm\n")
                self.Txt_Messfile.write("X-Center:\t" + str(round(((PiezoX/4095)*xoff)+((xDim*1000)/2),1)) + " nm\t" + "Y-Offset:\t" + str(round(((PiezoY/4095)*yoff)+((yDim*1000)/2),1)) + " nm\n")
                self.Txt_Messfile.write("X-Range:\t" + str(xDim*1000) + " nm\t" + "Y-Range:\t" + str(yDim*1000) + " nm\n")                                    #Schreibt die Verstärkung in die txt-Datei
                self.Txt_Messfile.write("Date: " + self.DateTime + "\n")

                if Meta == 1:
                        self.Txt_Messfile.write("\n")
                        self.Txt_Messfile.write("----------------------- Meta Data -----------------------\n")  
                        if LaserWL:
                                self.Txt_Messfile.write("Laser Wavelength: " + LaserWL + "\n")
                        if LaserPower:
                                self.Txt_Messfile.write("Laser Power: " + LaserPower + "\n")
                        if Filter:
                                self.Txt_Messfile.write("Filter: " + Filter + "\n")
                        if Sample:
                                self.Txt_Messfile.write("Sample: " + Sample + "\n")
                        self.Txt_Messfile.write("---------------------------------------------------------")
                        self.Txt_Messfile.write("\n")
                
                self.Txt_Messfile.write("\n")                                   
                self.Txt_Messfile.write("Count\tX\tY\tZ\t" + CH1 + "\t" + CH2 + "\t" + CH3 + "\t" + CH4 + "\t" + CHA + "\t" + CHB + "\t" + L2 + "\t" + L3 + "\n")

                if self.Subgrid1 == True:
                        self.Txt_TTL = open(self.DateTimeSub, "w")
                        self.Txt_TTL.write("Start: " + str(self.XStartValue) + " X " + str(self.YStartValue) + "\n")                                    #Schreibt die Messschranke in die txt-Datei
                        self.Txt_TTL.write("Stop: " + str(self.XStopValue) + " X " + str(self.YStopValue) + "\n")                                       #Schreibt die Messschranke in die txt-Datei
                        self.Txt_TTL.write("Stepsize X: " + str(self.XStep) + "\tStepsize Z: " + str(self.YStep) + "\n")
                        self.Txt_TTL.write("Subgrid-Start: " + str(self.XStartSub) + " X " + str(self.YStartSub) + "\n")                                #Schreibt die Messschranke in die txt-Datei
                        self.Txt_TTL.write("Subgrid-Stop: " + str(self.XStopSub) + " X " + str(self.YStopSub) + "\n") 
                        self.Txt_TTL.write("Measurement with " + str(self.BitsValue) + " Pixel\n")                                                      #Schreibt die Verstärkung in die txt-Datei
                        self.Txt_TTL.write("Date: " + self.DateTime + "\n")                                                                              #Schreibt das Datum und die Uhrzeit in die txt-Datei
                        self.Txt_TTL.write("\n")
                        if self.SubgridAuto == True:
                                self.Txt_TTL.write("Subplotpoints: " + str(self.ScanPos) + "\n")
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
                self.value1 = 0
                self.value2 = 0
                self.value3 = 0
                self.value4 = 0
                self.value5 = 0
                self.value6 = 0
                self.value7 = 0
                self.value8 = 0
                self.TTL = 0
                time.sleep(0.5)                     
                dacX.set_voltage(int(self.XStartValue * (4095 / self.BitsValue)))
                dacY.set_voltage(int(self.YStartValue * (4095 / self.BitsValue)))


                self.Voltage = round(xDim/10, 1)
                CurrentPoti = self.Voltage
                Poti.write_range(self.Voltage)

                self.XOffset = xoff
                self.YOffset = yoff
                CurrentOffsetX = self.XOffset
                CurrentOffsetY = self.YOffset
                dacOffset.setAllVoltage(self.XOffset, self.YOffset, 0, 0)
                #print("Offset: " + str(self.XOffset) + " x " + str(self.YOffset))

                self._running = True

                time.sleep(2)

        def breakIt(self):
                self.i = 1
                self._running = False
                

        def EventHandler_rising(self, pin):
                self.TTL = 1

        def calculate_z(self, x, y):
                a, b, c, d = self.plane_coeffs
                z = a*x + b*y + d
                #print("Eq: " + str(z) + " = " + str(a) + "*" + str(x) + " + " + str(b) + "*" + str(y) + " + " + str(d))

                return z
                
        def run(self):
                global PiezoDistanceZ
                global APDArduinoOn
                global APDBSOn    
                global StartValX
                global StartValY
                global FocusZ
                global zNew
                global t
                global zNew2
                global tt
                global TTLOUT7
                global TTLOUT8
                global ShutterMode

                self.zNew = zNew
                self.t = t
                self.zNew2 = zNew2
                self.tt = tt
                self.MaxVal1 = 10
                self.MaxVal2 = 10
                self.MinVal1 = 0
                self.MinVal2 = 0
                NewMax1 = 0
                NewMax2 = 0

                #APDread --------------------------------------------
                if self.Logic == True:
                        if APDArduinoOn == 1:
                                APDs = ArduinoLogic()
                        elif APDBSOn == 1:
                                APDs = APDLogic(5000,self.IntegrationTime) 
                
                self.starttime = time.time()
                
                """
                zpart = []
                ChannelCount = 0
                if self.Channel[0] == 1:
                        self.z1 = []
                        z1part = []
                        zpart.append(z1part)
                        ChannelCount += 1
                if self.Channel[1] == 1:
                        self.z2 = []
                        z2part = []
                        zpart.append(z2part)
                        ChannelCount += 1
                if self.Channel[2] == 1:
                        self.z3 = []
                        z3part = []
                        zpart.append(z3part)
                        ChannelCount += 1
                if self.Channel[3] == 1:
                        self.z4 = []
                        z4part = []
                        zpart.append(z4part)
                        ChannelCount += 1
                if self.Channel[4] == 1:
                        self.z5 = []
                        z5part = []
                        zpart.append(z5part)
                        ChannelCount += 1
                if self.Channel[5] == 1:
                        self.z6 = []
                        z6part = []
                        zpart.append(z6part)
                        ChannelCount += 1
                if self.Channel[6] == 1:
                        self.z7 = []
                        z7part = []
                        zpart.append(z7part)
                        ChannelCount += 1
                if self.Channel[7] == 1:
                        self.z8 = []
                        z8part = []
                        zpart.append(z8part)
                        ChannelCount += 1
                """

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
                zpart = []
                zpart.append(z1part)
                zpart.append(z2part)
                zpart.append(z3part)
                zpart.append(z4part)
                zpart.append(z5part)
                zpart.append(z6part)
                zpart.append(z7part)
                zpart.append(z8part)

                self.LineCounter = 0
                self.counterIntern = 1
                self.counterSubgrid = 0
                self.StackZPos = self.ZStartValue
                SlopeVal = 2048

                RandomGen = random.randint(900, 1000)
                RandomGen = 1000

                if self.Sympho1 == True:
                        GPIO.setup(self.SymphoOut1, GPIO.OUT)
                        GPIO.setup(self.SymphoOut2, GPIO.OUT)

                
                print("Messung Start")
                if self.Shutters == 0 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                        if ShutterMode[0] == 0:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                        elif ShutterMode[0] == 1:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                if self.Shutters == 1 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                        if ShutterMode[1] == 0:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                        elif ShutterMode[1] == 1:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                while self.i == 0:
                        if not self._running:
                                break
                        while self.StackRun <= self.Stacks:
                                if not self._running:
                                        break
                                ZPosition = self.StackZPos
                                if self.Sympho1 == True:
                                        GPIO.output(self.SymphoOut1, GPIO.HIGH)
                                while self.YRun <= self.YStopValue:
                                        if not self._running:
                                                break
                                        self.LineCounter += 1
                                        #print(self.YRun)
                                        print("Line Start")
                                        if self.Shutters == 0 or self.Shutters == 2:
                                                if ShutterMode[0] == 2:
                                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                                elif ShutterMode[0] == 3:
                                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                                        time.sleep(0.1)
                                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                        if self.Shutters == 1 or self.Shutters == 2:
                                                if ShutterMode[1] == 2:
                                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                                elif ShutterMode[1] == 3:
                                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                                        time.sleep(0.1)
                                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                        if self.Sympho1 == True:
                                                GPIO.output(self.SymphoOut2, GPIO.HIGH)
                                        
                                        while self.XRun <= self.XStopValue:
                                                if not self._running:
                                                        break
                                                self.value1 = 0
                                                self.value2 = 0
                                                self.value3 = 0
                                                self.value4 = 0
                                                self.value5 = 0
                                                self.value6 = 0
                                                self.value7 = 0
                                                self.value8 = 0
                                                #print(self.XRun)
                                                #starttime = time.time()
                                                if self.Stack1 == False:
                                                        if self.Slope1 == True:
                                                                #XSlopePos = (self.XSlopeUpper - (self.XRun * ((self.XSlopeUpper*2)/self.BitsValue)))
                                                                #YSlopePos = (self.YSlopeUpper - (self.YRun * ((self.YSlopeUpper*2)/self.BitsValue)))
                                                                #SlopePos = (XSlopePos + YSlopePos)
                                                                #SlopeVal = ((((SlopePos + 2000) / 4000) * self.BitsValue))
                                                                #ZPosition = int(SlopeVal * (4095 / self.BitsValue))
                                                                ZPosition = int(self.calculate_z(int(self.XRun * (4095 / self.BitsValue)), int(self.YRun * (4095 / self.BitsValue))))
                                                        else:
                                                                #print("zstartFocus = " + str(self.zstartFocus))
                                                                ZPosition = self.zstartFocus
                                                        
                                                if self.Voltage == 10:
                                                        dacOffset.setAllVoltage(int(self.XRun * (4095 / self.BitsValue)), int(self.YRun * (4095 / self.BitsValue)), 0, 0)
                                                else:                     
                                                        dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                                        dacY.set_voltage(int(self.YRun * (4095 / self.BitsValue)))
                                                dacZ.set_voltage(ZPosition)     
                                                
                                                ScanPosition = (self.XRun, self.YRun)
                                                if ScanPosition in self.ScanPos:
                                                        self.counterSubgrid = self.counterSubgrid + 1
                                                        if self.sendTTL == True:
                                                                print("TTLOUT " + str(self.TTLOUT))
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
                                                                        if self.ChannelTimeing == True:
                                                                                while self.TTL == 0: 
                                                                                        if self.Channel[0] == 1:
                                                                                                self.value1 = adc.read_adc(0, gain=GAIN)
                                                                                        if self.Channel[1] == 1:
                                                                                                self.value2 = adc.read_adc(1, gain=GAIN)
                                                                                        if self.Channel[2] == 1:
                                                                                                self.value3 = adc.read_adc(2, gain=GAIN)
                                                                                        if self.Channel[3] == 1:
                                                                                                self.value4 = adc.read_adc(3, gain=GAIN)
                                                                                        if self.Channel[4] == 1 and self.Channel[5] == 1:
                                                                                                self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                                        elif self.Channel[4] == 1:
                                                                                                self.value5 = APDs.capture1(self.IntegrationTime)
                                                                                        elif self.Channel[5] == 1:
                                                                                                self.value6 = APDs.capture2(self.IntegrationTime)
                                                                                        """
                                                                                        if self.Logic:
                                                                                                #print("1")
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
                                                                                                        self.value7 = 0  
                                                                                                        self.value8 = 0 
                                                                                        """    
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
                                                                                if self.Channel[1] == 1:
                                                                                        self.value2 = adc.read_adc(1, gain=GAIN)
                                                                                if self.Channel[2] == 1:
                                                                                        self.value3 = adc.read_adc(2, gain=GAIN)
                                                                                if self.Channel[3] == 1:
                                                                                        self.value4 = adc.read_adc(3, gain=GAIN)
                                                                                if self.Channel[4] == 1 and self.Channel[5] == 1:
                                                                                        self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                                elif self.Channel[4] == 1:
                                                                                        self.value5 = APDs.capture1(self.IntegrationTime)
                                                                                elif self.Channel[5] == 1:
                                                                                        self.value6 = APDs.capture2(self.IntegrationTime)
                                                                                """
                                                                                if self.Logic:
                                                                                        #print("2")
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
                                                                                                self.value7 = 0  
                                                                                                self.value8 = 0 
                                                                                """                      
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
                                                if APDArduinoOn == 1:
                                                        if self.Channel[4] == 1 and self.Channel[5] == 1:
                                                                self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                z5part.append(self.value5)
                                                                z6part.append(self.value6)
                                                        elif self.Channel[4] == 1:
                                                                self.value5 = APDs.capture1(self.IntegrationTime)
                                                                z5part.append(self.value5)
                                                        elif self.Channel[5] == 1:
                                                                self.value6 = APDs.capture2(self.IntegrationTime)
                                                                z6part.append(self.value6)
                                                else:
                                                        RandomGen = random.randint(500, 800)
                                                        if self.XRun != 0 and self.YRun!=0 and ((self.XRun * self.YRun) % (RandomGen)) == 0:
                                                                self.value5 = random.randint(201, 300)
                                                        else:
                                                                self.value5 = random.randint(100, 200)
                                                        if self.XRun == int(self.XStopValue/2) and self.YRun == int(self.YStopValue/2):
                                                                self.value5 = 300
                                                        self.value6 = random.randint(5, 100)
                                                if self.Channel[6] == 1:
                                                        self.value7 = 0
                                                        z7part.append(self.value7)
                                                if self.Channel[7] == 1:
                                                        self.value8 = 0
                                                        z8part.append(self.value8)
                                                """
                                                if self.Logic:
                                                        if APDBSOn == 1:
                                                                self.value5 = APDs.captureData()             
                                                                z5part.append(5)           
                                                                z6part.append(6)          
                                                                z7part.append(7)
                                                                z8part.append(8)
                                                        elif APDArduinoOn == 1:
                                                                self.value5, self.value6 = APDs.captureDual(self.IntegrationTime)
                                                                self.value7 = 0
                                                                self.value8 = 0
                                                        else:
                                                                RandomGen = random.randint(500, 800)
                                                                if self.XRun != 0 and self.YRun!=0 and ((self.XRun * self.YRun) % (RandomGen)) == 0:
                                                                        self.value5 = random.randint(201, 300)
                                                                else:
                                                                        self.value5 = random.randint(100, 200)
                                                                if self.XRun == int(self.XStopValue/2) and self.YRun == int(self.YStopValue/2):
                                                                        self.value5 = 300
                                                                self.value6 = random.randint(5, 100) 
                                                                self.value7 = 0  
                                                                self.value8 = 0
                                                """
                                                #midtime2 = time.time()
                                                #z5part.append(self.value5)
                                                #z6part.append(self.value6)
                                                #z7part.append(self.value7)
                                                #z8part.append(self.value8)
                                                zpart[0].append(self.value1)
                                                zpart[1].append(self.value2)
                                                zpart[2].append(self.value3)
                                                zpart[3].append(self.value4)
                                                zpart[4].append(self.value5)
                                                zpart[5].append(self.value6)
                                                zpart[6].append(self.value7)
                                                zpart[7].append(self.value8)
                                                self.zNew[self.XRun][self.YRun] = zpart[self.PlotChannel1][self.XRun]
                                                self.zNew2[self.XRun][self.YRun] = zpart[self.PlotChannel2][self.XRun]
                                                self.t[self.XRun] = zpart[self.PlotChannel1][self.XRun]
                                                self.tt[self.XRun] = zpart[self.PlotChannel2][self.XRun]

                                                SlopeVal = round(ZPosition, 2)

                                                self.Txt_Messfile.write(str(self.counter) + "\t" + str(self.XRun-self.XStartValue) + "\t" + str(self.YRun-self.YStartValue) + "\t" + str(ZPosition) + "\t" + str(self.value1) + "\t" + str(self.value2) + "\t" + str(self.value3) + "\t" + str(self.value4) + "\t" + str(self.value5) + "\t" + str(self.value6) + "\t" + str(self.value7) + "\t" + str(self.value8) + "\n")
                                                
                                                self.XRun = self.XRun + 1
                                                self.counter = self.counter + 1
                                                self.counterIntern = self.counterIntern + 1
                                                #endtime = time.time()
                                                
                                                time.sleep(self.DelayTime)                                                                              #Setzt die Wartezeit zwischen den Spalten

                                        
                                        if self.Voltage == 10:
                                                dacOffset.setAllVoltage(int(self.XRun * (4095 / self.BitsValue)), int(self.YRun * (4095 / self.BitsValue)), 0, 0)
                                        else:                     
                                                dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                        progress = int((self.counterIntern) * (100 / (self.length*self.Stacks)))
                                        self.progress_bar.emit(progress)
                                        self.progress_Filename.emit(self.DateTime)
                                        
                                        """
                                        i = 0
                                        if self.YRun == 0:
                                                self.MinVal1 = zpart[self.PlotChannel1][i]
                                                self.MinVal2 = zpart[self.PlotChannel2][i]
                                                self.progress_Max.emit(0, self.MaxVal1, self.MinVal1)
                                                self.progress_Max.emit(1, self.MaxVal2, self.MinVal2)
                                        while i <= self.XRun-1:
                                                self.zNew[i][self.YRun] = zpart[self.PlotChannel1][i]
                                                self.zNew2[i][self.YRun] = zpart[self.PlotChannel2][i]
                                                self.t[i] = zpart[self.PlotChannel1][i]
                                                self.tt[i] = zpart[self.PlotChannel2][i]
                                                if zpart[self.PlotChannel1][i] > self.MaxVal1:
                                                        self.MaxVal1 = zpart[self.PlotChannel1][i]
                                                        self.progress_Max.emit(0, self.MaxVal1, self.MinVal1)
                                                if zpart[self.PlotChannel1][i] < self.MinVal1:
                                                        self.MinVal1 = zpart[self.PlotChannel1][i]
                                                        self.progress_Max.emit(0, self.MaxVal1, self.MinVal1)
                                                
                                                if zpart[self.PlotChannel2][i] > self.MaxVal2:
                                                        self.MaxVal2 = zpart[self.PlotChannel2][i]
                                                        self.progress_Max.emit(1, self.MaxVal2, self.MinVal2)
                                                if zpart[self.PlotChannel2][i] < self.MinVal2:
                                                        self.MinVal2 = zpart[self.PlotChannel2][i]
                                                        self.progress_Max.emit(1, self.MaxVal2, self.MinVal2)
                                                i += 1
                                        self.progress_values2.emit(self.zNew, self.zNew2, self.t, self.tt)
                                        """


                                        LineMax1 = max(zpart[self.PlotChannel1])
                                        LineMin1 = min(zpart[self.PlotChannel1])
                                        LineMax2 = max(zpart[self.PlotChannel2])
                                        LineMin2 = min(zpart[self.PlotChannel2])
                                        if self.YRun == 0:
                                                self.MinVal1 = LineMin1
                                                self.MinVal2 = LineMin2
                                        if LineMax1 > self.MaxVal1 and ((LineMax1-self.MaxVal1) < 10000):
                                                self.MaxVal1 = LineMax1
                                                NewMax1 = 1
                                                #self.progress_Max.emit(0, self.MaxVal1, self.MinVal1)
                                        if LineMin1 < self.MinVal1:
                                                self.MinVal1 = LineMin1
                                                #self.progress_Max.emit(0, self.MaxVal1, self.MinVal1)
                                                NewMax1 = 1
                                        if LineMax2 > self.MaxVal2 and ((LineMax2-self.MaxVal2) < 10000):
                                                self.MaxVal2 = LineMax2
                                                #self.progress_Max.emit(1, self.MaxVal2, self.MinVal2)
                                                NewMax2 = 1
                                        if LineMin2 < self.MinVal2:
                                                self.MinVal2 = LineMin2
                                                #self.progress_Max.emit(1, self.MaxVal2, self.MinVal2)
                                                NewMax2 = 1

                                        #print((self.LineCounter)%self.BitsNum)
                                        #if (self.LineCounter%self.BitsNum)==0:
                                        if (self.LineCounter%self.BitsNum)==0:
                                                #print("++++++++++++++++++++++++++++++++++++++++++ NewLines")
                                                progress = int((self.counterIntern) * (100 / (self.length*self.Stacks)))
                                                self.progress_bar.emit(progress)
                                                self.progress_Filename.emit(self.DateTime)
                                                self.progress_values2.emit(self.zNew, self.zNew2, self.t, self.tt)
                                                if NewMax1 == 1:
                                                        #print("****************************************************** NewMinMax")
                                                        self.progress_Max.emit(0, self.MaxVal1, self.MinVal1)
                                                        NewMax1 = 0
                                                if NewMax2 == 1:
                                                        self.progress_Max.emit(1, self.MaxVal2, self.MinVal2)
                                                        NewMax2 = 0

                                        self.YRun = self.YRun + 1
                                        while self.XRun > self.XStartValue:
                                                if self.Voltage == 10:
                                                        dacOffset.setAllVoltage(int(self.XRun * (4095 / self.BitsValue)), int(self.YRun * (4095 / self.BitsValue)), 0, 0)
                                                else:                     
                                                        dacX.set_voltage(int(self.XRun * (4095 / self.BitsValue)))
                                                self.XRun -= 1
                                        self.XRun = self.XStartValue
                                        
                                        if self.Sympho1 == True:
                                                GPIO.output(self.SymphoOut2, GPIO.LOW)
                                        
                                        print("Line Stop")
                                        if self.Shutters == 0 or self.Shutters == 2:
                                                if ShutterMode[0] == 2:
                                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                                elif ShutterMode[0] == 3:
                                                        GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                                        time.sleep(0.1)
                                                        GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                                        if self.Shutters == 1 or self.Shutters == 2:
                                                if ShutterMode[1] == 2:
                                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                                elif ShutterMode[1] == 3:
                                                        GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                                        time.sleep(0.1)
                                                        GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                                        

                                        zpart[0].clear()
                                        zpart[1].clear()
                                        zpart[2].clear()
                                        zpart[3].clear()
                                        zpart[4].clear()
                                        zpart[5].clear()
                                        zpart[6].clear()
                                        zpart[7].clear()
                                        z1part = []
                                        z2part = []
                                        z3part = []
                                        z4part = []
                                        z5part = []
                                        z6part = []
                                        z7part = []
                                        z8part = []

                                        if self.i == 1:
                                                break

                                self.counter = 1
                                self.YRun = self.YStartValue
                                self.StackRun = self.StackRun + 1
                                if self.Sympho1 == True:
                                        GPIO.output(self.SymphoOut1, GPIO.LOW)

                                
                                if self.Direct == 0:
                                        self.StackZPos = int(self.StackZPos + ((self.StackStep * 1000) * (4096/self.PiezoDistanceZ)))
                                elif self.Direct == 1:
                                        self.StackZPos = int(self.StackZPos - ((self.StackStep * 1000) * (4096/self.PiezoDistanceZ)))

                                if self.StackZPos <= 0:
                                        self.StackZPos = 0
                                elif self.StackZPos >=4095:
                                        self.StackZPos = 4095

                        self.data = -1

                        self.stoptime = time.time()
                        self.runtime = self.stoptime - self.starttime
                        print("Runtime: " + str(self.runtime))
                        
                        self.i = 1
                
                print("Messung Stop")
                if self.Shutters == 0 or self.Shutters == 2:
                        if ShutterMode[0] == 0:
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                        elif ShutterMode[0] == 1:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                if self.Shutters == 1 or self.Shutters == 2:
                        if ShutterMode[1] == 0:
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                        elif ShutterMode[1] == 1:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)
                
                time.sleep(0.5)
                                
                YDown = self.YStopValue
                XDown = self.XStopValue
                XOff = self.XOffset
                YOff = self.YOffset
                print(self.Voltage)
                if self.Voltage >= 9.6:
                        print("Way back!")
                        while XDown > 0:
                                dacOffset.setAllVoltage(XDown, YDown, 0, 0)
                                XDown -= 4
                                time.sleep(0.001)
                        while YDown > 0:
                                dacOffset.setAllVoltage(XDown, YDown, 0, 0)
                                YDown -= 4
                                time.sleep(0.001)
                        print("Way back!")
                else:
                        print("Way back2!")
                        while YDown > 0:
                                dacX.set_voltage(YDown)
                                YDown -= 4
                                time.sleep(0.001)
                        while XDown > 0:
                                dacY.set_voltage(XDown)
                                XDown -= 4
                                time.sleep(0.001)
            
                        print("Way back2.1!")
                        while XOff > 0:
                                dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                                XOff -= 4
                                time.sleep(0.001)
                        while YOff > 0:
                                dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                                YOff -= 4
                                time.sleep(0.001)
                                
                        print("Way back2!")
                
            
                #print("YDown" + str(YDown))
                #print("XDown" + str(XDown))
                #print("XOff" + str(XOff))
                #print("YOff" + str(YOff))
                #print("StartValX" + str(StartValX))
                #print("StartValY" + str(StartValY))
                
                print("Way back3!")
                while XOff < StartValX:
                        #print("XOff" + str(XOff))
                        dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                        XOff += 4
                        time.sleep(0.001)
                while YOff < StartValY:
                        #print("YOff" + str(YOff))
                        dacOffset.setAllVoltage(XOff, YOff, 0, 0)
                        YOff += 4
                        time.sleep(0.001)

                #print("YDown" + str(YDown))
                #print("XDown" + str(XDown))
                #print("XOff" + str(XOff))
                #print("YOff" + str(YOff))
                #print("StartValX" + str(StartValX))
                #print("StartValY" + str(StartValY))
                dacX.set_voltage(0)
                dacY.set_voltage(0)
                dacZ.set_voltage(FocusZ)
                dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
                

                self.progress_bar.emit(100)
                self.killFred()
                return

        def killFred(self):    
                global StartValX
                global StartValY
                global FocusZ
                global TTLOUT7
                global TTLOUT8
                global ShutterMode
                
                if self.Shutters == 0 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                        if ShutterMode[0] == 0:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                        elif ShutterMode[0] == 1:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                if self.Shutters == 1 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                        if ShutterMode[1] == 0:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                        elif ShutterMode[1] == 1:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                self.i = 1     
                self.Txt_Messfile.close()                                                                                                                         #Beendet den Schreibmodus und schließt die txt-Datei
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
                        dacZ.set_voltage(FocusZ)
                        dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
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
                self.progress_bar.emit(100) 
                self.progress_value.emit(1)
                time.sleep(0.5)
                print("Fred beendet")                                                                                                                   #Die kill()-Funktion beendet den Thread und wird aus dem Hauptprogramm heraus aufgerufen

        def killFredHard(self):
                global StartValX
                global StartValY
                global FocusZ
                global TTLOUT7
                global TTLOUT8
                global ShutterMode
                
                
                if self.Shutters == 0 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT7["Pin"], GPIO.OUT)
                        if ShutterMode[0] == 0:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                        elif ShutterMode[0] == 1:
                                GPIO.output(TTLOUT7["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT7["Pin"], GPIO.LOW)
                if self.Shutters == 1 or self.Shutters == 2:
                        #GPIO.setup(TTLOUT8["Pin"], GPIO.OUT)
                        if ShutterMode[1] == 0:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                        elif ShutterMode[1] == 1:
                                GPIO.output(TTLOUT8["Pin"], GPIO.HIGH)
                                time.sleep(0.1)
                                GPIO.output(TTLOUT8["Pin"], GPIO.LOW)

                self.i = 1   
                self.Txt_Messfile.close()                                                                                                                             #Beendet den Schreibmodus und schließt die txt-Datei
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
                dacZ.set_voltage(FocusZ)
                dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
                self.Voltage = 10
                Poti.write_range(self.Voltage)
                self.progress_bar.emit(100) 
                self.progress_value.emit(1) 
                GPIO.output(LEDPin, GPIO.LOW)
                self.quit()
                #self.terminate()
                print("Fred beendet")  


"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 11: Slope Subclass -------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
#SearchSlope Subclass is a new Thread that is started in Tab5
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

                self.Voltage = 10
                Poti.write_range(self.Voltage)

                self.XOffset = 0
                self.YOffset = 0
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


"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------- Section 12: Exception Catcher & Main ---------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
#Exception Catcher

def send_error_report(error_message):
        # --- KONFIGURATION ---
        # Daten aus der Umgebung laden
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
        SENDER_EMAIL = os.getenv("SENDER_EMAIL")
        SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
        SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL")
        # ---------------------

        if not all([SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD]):
                print("Fehler: E-Mail-Zugangsdaten unvollständig (Prüfe .env Datei).")
                return

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SUPPORT_EMAIL
        msg['Subject'] = f"Crash Report: v{__version__} auf {platform.system()}"

        # Body der E-Mail mit Systeminfos anreichern
        body = f"""
        Ein Fehler ist aufgetreten!
        
        Version: {__version__}
        System: {platform.system()} {platform.release()}
        Python: {platform.python_version()}
        
        FEHLERMELDUNG:
        {error_message}
        """
    
        msg.attach(MIMEText(body, 'plain'))

        #Logging File als Anhang
        if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                "Content-Disposition",
                f"attachment; filename= {LOG_FILE}",
                )
                msg.attach(part)

        try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls() # Verschlüsselung aktivieren
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
                server.quit()
                print("Fehlerbericht wurde an den Support gesendet.")
        except Exception as e:
                print(f"E-Mail konnte nicht gesendet werden: {e}")


def excepthook(exc_type, exc_value, exc_tb):
        DateTime = time.strftime("%d-%m-%Y_%H-%M-%S")
        FailFile = "ErrorLog_" + str(DateTime) + ".txt"
        f = open(FailFile,'w')
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        f.write("\n\n" + DateTime + "\n" + str(tb))
        f.close()
        print(exc_type, exc_value, exc_tb)
        #print("error catched!:")
        #print("error message:\n", tb)
        print("Not an Error just some more Work to do! ;-)")
        #time.sleep(1)
        
        if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_tb)
                return

        #print("Test1")
        # Fehler im Log speichern (mit vollständigem Stacktrace)
        logger.critical("Unbehandelter Ausnahmefehler aufgetreten:", 
                        exc_info=(exc_type, exc_value, exc_tb))
        
        #print("Test2")
        # E-Mail senden
        send_error_report(tb)
        #time.sleep(1)
        #print("Test3")

        #QApplication.quit()
        # or QtWidgets.QApplication.exit(0)


#Main Function of the programm
def main():
        global StyleName
        global StyleColor
        #try:
        app = QApplication(sys.argv)   
        app.setStyle(StyleName)
        if StyleColor == "dark" and StyleName != "windowsvista":
                palette = QPalette()
                palette.setColor(QPalette.Window, QColor(53,53,53))
                palette.setColor(QPalette.WindowText, Qt.white)
                palette.setColor(QPalette.Base, QColor(15,15,15))
                palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
                palette.setColor(QPalette.ToolTipBase, QColor(53,53,53))
                #palette.setColor(QPalette.ToolTipText, Qt.black)
                #palette.setColor(QPalette.ToolTipBase, Qt.white)
                palette.setColor(QPalette.ToolTipText, Qt.white)
                palette.setColor(QPalette.Text, Qt.white)
                palette.setColor(QPalette.Button, QColor(53,53,53))
                palette.setColor(QPalette.ButtonText, Qt.white)
                palette.setColor(QPalette.BrightText, Qt.red)
                palette.setColor(QPalette.Highlight, QColor(34,139,34).lighter())
                palette.setColor(QPalette.HighlightedText, Qt.black)
                app.setPalette(palette)
        elif StyleColor == "dark" and StyleName == "windowsvista":
                palette = QPalette()
                palette.setColor(QPalette.Window, QColor(53,53,53))
                palette.setColor(QPalette.WindowText, Qt.black)
                palette.setColor(QPalette.Base, QColor(15,15,15))
                palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
                palette.setColor(QPalette.ToolTipBase, QColor(53,53,53))
                palette.setColor(QPalette.ToolTipText, Qt.white)
                #palette.setColor(QPalette.ToolTipBase, Qt.white)
                #palette.setColor(QPalette.ToolTipText, Qt.black)
                palette.setColor(QPalette.Text, Qt.white)
                palette.setColor(QPalette.Button, QColor(153,153,153))
                palette.setColor(QPalette.ButtonText, Qt.black)
                palette.setColor(QPalette.BrightText, Qt.red)
                palette.setColor(QPalette.Highlight, QColor(34,139,34).lighter())
                palette.setColor(QPalette.HighlightedText, Qt.black)
                app.setPalette(palette)

        w = Fenster()
        sys.excepthook = excepthook
        sys.exit(app.exec_())                                                                                                                           #Programm endet wenn Fenster endet
        """
        except KeyboardInterrupt:
                print("Own KeyboardInterrupt")                                                                                                          #Programm endet wenn Fenster endet
        except:
                GPIO.cleanup()
                print("Cleanup6")
        finally:
                global StartValX
                global StartValY
                global FocusZ

                print("finally")
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
                        connFile.commit()                                                           
                        connFile.close()
                except:
                        connFile.close()
                try:
                        connTTL.commit()                                                           
                        connTTL.close()
                except:
                        connTTL.close()
                try:
                        dacX.set_voltage(0, persist=True)
                        dacY.set_voltage(0, persist=True)
                        dacZ.set_voltage(FocusZ, persist=True)
                        dacOffset.setAllVoltage(StartValX, StartValY, 0, 0)
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
                try:
                        w.quitall()
                except:
                        pass
                print("Everything is over!")
                GPIO.cleanup()
                print("Cleanup7")
        """
        
if __name__ == '__main__':
        update_full_repo()
        main()                                                                                                                                          #Programm endet wenn Fenster endet
"""
except KeyboardInterrupt:
        print("Own KeyboardInterrupt")

except:
        print("A big Exception occurred")

finally:
        global StartValX
        global StartValY
        global FocusZ
                
        print("Catch it if you can")
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
                connFile.commit()                                                           
                connFile.close()
        except:
                connFile.close()
        try:
                connTTL.commit()                                                           
                connTTL.close()
        except:
                connTTL.close()
        try:
                dacX.set_voltage(StartValX)
                dacY.set_voltage(StartValY)
                dacZ.set_voltage(FocusZ)
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
        print("Everything is over!")
        GPIO.cleanup()
"""
