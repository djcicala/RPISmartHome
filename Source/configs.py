#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: configs.py                                                       *
* Purpose:   Global variables and configurations for RPI Smart Home.          *
* Date:      11/26/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# Note: none of the values in this file are meant to be used as variables.
# they can be equated to #define macros in C/C++.

# document version
__version__ = "0.4.1"

# there should be no imports in this file!

############################## Global Switches #################################
SW_USE_METRIC_UNITS = False

################################ Error Codes ###################################
SYSERROR_NO_ERROR                    = 0
SYSERROR_TEMP_OUTDOOR_SENSOR_FAILURE = 1
SYSERROR_TEMP_INDOOR_SENSOR_FAILRUE  = 2
SYSERROR_WL_MOISTURE_SENSOR_FAILURE  = 3
SYSERROR_WL_API_CALL_FAILURE         = 4
SYSERROR_GUI_GENERAL_FAILURE         = 5

############################### API information ################################

s_ApiBase            = "https://api.darksky.net/forecast/"     # root API 
s_ApiKey             = "dea7ee9f3820aa9e6f8c6f1528ebb0aa" # modify this with your own darksky key
s_GPSLocation_LatLon = "42.344137,-83.309652" # modify this with your own GPS coordinates, e.g. "37.5148,15.7891"
s_FullAPI = s_ApiBase + s_ApiKey +  "/" + s_GPSLocation_LatLon # full API path

######################### Temperature sensor information #######################

i_IndoorSensorPin  = 17   # modify this with your own sensor signal pin for the outside
i_OutdoorSensorPin = 26   # modify this with your own sensor signal pin for indoors

i_DoNothingFlag  = 0  # flag state indicating system will not heat or cool
i_HeatFlag       = 1  # flag state indicating system will heat 
i_CoolFlag       = 2  # flag state indicating system will cool

i_HvacOff = 0
i_HvacOn  = 1

f_HeatThreshold  = 65 # temperature (in F) that the system will switch to heating
f_CoolThreshold  = 75 # temperature (in F) that the system will switch to cooling

f_HeatSetting        = 68 # temp to se
f_CoolSetting        = 75
f_TemperatureSetback = 2
f_ComfortZoneRange   = 5

if SW_USE_METRIC_UNITS:
  f_HeatThreshold = (0.55556 * f_HeatThreshold) - 32
  f_CoolThreshold = (0.55556 * f_CoolThreshold) - 32
  f_HeatSetting   = (0.55556 * f_HeatSetting) - 32
    
  f_TemperatureSetback = 1.11 
  f_ComfortZoneRange   = 2.75
  f_CoolSettingLowHum  = (0.55556 * f_CoolSettingLowHum) - 32
  f_CoolSettingHighHum = (0.55556 * f_CoolSettingHighHum) - 32
    
f_HumThreshold_Pct = 50

########################### Moisture Sensor Configs ############################

# note: to enable SPI for you:
# 1. run sudo raspi-config
# 2. go to interfacing options
# 3. go to SPI, press enter to enable
# 4. check to see if /dev/spidev0.0 exists, this is the SPI device shown below
i_SPIDevice = 0
i_SPIPort   = 0

i_AdcChannel = 2 # read channel 2 of the ADC

i_WaterSensorScalar = 1024 # ADC outputs (0,1024), will scale to a percentage

#turn sprinkler on and off
i_SprinklerOff = 0
i_SprinklerOn = 1

#time to start and end rain check
i_StartRain = 6   #based on time before sun rises 5AM
i_EndRain = 17    #based on usual peak hotness of day 5PM

#percentage of precipitation that counts as going to rain
f_ExpectRainPercent = 0.65

#1:Sand, 2:Loamy Sand, 3:Sandy Loam, 4:Loam, 5:Silt Loam, 6:Silty Clay Loam, 7:Clay Loam
#8:Sandy Clay Loam, 9:Sandy Clay, 10:Silty Clay, 11:Clay
i_SandType = 4

#Sand
if i_SandType == 1:
  f_Wilt = 5.5
  f_Capacity = 10
#Loamy Sand
elif i_SandType == 2:
  f_Wilt = 9.25
  f_Capacity = 16
#Sandy Loam
elif i_SandType == 3:
  f_Wilt = 12
  f_Capacity = 21
#Loam
elif i_SandType == 4:
  f_Wilt = 15.75
  f_Capacity = 27
#Silt Loam
elif i_SandType == 5:
  f_Wilt = 18.75
  f_Capacity = 30
#Silty Clay Loam
elif i_SandType == 6:
  f_Wilt = 24
  f_Capacity == 36
#Clay Loam
elif i_SandType == 7:
  f_Wilt = 21.5
  f_Capacity = 32
#Sandy Clay Loam
elif i_SandType == 8:
  f_Wilt = 20.75
  f_Capacity = 29
#Sandy Clay
elif i_SandType == 9:
  f_Wilt = 18.25
  f_Capacity = 28
#Silty Clay
elif i_SandType == 10:
  f_Wilt = 25
  f_Capacity = 40
#Clay
elif i_SandType == 11:
  f_Wilt = 26.5
  f_Capacity = 40
  


############################## Timing Configs ##################################
# note: all times considered to be in military time
i_NighttimeHour = 21  # when does night start?
i_MorningHour   = 9   # when does the day start?

i_SummertimeFlag = 0  # the current state of the system is summertime
i_WintertimeFlag = 1  # the current state of the system is wintertime

i_DaytimeFlag = 0  # the current state of the system is day
i_NightFlag   = 1  # the current state of the system is night

i_StartSummerMonth = 4  # summer starts in May
i_EndSummerMonth   = 10 # summer ends in October
################################## end file ####################################
