from smbus import SMBus
import time


class ArduinoLogic(object):
    def __init__(self):
        self.addr1 = 0x8
        self.addr2 = 0x9
        self.bus = SMBus(1)
        self.counter1 = 0
        self.counter2 = 0

    def closeDevice(self):
        print("Device colsed")

    def captureDual(self, ms):
        self.ms = ms
        try:
            self.bus.write_byte(self.addr1, self.ms)
            self.bus.write_byte(self.addr2, self.ms)
        except:
            self.bus.write_byte(self.addr1, self.ms)
            self.bus.write_byte(self.addr2, self.ms)
        time.sleep((self.ms)/1000)
        try:
            Data1 = self.bus.read_i2c_block_data(self.addr1, 0)
            LSB1 = Data1[0]
            MSB1 = Data1[1]
            self.counter1 = (MSB1 << 8) + LSB1
            Data2 = self.bus.read_i2c_block_data(self.addr2, 0)
            LSB2 = Data2[0]
            MSB2 = Data2[1]
            self.counter2 = (MSB2 << 8) + LSB2
        except:
            try:
                Data1 = self.bus.read_i2c_block_data(self.addr1, 0)
                LSB1 = Data1[0]
                MSB1 = Data1[1]
                self.counter1 = (MSB1 << 8) + LSB1
                Data2 = self.bus.read_i2c_block_data(self.addr2, 0)
                LSB2 = Data2[0]
                MSB2 = Data2[1]
                self.counter2 = (MSB2 << 8) + LSB2
            except:
                try:
                    self.bus.write_byte(self.addr1, self.ms)
                    self.bus.write_byte(self.addr2, self.ms)
                except:
                    self.bus.write_byte(self.addr1, self.ms)
                    self.bus.write_byte(self.addr2, self.ms)
                    time.sleep(self.ms/1000)
                try:
                    Data1 = self.bus.read_i2c_block_data(self.addr1, 0)
                    LSB1 = Data1[0]
                    MSB1 = Data1[1]
                    self.counter1 = (MSB1 << 8) + LSB1
                    Data2 = self.bus.read_i2c_block_data(self.addr2, 0)
                    LSB2 = Data2[0]
                    MSB2 = Data2[1]
                    self.counter2 = (MSB2 << 8) + LSB2
                except:
                    pass
                    
        return self.counter1, self.counter2


    def capture1(self, ms):
        self.ms = ms
        try:
            self.bus.write_byte(self.addr1, self.ms)
        except:
            self.bus.write_byte(self.addr1, self.ms)
        time.sleep((self.ms)/1000)
        try:
            Data1 = self.bus.read_i2c_block_data(self.addr1, 0)
            LSB1 = Data1[0]
            MSB1 = Data1[1]
            self.counter1 = (MSB1 << 8) + LSB1
        except:
            try:
                Data1 = self.bus.read_i2c_block_data(self.addr1, 0)
                LSB1 = Data1[0]
                MSB1 = Data1[1]
                self.counter1 = (MSB1 << 8) + LSB1
            except:
                try:
                    self.bus.write_byte(self.addr1, self.ms)
                except:
                    self.bus.write_byte(self.addr1, self.ms)
                    time.sleep(self.ms/1000)
                try:
                    Data1 = self.bus.read_i2c_block_data(self.addr1, 0)
                    LSB1 = Data1[0]
                    MSB1 = Data1[1]
                    self.counter1 = (MSB1 << 8) + LSB1
                except:
                    pass

        return self.counter1


    def capture2(self, ms):
        self.ms = ms
        try:
            self.bus.write_byte(self.addr2, self.ms)
        except:
            self.bus.write_byte(self.addr2, self.ms)
        time.sleep((self.ms)/1000)
        try:
            Data2 = self.bus.read_i2c_block_data(self.addr2, 0)
            LSB2 = Data2[0]
            MSB2 = Data2[1]
            self.counter2 = (MSB2 << 8) + LSB2
        except:
            try:
                Data2 = self.bus.read_i2c_block_data(self.addr2, 0)
                LSB2 = Data2[0]
                MSB2 = Data2[1]
                self.counter2 = (MSB2 << 8) + LSB2
            except:
                try:
                    self.bus.write_byte(self.addr2, self.ms)
                except:
                    self.bus.write_byte(self.addr2, self.ms)
                    time.sleep(self.ms/1000)
                try:
                    Data2 = self.bus.read_i2c_block_data(self.addr2, 0)
                    LSB2 = Data2[0]
                    MSB2 = Data2[1]
                    self.counter2 = (MSB2 << 8) + LSB2
                except:
                    pass

        return self.counter2

#APD = ArduinoLogic()
#count = APD.captureDual(5)
#print(count[0])
#print(count[1])
