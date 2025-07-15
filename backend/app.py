from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

# -------------------------------
# Initialize Flask app
# -------------------------------
app = Flask(__name__)
CORS(app)  # Allow frontend (React) to connect

# -------------------------------
# MongoDB connection (via environment variable)
# -------------------------------
MONGO_URI = os.environ.get("mongodb+srv://psychology001:P$ych0l0gy#001@cluster0.gsvno.mongodb.net/dashboard?retryWrites=true&w=majority")  # Set this in Render environment variables
client = MongoClient(MONGO_URI)
db = client["dashboard"]
collection = db["insights"]

# -------------------------------
# Optional: Home route for sanity check
# -------------------------------
@app.route("/")
def home():
    return "✅ Insight Dashboard API is live!"

# -------------------------------
# Route: Get filtered insights
# Example: /api/data?topic=oil&country=India
# -------------------------------
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

# -------------------------------
# Route: Get all unique topics
# -------------------------------
@app.route("/api/topics")
def get_topics():
    topics = collection.distinct("topic")
    cleaned = sorted([t for t in topics if t and t.strip()])
    return jsonify(cleaned)

# -------------------------------
# Route: Get all unique countries (optionally filter by topic)
# -------------------------------
@app.route("/api/countries")
def get_countries():
    topic = request.args.get("topic")
    if topic:
        countries = collection.distinct("country", {"topic": topic})
    else:
        countries = collection.distinct("country")
    cleaned = sorted([c for c in countries if c and c.strip()])
    return jsonify(cleaned)

# -------------------------------
# Route: Get unique regions
# -------------------------------
@app.route("/api/regions")
def get_regions():
    regions = collection.distinct("region")
    cleaned = sorted([r for r in regions if r and r.strip()])
    return jsonify(cleaned)

# -------------------------------
# Route: Get all cleaned start years (numbers only)
# -------------------------------
@app.route("/api/years")
def get_years():
    years = collection.distinct("start_year")
    cleaned = sorted({int(str(y)) for y in years if y is not None and str(y).strip().isdigit()})
    return jsonify(cleaned)

# -------------------------------
# Start the Flask app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

