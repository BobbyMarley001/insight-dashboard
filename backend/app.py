from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection from environment
MONGODB_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["dashboard"]
collection = db["insights"]

@app.route("/")
def home():
    return "✅ Insight Dashboard API is live!"

@app.route("/api/data")
def get_data():
    query = {}
    filters = ["end_year", "start_year", "topic", "sector", "region", "pestle", "source", "country", "city"]
    for field in filters:
        value = request.args.get(field)
        if value:
            query[field] = value
    result = list(collection.find(query, {"_id": 0}))
    return jsonify(result)

@app.route("/api/topics")
def get_topics():
    topics = collection.distinct("topic")
    cleaned = sorted([t for t in topics if t and t.strip()])
    return jsonify(cleaned)

@app.route("/api/countries")
def get_countries():
    topic = request.args.get("topic")
    if topic:
        countries = collection.distinct("country", {"topic": topic})
    else:
        countries = collection.distinct("country")
    cleaned = sorted([c for c in countries if c and c.strip()])
    return jsonify(cleaned)

@app.route("/api/regions")
def get_regions():
    regions = collection.distinct("region")
    cleaned = sorted([r for r in regions if r and r.strip()])
    return jsonify(cleaned)

@app.route("/api/years")
def get_years():
    years = collection.distinct("start_year")
    cleaned = sorted({int(str(y)) for y in years if y is not None and str(y).strip().isdigit()})
    return jsonify(cleaned)

