
# defining the use case

# Inputs
# 1. enter a bunch of cities
# 2. enter the city whose timezone you want the times to be

# Outputs
# 1. suggested blocks of time that work well

# Extensions
# 1. adding scores for times of the day
# 2. exclusion of certain times

numCities = int(input('How many cities would you like to consider? '))
listCities = []
for i in range(numCities):
    line = 'Enter city # ' + str(i) + ": "
    listCities.append(input(line))