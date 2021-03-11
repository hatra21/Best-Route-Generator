import findRoute
import time

file = input('Enter filename: ')
startCity = int(input('Enter start city (0 to 9): '))
print('')

myRoute = findRoute.bestRoute(file)
myRoute.computeDistances()
myRoute.computeGreedyTour(startCity)
myRoute.printCityInformation()
myRoute.printDistances()
myRoute.printTour()
myRoute.plot()

print ("\nProgrammed by Hung Anh Tran")
print ("Date: " + time.ctime())
print ("End of processing")