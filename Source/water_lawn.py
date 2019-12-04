#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''****************************************************************************
* File Name: water_lawn.py                                                    *
* Purpose:   Methods and functions pertaining to the water lawn module.       *
* Date:      11/26/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "0.3.0"

# imports 
import configs                # global configs file for the system
import urllib.request         # library to handle HTTPGet requests
import json                   # library to handle JSON parsing
from Adafruit_GPIO import SPI # library for SPI communication
import Adafruit_MCP3008       # library for decoding the output of the ADC
import datetime               # library for time capturing
import time

class Forecast:
  
  # do an initial API call when we create the object 
  def __init__(self):
    # get the API string from the configs file
    self.s_APILink = configs.s_FullAPI   
    # make an API request 
    s_Contents = urllib.request.urlopen(self.s_APILink).read().decode("utf-8") 
    # dump the return string into a dictionary
    self.d_ForecastInformation = json.loads(s_Contents)
    
  def update(self):
    # make an API request 
    s_Contents = urllib.request.urlopen(self.s_APILink).read().decode("utf-8") 
    # dump the return string into a dictionary
    self.d_ForecastInformation = json.loads(s_Contents)
    # capture the hourly forecasts for ease of access 
    self.l_HourlyForecasts = self.d_ForecastInformation["hourly"]["data"]
    self.CheckForRain()
    
  def CheckForRain(self):
    
    self.i_Rain = 1
    for each_forecast in self.l_HourlyForecasts:
      if(each_forecast["precipProbability"] > 0.40):
        self.i_Rain = 1
        return
    self.i_Rain = 0
    
class WaterSensor:
  def __init__(self):
    self.o_AdcDevice = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(configs.i_SPIDevice, configs.i_SPIPort))
    #self.o_SysTime   = o_Systime
    
  def read(self):
    i_DigitalValue = self.o_AdcDevice.read_adc_difference(configs.i_AdcChannel)
    self.f_WaterLevel_Pct = 100 * (i_DigitalValue / configs.i_WaterSensorScalar)

class WaterModule:
  def __init__(self, o_InputSysTime, o_OutdoorTemperatureSensor):
    self.o_WaterSensor = WaterSensor()
    self.o_Forecast = Forecast()
    self.o_OutdoorTempSensor = o_OutdoorTemperatureSensor #TemperatureSensor(configs.i_OutdoorSensorPin)
    self.o_SysTime = o_InputSysTime
    self.i_WaterFlag = 0
    self.f_SoilMoistureWilt = configs.f_Wilt
    self.f_SoilMoistureCapacity = configs.f_Capacity
                                                
  def ReadSensors(self):
    self.o_WaterSensor.read()
    self.o_OutdoorTempSensor.read()
    
  def MakeWateringDecision(self):
    #get refreshed values
    self.o_Forecast.update()
    
    #check temperature and 
    if self.o_OutdoorTempSensor.f_Temperature_F < 40 or self.o_Forecast.i_Rain == 1:
      self.i_WaterFlag = 0
      
    elif self.i_WaterFlag == 1 and datetime.datetime.now() >= self.o_LastWaterTime:
      if self.o_WaterSensor.f_WaterLevel_Pct > self.f_SoilMoistureCapacity:
        self.i_WaterFlag = 0
      else:
        self.o_LastWaterTime = datetime.datetime.now()
    elif self.i_WaterFlag == 0:
      if self.o_WaterSensor.f_WaterLevel_Pct < self.f_SoilMoistureWilt:
        self.i_WaterFlag = 1
        self.o_LastWaterTime = datetime.datetime.now()                                          
                                                
  def main(self):
      self.ReadSensors()
      self.MakeWateringDecision()                                          
      print("Should we water?: " + str(self.i_WaterFlag))
      print(self.o_WaterSensor.f_WaterLevel_Pct)


################################## end file ###################################
