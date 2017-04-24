# PC7 = Fan 
# PC4 = Dry Heat Source
# PA8 = Humid Heat Source
# PA20 = Temp/Humidity Sensor

from pyA20.gpio import gpio
from pyA20.gpio import port
import dht11
import time
import datetime

gpio.init()
PIN = port.PA20
gpio.setcfg(port.PA20, gpio.OUTPUT)
gpio.setcfg(port.PC4, gpio.OUTPUT)
gpio.setcfg(port.PC7, gpio.OUTPUT)
gpio.output(port.PC4, gpio.HIGH)
gpio.output(port.PC7, gpio.HIGH)

instance = dht11.DHT11(pin=PIN)
Fan = 0
DryHeat = 0
while True:
    result = instance.read()
    if (result.temperature) == 0:
      continue 
    tempHI = 39
    tempLOW = 37
    humidHIGH = 65
    humidLOW = 50
    print "Temp n Humidity Results:", result.temperature, result.humidity
    DATA = [ result.temperature, result.humidity ]  
    if (result.temperature) >= tempHI and Fan == 0:
      print "Detected High Temp, humidity seems okay, Turning on fan, turning off dry heat source"
      gpio.setcfg(port.PC7, gpio.OUTPUT)
      gpio.setcfg(port.PC4, gpio.OUTPUT)
      gpio.output(port.PC7, gpio.LOW) 
      gpio.output(port.PC4, gpio.HIGH)
      Fan = 1
      DryHeat = 0
      HumidHeat = 0 
      elif (result.humidity) <= humidLOW:
        print "Detected High Temp & High humidity, Turning on fan, and turning off both dry and humid heat sources"
        gpio.setcfg(port.PC7, gpio.OUTPUT)
        gpio.setcfg(port.PA8, gpio.OUTPUT)
        gpio.setcfg(port.PC4, gpio.OUTPUT)
        gpio.output(port.PC7, gpio.LOW) 
        gpio.output(port.PC4, gpio.HIGH)
        gpio.output(port.PA21, gpio.LOW)
        Fan = 1
        DryHeat = 0
        HumidHeat = 0
        else:
          print "Detected High Temp & Low humidity, Turning on humid heat source, turning off dry heat source and turning on Fan"
          gpio.setcfg(port.PC7, gpio.OUTPUT)
          gpio.setcfg(port.PA21, gpio.OUTPUT)
          gpio.setcfg(port.PC4, gpio.OUTPUT)
          gpio.output(port.PC7, gpio.LOW) 
          gpio.output(port.PC4, gpio.HIGH)
          gpio.output(port.PA21, gpio.LOW)
          Fan = 1
          DryHeat = 0
          HumidHeat = 1

    if (result.temperature) <= tempLOW and (result.temperature) != 0 and DryHeat != 1:
      print "Detected Low Temp humidity seems okay, turning off fan and turning dry heat source on"
      gpio.setcfg(port.PC7, gpio.OUTPUT)
      gpio.setcfg(port.PC4, gpio.OUTPUT)
      gpio.output(port.PC7, gpio.HIGH)
      gpio.output(port.PC4, gpio.LOW)
      Fan = 1 
      DryHeat = 1
      HumidHeat = 0
      elif (result.humidity) <= humidLOW:
        print "Detected Low Temperature & Low Humidity, Turning on fan, and turning on humid heat source"
        gpio.setcfg(port.PC7, gpio.OUTPUT)
        gpio.setcfg(port.PA8, gpio.OUTPUT)
        gpio.setcfg(port.PC4, gpio.OUTPUT)
        gpio.output(port.PC7, gpio.LOW) 
        gpio.output(port.PC4, gpio.HIGH)
        gpio.output(port.PA8, gpio.LOW)
        Fan = 0
        DryHeat = 0
        HumidHeat = 1
        else:
          print "Detected Low Temperature & High Humidity, Turning off humid heat source, turning on dry heat source and Fan"
          gpio.setcfg(port.PC7, gpio.OUTPUT)
          gpio.setcfg(port.PA8, gpio.OUTPUT)
          gpio.setcfg(port.PC4, gpio.OUTPUT)
          gpio.output(port.PC7, gpio.LOW) 
          gpio.output(port.PC4, gpio.LOW)
          gpio.output(port.PA8, gpio.HIGH)
          Fan = 1
          DryHeat = 1
          HumidHeat = 0
    time.sleep(5)
