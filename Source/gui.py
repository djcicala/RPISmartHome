#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''****************************************************************************
* File Name: gui.py                                                           *
* Purpose:   GUI renderer using TKinter objects.                              *
* Date:      12/05/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
* Powered by the DarkSky API.                                                 *
****************************************************************************'''

# document version 
__version__ = "2.0.0"

# file imports
import configs
from tkinter import * 
import time
import urllib.request
import datetime
import json
from PIL import Image, ImageTk


# class to handle a single forecast. Members include temperature, chance of rain,
# weather condition (icon) and time (can be day or hour)
class SingleForecast:
  
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for a single forecast label                     
  * Parameters:  int i_X                                              
  *                    X location of the top left corner of the object. 
  *              int i_Y                                              
  *                    Y location of the top left corner of the object.
  *              obj   master
  *                    Master tkinter canvas.
  * Returns:     N/A                     
  *****************************************************************'''
  def __init__(self, master, i_X, i_Y):
    
    # string var is a type that allows you to update strings on the fly without
    # destroying the label each time
    self.o_Time    = StringVar()
    self.o_Temp    = StringVar()
    self.o_RainPct = StringVar()
    
    # default icon is cloudy
    self.o_Image   = Image.open("/home/pi/Git/RPISmartHome/Source/Images/cloudy.png")
    self.o_Image   = ImageTk.PhotoImage(self.o_Image)
    
    # padding on the ends of objects drawn
    self.i_Padx = 10
    self.i_Pady = 5
    
    # capture the x and y in in a self-referenced value
    self.i_Xin = i_X
    self.i_Yin = i_Y
    
    # this label can be time of day or day of the week
    self.o_TimeLabel = Label(master, textvariable = self.o_Time,
                               font=("Helvetica", 12, "bold"),
                               bg = "white",
                               fg = "black",
                               padx = self.i_Padx,
                               pady = self.i_Pady )
                               
    # this one is the icon indicating the type of weather                           
    self.o_ImageLabel = Label(master, image = self.o_Image,
                              borderwidth = 0,
                              highlightthickness = 0,
                              bg = 'white')
    
    # this one is the forecasted temperature for the given time                           
    self.o_TempLabel = Label(master, textvariable = self.o_Temp,
                               font=("Helvetica", 12, "bold"),
                               bg = "white",
                               fg = "black",
                               padx = self.i_Padx,
                               pady = self.i_Pady )
    
    # this is the chance of rain                           
    self.o_RainLabel = Label(master, textvariable = self.o_RainPct,
                               font=("Helvetica", 12, "bold"),
                               bg = "white",
                               fg = "black",
                               padx = self.i_Padx,
                               pady = self.i_Pady )
    
    # next we stack these labels and place them in the frame at an interval of 30
    # (64 for the icon since it is a 64x64 resolution)                           
    self.o_TimeLabel.place(x = self.i_Xin, y = self.i_Yin)
    self.o_ImageLabel.place(x = self.i_Xin, y = self.i_Yin + 30)
    self.o_TempLabel.place(x = self.i_Xin, y = self.i_Yin + 104)
    self.o_RainLabel.place(x = self.i_Xin, y = self.i_Yin + 134)
  

