# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 22:06:47 2019

@author: Nastya
"""
import random
import matplotlib.pyplot as plt

class ACO:
    def __init__(self, ant_count, cities_amount, generations, alpha, beta, rho, distance_matrix, eta_matrix):
        self.ant_count = ant_count  # amount of ant
        self.cities_amount = cities_amount #amount of cities
        self.generations = generations   # amount of generations
        self.alpha = alpha   # alpha, beta and rho are parameters of alg.
        self.beta = beta     
        self.rho = rho
        
        self.distance_matrix = distance_matrix  # distances btw cities
        self.eta_matrix = eta_matrix   # matrix with 1/distance for cities
        
        
        self.L = [] # route for each ant
        self.allowed = [[0 for i in range(cities_amount)] for j in range(ant_count)] # cities that haven't visited by each ant
        self.totalCost = []  # cost of each route
        self.pheromone_delta = {}  #pheromones
        
        self.pheromone = [[1 / (cities_amount * cities_amount) for j in range(cities_amount)] for i in range(cities_amount)]
        
        self.best_cost = 1000000  # cost of the best solution
        self.best_sol = []  # best route
        
    def initAnts(self):
        self.L = []
        self.totalCost = []
        self.pheromone_delta = {}
        for k in range(self.ant_count):
            for i in range(self.cities_amount):
                self.allowed[k][i] = 0
            self.L.append([0]) # start from 0 city    
            self.allowed[k][0] = 1  #first city (0) have been already visited
            self.totalCost.append(0)
    
    def nextCity(self, k, prev):
        selected = 0
        probability = {}
        denominator = 0
        
        # choose city according the rule
        for c in range(self.cities_amount):
            if (self.allowed[k][c] == 0):
                denominator += self.pheromone[prev][c] ** self.alpha * self.eta_matrix[prev][c] ** self.beta 
        
        for c in range(self.cities_amount):
            if (self.allowed[k][c] == 0):
                probability[c] = (self.pheromone[prev][c] ** self.alpha * self.eta_matrix[prev][c] ** self.beta)/denominator
        
        #print("Prob ", sum(probability.values()))
        
       # while (selected == 0):
        r = random.random()
        sumProb = 0
        
        for key, value in probability.items():
           sumProb+=value
           if (r < sumProb):
                selected = key
                break
        
        return selected
        
    
    def buildSolution(self, k):
        for сity in range(1,self.cities_amount):
            prev = self.L[k][len(self.L[k]) - 1]
            selected  = self.nextCity(k, prev)
            self.L[k].append(selected)
            self.allowed[k][selected] = 1
            self.totalCost[k] += self.distance_matrix[prev][selected] 
            
        self.totalCost[k]+= self.distance_matrix[selected][0]
            
        
    def update_pheromone_delta(self, k):
        self.pheromone_delta[k] = [[0 for i in range(self.cities_amount)] for j in range(self.cities_amount)]
        
        for c in range(len(self.L[k]) - 1):
            i = self.L[k][c]
            j = self.L[k][c+1]
            self.pheromone_delta[k][i][j] = 1/self.totalCost[k]
        

    def update_pheromone(self):
        for i in range(self.cities_amount):
            for j in range(self.cities_amount):
                self.pheromone[i][j]*= self.rho
                for k in range(self.ant_count):
                    self.pheromone[i][j] += self.pheromone_delta[k][i][j]

    
    def solve(self):
        progress = []
        for iteration in range(self.generations):
            self.initAnts()
            
            #build solution
            for k in range(self.ant_count):
                self.buildSolution(k)
                self.update_pheromone_delta(k)
                if (self.totalCost[k] < self.best_cost):
                    self.best_cost = self.totalCost[k]
                    self.best_sol = self.L[k]
           
                
            self.update_pheromone()
            
            progress.append(self.best_cost)
            
        
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()
        
        return self.best_cost, self.best_sol   
            
        
       
        
        
        