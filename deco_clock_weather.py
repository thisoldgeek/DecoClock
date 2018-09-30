#!/usr/bin/python3
import feedparser
import pi3d
import time
import datetime
import os
import urllib.request  as request 
import json
from PIL import Image, ImageDraw
from time import sleep

global time24
global display_interval
global display_start_time 
display_start_time =time.time()		# Keep track of how long screen is displayed, for switching

# user modifiable variables follow; default values for startup are already set
time24 = False				# If True, uses 24 hour clock, else 12 hour clock
clock_style = 2				# clock_style: 1 = white, 2 = green
wi_style = 2				# wi_style (weather icon style); 1 = plain/flat, 2 = art deco style
screen_num = 1				# 1 = Clock, 2 = Weather
rotate_display = False			# False: Show one screen only, either clock or weather based on screen_num; True: rotate screens every display_interval
display_interval = 30			# Switch between clock and weather every 'n' seconds

weather_API = False			# weather_API = False, use feedparser; True, use wunderground API with API key
centigrade = False			# centigrade = True, use degrees C; False, use degrees Fahrenheit

# user modifiable backlight variables; default values for startup are already set
dim_backlight = True			# If True, Turn STMPE control off, use GPIO 18 to dim screen; False = Full Brightness with STMPE
dim_start = 21				# Backlight starts dim mode at this hour, using 24hr style
dim_end = 7				# Backlight ends dim mode at this hour
dim_value = 100				# Backlight will be dimmed to this value (Range: 0-1023) during dark hours
full_brightness = 1023			# Backlight fulll brightness value for daylight hours

# DO NOT CHANGE program variable defaults that follow; : dim_staTE, STMPE
dim_state = False			# Program toggles to indicate if screen iS dim (= True) or normal brightness (= False)
STMPE = 1				# STMPE is ON; DO NOT MANUALLY CHANGE THIS! Set in code

# API Weather Variables - change for your Key and location
myKey = '***************'	# wunderground API Key - see wunderground developer's site to get yours
Location = 'CA/94523'		# your location US State/zip code
#Location = 'Australia/Sydney'	# English name for country/city
#Location = 'Germany/Munich'


# Feedparser Weather variables foloow

#
# For world-wide locations, condisder using the wunderground 4 letter ICAO airport code
# available at https://www.wunderground.com/about/faq/international_cities.asp
# This will return both Fahrenheit and Centigrade and should not break this script!
#

# LOCATION is a user modifiable variable you must set to display weather for your location

LOCATION =  "CA/Pleasant_Hill"  	# US Format: State/City
#LOCATION =  "WA/Seattle"
#LOCATION =  "NY/New_York"
#LOCATION =   "IL/Chicago"
#LOCATION =  "global/DE/Munich"		# Germany
#LOCATION =  "global/FR/Paris"		# France
#LOCATION  = "global/BR/Copacabana"     # Brazil
#LOCATION  = "global/NO/Oslo"		# Norway
#LOCATION  = "global/UK/London"		# United Kingdom
#LOCATION  =  "global/cn/ZBAA"		# Beijing Airport
#LOCATION  = "global/stations/cn/shenzhen/IGUANDON2"		# China: returned data in different format, no Centigrade
#LOCATION  = "global/ZA/Johannesburg"	# South Africa
#LOCATION  = "global/AU/Sydney"		# Australia
#LOCATION  = "global/NZ/Wellington"	# New Zealand
#LOCATION  = "global/mx/MMMX"           # Mexico City Airport
#LOCATION  = "global/mx/Monterrey"       			# Mexico: returned data in different format, no Centigrade


#pi3d Setup
DISPLAY = pi3d.Display.create(use_pygame=True, samples=4)
DISPLAY.set_background(0,0,0,1) #r,g,b and alpha
shader = pi3d.Shader("uv_flat")
CAMERA = pi3d.Camera(is_3d=False)


