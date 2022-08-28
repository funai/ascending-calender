#!/usr/bin/env python3
# coding=utf8

import sys
import calendar
from datetime import date
from urllib.request import urlopen
import json

today = date.today()
this_month = today.month
this_year = today.year

api_url = "https://holidays-jp.github.io/api/v1/date.json"
response = urlopen(api_url)
hol_data = json.loads(response.read())

arg = sys.argv
argc = len(arg)
if (argc > 2):
    print('Usage: python %s [1-12]' % arg[0])
    sys.exit()
    
if (argc == 2):
    try:
        x = int(arg[1])
        if x <= 12:
            if x < this_month:
                target_year = this_year + 1
            else:
                target_year = this_year
            target_month = x
        elif x >= 197001:
            target_year = int(arg[1][0:4])
            target_month = int(arg[1][4:])
    except ValueError:
        print('Usage: python %s [1-12]' % arg[0])
        sys.exit()

# first week of the year/month is where the 4th date of the year/month belongs to. 
start_date = date(target_year, target_month, 4)
start_week = start_date.isocalendar()[1]
#print("Start %02d:W%02d" % (target_year, start_week))
end_date = date(target_year, target_month, calendar.monthrange(target_year, target_month)[1])
e_yr, e_wk, e_wd = end_date.isocalendar()
if e_wd > 3:
    # Thu is included:w
    end_week = e_wk
else:
    # end with previous week
    end_week = e_wk - 1
#print("End %02d:W%02d" % (target_year, end_week))

for target_week in range(end_week, start_week -1, -1):
    monday = date.fromisocalendar(target_year, target_week, 1)
    sunday = date.fromisocalendar(target_year, target_week, 7)
    print("W{:02}: {:%m%d}-{:%m%d}".format(target_week, monday, sunday))
    for day in range(7, 0, -1):
        dt = date.fromisocalendar(target_year, target_week, day)
        # dt = date(target_date) 
        iso_year, iso_week, iso_wday = dt.isocalendar()
        hol = ''
        hol_name = '' 
        if iso_wday > 5:
            hol = ' ⚪'
        if dt.isoformat() in hol_data:
            hol = ' 🔴'
            hol_name = hol_data[dt.isoformat()]
        print("\t%s W%02d.%s D%03d:%s" \
           % (dt.strftime('%m%d'), iso_week, iso_wday, dt.timetuple().tm_yday, hol))
        if hol_name:
            print("\t\t{}".format(hol_name))
