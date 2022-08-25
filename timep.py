#!/usr/bin/env python3
# coding=utf8

import sys
import calendar
from datetime import date

today = date.today()
this_month = today.month
this_year = today.year
#this_month = this_month + 1
#this_year = 2004
#leap_year = 2004

# import urllib library
from urllib.request import urlopen

# import json
import json
# store the URL in url as
# parameter for urlopen
url = "https://holidays-jp.github.io/api/v1/date.json"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())

arg = sys.argv
argc = len(arg)
if (argc > 2):
    print('Usage: python %s [1-12]' % arg[0])
    sys.exit()
    
if (argc == 2):
    try:
        x = int(arg[1])
        if x < this_month:
            this_year = this_year + 1
        this_month = x
    except ValueError:
        print('Usage: python %s [1-12]' % arg[0])
        sys.exit()

jp_isoweekday = ["月", "火", "水", "木", "金", "土", "日"]
month_ends = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
year_ends = 365

if calendar.isleap(this_year):
    month_ends[1] = 29
    year_ends = 366

prev_week = 0
print("{0:04d}-{1:02d}:".format(this_year, this_month))
#print("\tM%02d:" % this_month)
for x in range(month_ends[this_month - 1], 0,  -1):
    dt = date(this_year, this_month, x) 
    iso_year, iso_week, iso_wday = dt.isocalendar()
    if iso_week != prev_week:
        #print("\t\tW%02d:" % iso_week)
        prev_week = iso_week
    hol = ''
    hol_name = '' 
    if iso_wday > 5:
        hol = ' ⚪'
    if dt.isoformat() in data_json:
        hol = ' 🔴'
        hol_name = data_json[dt.isoformat()]
    print("\t%s W%02d.%s D%03d:%s" \
     % (dt.strftime('%m%d'), iso_week, iso_wday, dt.timetuple().tm_yday, hol))
    if hol_name:
        print("\t\t{}".format(hol_name))
