import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class bestRoute():
    'This method reads file, initializes city names and their corresponded latitudes and longitudes, the distance array, and the tour array'
    def __init__(self, fileName):
        self.fileName = open(fileName)
            
        self.numCities = int(self.fileName.readline()) #number of cities
        self.cityNames = [] #initalizing city names
        self.latitudes = [] #initalzing latitudes
        self.longitudes = []
        
        self.distances = np.zeros((self.numCities, self.numCities))
        self.tour = np.zeros(self.numCities + 1, dtype='int')
        
        for row in self.fileName:
            column = row.strip().split(',')
            
            self.cityNames.append(column[0])
            self.latitudes.append(float(column[1]))
            self.longitudes.append(float(column[2]))
            
        self.cityNames = np.array(self.cityNames)
        self.latitudes = np.array(self.latitudes)
        self.longitudes = np.array(self.longitudes)
        
       # print(self.cityNames)
        
    'this method computes the distances between any cities and put them in a 2D numpy array'
    def computeDistances(self):
        self.radius = 6356.752
        self.convertedLat = np.radians(self.latitudes)
        self.convertedLon = np.radians(self.longitudes)
        
        for i in range(self.numCities):
            for j in range(self.numCities):                  
                self.distances[i,j] += 2 * self.radius * np.arcsin( np.sqrt( np.abs( (np.sin((self.convertedLat[i] - self.convertedLat[j])/2))**2  + ( np.cos(self.convertedLat[i]) * np.cos(self.convertedLat[j]) * (np.sin((self.convertedLon[i] - self.convertedLon[j])/2) )**2    ))))
       
    '''This method takes the number of a city that user wants to start in 
    then from there compute the shortest distance that go through every other city and marks off a city off the list once it's visited
    finally the method will add the total distance of the tour and return it'''
    def computeGreedyTour(self, startCityNumber):
        self.startCityNumber = startCityNumber
        self.tour[0] = startCityNumber #set a starting city
        self.tour[self.numCities] = startCityNumber  #coming back to the starting city
          
        self.unvisitedCity = [cityNumber for cityNumber in range(self.numCities)] #list of unvisited cities
        
        self.tourDist = self.distances[self.tour[self.numCities -1], self.tour[self.numCities]] #initalizing the total distance to late add on to itself
        
        for i in range(self.numCities-1):
            shortestDist = max(self.distances[self.numCities-1]) #set something to compare the distance to
            self.unvisitedCity.remove(self.tour[i]) #remove the visited city
            
            for city in self.unvisitedCity:
                if self.distances[self.tour[i], city] < shortestDist:
                    shortestDist = self.distances[self.tour[i], city]
                    goToCity = city     
                
            self.tourDist += shortestDist
            self.tour[i+1] = goToCity        
        return self.tourDist
    
    'This method print out the 2D distance array'
    def printDistances(self):
        print('Distance array: ')
        for row in self.distances: 
            for i in range(len(row)):          
                print('{:7.2f}'.format(row[i]), end = ' ')
            print('')            
        print('')
                       
        #print(self.distances)
    "this method print out the city's number, name, latitude, and longitude"  
    def printCityInformation(self):
        print('{} {:15} {:11} {}'.format('City', '# City', 'Latitude', 'Longitude'))            
        for i in range(self.numCities):
            print('{:6} {:14}{:8.4f}{:12.4f}'.format(i, self.cityNames[i], self.latitudes[i], self.longitudes[i]))
         
        print('')    
        
    'this method generates the numbers of the cities in the tour and returns a list of numbers'   
    def getTour(self):     
        getCityTour = []
        for cityNum in self.tour:
            getCityTour.append(self.cityNames[cityNum])           
        return getCityTour
            
    'this method prints the tour with the city names and its corresponding number'
    def printTour(self):
        getCityTour = self.getTour()
        print('Tour constructed: ')        
        i = 0
        while i < len(getCityTour) - 1:
            print('{}({})'.format(getCityTour[i], self.tour[i]), end = '-->')
            i +=1
        print('{}({})'.format(getCityTour[0], self.tour[0]))
        print('')
        tourLength = self.getTourDistance()
        print('Length of tour constructed = {} km.'.format(tourLength))
        
        
    'this method gets the total distance of the tour in kilometers'   
    def getTourDistance(self):
        tourLen = '{:.2f}'.format(self.computeGreedyTour(self.startCityNumber))
        return tourLen
              
    'this method plots the tour'
    def plot(self):
        figure(num=None, figsize=(9,6), dpi=80, facecolor='w', edgecolor='k')
       # plt.plot(self.longitudes, self.latitudes,'bo-') #blue lines joining points
        tourLon = []
        tourLat = []
        
        for city in self.tour:
            tourLon.append(self.longitudes[city])
            tourLat.append(self.latitudes[city])
            
        plt.plot(tourLon, tourLat,'bo-') #blue lines joining points
             
        points = zip(self.longitudes,self.latitudes)
    
        i = 0     
        for a,b in points:
            plt.annotate((self.cityNames[i] + '({})'.format(i)),     #label
            (a,b),                      #point
            textcoords="offset points", # how to position the text
            xytext=(0,10), # distance from text to points (x,y)
            ha='center') # horizontal alignment can be left, right or center                  
            i += 1
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()
        
        
#t = bestRoute('us-big-10.txt')
#t.computeDistances()
#t.computeGreedyTour(0)
#t.printCityInformation()
#t.printDistances()
#t.printTour()
#t.plot()