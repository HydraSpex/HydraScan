#!/usr/bin/env python

import spidev
import math

PotiValues = [[10, 13],
                [9.5, 14],
                [9, 15],
                [8.5, 16],
                [8, 17],
                [7.5, 18],
                [7, 19],
                [6.5, 21],
                [6, 22],
                [5.5, 24],
                [5, 26],
                [4.5, 30],
                [4, 33],
                [3.5, 38],
                [3, 45],
                [2.5, 54],
                [2, 68],
                [1.5, 90],
                [1, 136],
                [0.5, 255]
                ]

class MCP4151_0(object):
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 976000

        self.write_pot(12)
        
    def scan_val(self, input):
        i = 0
        result = -1
        elem_to_find = 2
        while i < len(PotiValues):
                if PotiValues[i][0] == input:
                    result = PotiValues[i][1]
                i += 1
        return result

    def write_pot(self, input):
        msb = input >> 8
        lsb = input & 0xFF
        self.spi.xfer([msb, lsb])

    def write_range(self, input):
        PotVal = self.scan_val(input)
        if PotVal != -1:
            self.write_pot(PotVal)


