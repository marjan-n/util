
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
for i in range(numCities):
    line = 'Enter city # ' + str(i+1) + ": "
    listCities.append(input(line))
    line = 'Enter country # ' + str(i+1) + ": "
    listCountries.append(input(line))
    print(getTimezone(listCities[i], listCountries[i]))
print(listCities)



# create a list of ones and zeros; ones if it's 9 am - 5 p.m.. 24 hour in UTC time.
# and then look at intersection point of all the cities.
# at the beginning, define the bounds.
# and then, define the bound for each city.