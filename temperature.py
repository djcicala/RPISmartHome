'''****************************************************************************
* File Name: temperature.py                                                   *
* Purpose:   Methods and functions pertaining to the temperature module.      *
* Date:      11/25/2019                                                       *
* Copyright © 2019 Darren Cicala and Tyler Skene. All rights reserved.        *
****************************************************************************'''

# document version
__version__ = "0.3.0"

# imports
import configs      # global configs file
import Adafruit_DHT # library to interface with DHT11 sensor
import datetime     # library for time capturing

# class members: (todo)

class TemperatureSensor:
	
	'''*****************************************************************
	* Name: __init__                                                                  
	* Description: Constructor for class TemperatureSensor                      
	* Parameters:  int i_InputGPIOPin                                              
	*                    GPIO pin on the Pi that the sensor is wired to.                      
	* Returns:     N/A                     
	*****************************************************************'''
	def __init__(i_InputGPIOPin):
		self.i_SensorType = Adafruit_DHT.DHT11 # type of sensor
		self.i_GPIOPin    = i_InputGPIOPin     # what pin the sensor is connected to
		self.i_ErrorFlag  = configs.SYSERROR_NO_ERROR # shocker! we don't have any errors because we just initialized it
	
	'''*****************************************************************
	* Name: read                                                                  
	* Description: Function to read from the sensor, and update class members.                      
	* Parameters:  N/A                     
	* Returns:     N/A (modifies class members)                 
	*****************************************************************'''	
	def read():
		# update "previous" values
		self.f_HumidityPrev_Pct  = self.f_Humidity_Pct
		self.f_TemperaturePrev_C = self.f_Temperature_C
		self.f_TemperaturePrev_F = self.f_Temperature_F
		
		# get new values 
		self.f_Humidity_Pct, self.f_Temperature_C = Adafruit_DHT.read_retry(sensor_name, sensor_pin)
		self.f_Temperature_F = ((9/5) * self.f_Temperature_C) + 32

# class members 
class TemperatureModule:
	
	def __init__():
		self.o_OutdoorTempSensor = TemperatureSensor(configs.i_OutdoorSensorPin)
		self.o_IndoorTempSensor  = TemperatureSensor(configs.i_IndoorSensorPin)
	
	def DetermineSeason():.
	    o_TimeNow = datetime.datetime.now()
	    if ( o_TimeNow.month < configs.i_StartSummerMonth
	      or o_TimeNow.month > configs.i_EndSummerMonth):
	        self.i_Season = configs.i_WintertimeFlag
	    else:
			self.i_Season = configs.i_SummertimeFlag
			
	def DetermineTime():
		# determine time of day
		if (o_TimeNow.hour > configs.i_NighttimeHour or o_TimeNow.hour < configs.i_MorningHour):
			self.i_TimeFlag = configs.i_NightFlag
		else:
			self.i_TimeFlag = configs.i_DaytimeFlag
	'''*****************************************************************
	* Name: MakeHVACDecision                                                                  
	* Description: Makes a decision to cool or warm the house based on
	*              the external temperature of the system. This function
	*              should only be called for the external temperature sensor.                      
	* Parameters:  N/A                     
	* Returns:     ??                 
	*****************************************************************'''
    def MakeHVACDecision():
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
	    if  (f_OutdoorTemp < f_LocalHeatThreshold):
			
			# if its summer, don't do anything
		    if(self.i_Season == configs.i_SummertimeFlag):
				return configs.i_DoNothingFlag, f_OutdoorTemp
			
			# otherwise, if it is winter
			else:
				# if its night, dial down the setting 2 degrees F
				if (self.i_TimeFlag == configs.i_NightFlag):
					f_LocalTempSetting = configs.f_HeatSetting - configs.f_TemperatureSetback
				# if its day, heat at the normal temperature
				else:
					f_LocalTempSetting = configs.f_HeatSetting
					
			    return configs.i_HeatFlag, f_LocalTempSetting
			
		# case 2: "do nothing" state (between 65 and 75)
		elif(f_OutdoorTemp > f_LocalHeatThreshold and f_OutdoorTemp < f_LocalCoolThreshold):
		    
		    # if low humidity or night, don't do anything
		    if(f_OutdoorHumidity < f_LocalHumThresh_Pct or self.i_TimeFlag == configs.i_NightFlag):
			    return configs.i_DoNothingFlag, f_OutdoorTemp
			
			# otherwise cool to clear out the humidity
			else:
				return configs.i_CoolFlag, (f_OutdoorTemp - configs.f_TemperatureSetback)
				
		# case 3: cool state (temperature greater than 75)
		else:
			f_LocalTempSetting = configs.f_CoolSetting
		
			# if its night, increase the set temperature by 2
			if(self.i_TimeFlag == configs.i_NightFlag):
				f_LocalTempSetting += configs.f_TemperatureSetback
				
			# if high humidity, decrease the set temperature by 2
			if(f_OutdoorHumidity > f_LocalHumThresh_Pct):
				f_LocalTempSetting -= configs.f_TemperatureSetback
			
			return configs.i_CoolFlag, f_LocalTempSetting
			
    def ChangeSystemState():
		self.o_OutdoorTempSensor.read()
		self.o_IndoorTempSensor.read()
		
		i_HvacStateFlag, f_SetTemperature = MakeHVACDecision()
		
		if(configs.SW_USE_METRIC_UNITS):
			f_IndoorTemp = self.o_IndoorTempSensor.f_Temperature_C
		else:
		    f_IndoorTemp = self.o_IndoorTempSensor.f_Temperature_F
		
		if(abs(f_IndoorTemp - f_SetTemperature) > 5):
			i_HvacState = configs.i_HvacOn
		else:
			i_HvacState = configs.i_HvacOff
		
################################## end file ###################################
