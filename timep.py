#!/usr/bin/env python3
# coding=utf8

import sys
import calendar
from datetime import date
from urllib.request import urlopen
import json

def print_cal(target_year, target_month, hol_data):
    print("{}-{}".format(target_year, target_month), file=sys.stderr)
    # print(hol_data, file=sys.stderr)

    # first week of the year/month is where the 4th date of the year/month belongs to. 
    start_date = date(target_year, target_month, 4)
    start_week = start_date.isocalendar()[1]
    #print("Start %02d:W%02d" % (target_year, start_week))
    end_date = date(target_year, target_month, calendar.monthrange(target_year, target_month)[1])
    e_yr, e_wk, e_wd = end_date.isocalendar()
    if e_wd > 3:
        # Thu is included in the month
        end_week = e_wk
    else:
        # Last date of the month belongs to the first week of the next MONTH
        if e_wk > 1:
            end_week = e_wk - 1
        else:
            # Last date of the month belongs to the first week of the next YEAR
            end_week = 52
    #print("End %02d:W%02d" % (target_year, end_week))

    #dow_str = 'MTWRFSU'
    #dow_str = 'MonTueWedThuFriSatSun'

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
                hol = ' ○'
            if dt.isoformat() in hol_data:
                # hol = ' ◉'
                hol = ' ●'
                hol_name = hol_data[dt.isoformat()]
            print("\t%s W%02d.%s D%03d:%s" \
               % (dt.strftime('%m%d'), iso_week, iso_wday, dt.timetuple().tm_yday, hol))
               # % (dt.strftime('%m%d'), iso_week, dow_str[iso_wday - 1], dt.timetuple().tm_yday, hol))
               # % (dt.strftime('%m%d'), iso_week, dow_str[(iso_wday - 1) * 3: (iso_wday - 1) * 3 + 3 ], dt.timetuple().tm_yday, hol))
            if hol_name:
                hol_name = hol_name.replace('休日', '振替休日 <')
                print("\t\t{}".format(hol_name))
    return

def get_holiday():
    csv_url = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
    with urlopen(csv_url) as f:
        lines = f.read().decode('cp932').splitlines()
    # remove header
    lines.pop(0)

    hol_data = {}
    for line in lines:
        date_str, hol_name = line.split(",")
        year, month, day = [int(x) for x in date_str.split("/")]
        iso_date = f"{year}-{month:02}-{day:02}"
        hol_data[iso_date] = hol_name

    # print(hol_data)
    return hol_data # dict

def main():
    today = date.today()
    this_month = today.month
    this_year = today.year

    hol_data = get_holiday()

    arg = sys.argv
    argc = len(arg)
    if (argc > 2):
        print('Usage: python %s [1-12]' % arg[0])
        sys.exit()
        
    if (argc == 2):
        try:
            x = int(arg[1])
            if len(arg[1]) == 4 and int(arg[1]) >= 1970:
                target_year = int(arg[1])
                for x in range(12, 0, -1):
                    print_cal(target_year, x, hol_data)
            elif x <= 12:
                if x < this_month:
                    target_year = this_year + 1
                else:
                    target_year = this_year
                target_month = x
                print_cal(target_year, target_month, hol_data)
            elif x >= 197001:
                target_year = int(arg[1][0:4])
                target_month = int(arg[1][4:])
                print_cal(target_year, target_month, hol_data)
            else:
                print('Usage: python %s [1-12]|YYMM|YYYYMM' % arg[0], file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print('Usage: python %s [1-12]|YYMM|YYYYMM' % arg[0], file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
