
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

def getTimezone(city):
    url = 'https://www.timeanddate.com/time/zone/canada/toronto'
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, "html.parser")
    # test = soup.findAll("table", attrs={"class":"table table--left table--inner-borders-rows"})
    # print(test)
    all_tables = pd.read_html(url,match='Current Offset')
    print(all_tables[0][1][2])

    pass

numCities = int(input('How many cities would you like to consider? '))
listCities = []
for i in range(numCities):
    line = 'Enter city # ' + str(i) + ": "
    listCities.append(input(line))
print(listCities)

getTimezone(listCities[0])


# create a list of ones and zeros; ones if it's 9 am - 5 p.m.. 24 hour in UTC time.
# and then look at intersection point of all the cities.
# at the beginning, define the bounds.
# and then, define the bound for each city.