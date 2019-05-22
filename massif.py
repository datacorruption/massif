from __future__ import unicode_literals
import youtube_dl
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from random import randrange
import math

print ("")
print ("'||    ||'     |      .|'''.|   .|'''.|  '||' '||''''| ")
print (" |||  |||     |||     ||..  '   ||..  '   ||   ||  .   ")
print (" |'|..'||    |  ||     ''|||.    ''|||.   ||   ||''|   ")
print (" | '|' ||   .''''|.  .     '|| .     '||  ||   ||      ")
print (".|. | .||. .|.  .||. |'....|'  |'....|'  .||. .||.     v1.0")
print ("")

# HIKING CALCULATOR SECTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Capture and validate all user inputs.

# ROUTE LENGTH | DEFAULT: NONE >>>
while True:
	try:
		route_length = float(input("Length of route in miles: "))
	except ValueError:
		print("Not an appropriate entry.")
		continue

	if route_length <= 0:
		print("Bumboclaat! Galang!")
		continue
	else:
		print(route_length)
		break


# HIKING SPEED | DEFAULT: 3.0 >>>

while True:
	try:
		speed = float(input("Average hiking speed in mph [3.0]: ") or "3.0")
	except ValueError:
		print("Not an appropriate entry.")
		continue

	if speed <= 0:
		print("Bumboclaat! Galang!")
		continue
	else:
		print(speed)
		break


# ASCENT | DEFAULT: 0 >>>

while True:
	try:
		ascent = int(input("Total ascent in feet [0]: ") or "0")
	except ValueError:
		print("Not an appropriate entry.")
		continue

	if ascent < 0:
		print("Bumboclaat! Galang!")
		continue
	else:
		print(ascent)
		# If there is any ascent on the route, add an extra hour per 2000 ft of ascent.
		ascent_modifier = ascent / 2000
		break


# PACK WEIGHT | DEFAULT: A (LIGHT) >>>

while True:
	try:
		pack = input("Weight of pack [a] light (b) regular (c) heavy: ") or "a"
	except ValueError:
		print("Sorry, I didn't understand that.")
		continue

	if pack.lower() not in ('a', 'b', 'c'):
		print("Not an appropriate choice.")
		continue
	else:
		# Pack was successfully parsed, and we're happy with its value.
		# If carrying a lightweight pack, our hiking speed is unchanged.
		if pack == "b":
			# If carrying a regular pack, decrease hiking speed by 0.25 mph
			speed = speed - 0.25
		elif pack == "c":
			 # If carrying a heavy pack, decrease hiking speed by 0.5 mph
			speed = speed - 0.5
		# Check hiking speed, exit program if too low after pack weight calculation.
		if speed <= 0:
			print("Unable to calculate hike duration because your adjusted hiking speed was too low.")
			print("Try again with a faster hiking speed or lighter pack.")
			exit()
		print(pack)
		break # Exit the loop.


# TERRAIN | DEFAULT: 0 >>>

while True:
	try:
		terrain = int(input("Percent of route over challenging terrain [0]: ") or "0")
	except ValueError:
		print("Not an appropriate entry. Must be an integer between 0 and 100.")
		continue

	if terrain < 0 or terrain > 100:
		print("Not an appropriate entry. Must be an integer between 0 and 100.")
		continue
	else:
		# Terrain was successfully parsed, and we're happy with its value.
		# Check hiking speed, exit program if too low after terrain calculation.
		if terrain > 0 and (speed - 1) <= 0:
			print("Unable to calculate hike duration because your adjusted hiking speed was too low.")
			print("Try again with a faster hiking speed or a route over less challenging terrain.")
			exit()
		print(terrain)
		route_length_challenging = route_length * (terrain/100)
		route_length_regular = route_length - route_length_challenging
		terrain_modifier = ((route_length * (terrain/100)) / (speed - 1))
		duration_of_hike = terrain_modifier + (route_length_regular / speed) + ascent_modifier
		break


