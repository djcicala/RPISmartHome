# RPISmartHome
This is a modular, automated smarthome designed to run on a Raspberry Pi Model 3B. This project was undertaken for the course ECE 574 for the University of Michigan-Dearborn.

For comprehensive documentation, check out the Documentation folder.

Software libraries used:
- TKinter for GUI rendering
- Adafruit_DHT for reading from the DHT11 sensors
- Adafruit_GPIO for reading from the SPI bus between the ADC and the Pi
- Adafruit_MCP3008 for interpreting the data from the SPI bus into usable information
- datetime for easy time capturing
- time for sleep operations
- urllib for handling HTTPGet requests
- json for JSON parsing
- PIL for image conversion

Hardware Bill of Materials:
- (1) Raspberry Pi Model 3B 
- (1) Raspberry Pi Power Supply (5.0V, 2.5A rating)
- (1) 32 GB SD Card flashed with Raspbian
- (2) DHT11 temperature and moisture sensors
- (1) VMA303 water level and moisture sensor
- (1) MCP3008 Analog to Digital Converter (ADC)
- (1) HDMI Monitor, or VGA monitor w/ HDMI dongle
- Wires and/or breadboard

Current features include: GUI rendering of forecasts, thermostat functionality, and lawn watering regulation.

Notable thanks: 

http://www.softicons.com/web-icons/vector-stylish-weather-icons-by-bartosz-kaszubowski for providing a free library of weather icons. Used under license https://creativecommons.org/licenses/by-nc-sa/3.0/.

https://darksky.net/ for providing a free (and quite comprehensive) weather API.
