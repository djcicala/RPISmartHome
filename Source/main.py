#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: main.py                                                          *
* Purpose:   Main loop for the RPI Smart Home.                                *
* Date:      12/05/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "2.0.0"

# imports
import configs
import temperature
import gui
import water_lawn
import systime 

import time

def main():
  # first, initialize the modules
  o_SystimeModule = systime.Systime()
  o_TemperatureModule = temperature.TemperatureModule(o_SystimeModule)
  o_WaterLawnModule   = water_lawn.WaterModule(o_SystimeModule, o_TemperatureModule.o_OutdoorTempSensor)
  o_GUI = gui.mainGUI()
  
  # this is the main loop of the program 
  while True:
    # first, we run the temperature module
    i_Error = o_TemperatureModule.main()
    
    # if the temp module didn't raise an error, run the water lawn module
    if(i_Error == configs.SYSERROR_NO_ERROR):
      print("here")
      i_Error = o_WaterLawnModule.main()
      
    # if the water module didn't raise an error, update the GUI
    if(i_Error == configs.SYSERROR_NO_ERROR):  
      o_GUI.update(o_TemperatureModule, o_WaterLawnModule)
    
    # if a temperature error was raised, re-initialize the module   
    if(i_Error == configs.SYSERROR_TEMP_INDOOR_SENSOR_FAILRUE
      or i_Error == configs.SYSERROR_TEMP_OUTDOOR_SENSOR_FAILURE):
      o_TemperatureModule = temperature.TemperatureModule(o_SystimeModule)
    
    # if a water error was raised, re-initialize the module
    if(i_Error == configs.SYSERROR_WL_API_CALL_FAILURE 
      or i_Error == configs.SYSERROR_WL_MOISTURE_SENSOR_FAILURE):
      o_TemperatureModule = temperature.TemperatureModule(o_SystimeModule)
      
    # 10 minute cycle time
    time.sleep(5)

if __name__ == "__main__":
  main()

################################## end file ###################################
