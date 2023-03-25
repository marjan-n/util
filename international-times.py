
### Use Case
## Inputs
# 1. enter a bunch of cities and countries
## Outputs
# 1. suggested blocks of time that work well across all cities

### Potential Extensions
# 1. adding scores for times of the day
# 2. exclusion of certain times where there are conflicts
# 3. additional error and exit handling
# 4. defining reference city
# 5. defining working hours instead of default 9 a.m. to 5 p.m.
# 6. removing spaces from city names. 
# 7. giving options for countries to standardize naming process. integer menu.

### Packages
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def fixTime(time):
    """
    Purpose: In case time exceeds 24 hr clock, this function returns time in range (0, 24)
    Inputs: Time
    Outputs: Time in range [0, 24]
    """
    if time > 24:
        time -= 24
        return time
    return time

def printTimeIn12Given24(time):
    """
    Purpose: Want numerical time translated to 12-hour clock and a.m. or p.m.
    Inputs: Time in range [0, 24]
    Outputs: Time in range [0, 12] and with a.m. or p.m.
    """
    if time == 12:
        print(f'12 p.m.')
    elif time > 12:
        print(f'{time-12} p.m.')
    else:
        print(f'{time} a.m.')

def translateCommonWorkingHours(referenceTimezoneOffset, commonWorkingHoursBinaries):
    """
    Purpose: printing out the common working hours
    Inputs: 
    1. the offset of the reference timezone (e.g. 9, which would be +9 UTC/GMT)
    2. list of 24 values where 1 if it's a common working hour to all cities, 0 otherwise
    Outputs: print statement of common working hours in the timezone of the reference city
    """
    for i in range(24):
       # requires translation
       afterNoon = False
       if commonWorkingHoursBinaries[i] == 1:
           time = referenceTimezoneOffset + i
           time = fixTime(time)
           printTimeIn12Given24(time)

def getWorkingHours(offset, startTime=9, endTime=17):
    """
    Purpose: determines working hours of a city in the format of 24 element list
    Inputs: 
    1. timezone offset (e.g. 9, which would be +9 UTC/GMT)
    2. start time of working hours in 24-hour clock
    3. end time of working hours in 24-hour clock (e.g. 17 for 5 p.m.)
    Outputs: working hours in 24 element list where 0s and 1s rep non-working and working hrs, respectively
    """
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
    """
    Purpose: return common working hours across multiple cities
    Inputs:
    1. binary array of 24 elements that reps working hours of some reference city
    2. list of offsets of all cities to be compared (e.g. [9, -4] if 2 cities w/ timezones +9 UTC and -4 UTC)
    3. start time of working hours in 24-hour clock
    4. end time of working hours in 24-hour clock (e.g 17 for 5 p.m.)
    Outputs: common working hours in 24 element list where 0s and 1s rep non-working and working hrs, respectively
    Logic: 
    choose a ref city. go through its hours and remove hours that aren't working hours for the other cities.
    continue until you've gone through all cities or until you've determined that there are 0 common working hours
    """
    # there was only ever 1 city inputted. we have common working hours already
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
    """
    Function that returns 1 if input is '+' and -1 otherwise
    """
    if sign == '+':
        return 1
    return -1

def getTimezone(city, country):
    """
    Purpose: get the UTC/GMT offset given a city and country
    Inputs: city and country name
    Outputs: offset in the form of an integer (e.g. -4 returned means UTC/GMT -4 is the offset)
    """
    url = 'https://www.timeanddate.com/time/zone/' + str(country) + "/" + str(city)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tableContents = soup.find("table", attrs={"class":"table table--left table--inner-borders-rows"})
    text = tableContents.text
    x = re.search(r"\+{0,1}\-{0,1}\d", text).group(0)
    sign = checkPos(x[0])
    return sign*int(x[1])


### Running code
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
print()
print(listCities)
print(listTimezones)
timezoneBinaries0 = getWorkingHours(listTimezones[0], startTime=9, endTime=17)
commonWorkingHoursBinaries = getCommonWorkingHours(timezoneBinaries0, listTimezones)
translateCommonWorkingHours(listTimezones[0], commonWorkingHoursBinaries)

### Other ideas
# Taking a look at the mathematical intersection of working hours across all cities to determine common working hrs