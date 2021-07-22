#!/usr/bin/env python3
import numpy as np
import s3fs
import datetime
import os


# Find Julian day from given year/month/day
def julian(year_name, month_name, day_name):
    
    calendar = datetime.datetime(year_name, month_name, day_name)
    julian_day = calendar.strftime('%j')
    
    return julian_day


# Create list of ABI data file names for given satellite, product, and datetime period
def aws_list(year_name, month_name, day_name, starthour, startmin, endhour, endmin, satellite_name, view_name, sat_band, product):
    
    # Access AWS using anonymous credentials
    aws = s3fs.S3FileSystem(anon=True)
    
    # Make a list of all data files for given date and start/end hours
    julian_day = julian(year_name, month_name, day_name)
    hour_range = range(int(starthour), int(endhour) + 1)
    all_hours_list = []
    
    for i in hour_range:
        hour_files = aws.ls('noaa-goes' + str(satellite_name) + '/' + product + '/' + str(year_name) + '/' + julian_day + '/' + str(i) + '/', refresh=True)
        all_hours_list.extend(hour_files)
    
    # Extract list of data files for specified period set by start/end times
    data = []
    
    # List file names
    for i in all_hours_list:
        if view_name == 'CONUS': 

            # Select the files that are between the desired start and end time
            if i[-42:-38] >= (starthour + startmin) and i[-26:-22] <= (endhour + endmin):  

                # Account for the change in default scan mode of the ABI
                if i[-60:-57] == 'M3C' or i[-60:-57] == 'M6C':
                    
                    # Get desired band/channel
                    if i[-57:-55]  == sat_band:
                        data.append(i)
        else:
            continue

    return data


def main():

    plugin.init()


if __name__ == "__main__":
    main()
