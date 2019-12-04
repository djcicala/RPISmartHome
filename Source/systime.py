#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: systime.py                                                       *
* Purpose:   Methods and functions pertaining to timekeeping.                 *
* Date:      11/26/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "0.1.0"

# imports
import configs 
import datetime

class Systime:
  
  def __init__(self):
    self.o_TimeNow = datetime.datetime.now()
  
  def DetermineSeason(self):
    self.o_TimeNow = datetime.datetime.now()
    if ( self.o_TimeNow.month < configs.i_StartSummerMonth or self.o_TimeNow.month > configs.i_EndSummerMonth):
      self.i_Season = configs.i_WintertimeFlag
    else:
      self.i_Season = configs.i_SummertimeFlag
			
  def DetermineTime(self):
    self.o_TimeNow = datetime.datetime.now()
    # determine time of day
    if(self.o_TimeNow.hour > configs.i_NighttimeHour or self.o_TimeNow.hour < configs.i_MorningHour):
      self.i_TimeFlag = configs.i_NightFlag
    else:
      self.i_TimeFlag = configs.i_DaytimeFlag

################################## end file ###################################
