#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: systime.py                                                       *
* Purpose:   Methods and functions pertaining to timekeeping.                 *
* Date:      12/05/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version
__version__ = "1.0.0"

# imports
import configs 
import datetime

# class to track the time of day and season
class Systime:
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for class Systime                      
  * Parameters:  N/A                    
  * Returns:     N/A                     
  *****************************************************************'''  
  def __init__(self):
    self.o_TimeNow = datetime.datetime.now()
  
  '''*****************************************************************
  * Name: DetermineSeason                                                                  
  * Description: Determines the current season. When it is not summer,
  *              it is winter. Summer is May 1-Sept 1.                      
  * Parameters:  N/A                    
  * Returns:     N/A (modifies class members)                    
  *****************************************************************'''
  def DetermineSeason(self):
    self.o_TimeNow = datetime.datetime.now()
    if ( self.o_TimeNow.month < configs.i_StartSummerMonth or self.o_TimeNow.month > configs.i_EndSummerMonth):
      self.i_Season = configs.i_WintertimeFlag
    else:
      self.i_Season = configs.i_SummertimeFlag
	
  '''*****************************************************************
  * Name: DetermineTime                                                                  
  * Description: Determines the current time of day. When it is not day,
  *              it is night. Daytime is defined from 9am to 9pm.                      
  * Parameters:  N/A                    
  * Returns:     N/A (modifies class members)                    
  *****************************************************************'''		
  def DetermineTime(self):
    self.o_TimeNow = datetime.datetime.now()
    # determine time of day
    if(self.o_TimeNow.hour > configs.i_NighttimeHour or self.o_TimeNow.hour < configs.i_MorningHour):
      self.i_TimeFlag = configs.i_NightFlag
    else:
      self.i_TimeFlag = configs.i_DaytimeFlag

################################## end file ###################################
