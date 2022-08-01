#!/usr/bin/env python

import smbus

# Register-Werte fuer Kommandos:
WRITEDAC         = 0x40
WRITEDACEEPROM   = 0x60
WRITEFAST        = 0x00

# Power-down Modi (per fast-mode command):
# (siehe table 5-2 im Datenblatt, table 6-2 fuer fast-mode)
POWER_DOWN = {1: 0x10, 100: 0x20, 500: 0x30}

# Default I2C-Addresse (moeglich sind 0x62 und 0x63):
MCP4725_DEFAULT_ADDRESS  = 0x62


class MCP4725_62(object):
    def writeList(self, register, data):
        # Write bytes to the specified register.
        self._bus.write_i2c_block_data(self._address, register, data)

    def __init__(self, address = MCP4725_DEFAULT_ADDRESS, busnum = 1):
        # eine Instanz des MCP4725 DAC erzeugen.
        self._address = address
        self._bus = smbus.SMBus(busnum)

    def set_voltage(self, value, persist=False):
        # Ausgangsspannung setzen. value ist eine positive 12-bit-Zahl
        # (0-4095), welche die Ausgangsspannung nach der folgenden Formel
        # festlegt:
        #
        #  Vout =  (VDD*value)/4096
        #
        # Ist der Parameter persist = True, wird der Wert auch im EEPROM
        # gespeichert und steht nach einem Reset am Ausgang an.

        # value auf einem positiven 12-Bit-Wert begrenzen.
        value = value & 0xFFF
        # Register-Bytes erzeugen und senden.
        # Siehe Datenblatt figure 6-2:
        reg_data = [(value >> 4) & 0xFF, (value << 4) & 0xFF]
        if persist:
            self.writeList(WRITEDACEEPROM, reg_data)
        else:
            self.writeList(WRITEDAC, reg_data)

    def set_fast(self, value):
        # Ausgangsspannung im Fast Mode setzen (Formel siehe oben).

        # value auf einem positiven 12-Bit-Wert begrenzen.
        value = value & 0xFFF
        # Kommando erzeugen, das gleichzeitig einen Teil des Werts enthaelt.
        # Siehe Datenblatt figure 6-1
        reg = value >> 8   # leave only the top 4 bits
        reg |= WRITEFAST   # include fast command
        self.writeList(reg, [value & 0xFF])

    def power_down(self,resistor=1):
        # In den Schlaf-Modus schalten, per Fast-Kommando
        if (resistor == 1) or (resistor == 100) or (resistor == 500):
            mode = POWER_DOWN[resistor]
            mode |= WRITEFAST
            self.writeList(mode, [0x00])
            return resistor
        else:
            return -1