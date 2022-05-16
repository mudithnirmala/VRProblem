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
RANGE = 100
KG_CAPACITY = 600
W=[] # weights of goods

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

    return new_seq

def cleanSequence(seq):
    # length of seq is N-1
    n=len(seq)

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

def getTotalTime(seq):
    td=0 # total distance
    for i in range(1,len(seq)):
        td+= disMat[seq[i-1]][seq[i]]
    
    tt=LOADING_TIME # + (td/90)*charging_time

    for i in range(1,len(seq)):
        tt+= timeMat[seq[i-1]][seq[i]] # service time and laoding time not included- no point of adding service time.constant for all cases

    return tt



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

if __name__ == '__main__':
    random.seed(666)
    n= 35#100
    p_size = 10000 #f  larger the population higher chance of finding local min/max, but program becomes slow


    getInput()
    print(addZeros([1,4,2,3]))
