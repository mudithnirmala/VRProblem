from asyncio import subprocess
import random
from bisect import bisect_right
from tkinter import W # right most number we can insert the number
import matplotlib.pyplot as plt
import subprocess
import sys
import os
import fileinput

EPS = pow(10,-30)

N=500
SERVICE_TIME = 100 # SET THESE NUMBERS CORRECTLY, SERVICE_TIME- PER CUSTOMER
LOADING_TIME = 100
CHRG_SPEED = 100
KWH_CAPACITY = 100
RANGE =90
KG_CAPACITY = 600
W=[] # weights of goods
min_f = pow(10,10)

disMat = [] 
timeMat = [] 


def addZeros(seq):
    zeros =0
    dis_from_last_zero=0
    global MX_RANGE

    new_seq = [0] # starting and ending at keels

    for i,v in enumerate(seq):
        if(i ==0 or dis_from_last_zero+disMat[seq[i-1]][v] + disMat[v][0] <= RANGE): # Can visit v
            new_seq.append(v)
            dis_from_last_zero+=disMat[seq[i-1]][v]
        else: 
            new_seq.append(0)
            new_seq.append(v)
            dis_from_last_zero=disMat[0][v]

    return new_seq+[0]

def cleanSequence(seq):
    # length of seq is N-1
    n=len(seq)
    global N

    isAdded = [False]*N
    isAdded[0] = True # anyway we will add zero later

    new_seq=[]

    for i,v in enumerate(seq):
        if(not(isAdded[v])):
            new_seq.append(v)
            isAdded[v]=True

    missing =[]
    for v,ia in enumerate(isAdded):
        if(not(ia)):
            missing.append(v)        

    random.shuffle(missing)
    new_seq+=missing

    return new_seq

def getTotalTime(sq):
    global timeMat,disMat

    td=0 # total distance
    seq =addZeros(sq)
    for i in range(1,len(seq)):
        td+= disMat[seq[i-1]][seq[i]]
        
    tt=LOADING_TIME # + (td/90)*charging_time

    for i in range(1,len(seq)):
        tt+= timeMat[seq[i-1]][seq[i]] # service time and laoding time not included- no point of adding service time.constant for all cases

    return tt


class Population:
    @staticmethod
    def mutate(offspring,n):
       # cnt = random.randint(0,5)
        if random.random() < 0.5:
        #  for i in range(cnt):
            i1 = random.randint(0,n-1)
            i2 = random.randint(0,n-1)
            tmp = offspring[i1]
            offspring[i1] = offspring[i2]
            offspring[i2] = tmp
        return offspring

    @staticmethod
    def get_fitness(creature,n):
        return getTotalTime(creature)

    @staticmethod
    def crossover(c1,c2,n):
        ll = random.randint(1,n)
        offspring = [0]*(n)
        for i in range(ll):
            offspring[i]= c1[i]
        for i in range(ll,n):
            offspring[i]= c2[i]
        return Population.mutate(cleanSequence(offspring),n)

    def build_probability(self):
        global min_f
        assert len(self.creatures) > 0
        probs = []
        self.fitness = []
        prob_den =0
        for c in self.creatures:
            f = Population.get_fitness(c,self.n) # total journey time
            min_f = min(f,min_f)
            self.fitness.append(f)
            prob = 1/(f+EPS-min_f+500) #pow(1.5,-f) # more conflicts-> less probability
            probs.append(prob)
            prob_den += prob
        self.probs = list(map(lambda x:x/prob_den,probs))

        for i in range(1,len(self.probs)-1):
            self.probs[i] += self.probs[i-1]
            self.probs[-1] = 1+ EPS

    def get_stochastic(self):
        val = random.random() # random number between 0-1
        idx = bisect_right(self.probs,val) #python built in binary search
        return self.creatures[idx]

    def __init__(self,creatures=None):
        self.creatures = creatures
        if creatures is not None:
            self.n = len(creatures[0])
            self.build_probability()

    def init_population(self,N,size):
        self.n = N-1
        self.creatures = []
        base = list(range(1,N)) 

        for _ in range(size):
            perm = base.copy()
            random.shuffle(perm)
            c_perm = cleanSequence(perm)
            self.creatures.append(c_perm)
        self.build_probability()


    def next_generation(self,size):
        n_crs = []
        for _ in range(size):
            c1 = self.get_stochastic()
            c2 = self.get_stochastic()
            offs = Population.crossover(c1,c2,self.n)
            n_crs.append(offs)
        return Population(n_crs)

    def get_best(self):
        best_val = self.fitness[0]
        best_idx=0
        for i in range(1,len(self.fitness)):
            if self.fitness[i] < best_val:
                best_val = self.fitness[i]
                best_idx = i
        return ( addZeros(self.creatures[best_idx]),best_val)

    def print_stats(self):
        avg_fitness = (sum(self.fitness) + 1.0)/len(self.fitness)
        print('ABG Weakness: ' + str(avg_fitness)) 
        print(self.get_best()) 
  
    def get_avg(self):
        return (sum(self.fitness) + 1.0)/len(self.fitness)


def getInput():

    global N,SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,W,RANGE
    global disMat,timeMat


    with open('input.txt','r') as file:
        N = int(file.readline().strip())
        SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,RANGE = map(int,file.readline().strip().split())

        W = list(map(int,file.readline().strip().split()))

        for row in range(N):
            disMat.append(list(map(int,file.readline().strip().split())))

        for col in range(N):
            timeMat.append(list(map(int,file.readline().strip().split())))
        

    #print(N,SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,W)
    #print(disMat)
    #print(timeMat)

if __name__ == '__main__':
    random.seed(666)
    p_size = 50000 #f  larger the population higher chance of finding local min/max, but program becomes slow

    getInput()

    population = Population()
    population.init_population(N,p_size)

    for iteration in range(1000): # iteration = echo
        population = population.next_generation(p_size)
        if(iteration %20==0):  
            population.print_stats()

        if population.get_best()[1] == 0:
            break

