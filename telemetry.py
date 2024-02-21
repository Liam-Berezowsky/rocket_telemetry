#!/usr/bin/env python3

import random
from time import sleep 
import config


class TemperatureSensor:

    def read(_self):
        return random.randint(1, 100)


if __name__ == '__main__':
    print('telemetry active')

    temperatureSensor = TemperatureSensor()
    while True:
        temperature =temperatureSensor.read() 
        print(temperature)
        sleep(config.time_delay_s)
