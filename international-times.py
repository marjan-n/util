
# defining the use case

# Inputs
# 1. enter a bunch of cities
# 2. enter the city whose timezone you want the times to be - no. answer in all timezones.

# Outputs
# 1. suggested blocks of time that work well
# 2. whether no time will work well

# Extensions
# 1. adding scores for times of the day
# 2. exclusion of certain times

# from selenium import webdriver
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def fixTime(time):
    if time > 24:
        time -= 24
        return time
    return time

def getWorkingHours(offset, startTime=9, endTime=17):
    # go through the ideal working hours of one city
    # and then eliminate if not ideal for other cities
    # stop once you've gone through all cities
    # or once you have no more ideal working hours

    idealWorkingHours = []
    for i in range(24):
        sum = i+offset
        sum = fixTime(sum)
        if sum >= startTime and sum < endTime:
            idealWorkingHours.append(1)
        else:
            idealWorkingHours.append(0)
    return idealWorkingHours

def getCommonWorkingHours(startingTimezoneHoursBinaryArray, timezoneOffsets, startTime = 9, endTime = 17):
    
    # there was only ever 1 city inputted. we have ideal working hours
    if len(timezoneOffsets) < 2:
        return startingTimezoneHoursBinaryArray
    
    dummyCopy = startingTimezoneHoursBinaryArray
    for offset in timezoneOffsets[1:]:
        for i in range(24):
            time = i + offset
            time = fixTime(time)
            # if ideal time in starting timezone but not in the 'offset' timezone
            if startingTimezoneHoursBinaryArray[i] == 1 and (time < startTime or  time > endTime):
                dummyCopy[i] = 0
                if np.sum(dummyCopy) == 0:
                    return [0]*24
    return dummyCopy
    
def checkPos(sign):
    if sign == '+':
        return 1
    return -1

def getTimezone(city, country):
    url = 'https://www.timeanddate.com/time/zone/' + str(country) + "/" + str(city)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tableContents = soup.find("table", attrs={"class":"table table--left table--inner-borders-rows"})
    text = tableContents.text
    x = re.search(r"\+{0,1}\-{0,1}\d", text).group(0)
    sign = checkPos(x[0])
    return sign*int(x[1])

numCities = int(input('How many cities would you like to consider? '))
listCities = []
listCountries = []
listTimezones = []
for i in range(numCities):
    line = 'Enter city # ' + str(i+1) + ": "
    listCities.append(input(line))
    line = 'Enter country # ' + str(i+1) + ": "
    listCountries.append(input(line))
    timezone = getTimezone(listCities[i], listCountries[i])
    listTimezones.append(timezone)
    # print(getWorkingHours(timezone))
print()
print(listCities)
print(listTimezones)

def translateCommonWorkingHours(referenceTimezoneOffset, commonWorkingHoursBinaries):
    for i in range(24):
       # requires translation
       afterNoon = False
       if commonWorkingHoursBinaries[i] == 1:
           time = referenceTimezoneOffset + i
           time = fixTime(time)
           if time == 12:
               print(f'12 p.m.')
           elif time > 12:
               print(f'{time-12} p.m.')
           else:
               print(f'{time} a.m.')
               

timezoneBinaries0 = getWorkingHours(listTimezones[0], startTime=9, endTime=17)
commonWorkingHoursBinaries = getCommonWorkingHours(timezoneBinaries0, listTimezones)
translateCommonWorkingHours(listTimezones[0], commonWorkingHoursBinaries)


# create a list of ones and zeros; ones if it's 9 am - 5 p.m.. 24 hour in UTC time.
# and then look at intersection point of all the cities.
# at the beginning, define the bounds.
# and then, define the bound for each city.
# still need to remove spaces from city names e.g. new york