# WEATHER CONDITIONS | DEFAULT: A (GOOD) >>>

while True:
	try:
		weather = input("Weather conditions during hike [a] good (b) poor (c) severe: ") or "a"
	except ValueError:
		print("Sorry, I didn't understand that.")
		continue

	if weather.lower() not in ('a', 'b', 'c'):
		print("Not an appropriate choice.")
		continue
	else:
		# Weather was successfully parsed, and we're happy with its value.
		# If hiking in good conditions, duration of hike is unchanged.
		if weather == "b":
			# If hiking in poor conditions, add 25% more time to the duration of the hike.
			weather_modifier = duration_of_hike * 0.25 
		elif weather == "c":
			# If hiking in severe conditions, add 50% more time to the duration of the hike.
			weather_modifier = duration_of_hike * 0.5
		else: 
			weather_modifier = 0
		print(weather)
		break # Exit the loop.


# CRUNCH THE REMAINING NUMBERS >>>

duration_of_hike = duration_of_hike + weather_modifier
duration_hours = int(math.floor(duration_of_hike))
duration_minutes = int((duration_of_hike % 1) * 60)
print("\nDuration of hike:", duration_hours, "hr", duration_minutes, "min", "\n")

# ASK USER IF THEY WOULD LIKE GENERATE A PLAYLIST >>>

while True:
	try:
		generate_playlist = input("Would you like to generate a playlist for your hike (Y/N)? ")
	except ValueError:
		print("\nBumboclaat!\n")
		continue

	if generate_playlist.lower() not in ('y', 'n'):
		print("Not an appropriate choice.")
		continue
	else:
		if generate_playlist == "n":
			print ("\nWi run tings, tings nuh run wi! Galang!")
			exit()
		else:
			break


# YOUTUBE-DL SETUP SECTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])
    elif d['status'] == 'finished':
        print('Done downloading, now converting ...')


# PLAYLIST GENERATOR SECTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

playlist_length = datetime.timedelta()
hike_duration = str(duration_hours) + ":" + str(duration_minutes).zfill(2) + ":00"
FMT = '%H:%M:%S'

# USE CREDS TO CREATE A CLIENT TO INTERACT WITH THE GOOGLE DRIVE API >>>

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# FIND A WORKBOOK BY NAME AND OPEN THE FIRST SHEET >>>

sheet = client.open("MASSIF - Jungle Database").sheet1

# POPULATE LISTS WITH EXTRACTED TRACK URLS AND LENGTHS >>>

artists_list = sheet.col_values(1)
artists_list.pop(0) # drop column heading
tracktitles_list = sheet.col_values(2)
tracktitles_list.pop(0) # drop column heading
urls_list = sheet.col_values(3)
urls_list.pop(0) # drop column heading
tracklengths_list = sheet.col_values(4)
tracklengths_list.pop(0) # drop column heading

while True:
	random_index = randrange(len(tracklengths_list))
	item = tracklengths_list[random_index]
	(h, m, s) = item.split(':')
	d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
	playlist_length +=d

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    },
	    {
			'key': 'FFmpegMetadata',
	    }
	    ],
	    'logger': MyLogger(),
	    'progress_hooks': [my_hook],
	    'ignoreerrors': True,
	    'outtmpl' : r'music/{} - {}.%(ext)s'.format(artists_list[random_index], tracktitles_list[random_index])
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([str(urls_list[random_index])])
	tracklengths_list.pop(random_index)
	urls_list.pop(random_index)
	tracktitles_list.pop(random_index)
	artists_list.pop(random_index)

	if (datetime.datetime.strptime(hike_duration, FMT) - datetime.datetime.strptime(str(playlist_length), FMT)).days < 0:
		print("BABYLON SHALL FALL!")
		print("Hike duration: ", str(hike_duration))
		print("Playlist duration: ", str(playlist_length))
		break