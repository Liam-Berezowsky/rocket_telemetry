#!/usr/bin/env python3

import random
from time import sleep, gmtime, strftime, time
import config
import smbus2
import bme280

class TemperatureSensor:

    def read(_self):
        return random.randint(1, 100)


if __name__ == '__main__':
    print('telemetry active')
    address = 0x76
    bus = smbus2.SMBus(1)
    calibration_params = bme280.load_calibration_params(bus, address)
    starttime = time()
    print("time,MET,temperature,pressure,humidity")
    while True:
        data = bme280.sample(bus, address, calibration_params)
        now = time()
        met = now - starttime
        now_str = strftime("%d/%m/%Y %H:%M:%S", gmtime(now))
        rem = int((now - int(now)) * 10000)
        print("{}.{:.0f},{:.4f},{:.2f},{:.2f},{:.2f}".format(now_str, rem, met, data.temperature, data.pressure, data.humidity))
        sleep(config.time_delay_s)
