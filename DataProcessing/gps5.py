import fileinput
from pickletools import long1
from tokenize import Double
import requests
import googlemaps

N=334
lon =[]
lat =[]
coords = []
timeMat = [[0]*N for i in range(N)]
disMat = [[0]*N for i in range(N)]

def constructAdjMatrix():

    global timeMat,disMat,N,coords

    API_key = 'AIzaSyAAXJkHB3jPwfCZYHDDxAK7XEVHL_jpIsI'#enter Google Maps API key
    gmaps = googlemaps.Client(key=API_key)

    for i in range(N):
        print(i)
        for j in range(N):
            origin = [coords[i],coords[j]]
            destination = origin
            result = gmaps.distance_matrix(origin, destination, mode = 'driving')
            disMat[i][j] = result["rows"][0]["elements"][1]["distance"]["value"]
            timeMat[i][j] = result["rows"][0]["elements"][1]["distance"]["value"]

def getInput():

    global N,coords,timeMat,disMat
    with open('coord.txt','r') as file:
        N = int(file.readline().strip())

        for i in range(N):
            x,y = file.readline().strip().split()

            coords.append(y+','+x)
            
    N=5
    coords = coords[:5]

def writeToFile(N,mat):

    lines = []
    with open('coord.txt','a') as file:
        lines.append(str(N)+'\n')
        file.writelines(str(N))

        for i in range(N):
            lines.append(' '.join(map(str,mat[i]))+'\n')
            
        file.writelines(lines)     

getInput()

constructAdjMatrix()

writeToFile(disMat)
writeToFile(timeMat)