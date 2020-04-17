# -*- coding: utf-8 -*-
"""

@author: varan
"""

import spidev
import time
import argparse 
import sys
import navio.mpu9250
import navio.util

import sys, time
import time
import sys, time

import navio.rcinput
import navio.util

import navio.ms5611
import navio.util


import navio.adc
import navio.util
parser = argparse.ArgumentParser()
parser.add_argument("-i", help = "Sensor selection: -i [sensor name]. Sensors names: mpu is MPU9250, lsm is LSM9DS1")
baro = navio.ms5611.MS5611()
baro.initialize()


if len(sys.argv) == 1:
    print "Enter parameter"
    parser.print_help()
    sys.exit(1)
elif len(sys.argv) == 2:
    sys.exit("Enter sensor name: mpu or lsm")

args = parser.parse_args()

if args.i == 'mpu':
    print "Selected: MPU9250"
    imu = navio.mpu9250.MPU9250()
elif args.i == 'lsm':
    print "Selected: LSM9DS1"
    imu = navio.lsm9ds1.LSM9DS1()
else:
    print "Wrong sensor name. Select: mpu or lsm"
    sys.exit(1)



if imu.testConnection():
    print "Connection established: True"
else:
    sys.exit("Connection established: False")

imu.initialize()

time.sleep(1)



adc = navio.adc.ADC()
results = [0] * adc.channel_count
rcin = navio.rcinput.RCInput()


while (True):
        s = ''
        for i in range (0, adc.channel_count):
            results[i] = adc.read(i)
            s += 'A{0}: {1:6.4f}V '.format(i, results[i] / 1000)
        print(s)
    # imu.read_all()
	# imu.read_gyro()
	# imu.read_acc()
	# imu.read_temp()
	# imu.read_mag()

	# print "Accelerometer: ", imu.accelerometer_data
	# print "Gyroscope:     ", imu.gyroscope_data
	# print "Temperature:   ", imu.temperature
	# print "Magnetometer:  ", imu.magnetometer_data

	# time.sleep(0.1)

	m9a, m9g, m9m = imu.getMotion9()

	print "Acc:", "{:+7.3f}".format(m9a[0]), "{:+7.3f}".format(m9a[1]), "{:+7.3f}".format(m9a[2]),
	print " Gyr:", "{:+8.3f}".format(m9g[0]), "{:+8.3f}".format(m9g[1]), "{:+8.3f}".format(m9g[2]),
	print " Mag:", "{:+7.3f}".format(m9m[0]), "{:+7.3f}".format(m9m[1]), "{:+7.3f}".format(m9m[2])
        baro.refreshPressure()
	time.sleep(0.01) # Waiting for pressure data ready 10ms
	baro.readPressure()

	baro.refreshTemperature()
	time.sleep(0.01) # Waiting for temperature data ready 10ms
	baro.readTemperature()

	baro.calculatePressureAndTemperature()

	print "Temperature(C): %.6f" % (baro.TEMP), "Pressure(millibar): %.6f" % (baro.PRES)

        period = rcin.read(2)
        print period
        time.sleep(1)


        time.sleep(5)
