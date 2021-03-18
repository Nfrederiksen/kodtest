import requests

# Given that the Server is running.
# === POST position in seconds on an asset for a user
r = requests.post('http://localhost:3000/position/user4/asset123/175')
print(r.content)

r = requests.post('http://localhost:3000/position/user4/asset234/180')
print(r.content)

r = requests.post('http://localhost:3000/position/user4/asset345/185')
print(r.content)

# === GET position for a given asset
r = requests.get('http://localhost:3000/position/user4/asset123')
print(r.content)

r = requests.get('http://localhost:3000/position/user4/asset345')
print(r.content)

# === GET all positions (ordered by last modified)
r = requests.get('http://localhost:3000/position/user4')
print(r.content)
