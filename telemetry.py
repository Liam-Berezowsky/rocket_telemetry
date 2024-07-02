#!/usr/bin/env python3

import random
from time import sleep, gmtime, strftime, time
import config
import smbus2
import bme280


class EnvironmentSensor:

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.calibration_params = bme280.load_calibration_params(bus, address)

    def read(self):
        return bme280.sample(self.bus, self.address, self.calibration_params)


class PositionalData:

    def __init__(self, Ax, Ay, Az, Gx, Gy, Gz):
        self.Ax = Ax
        self.Ay = Ay
        self.Az = Az
        self.Gx = Gx
        self.Gy = Gy
        self.Gz = Gz


class PositionalSensor:

    def __init__(self, bus, Device_Address):
        self.PWR_MGMT_1   = 0x6B
        self.SMPLRT_DIV   = 0x19
        self.CONFIG       = 0x1A
        self.GYRO_CONFIG  = 0x1B
        self.INT_ENABLE   = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H  = 0x43
        self.GYRO_YOUT_H  = 0x45
        self.GYRO_ZOUT_H  = 0x47 
        self.bus = bus
        self.Device_Address = Device_Address

        #write to sample rate register
        bus.write_byte_data(Device_Address, self.SMPLRT_DIV, 7)
        
        #Write to power management register
        bus.write_byte_data(Device_Address, self.PWR_MGMT_1, 1)
        
        #Write to Configuration register
        bus.write_byte_data(Device_Address, self.CONFIG, 0)
            
        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, self.GYRO_CONFIG, 24)
    
        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, self.INT_ENABLE, 1)

    def read_raw_data(self, addr):
        #Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr+1)
        
        #concatenate higher and lower value
        value = ((high << 8) | low)
            
        #to get signed value from mpu6050
        if(value > 32768):
            value = value - 65536
        return value

    def read(self):
        return PositionalData(
            self.read_raw_data(self.ACCEL_XOUT_H)/16384.0,
            self.read_raw_data(self.ACCEL_YOUT_H)/16384.0,
            self.read_raw_data(self.ACCEL_ZOUT_H)/16384.0,
            self.read_raw_data(self.GYRO_XOUT_H)/131.0,
            self.read_raw_data(self.GYRO_YOUT_H)/131.0,
            self.read_raw_data(self.GYRO_ZOUT_H)/131.0
        )


class Timer:
   
    def __init__(self):
        self.starttime = time()

    def str(self):
        now = time()
        now_str = strftime("%d/%m/%Y %H:%M:%S", gmtime(now))
        rem = int((now - int(now)) * 10000)
        return "{}.{:.0f}".format(now_str, rem)

    def met(self):
        return time() - self.starttime


if __name__ == '__main__':
    print('telemetry active')
    bus = smbus2.SMBus(1)
    esensor = EnvironmentSensor(bus, 0x76)
    psensor = PositionalSensor(bus, 0x68)
    timer = Timer()

    with open("log.csv","w") as log:
        log.write("time,MET,temperature,pressure,humidity,acc_x,acc_y,acc_z,gyr_x,gyr_y,gyr_z\n")
        while True:
            edata = esensor.read()
            pdata = psensor.read()
            log.write("{},{:.4f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(
                timer.str(),
                timer.met(),
                edata.temperature, 
                edata.pressure, 
                edata.humidity,
                pdata.Ax,
                pdata.Ay,
                pdata.Az,
                pdata.Gx,
                pdata.Gy,
                pdata.Gz
                ))
            log.flush()
            sleep(config.time_delay_s)
