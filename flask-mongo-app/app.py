from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json

app = Flask(__name__)

# 🔹 Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://{username}:{passwrd}@cluster-app.p0plxgf.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["flaskdb"]
collection = db["users"]

# -----------------------------
# 1️⃣ API Route
# -----------------------------
@app.route("/api", methods=["GET"])
def get_data():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)

# -----------------------------
# 2️⃣ Form Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")

            if not name or not email:
                return render_template("index.html", error="All fields are required!")

            collection.insert_one({
                "name": name,
                "email": email
            })

            return redirect(url_for("success"))

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
