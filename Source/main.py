#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: main.py                                                          *
* Purpose:   Main loop for the RPI Smart Home.                                *
* Date:      11/26/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "0.3.0"

# imports
import configs
import temperature
#import gui
import water_lawn
import systime 

class Controller:
  def SystemInit():
    self.o_TemperatureModule = temperature.TemperatureModule()

def main():
  o_SystimeModule = systime.Systime()
  o_TemperatureModule = temperature.TemperatureModule(o_SystimeModule)
  o_WaterLawnModule   = water_lawn.WaterModule(o_SystimeModule, o_TemperatureModule.o_OutdoorTempSensor)
  while True:
    o_TemperatureModule.main()
    o_WaterLawnModule.main()
  

if __name__ == "__main__":
  main()

################################## end file ###################################
