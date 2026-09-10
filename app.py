from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO locations (latitude, longitude, time) VALUES (?, ?, ?)",
        (latitude, longitude, time)
    )

    conn.commit()
    conn.close()

    print("📍 Location saved:", latitude, longitude, time)

    return jsonify({"status": "Location saved"})


@app.route("/history")
def history():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, latitude, longitude, time FROM locations ORDER BY id"
    )

    rows = cursor.fetchall()
    conn.close()

    locations = []

    for row in rows:
        locations.append({
            "id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "time": row[3]
        })

    return jsonify(locations)


init_db()

app.run(
    host="0.0.0.0",
    port=5000,
    ssl_context=("cert.pem", "key.pem")
)