# this class handles the forecasts for twelve hours in advance 
class TwelveHourForecast:
  
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for a twelve hour forecast label                     
  * Parameters:  int i_X                                              
  *                    X location of the top left corner of the object. 
  *              int i_Y                                              
  *                    Y location of the top left corner of the object.
  *              obj   master
  *                    Master tkinter canvas.
  * Returns:     N/A                     
  *****************************************************************'''
  def __init__(self, master, i_X, i_Y):
    
    # overall title label for the group of objects
    self.o_TitleLabel = Label(master, text = "Next Twelve Hours",
                               font=("Helvetica", 12, "bold"),
                               bg = "blue",
                               fg = "white")
    
    # object should be appx centered                           
    self.o_TitleLabel.place(x=540, y=i_Y - 30)
    
    # create twelve forecast objects at a spacing of 100 pixels
    self.l_Forecasts = []
    for i in range(0,12):
      self.l_Forecasts.append(SingleForecast(master, i_X + (i * 100), i_Y))
  
  '''*****************************************************************
  * Name: update                                                                  
  * Description: Function to update the forecast for the next twelve hours.                   
  * Parameters:  obj o_Forecast
  *                  Iterable list of forecasts returned by the API.
  * Returns:     N/A                     
  *****************************************************************'''    
  def update(self, o_Forecast):
    self.o_Image = []
    # loop over all 12 forecasts returned by the API
    for i in range(0,12):
      # get the forecast for the current hour
      o_HourlyForecast = o_Forecast[i]
      
      # convert the time from UTC to a string like 12:30, 1:45
      s_TimeOfForecast = datetime.datetime.fromtimestamp(o_HourlyForecast["time"]).strftime("%I:%M")
      
      # get the image from the library with the icon returned from the API
      self.o_Image.append("")
      self.o_Image[i]   = Image.open("/home/pi/Git/RPISmartHome/Source/Images/" + o_HourlyForecast["icon"] + ".png")
      self.o_Image[i]   = ImageTk.PhotoImage(self.o_Image[i])
      
      # update all of the labels with the new information
      self.l_Forecasts[i].o_ImageLabel.config(image=self.o_Image[i])
      self.l_Forecasts[i].o_Time.set(s_TimeOfForecast)
      self.l_Forecasts[i].o_Temp.set(str(o_HourlyForecast["temperature"]))
      self.l_Forecasts[i].o_RainPct.set(str(o_HourlyForecast["precipProbability"]))

# this class handles the forecasts for the next five days instead of hourly      
class FiveDayForecast:
  
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for a five day forecast label                     
  * Parameters:  int i_X                                              
  *                    X location of the top left corner of the object. 
  *              int i_Y                                              
  *                    Y location of the top left corner of the object.
  *              obj   master
  *                    Master tkinter canvas.
  * Returns:     N/A                     
  *****************************************************************'''
  def __init__(self, master, i_X, i_Y):
    self.l_Forecasts = []
    
    # overall title for this section of the GUI
    self.o_TitleLabel = Label(master, text = "Next Five Days",
                               font=("Helvetica", 12, "bold"),
                               bg = "blue",
                               fg = "white")
    
    # label should be approximately centered                           
    self.o_TitleLabel.place(x=560, y=i_Y - 30)
    
    # create five forecast objects
    for i in range(0,5):
      self.l_Forecasts.append(SingleForecast(master, i_X + (i*100), i_Y))
      
  '''*****************************************************************
  * Name: update                                                                  
  * Description: Function to update the forecast for the next five days.                   
  * Parameters:  obj o_Forecast
  *                  Iterable list of forecasts returned by the API.
  * Returns:     N/A                     
  *****************************************************************'''      
  def update(self, o_Forecast):
    self.o_Image = []
    # loop over the forecasts
    for i in range(0,5):
      o_DailyForecast = o_Forecast[i]
      # get the day of thee week
      s_TimeOfForecast = datetime.datetime.fromtimestamp(o_DailyForecast["time"]).strftime("%A")
      
      # get the image from the library with the icon returned from the API
      self.o_Image.append("")
      self.o_Image[i]   = Image.open("/home/pi/Git/RPISmartHome/Source/Images/" + o_DailyForecast["icon"] + ".png")
      self.o_Image[i]   = ImageTk.PhotoImage(self.o_Image[i])
      
      # update the labels with the new information
      self.l_Forecasts[i].o_Time.set(s_TimeOfForecast)
      self.l_Forecasts[i].o_Temp.set(str(o_DailyForecast["temperatureHigh"]))
      self.l_Forecasts[i].o_RainPct.set(str(o_DailyForecast["precipProbability"]))

