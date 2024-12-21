import http.client
import json
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs('../data', exist_ok=True)

# Make API request
conn = http.client.HTTPSConnection("ipl-api1.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "b632789b9dmshba050c77c55790cp1400ebjsnfaf66c81c4a6",
    'x-rapidapi-host': "ipl-api1.p.rapidapi.com"
}
conn.request("GET", "/players", headers=headers)

# Get response
res = conn.getresponse()
data = res.read()

# Convert JSON response to Python dictionary
json_data = json.loads(data.decode("utf-8"))

# Convert to DataFrame
df = pd.DataFrame(json_data)

# Save to CSV
df.to_csv('ipl_players_api.csv', index=False)

# Display first few rows to verify
print(df.head())
