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

def getTotalDis(sq):
    global disMat
    td=0
    seq =addZeros(sq)
    for i in range(1,len(seq)):
        td+= disMat[seq[i-1]][seq[i]]
        print(td)

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




def getInput():

    global N,SERVICE_TIME,LOADING_TIME, KG_CAPACITY,CHRG_SPEED,W,RANGE
    global disMat,timeMat


    with open('input2.txt','r') as file:#8277
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

bestTime =pow(10,10)
bestConfig = []
isTaken = [0]*300

def completeSearch(N,config):

    global bestTime,bestConfig
    if(len(config)==N):
        tm = getTotalTime(config)
        if(tm<bestTime):
            bestTime=tm
            bestConfig=config
            print(tm,config)
        return
    for i in range(1,N+1):
        if(not(isTaken[i])):
            isTaken[i]= True
            completeSearch(N,config+[i])
            isTaken[i] = False

if __name__ == '__main__':
    random.seed(666)
    
    getInput()

    completeSearch(N-1,[])

    print(bestTime,bestConfig)



