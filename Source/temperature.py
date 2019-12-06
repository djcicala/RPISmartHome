#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: temperature.py                                                   *
* Purpose:   Methods and functions pertaining to the temperature module.      *
* Date:      12/05/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "2.0.0"

# imports
import configs      # global configs file
import Adafruit_DHT # library to interface with DHT11 sensor
import datetime     # library for time capturing
import time 


# this class will read from the temperature sensor and store values read from it
class TemperatureSensor:
	
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for class TemperatureSensor                      
  * Parameters:  int i_InputGPIOPin                                              
  *                    GPIO pin on the Pi that the sensor is wired to.                      
  * Returns:     N/A                     
  *****************************************************************'''
  def __init__(self,i_InputGPIOPin):
    self.i_SensorType = Adafruit_DHT.DHT11 # type of sensor
    self.i_GPIOPin    = i_InputGPIOPin     # what pin the sensor is connected to
    self.i_ErrorFlag  = configs.SYSERROR_NO_ERROR # shocker! we don't have any errors because we just initialized it
	
  '''*****************************************************************
  * Name: read                                                                  
  * Description: Function to read from the sensor, and update class members.                      
  * Parameters:  N/A                     
  * Returns:     N/A (modifies class members)                 
  *****************************************************************'''	
  def read(self):
    # get new values using the Adafruit library
    self.f_Humidity_Pct, self.f_Temperature_C = Adafruit_DHT.read_retry(self.i_SensorType, self.i_GPIOPin)
    if(self.f_Temperature_C != None):
      self.f_Temperature_F = (1.8 * self.f_Temperature_C) + 32

# this class is the main loop for the temperature module 
class TemperatureModule:

  '''*****************************************************************
  * Name: init                                                                  
  * Description: Function to initialize the main temperature module.                      
  * Parameters:  obj o_InputSysTime
  *                  Systime module to determine season and time of day.                     
  * Returns:     N/A (modifies class members)                 
  *****************************************************************'''		
  def __init__(self, o_InputSysTime):
    self.o_OutdoorTempSensor = TemperatureSensor(configs.i_OutdoorSensorPin)
    self.o_IndoorTempSensor  = TemperatureSensor(configs.i_IndoorSensorPin)
    self.o_SysTime = o_InputSysTime
  
  '''*****************************************************************
  * Name: ReadSensors                                                                  
  * Description: Function to read new data from the temperature sensors.                      
  * Parameters:  N/A                     
  * Returns:     int i_ErrorFlag
  *                  Error flag raised when a sensor read error occurs.                 
  *****************************************************************'''	
  def ReadSensors(self):
    # read the data from the sensors
    self.o_OutdoorTempSensor.read()
    self.o_IndoorTempSensor.read()
    
    # check here for errors in sensor communication. sensor will return None if
    # its connection is disconnected
    if(self.o_OutdoorTempSensor.f_Temperature_C == None):
      self.i_ErrorFlag = configs.SYSERROR_TEMP_OUTDOOR_SENSOR_FAILURE
    elif(self.o_IndoorTempSensor.f_Temperature_C == None):
      self.i_ErrorFlag = configs.SYSERROR_TEMP_OUTDOOR_SENSOR_FAILURE
    else:
      self.i_ErrorFlag = configs.SYSERROR_NO_ERROR
    return self.i_ErrorFlag
      
  '''*****************************************************************
  * Name: MakeHVACDecision                                                                  
  * Description: Makes a decision to cool or warm the house based on
  *              the external temperature of the system. This function
  *              should only be called for the external temperature sensor.                      
  * Parameters:  N/A                     
  * Returns:     int   i_StateFlag
  *                    Flag that indicates whether to heat/cool the system.
  *              float f_Temperature
  *                    Floating point temperature setting.
  *****************************************************************'''
  def MakeHVACDecision(self):
    # get local copies of variables 
    o_TimeNow             = datetime.datetime.now()
    f_LocalHeatThreshold  = configs.f_HeatThreshold
    f_LocalCoolThreshold  = configs.f_CoolThreshold
    f_LocalHumThresh_Pct  = configs.f_HumThreshold_Pct
    f_OutdoorHumidity     = self.o_OutdoorTempSensor.f_Humidity_Pct
    
    # convert data if metric units are desired 
    if(configs.SW_USE_METRIC_UNITS):
      f_OutdoorTemp = self.o_OutdoorTempSensor.f_Temperature_C
    else:
      f_OutdoorTemp = self.o_OutdoorTempSensor.f_Temperature_F
      
    # case 1: external temp less than 65 degrees F (don't care abt. hum.)
    if(f_OutdoorTemp < f_LocalHeatThreshold):
      
      # if its summer, don't do anything
      if(self.o_SysTime.i_Season == configs.i_SummertimeFlag):
        return configs.i_DoNothingFlag, f_OutdoorTemp
      
      # otherwise, if it is winter
      else:
        # if its night, dial down the setting 2 degrees F
        if (self.o_SysTime.i_TimeFlag == configs.i_NightFlag):
          f_LocalTempSetting = configs.f_HeatSetting - configs.f_TemperatureSetback
        # if its day, heat at the normal temperature
        else:
          f_LocalTempSetting = configs.f_HeatSetting
          
        return configs.i_HeatFlag, f_LocalTempSetting
      
    # case 2: "do nothing" state (between 65 and 75)
    elif(f_OutdoorTemp > f_LocalHeatThreshold and f_OutdoorTemp < f_LocalCoolThreshold):
        
      # if low humidity or night, don't do anything
      if(f_OutdoorHumidity < f_LocalHumThresh_Pct or self.o_SysTime.i_TimeFlag == configs.i_NightFlag):
        return configs.i_DoNothingFlag, f_OutdoorTemp
      
      # otherwise cool to clear out the humidity
      else:
        return configs.i_CoolFlag, (f_OutdoorTemp - configs.f_TemperatureSetback)
        
    # case 3: cool state (temperature greater than 75)
    else:
      f_LocalTempSetting = configs.f_CoolSetting
    
      # if its night, increase the set temperature by 2
      if(self.o_SysTime.i_TimeFlag == configs.i_NightFlag):
        f_LocalTempSetting += configs.f_TemperatureSetback
        
      # if high humidity, decrease the set temperature by 2
      if(f_OutdoorHumidity > f_LocalHumThresh_Pct):
        f_LocalTempSetting -= configs.f_TemperatureSetback
      
      return configs.i_CoolFlag, f_LocalTempSetting
      
  
  '''*****************************************************************
  * Name: ChangeSystemState                                                                  
  * Description: Function to either turn the system on or off.                      
  * Parameters:  N/A                     
  * Returns:     int i_HvacState
  *                  Flag to indicate if the thermostat is on (1) or off (0)                 
  *****************************************************************'''	
  def ChangeSystemState(self):
    
    # use metric units if desired
    if(configs.SW_USE_METRIC_UNITS):
      f_IndoorTemp = self.o_IndoorTempSensor.f_Temperature_C
    else:
        f_IndoorTemp = self.o_IndoorTempSensor.f_Temperature_F
    
    # if the indoor temperature is outside of the set comfort range, turn it on
    if(abs(f_IndoorTemp - self.f_SetTemperature) > configs.f_ComfortZoneRange):
      i_HvacState = configs.i_HvacOn
    else:
      i_HvacState = configs.i_HvacOff
    
    return i_HvacState
   
  '''*****************************************************************
  * Name: main                                                                  
  * Description: Main loop of the temperature module                      
  * Parameters:  N/A                     
  * Returns:     int i_Error
  *                  Error flag indicating an error within the system.                 
  *****************************************************************'''	  
  def main(self):
    print("===========================Start Temp Module")
    
    # use the systime module to determine the season and time of day
    self.o_SysTime.DetermineSeason()
    self.o_SysTime.DetermineTime()
    
    # read the temperature sensors
    i_Error = self.ReadSensors()
    
    # if the sensors returned no error, run through our decision trees and
    # print some output 
    if(i_Error == configs.SYSERROR_NO_ERROR):
      self.i_HvacStateFlag, self.f_SetTemperature = self.MakeHVACDecision()
      self.i_HvacState = self.ChangeSystemState()
      print("Flag:" + str(self.i_HvacStateFlag))
      print("Setting:" + str(self.f_SetTemperature))
      print("State:" + str(self.i_HvacState))
      print("Indoor Temp:" +str(self.o_IndoorTempSensor.f_Temperature_F))
      print("Outdoor Temp:" +str(self.o_OutdoorTempSensor.f_Temperature_F))
      print("Outdoor Humid:" +str(self.o_OutdoorTempSensor.f_Humidity_Pct))
      print("===================================End Temp Module")
      return i_Error
    
    # otherwise, just return the error code
    else:
      print("Error raised in temperature module! Error code: %d"%(i_Error))
      return i_Error
################################## end file ###################################
