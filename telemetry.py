#!/usr/bin/env python3


class TemperatureSensor:

    def read(_self):
        return 10


if __name__ == '__main__':
    print('telemetry active')

    temperatureSensor = TemperatureSensor()
    while True:
        temperature =temperatureSensor.read() 
        print(temperature)
