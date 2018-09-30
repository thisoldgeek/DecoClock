# **Art Deco Clock and Weather**
![Art Deco Clock](https://github.com/thisoldgeek/DecoClock/blob/master/Deco_Clock_for_READme.jpg "Art Deco Clock and Weather Display")
 
## *Description:*
A 3D printed case in the sytle of Gilbert Rohde Model 6356 for Herman Miller.

In the as-built version of this project, I'm using the free downloadable Deco typefont from Nick Curtis, called "Dubba Dubba". If you like Nick's work, please contribute a few $$ at: http://www.1001fonts.com/search.html?search=dubba+dubba&x=10&y=6

See the posting at (future):

hackster.io/thisoldgeek Art Deco Clock


## *Required Hardware:*
* raspberry pi zero W
* Adafruit piTFT Plus 3.5in display
* Optional but highly recommended: right-angle micro-usb to barrel connector
* 4x M2.5/3mm screws, steel

## *Fabrication:*
* 3D print files in STL_files folder
* 3D printed case required; other 3d parts optional
* See docs folder for 3D print settings

## *Configuration:*
 Install python programs and run scripts. See tutorial at hackster.io/thisoldgeek
 The following are the program variable defaults; change to your preference

  user modifiable variables follow; default values for startup are already set
* time24 = False  			#If True, uses 24 hour clock, else 12 hour clock
* clock_style = 2			# clock_style: 1 = white, 2 = green
* wi_style = 2				# wi_style (weather icon style); 1 = plain/flat, 2 = art deco style
* screen_num = 1				# 1 = Clock, 2 = Weather; weather needs configuration
* rotate_display = False	 # False: Show one screen only, either clock or weather based on screen_num; True: rotate screens every display_interval
* display_interval = 30			# Switch between clock and weather every 'n' seconds

* weather_API = False			# weather_API = False, use feedparser; True, use wunderground API with API key
* centigrade = False			# centigrade = True, use degrees C; False, use degrees Fahrenheit

 user modifiable backlight variables; default values for startup are already set
* dim_backlight = True			# If True, Turn STMPE control off, use GPIO 18 to dim screen; False = Full Brightness with STMPE
* dim_start = 21			# Backlight starts dim mode at this hour, using 24hr style
* dim_end = 7				# Backlight ends dim mode at this hour
* dim_value = 100			# Backlight will be dimmed to this value (Range: 0-1023) during dark hours
* full_brightness = 1023		# Backlight fulll brightness value for daylight hours

## * Defaults on Startup *
* Clock is Green
* screen_num = 1 means ONLY a clock will display

## * Weather Display Settings *
* Weather is displayed if display_rotate = True, OR if screen_num = 2 AND display_rotate = False
* You MUST set LOCATION variable for your area if using weather
* Default - weather_API = False,  use feedparser; if True, use wunderground API and supply wunderground API key
* Default - Art Deco style weather icons used if weather is chosen
* centigrade = False, Fahrenheit is used
* time24 = False, AM/PM is shown; True, 00:00 thru 23:59 shown
* Default display_interval = 30; time in seconds before screen transitions to clock or weather if display_rotate = True

## * Dimmer Settings *
* Default - screen is dim between hours of 8PM/21:00 and 7:00AM


## *REQUIRED:*
Intentionally blank

## *More Information:*
See the build log at https://www.hackster.io/thisoldgeek/Art Deco Clock
## *Update September 2018:*
Initial install.
