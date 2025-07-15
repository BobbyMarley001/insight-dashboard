from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# -------------------------------
# Initialize Flask app
# -------------------------------
app = Flask(__name__)
CORS(app)  # Allow frontend (React) to connect

# -------------------------------
# MongoDB connection
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["dashboard"]
collection = db["insights"]

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
# Route: Get countries (optionally filtered by topic)
# Example: /api/countries or /api/countries?topic=oil
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
# Route: Get regions (optional)
# -------------------------------
@app.route("/api/regions")
def get_regions():
    regions = collection.distinct("region")
    cleaned = sorted([r for r in regions if r and r.strip()])
    return jsonify(cleaned)

# -------------------------------
# Route: Get start years (cleaned + sorted numerically)
# -------------------------------
@app.route("/api/years")
def get_years():
    years = collection.distinct("start_year")

    # Convert all years to strings, then check if digits, then back to int for sorting
    cleaned = sorted(
        {int(str(y)) for y in years if y is not None and str(y).strip().isdigit()}
    )

    return jsonify(cleaned)
# -------------------------------
# Run Flask app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