# this class handles the current states of the temperature system      
class TempSystemStates:
  
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for the temperature module labels.                     
  * Parameters:  int i_X                                              
  *                    X location of the top left corner of the object. 
  *              int i_Y                                              
  *                    Y location of the top left corner of the object.
  *              obj   master
  *                    Master tkinter canvas.
  * Returns:     N/A                     
  *****************************************************************'''
  def __init__(self, master, i_X, i_Y):
    
    # stringvars can be used to update labels without destroying them
    self.o_OutdoorTemp = StringVar()
    self.o_OutdoorHum  = StringVar()
    self.o_IndoorTemp  = StringVar()
    self.o_IndoorHum   = StringVar()
    self.o_TempSetting = StringVar()
    
    # padding for the label edges
    self.i_Padx = 10
    self.i_Pady = 5
    
    # this is the outdoor temperature rendering
    self.o_OutdoorTempLabel = Label(master, textvariable = self.o_OutdoorTemp,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the label for the outdoor temperature (should be static)                                
    self.o_OutdoorTempDesc = Label(master, text = "Outdoor Temperature:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
    
    # this is the outdoor humidity label                             
    self.o_OutdoorHumLabel  = Label(master, textvariable = self.o_OutdoorHum,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the label for the outdoor humidity (should be static)                                
    self.o_OutdoorHumDesc = Label(master, text = "Outdoor Humidity:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the outdoor temperature label                            
    self.o_IndoorTempLabel  = Label(master, textvariable = self.o_IndoorTemp,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the label for the indoor temperature (should be static)                                
    self.o_IndoorTempDesc = Label(master, text = "Indoor Temperature:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the indoor humidity label                            
    self.o_IndoorHumLabel  = Label(master, textvariable = self.o_IndoorHum,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the label for the indoor humidity (should be static)                                
    self.o_IndoorHumDesc = Label(master, text = "Indoor Humidity:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the recommended temperature setting as provided by the decision tree                            
    self.o_TempSettingLabel = Label(master, textvariable = self.o_TempSetting,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # this is the label for the set temperature (should be static)                                
    self.o_TempSettingDesc = Label(master, text = "Recommended Temperature:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
     
    # now lets place the labels where they belong     
    self.o_OutdoorTempDesc.place(x=i_X, y=i_Y)                       
    self.o_OutdoorTempLabel.place(x = i_X + 250, y = i_Y)
    
    self.o_OutdoorHumDesc.place(x=i_X, y=i_Y + 30)
    self.o_OutdoorHumLabel.place(x = i_X + 250, y = i_Y + 30)
    
    self.o_IndoorTempDesc.place(x = i_X, y = i_Y+60)
    self.o_IndoorTempLabel.place(x = i_X + 250, y = i_Y+60)
    
    self.o_IndoorHumDesc.place(x = i_X, y = i_Y + 90)
    self.o_IndoorHumLabel.place(x = i_X + 250, y = i_Y + 90)
    
    self.o_TempSettingDesc.place(x = i_X, y = i_Y+120)
    self.o_TempSettingLabel.place(x = i_X + 250, y = i_Y+120)
    
  '''*****************************************************************
  * Name: update                                                                  
  * Description: Function to update the current states of the temp module.                   
  * Parameters:  obj o_TempModule
  *                  Full temperature module to access its variables.
  * Returns:     N/A                     
  *****************************************************************'''   
  def update(self, o_TempModule):
    
    # set the action string based on the state of the module
    if(o_TempModule.i_HvacStateFlag == configs.i_DoNothingFlag):
      s_HvacAction = "Do nothing at "
    elif(o_TempModule.i_HvacStateFlag == configs.i_HeatFlag):
      s_HvacAction = "Heat at "
    else:
      s_HvacAction = "Cool at "
    
    # show Fahrenheit
    if(configs.SW_USE_METRIC_UNITS == False):
      self.o_OutdoorTemp.set(str(o_TempModule.o_OutdoorTempSensor.f_Temperature_F) + " °F")
      self.o_IndoorTemp.set(str(o_TempModule.o_IndoorTempSensor.f_Temperature_F) + " °F")
      self.o_TempSetting.set(s_HvacAction + str(o_TempModule.f_SetTemperature) + " °F")
    
    # otherwise, show Celsius
    else:
      self.o_OutdoorTemp.set(str(o_TempModule.o_OutdoorTempSensor.f_Temperature_C) + " °C")
      self.o_IndoorTemp.set(str(o_TempModule.o_IndoorTempSensor.f_Temperature_C) + " °C")
      self.o_TempSetting.set(s_HvacAction + str(o_TempModule.f_SetTemperature) + " °C")
    
    # show the humidity  
    self.o_OutdoorHum.set(str(o_TempModule.o_OutdoorTempSensor.f_Humidity_Pct) + "%")
    self.o_IndoorHum.set(str(o_TempModule.o_IndoorTempSensor.f_Humidity_Pct) + "%")
    
                                
# class to render the current states of the water system  
class WaterSystemStates:
  
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Constructor for the water module labels.                     
  * Parameters:  int i_X                                              
  *                    X location of the top left corner of the object. 
  *              int i_Y                                              
  *                    Y location of the top left corner of the object.
  *              obj   master
  *                    Master tkinter canvas.
  * Returns:     N/A                     
  *****************************************************************'''
  def __init__(self, master, i_X, i_Y):
    
    self.o_MoistureLvl = StringVar()
    self.o_NeedsWater  = StringVar()
    self.o_SprinklerSt = StringVar()
    
    self.i_Padx = 10
    self.i_Pady = 5
    
    # label for the moisture level value
    self.o_MoistureLvlLabel = Label(master, textvariable = self.o_MoistureLvl,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # descriptor label for the moisture level
    self.o_MoistureLvlDesc = Label(master, text = "Moisture Level:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # label for if the lawn or plant needs water                            
    self.o_NeedsWaterLabel  = Label(master, textvariable = self.o_NeedsWater,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # descriptor label for the water state                            
    self.o_NeedsWaterDesc = Label(master, text = "Water Level State:",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
    
    # value label for the sprinkler state                            
    self.o_SprinklerStLabel  = Label(master, textvariable = self.o_SprinklerSt,
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
                                
    # descriptor label for the sprinkler state                            
    self.o_SprinklerStDesc  = Label(master, text = "Sprinkler State: ",
                                font=("Helvetica", 12, "bold"),
                                bg = "white",
                                fg = "black",
                                padx = self.i_Padx,
                                pady = self.i_Pady )
    # place the labels with an offset of 30 with each row, 175 for each column                            
    self.o_MoistureLvlDesc.place(x=i_X, y=i_Y)                            
    self.o_MoistureLvlLabel.place(x = i_X + 175, y = i_Y)
    self.o_NeedsWaterDesc.place(x = i_X, y = i_Y + 30)
    self.o_NeedsWaterLabel.place(x = i_X + 175, y = i_Y + 30)
    self.o_SprinklerStDesc.place(x = i_X, y = i_Y + 60)
    self.o_SprinklerStLabel.place(x = i_X + 175, y = i_Y + 60)
  
  '''*****************************************************************
  * Name: update                                                                  
  * Description: Function to update the current states of the water module.                   
  * Parameters:  obj o_WaterModule
  *                  Full water module to access its variables.
  * Returns:     N/A                     
  *****************************************************************'''   
  def update(self, o_WaterModule):
    # set the water level percentage string
    self.o_MoistureLvl.set(str(o_WaterModule.o_WaterSensor.f_WaterLevel_Pct) + " %")
    
    # if the water flag is off, the system is OK
    if(o_WaterModule.i_WaterFlag == 0):
      self.o_NeedsWater.set("OK")
      self.o_NeedsWaterLabel.config(fg="green")
      self.o_SprinklerSt.set("OFF")
      
    # otherwise, the system needs water and the sprinkler should be on
    else:
      self.o_NeedsWater.set("Needs Water")
      self.o_NeedsWaterLabel.config(fg="red")
      self.o_SprinklerSt.set("ON")

class mainGUI:
  
  '''*****************************************************************
  * Name: __init__                                                                  
  * Description: Function to create the main GUI and tkinter canvas.                   
  * Parameters:  N/A
  * Returns:     N/A                     
  *****************************************************************''' 
  def __init__(self):
    
    # set window height and width
    self.windowH = 740
    self.windowW = 1240

    # master tkinter object
    self.master = Tk() 
    self.master.title('RPi Smart Home')
    self.master.geometry("%dx%d+0+0" % (self.windowW,self.windowH))
    self.master.config(bg="white")
    
    # create the label bins
    self.o_THF = TwelveHourForecast(self.master, 50, 100)
    self.o_FDF = FiveDayForecast(self.master, 400, 300)
    self.o_TSS = TempSystemStates(self.master, 100, 475)
    self.o_WSS = WaterSystemStates(self.master, 600,475)
  
  '''*****************************************************************
  * Name: update                                                                   
  * Description: Function to update and redraw the tkinter canvas.                   
  * Parameters:  obj o_TempModule
  *                  Full temperature module.
  *              obj o_WaterModule
  *                  Full water module.
  * Returns:     N/A                     
  *****************************************************************'''   
  def update(self, o_TempModule, o_WaterModule):
    print("update")
    self.o_WSS.update(o_WaterModule)
    self.o_TSS.update(o_TempModule)
    self.o_FDF.update(o_WaterModule.o_Forecast.l_DailyForecasts)
    self.o_THF.update(o_WaterModule.o_Forecast.l_HourlyForecasts)
    self.master.update()
    
################################## end file ###################################
