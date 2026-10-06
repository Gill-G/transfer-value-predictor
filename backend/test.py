import requests
import pandas as pd

url = "https://understat.com/getLeagueData/EPL/2025"
headers = {"X-Requested-With": "XMLHttpRequest"} 

response = requests.get(url, headers=headers)
response.raise_for_status()  # raise an error if the request failed    

print("Status Code:", response.status_code)
print("Content Type:", response.headers.get("Content-Type"), '\n')

data = response.json()  # parse JSON into a python dictionary

print("Number of players:", len(data["players"]), '\n')
print("Player 01:", data["players"][0], '\n')

player_df = pd.DataFrame(data["players"])
print(player_df.head(10))