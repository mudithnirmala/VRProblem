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
        
        origin = [coords[i]]+ coords[:N//2]
        destination = origin
        result = gmaps.distance_matrix(origin, destination, mode = 'driving')

        for j in range(N//2):
            disMat[i][j] = result["rows"][0]["elements"][j]["distance"]["value"]
            timeMat[i][j] = result["rows"][0]["elements"][j]["distance"]["value"]

        origin = [coords[i]]+ coords[N//2:]
        destination = origin
        result = gmaps.distance_matrix(origin, destination, mode = 'driving')
        
        for j in range(N//2,N):
            disMat[i][j] = result["rows"][0]["elements"][j]["distance"]["value"]
            timeMat[i][j] = result["rows"][0]["elements"][j]["distance"]["value"]

def getInput():

    global N,coord,timeMat,disMat
    with open('coord.txt','r') as file:
        N = int(file.readline().strip())

        for i in range(N):
            x,y = file.readline().strip().split()

            coords.append(y+','+x)
            
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

"""
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=40.6655101%2C-73.89188969999998&destinations=40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=YOUR_API_KEY"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
"""

"""
#print(coords)

#Perform request to use the Google Maps API web service

origin = coords[:3] #["6.8748928,79.9342983","6.8441964,79.9458155"]


result_distance = result["rows"][0]["elements"][1]["distance"]["value"]
result_time = result["rows"][0]["elements"][1]["duration"]["value"]

print(result_distance)
print(result_time)

print(result)
"""