# Clock Face Sprites
if clock_style == 1:
	clock_face = pi3d.ImageSprite("textures/clock1_face.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	clock_hour = pi3d.ImageSprite("textures/clock1_hour_hand.png", shader,  w=128.0,  h=176.0,  x=12.0, y=-5.0, z=4.0)
	clock_min  = pi3d.ImageSprite("textures/clock1_minute_hand.png", shader,  w=16.0,  h=240.0,  x=12.0, y=-5.0, z=4.0)
	clock_sec  = pi3d.ImageSprite("textures/clock1_second_hand.png", shader,  w=16.0, h=164.0, x=12.0, y=-5.0, z=3.0)
	clock_center  = pi3d.ImageSprite("textures/clock1_center.png", shader,  w=16.0,  h=16.0,  x=12.0, y=-5.0, z=2.0)
elif clock_style == 2: 
	clock_face = pi3d.ImageSprite("textures/clock2_face.png",  shader,  w=320.0,  h=320.0,  x=15.0, y=-5.0, z=6.0)
	clock_hour = pi3d.ImageSprite("textures/clock2_hour_hand.png", shader,  w=32.0,  h=176.0,  x=15.0, y=-5.0, z=4.0)
	clock_min  = pi3d.ImageSprite("textures/clock2_minute_hand.png", shader,  w=16.0,  h=156.0,  x=15.0, y=-5.0, z=4.0)

# Weather Condition Sprites
weather_dial =  pi3d.ImageSprite("/home/pi/DecoClock/textures/weather_dial.png", shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
if wi_style == 1:
	sunny = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_sunny.png",  shader,  w=96.0,  h=80.0,  x=12.0, y=40.0, z=4.0)
	clouds = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_clouds.png",  shader,  w=112.0,  h=64.0,  x=16.0, y=50.0, z=4.0)
	partly_cloudy = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_partly_cloudy.png",  shader,  w=136.0,  h=88.0,  x=16.0, y=40.0, z=4.0)
	rain = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_rain.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
	thunder = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_thunder.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	snow = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_snow.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	wind = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_wind.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	fog = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_fog.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	smoke = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_smoke.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	haze = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_haze.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
	unknown = pi3d.ImageSprite("/home/pi/DecoClock/textures/wi_unknown.png",  shader,  w=320.0,  h=320.0,  x=12.0, y=-5.0, z=6.0)
elif wi_style == 2:
		sunny = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_sunny.png",  shader,  w=96.0,  h=80.0,  x=12.0, y=40.0, z=4.0)
		clouds = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_clouds.png",  shader,  w=112.0,  h=64.0,  x=16.0, y=50.0, z=4.0)
		partly_cloudy = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_partly_cloudy.png",  shader,  w=136.0,  h=88.0,  x=16.0, y=40.0, z=4.0)
		rain = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_rain.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
		thunder = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_thunder.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
		snow = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_snow.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
		wind = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_wind.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
		fog = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_fog2.png",  shader,  w=128.0,  h=96.0,  x=16.0, y=40.0, z=4.0)
		smoke = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_smoke.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
		haze = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_haze.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)
		unknown = pi3d.ImageSprite("/home/pi/DecoClock/textures/d_unknown.png",  shader,  w=112.0,  h=96.0,  x=16.0, y=30.0, z=4.0)


global myFont
global wi_font
# colors
gold=(233,215,127) # RGB Values
white=(1,1,1)
black=(0,0,0)
blue=(0,0,255)

myFont = pi3d.Font("/home/pi/DecoClock/fonts/DubbaDubbaNF.ttf", gold, font_size = 30)   #load ttf font and set the font color to gold
#wi_font = pi3d.Font("/home/pi/DecoClock/fonts/weathericons-regular-webfont.ttf", gold, font_size = 100)   #load ttf font and set the font color to gold


#Variables
#weather_check_time = 900 # Check the feed every 15 minutes if using weather underground free API- you only get 500 calls/day on free developer account
weather_check_time = 30 # Check the feed every 30 seconds if using weather underground feed parser; change to as little as 10 seconds
weather_start_time = time.time() - weather_check_time	# forces a weather api call on start-up
curr_cond = "clear"


def get_curr_conds():	# Optional Current Weather Conditions Display
	global feed
	global weather_start_time
	global weather_check_time
	global conds
	global temp_f
	global temp_c
	global shader
	global time24
	
	if time.time() - weather_start_time > weather_check_time:	# check the number of seconds in weather_check_time has passed
		weather_start_time = time.time()
		if weather_API:
			wuRequest = "http://api.wunderground.com/api/"+ myKey +"/geolookup/conditions/q/" + Location  + ".json"
			f = request.urlopen(wuRequest)
			json_string = f.read().decode('utf-8')
			parsed_json = json.loads(json_string)
			location = parsed_json['location']['city']
			conds =  parsed_json['current_observation']['weather']
			conds = conds.strip()  # get rid of spaces at beginning and end but not middle of string for dict (cond_face) lookup
			temp_c = parsed_json['current_observation']['temp_c']	# Use the appropriate units for your location, see below
			temp_f = parsed_json['current_observation']['temp_f']	
		elif weather_API is False:	
			d = feedparser.parse('http://rss.wunderground.com/auto/rss_full/'+LOCATION)
			# bozo is built-in feedparser flag for malformed feed
			if d.bozo: print(d.bozo_exception)  #trap error and print it out
			#d = feedparser.parse('http://rss.wunderground.com/auto/rss_full/CA/Pleasant_Hill')
			try:
				line =  str(d.entries[0].summary)
			except IndexError:
				print(time.strftime("%H:%M:%S", time.localtime()))," IndexError "

			# Format temp and conds	
			line = line.replace(":","|")
			#print line
			a = line.split("|")
			# print a
			mytemp = str(a[1])
			mytemp = mytemp.replace("&#176;", " ")
			mytemp = mytemp.replace("&deg;", " ")
			mytemp = mytemp.split("/")
		
			#b = a[11].split("/")

			# strip spaces at beginning and end but not in the middle
			temp_f = mytemp[0]
			temp_f = temp_f.strip()

			temp_c = mytemp[1]
			temp_c = temp_c.strip()
		
			#cond.strip REQUIRED for proper lookup in cond_face dict
			conds = a[7]
			conds = conds.strip()
	else:	
		pass
	
	cond_face = {"Light Dizzle":"rain",
		"Heavy Drizzle":"rain", 
		"Drizzle":"rain", 
		"Light Rain":"rain", 
		"Heavy Rain":"rain", 
		"Rain":"rain",
		"Clear":"sunny",
		"Light Snow":"snow", 
		"Heavy Snow":"snow", 
		"Snow":"snow", 
		"Light Fog":"fog", 
		"Heavy Fog":"fog", 
		"Fog":"fog", 
		"Light Fog Patches":"fog",
		"Heavy Fog Patches":"fog",
		"Fog Patches":"fog", 
		"Light Smoke":"smoke", 
		"Heavy Smoke":"smoke", 
		"Smoke":"smoke", 
		"Light Haze":"haze", 
		"Heavy Haze":"haze", 
		"Haze":"haze", 
		"Light Low Drifting Snow":"snow",
 		"Heavy Low Drifting Snow":"snow",  
		"Low Drifting Snow":"snow", 
		"Light Blowing Snow":"snow", 
		"Heavy Blowing Snow":"snow",
		"Blowing Snow":"snow", 
		"Light Rain Mist":"rain",
		"Heavy Rain Mist":"rain", 
		"Rain Mist":"rain", 
		"Light Rain Showers":"rain",
		"Heavy Rain Showers":"rain",
		"Rain Showers": "rain", 
		"Light Snow Showers":"snow",
		"Heavy Snow Showers":"snow", 
		"Snow Showers":"snow", 
		"Light Snow Blowing Snow Mist":"snow",
		"Heavy Snow Blowing Snow Mist":"snow", 
		"Snow Blowing Snow Mist":"snow", 
		"Light Thunderstorm":"thunder",
		"Heavy Thunderstorm":"thunder",
		"Thunderstorm":"thunder", 
		"Light Thunderstorms and Rain":"thunder", 
		"Heavy Thunderstorms and Rain ":"thunder",
		"Thunderstorms and Rain":"thunder",
		"Light Thunderstorms and Snow":"thunder", 
		"Heavy Thunderstorms and Snow ":"thunder",
		"Thunderstorms and Snow":"thunder", 
		"Patches of Fog":"fog",
		"Shallow Fog":"fog", 
		"Partial Fog":"fog",
 		"Overcast":"clouds", 
		"Partly Cloudy":"partly_cloudy", 
		"Mostly Cloudy":"clouds",
		"Scattered Clouds":"partly_cloudy"}

	weather_face = cond_face.get(conds)

	weather_dial.draw()  # draw the background for weather conds

	if weather_face == "sunny":
   		sunny.draw()
	elif weather_face == "rain":
		rain.draw()
	elif weather_face == "clouds":
		clouds.draw()
	elif weather_face == "partly_cloudy":
		partly_cloudy.draw()
	elif weather_face == "thunder":
		thunder.draw()
	elif weather_face == "snow":
		snow.draw()
	elif weather_face == "haze":
		haze.draw()
	elif weather_face == "smoke":
		smoke.draw()
	elif weather_face == "fog":
		fog.draw()
	else:   unknown.draw()
	
	if time24 is True:
		myTime = time.strftime("%H:%M")
	else:
		myTime = time.strftime("%-I:%M %p")

	if centigrade:	
		timetempStr = myTime +"  "+ str(temp_c)	# centigrade = True
	elif centigrade is False: 
		timetempStr = myTime +"  "+ str(temp_f)	
	

	dispTemp = pi3d.String(camera=CAMERA, is_3d=False, font=myFont, string=timetempStr,  x=12, y=-30, z=1.0)
	dispTemp.set_shader(shader)
	dispTemp.draw()

	dispConds = pi3d.String(camera=CAMERA, is_3d=False, font=myFont, string=conds,  x=12, y=-60, z=1.0)
	dispConds.set_shader(shader)
	dispConds.draw()
	
def dim_screen():
	global STMPE		# must be changed to "0" from "1" so GPIO PWM can change brightness value
	global dim_value	# PWM value for backlight when dim		
	global full_brightness	# PWM value for backlight when fully on 
	global dim_start	# start time for dim	
	global dim_end		# end time for dim, return to full brightness
	global dim_state	# dim True/False

	if STMPE == 1:	#STMPE is on at startup, should be turned off
		# STMPE code to turn off Backlight control, so PWM can control backlight brightness
		STMPE = 0
		os.system ("sudo sh -c 'echo ''0'' > /sys/class/backlight/soc\:backlight/brightness'")
		os.system('gpio -g mode 18 pwm')
		os.system('gpio pwmc 1000')
		os.system('gpio -g pwm 18 '+ str(full_brightness)) # backlight high
	else:
		pass
	
	now = datetime.datetime.now()
	t = now.hour	# will be in 24hr format
		
	if dim_state is False:
		if t >= dim_start:
			dim_state = True
			os.system('gpio -g pwm 18 '+ str(dim_value))  #backlight dim
	if dim_state is True and t <= 12:
		if t >= dim_end:
			dim_state = False 
			os.system('gpio -g pwm 18 '+ str(full_brightness)) # backlight high
		
	
# draw the sprites depending on screen_num passed from main
# this MUST be called from the Main Thread/Main while loop
def draw_sprites():
	global screen_num
	global display_start_time
	global display_interval
	global dim_backlight
	global dim_value

	if dim_backlight:
		dim_screen()

	if rotate_display is True:
		if time.time() - display_start_time > display_interval:	# check the number of seconds current display has been active
			display_start_time = time.time()
			if screen_num == 2:
				screen_num = 1
			else:
				screen_num = 2
		else:
			pass

	if screen_num == 1:	# draw the clock
		seconds= time.localtime(time.time()).tm_sec
		minutes= time.localtime(time.time()).tm_min
		hours = time.localtime(time.time()).tm_hour	
		clock_min.rotateToZ(360-(minutes*6-1))
		clock_hour.rotateToZ(360-hours*30-minutes*0.5)
		clock_face.draw()
		clock_min.draw()
		clock_hour.draw()	
		if clock_style == 1:
			clock_sec.rotateToZ(360-seconds*6)
			clock_center.draw()		
			clock_sec.draw()
	elif screen_num == 2:	#  Show Current Weather Conditions Screen
		get_curr_conds()

	return


while DISPLAY.loop_running():
  draw_sprites()
  sleep(.2)
