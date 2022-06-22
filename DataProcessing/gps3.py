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

def getInput():

    global N,coord,timeMat,disMat
    with open('coord.txt','r') as file:
        N = int(file.readline().strip())

        for i in range(N):
            x,y = file.readline().strip().split()

            coords.append(y+','+x)

"""
def getInput():

    global N,coord,timeMat,disMat
    with open('coord.txt','r') as file:
        N = int(file.readline().strip())

        x,y = file.readline().strip().split()

        lon.append(x)
        lat.append(y)
        

url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=40.6655101%2C-73.89188969999998&destinations=40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key=YOUR_API_KEY"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
"""

getInput()

#Perform request to use the Google Maps API web service
API_key = 'AIzaSyCS7bJjKSmZUizpm_r3Gmslb_FxifDrYRw'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

"""
from googlemaps import convert

params = {
        "origins": convert.location_list([lat,lon]),
        "destinations": convert.location_list([lat,lon])
    }

gmaps._request("/maps/api/distancematrix/json", params)
"""

origin = coords[:2]
destination = coords[:2]
result = gmaps.distance_matrix(origin, destination, mode = 'driving')

print(result["rows"][0]["elements"][1]["distance"]["value"])
print(result)