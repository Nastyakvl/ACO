# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 22:03:10 2019

@author: Nastya
"""
from math import sqrt
from time import time
import numpy as np
from ACO import ACO

#calculate distance btw cities
def distance(city1, city2):
        global time_sqrt
        
        start = time()
        xDis = (city2[0] - city1[0]) ** 2
        yDis = (city2[1] - city1[1]) ** 2
        distance = sqrt((xDis ) + (yDis))
        
        time_sqrt+=time()-start
        return distance    

def readData(fileName):  
    cities={}
    with open(fileName, newline='') as f:
        i=0
        j=0
        for line in f: 
            if (i<6):
                i+=1
            else: 
                x=np.fromstring(line, dtype=float,sep=" ")
                if(len(x)==3):
                    cities[j] = (x[1],x[2])
                    j+=1
                    
    return cities
    
def main():
    cities = readData('Assignment 3 berlin52.tsp')
   
    startTime = time()
    
    d = []
    eta = [] # 1/d(ij)
    rank = len(cities)
    
    for i in range(rank):
        row = []
        eta_row = []
        
        for j in range(rank):
            dist = distance(cities[i], cities[j])
            row.append(dist)  #d(ij)
            if(i != j):
                eta_row.append(1/dist)
            else: 
                eta_row.append(0)
        d.append(row)
        eta.append(eta_row)
    
    # initialize ACO alg.
    aco = ACO( ant_count = 10, cities_amount = rank, generations = 10, alpha = 0.6, beta = 7, rho = 0.8, distance_matrix = d, eta_matrix = eta)
    # run AC) alg.
    dist, sol = aco.solve()
    print("distance: ", dist)
    print("time: ", time()-startTime)
    
    
    
if __name__ == "__main__":
    main()