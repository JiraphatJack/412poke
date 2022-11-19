import requests
import json
import pandas as pd
#import psycopg2
 
move = "https://pokeapi.co/api/v2/move?limit=100000&offset=0"
payload = ""
response = requests.request("GET", move, data=payload)
data = response.json()
data_formatted = json.dumps(data, indent=4)

df = pd.DataFrame(data['results']).drop('url', axis=1)
print(df)