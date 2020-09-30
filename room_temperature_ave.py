#!/usr/bin/python

import sys
import Adafruit_DHT
import time
import os
from statistics import stdev, median

sensor = 22
pin = 17

output_dir="/home/pi/reporting/"

def average(l):
    return(sum(l)/len(l))    

readings = [] 
h_readings = []
while (True):
    try:
        temps = []
        humids = []
        for i in range(3):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            temperature = temperature * 9/5.0 + 32
	    if humidity is not None and temperature is not None:
                temps.append(float(temperature))
                humids.append(float(humidity))
        if stdev(temps) > 1:
            temps.remove(min(temps))
        if stdev(humids) > 1:
            humids.remove(min(humids))

        if sum(humids) > 300:
            continue
        
        readings.append(average(temps))
        h_readings.append(average(humids))

        if len(readings) > 3:
            readings = readings[-3:]

        if len(h_readings) > 3:
            h_readings = h_readings[-3:]

        print h_readings
        temps = average(readings)
        humids = average(h_readings)
        print temps
        print humids
        t = open(output_dir + "temps.foo", "a")
        t.write("room_temperature %f\n" % float(temps))
        t.close()

        h = open(output_dir + "humids.foo", "a")
        h.write("room_humidity %f\n" % humids)
        h.close()

        os.rename(output_dir + "temps.foo", output_dir + "temps.prom")
        os.rename(output_dir + "humids.foo", output_dir + "humids.prom")
    except:
        print "failed"
        pass

    time.sleep(15)
