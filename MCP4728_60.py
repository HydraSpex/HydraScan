#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C

MCP4728_DEFAULT_ADDRESS  = 0x60

class MCP4728 :
  i2c = None
  
  # Registers
  __REG_WRITEALLDAC    = 0x50
  __REG_WRITEPROMCH0   = 0x58  # Not Done Yet
  __REG_WRITEPROMCH1   = 0X5A  # Not Done Yet
  __REG_WRITEPROMCH2   = 0X5C  # Not Done Yet
  __REG_WRITEPROMCH3   = 0X5E  # Not Done Yet

  # Constructor
  def __init__(self, address = MCP4728_DEFAULT_ADDRESS, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def setAllVoltage(self, volt0, volt1, volt2, volt3):
    "Sets the output voltage to the specified value"
    if (volt0 > 4095):
      volt0 = 4095
    if (volt0 < 0):
          volt0 = 0
    if (volt1 > 4095):
      volt1 = 4095
    if (volt1 < 0):
          volt1 = 0
    if (volt2 > 4095):
      volt2 = 4095
    if (volt2 < 0):
           volt2 = 0
    if (volt3 > 4095):
      volt3 = 4095
    if (volt3 < 0):
           volt3 = 0       
    if (self.debug):
      print('Setting voltage to {0:8.3f}{1:8.3f}{2:8.3f}{3:8.3f} '.format(volt0, volt1, volt2, volt3))
    # Break integers into 2 bytes for sending to MCP4728
    bytes = [(volt0 >> 8) & 0xFF, (volt0) & 0xFF, (volt1 >> 8) & 0xFF, (volt1) & 0xFF,
             (volt2 >> 8) & 0xFF, (volt2) & 0xFF, (volt3 >> 8) & 0xFF, (volt3) & 0xFF]    
    self.i2c.writeList(self.__REG_WRITEALLDAC, bytes)
