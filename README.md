<p align="center"><img src="https://user-images.githubusercontent.com/2317743/58094890-b51b6a00-7b9f-11e9-8504-4ae553ba1ed2.png"></p>

<b>massive</b> <i>noun</i></br>
/ˈmasiv/</br>
The people, the crew, lovers of jungle and drum & bass.

<b>massif</b> <i>noun</i></br>
/maˈsēf/</br>
A principal mountain mass.

# About

MASSIF is the first hiking calculator by and for junglists. It is a command line utility that helps you plan hikes by approximating the duration of your route and generating a playlist of jungle and drum & bass music to match. Planning a hike with MASSIF requires that you know the following:

- Length of your route
- Your average hiking speed
- Ascent during your route
- Terrain of your route
- Weather conditions
- Weight of your pack
- Whether or not you're a junglist

Based on these parameters MASSIF will use generally accepted heuristics, such as [Naismith’s Rule](https://en.wikipedia.org/wiki/Naismith%27s_rule), along with Aitken corrections for terrain and ascent to calculate an approximate duration for the hike.

It will then present the option of generating an accompanying playlist. Track selections are currently based on the Top 100 Most Wanted Jungle / Drum & Bass Records Released in 1994-1995 based on [Discogs data from August 17, 2010](https://data.discogs.com). 

At the moment the database contains 12 hours 57 minutes 23 seconds of music.

<br />
<p align="center"><img src="https://user-images.githubusercontent.com/2317743/57045143-bb6e9400-6c3a-11e9-8479-ece10220b79e.png" /></p>

# Requirements
- Python3
- Network Connection (for playlist generation only)

# Dependencies
- youtube-dl
- gspread
- oauth2client

# Setup

Install Python3

```sh
$ pip install --upgrade youtube_dl
$ pip install --upgrade gspread
$ pip install --upgrade oauth2client
```

# Usage

```sh
$ python3 massif.py
```

Follow onscreen instructions.


# To Do
- Continue building up music database
- Improve ID3 tagging
- Improve error handling
- Improve CLI UX


# Who Made This?
I'm [Jeremiah Johnson](http://jeremiahjohnson.rip) — electronic musician, creative technologist, and hiker. Currently designing, coding, consulting, and directing the artist residency program at [Barbarian](https://wearebarbarian.com). Previously, I’ve worked as a Data Engineer at Columbia University Medical Center, Adjunct Professor at New York University, Creative Director for an international music festival, and contributor to O'Reilly's technical books. I have a music production studio in Brooklyn where I use modular synths and drum machines alongside obsolete videogame consoles to produce under the name [𝑵𝑼𝑳𝑳𝑺𝑳𝑬𝑬𝑷](http://nullsleep.com) in a wide range of styles. During 2018, I wrote and recorded one new song every week for the entire year — you can find many of them on [my soundcloud](https://soundcloud.com/nullsleep).

Twitter: [@Nullsleep](https://twitter.com/Nullsleep)</br>
Instagram: [@Nullsleep](https://instagram.com/Nullsleep)
