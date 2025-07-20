
from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/incidents")
def get_incidents():
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, '..', 'backend', 'database.db')
    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()
    cur.execute("SELECT type, description, timestamp FROM incidents ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
