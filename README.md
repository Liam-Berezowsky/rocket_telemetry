# rocket_telemetry

# Summary

This code supports a Raspberry Pi telemetry system.

Running the telemetry.py with appropriate electronic wiring will output a CSV with the raw data for:

| Column | Description |
| ------ | ----------- |
| time| data point timestamp |
| MET | Mission elapsed time |
| temperature | Ambient temperature |
| pressure | Barometric pressure |
| humidity | Relative humidity |
| acc_x |X axis translation acceleration |
| acc_y | Y axis translation acceleration |
| acc_z | Z axis translation acceleration |
| gyr_x | X axis rotation acceleration |
| gyr_y | Y axis rotation acceleration |
| gyr_z | Z axis rotation acceleration |

The next step is to calibrate these values into standard units after environment experimentation

1. Some time in the fridge and outside to match temperature value to real temperature (or at least calibrate better)
2. Use real altitude differences of some known structures to calibrate the altitude using pressure value
3. Compare interior home humidity from Ecobee to calibrate humidity
4. Measure the acceleration using the unit attached to my RC car. Not sure yet about rotation.

# Images

## Power Management Unit

<img src="images/powermanagement.jpg" alt="Alt text" width="600" />

# Some Personal Reminders

## connect over wifi

ssh liam@192.168.1.180
cd rocket_telemetry

## git reminders

* git status
* git commit [-m "message"]
* git push
* git pull
