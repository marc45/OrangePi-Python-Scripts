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
    print "Temp n Humidity Results:", result.temperature, result.humidity
    DATA = [ result.temperature, result.humidity ]  
    if (result.temperature) >= tempHI and Fan == 0:
      print "Detected High Temp, fan is not activated, Turning on fan and turning off light if active"
      gpio.setcfg(port.PC7, gpio.OUTPUT)
      gpio.output(port.PC7, gpio.LOW) 
      gpio.output(port.PC4, gpio.HIGH)
      Fan = 1
      DryHeat = 0
    if (result.temperature) <= tempLOW and (result.temperature) != 0 and DryHeat != 1:
      print "Detected Low Temp,turning off fan and turning dry heat source on"
      gpio.setcfg(port.PC7, gpio.OUTPUT)
      gpio.output(port.PC7, gpio.HIGH)
      gpio.output(port.PC4, gpio.LOW)
      Fan = 0 
      DryHeat = 1
    time.sleep(5)
