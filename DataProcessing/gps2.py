import pandas as pd
import googlemaps
from itertools import tee


"""**Step 1: Data Input** 
Read in the datafile with the X & Y coordinates. X-coordinate = Latitude, Y-coordinate = Longitude
"""

#Read CSV file into data frame named 'df'
#change seperator (sep e.g. ',') type if necessary

df = pd.read_excel("data.xlsx")

# Visualize the dataframe to get a look at the input. 
# It should look like this with the exact same column names
df = df[:5]

print(df)


"""**Step 2: Set up Google API Account** 
Connect to your local Google account by using your personal API-key.
 Make sure that you have enabled the distance matrix API.
"""

#Perform request to use the Google Maps API web service
API_key = 'AIzaSyAAXJkHB3jPwfCZYHDDxAK7XEVHL_jpIsI'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

"""**Step 3: Initialize lists** 
We are going to write out our API calls results to seperate lists for each variable:
*   Origin ID: This is the ID of the origin location. 
*   Destination ID: This is the ID of the destination location. 
*   Distance: We will store the estimated distance here.
*   Time: We will store the estimated duration here.
"""

#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []

"""**Step 4: Loop over the locations & get the distance** 
This function enables us to take an location and loop over all the possible destination locations,
fetching the estimated duration and distance.
"""

for (i1, row1) in df.iterrows():
  print("origin")
  print(row1['ID'])
  LatOrigin = row1['latitude']
  LongOrigin = row1['longitude']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['ID'] 

  for (i2, row2) in  df.iterrows():

    print("destination id")
    print(row2['ID'])
    LatDestination = row2['latitude']
    LongDestination = row2['longitude']
    destination_id = row2['ID']
    destination = (LatDestination, LongDestination)
    result = gmaps.distance_matrix(origin, destination, mode = 'driving')
    result_distance = result["rows"][0]["elements"][0]["distance"]["value"]
    result_time = result["rows"][0]["elements"][0]["duration"]["value"]



    
    time_list.append(result_time)
    distance_list.append(result_distance)
    origin_id_list.append(origin_id)
    destination_id_list.append(destination_id)


"""**Step 5: Convert the lists to a dataframe** 
We now consolidate our lists in one dataframe.
"""

output = pd.DataFrame(distance_list, columns = ['Distance in meter'])
output['duration in seconds'] = time_list
output['origin_id'] = origin_id_list
output['destination_id'] = destination_id_list

print(output)