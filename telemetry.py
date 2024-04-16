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
    timer = Timer()
    print("time,MET,temperature,pressure,humidity")
    while True:
        data = esensor.read()
        print("{},{:.4f},{:.2f},{:.2f},{:.2f}".format(timer.str(), timer.met(), data.temperature, data.pressure, data.humidity))
        sleep(config.time_delay_s)
