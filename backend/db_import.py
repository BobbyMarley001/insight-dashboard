import json
import certifi
from pymongo import MongoClient

# ✅ Corrected MongoDB Atlas connection string
client = MongoClient(
    "mongodb+srv://psychology001:P%24ych0l0gy%23001@cluster1.igw00bm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1",
    tlsCAFile=certifi.where()
)

# Use your database and collection
db = client["dashboard"]
collection = db["insights"]

# Load data from JSON file
with open("jsondata.json", "r") as f:
    data = json.load(f)

# Insert the data
collection.insert_many(data)

print("🎉 Data has been loaded into MongoDB Atlas!")
