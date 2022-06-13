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
SERVICE_TIME = 0 # SET THESE NUMBERS CORRECTLY, SERVICE_TIME- PER CUSTOMER
LOADING_TIME = 0
CHRG_TIME =0 # time it takes for a full charge
KWH_CAPACITY = 100
MX_CUS = 200 # maximum customers per visit
RANGE =88000
KG_CAPACITY = 554
WORK_SECS = 12*3600
W=[] # weights of goods
min_f = pow(10,10)

disMat = [] 
timeMat = [] 


def addZeros(seq):
    zeros =0
    dis_from_last_zero=0
    curr_weight=0
    cus_count=0
    global MX_RANGE,MX_CUS,KG_CAPACITY,W

    new_seq = [0] # starting and ending at keels

    for i,v in enumerate(seq):
        if(i ==0 or (dis_from_last_zero+disMat[seq[i-1]][v] + disMat[v][0] <= RANGE) and curr_weight+W[v]<KG_CAPACITY and cus_count<MX_CUS ): # Can visit v
            new_seq.append(v)
            dis_from_last_zero+=disMat[seq[i-1]][v]

            curr_weight+= W[v]
            cus_count+=1
        else: 
            new_seq.append(0)
            new_seq.append(v)
            dis_from_last_zero=disMat[0][v]

            cus_count =1
            curr_weight=W[v]

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

def getTotalDis(sq):
    global disMat
    td=0
    seq =addZeros(sq)
    for i in range(1,len(seq)):
        td+= disMat[seq[i-1]][seq[i]]
        print(td)

def getTotalDisTime(sq):
    global timeMat,disMat,LOADING_TIME,SERVICE_TIME,CHRG_TIME,N

    td=0 # total distance
    #print("GetTotalDisTime")
    seq =addZeros(sq)
    #print(sq,seq)
    for i in range(1,len(seq)):
        td+= disMat[seq[i-1]][seq[i]]
        
    tt=0
    tt_c=LOADING_TIME*(len(sq)-N) + SERVICE_TIME*(N-1) + int((max(td-RANGE,0)/RANGE)*CHRG_TIME) # constant time
    
    for i in range(1,len(seq)):
        tt+= timeMat[seq[i-1]][seq[i]] # service time and laoding time not included- no point of adding service time.constant for all cases

    return [td,tt,tt+tt_c]


class Population:
    @staticmethod
    def mutate(offspring,n):
       # cnt = random.randint(0,5)
        if random.random() < 0.7: 
        #  for i in range(cnt):
            i1 = random.randint(0,n-1)
            i2 = random.randint(0,n-1)
            tmp = offspring[i1]
            offspring[i1] = offspring[i2]
            offspring[i2] = tmp
        return offspring

    @staticmethod
    def get_fitness(creature,n):
        return getTotalDisTime(creature)[0]

    @staticmethod
    def crossover_1(c1,c2,n):
        ll = random.randint(1,n)
        offspring = [0]*(n)
        for i in range(ll):
            offspring[i]= c1[i]
        for i in range(ll,n):
            offspring[i]= c2[i]
        return Population.mutate(cleanSequence(offspring),n)
    
    @staticmethod
    def crossover_2(c1,c2,n):
        a = random.randint(0,n-2)
        b = min(a + random.randint(int(n/6),int(2*n/3)),n-1)

        offspring = []

        mid_set = c2[a:b+1]
        free_des = [1]*(n+1)

        for x in mid_set:
            free_des[x]=0

        for i in range(0,n):
            if(free_des[c1[i]]):
                offspring.append(c1[i])
                free_des[c1[i]]=0
        offspring = offspring[:a]+mid_set+ offspring[a:]

        return Population.mutate(offspring,n)

    def build_probability(self):
        global min_f
        assert len(self.creatures) > 0
        probs = []
        self.fitness = []
        prob_den =0
        for c in self.creatures:
            f = Population.get_fitness(c,self.n) # total journey distance
            min_f = min(f,min_f)
            self.fitness.append(f)
            prob = 1/max(10,f+EPS-min_f+200) #pow(1.5,-f) # more conflicts-> less probability
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
            offs = Population.crossover_2(c1,c2,self.n)
            n_crs.append(offs)
        return Population(n_crs)

    def get_best(self):
        best_val = self.fitness[0]
        best_idx=0
        for i in range(1,len(self.fitness)):
            if self.fitness[i] < best_val:
                best_val = self.fitness[i]
                best_idx = i
        return (self.creatures[best_idx],best_val)
        #return ([],best_val)

    def print_stats(self):
        avg_fitness = (sum(self.fitness) + 1.0)/len(self.fitness)
        #print('ABG Weakness: ' + str(avg_fitness)) 
        #print(self.get_best()[1])
        #print(self.get_best()[0])
        print("Dis Travel_Time TotTime :",getTotalDisTime(self.get_best()[0])) 
        print("Number of Vehicles : ",int(getTotalDisTime(self.get_best()[0])[-1]/WORK_SECS) +1 )
  
    def get_avg(self):
        return (sum(self.fitness) + 1.0)/len(self.fitness)


def getInput():

    global N,SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,W,RANGE
    global disMat,timeMat


    with open('input_full.txt','r') as file:
        N = int(file.readline().strip())
        #SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,RANGE = map(int,file.readline().strip().split())

        W = list(map(float,file.readline().strip().split()))
        W=[0]+W # add zero at the beginning

        for row in range(N):
            disMat.append(list(map(int,file.readline().strip().split())))

        for col in range(N):
            timeMat.append(list(map(int,file.readline().strip().split())))
        

    #print(N,SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,W)
    #print(disMat)
    #print(timeMat)

def plot(xx,yy,fname):
    plt.plot(xx,yy)
    plt.savefig(fname)


if __name__ == '__main__':
    random.seed(666)
    p_size = 1000 #f  larger the population higher chance of finding local min/max, but program becomes slow

    getInput()

    xx = []
    yy = []
    fname = 'graph.png'

    if len(sys.argv) > 1:
        plot(xx,yy,fname)

    population = Population()
    population.init_population(N,p_size)


    for iteration in range(1000): # iteration = echo
        xx.append(iteration)
        yy.append(population.get_avg())
        plot(xx,yy,fname)

        population = population.next_generation(p_size)
        if(iteration %20==0):  
            population.print_stats()

        if population.get_best()[1] == 0:
            break

