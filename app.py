from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "logs.db"

# Initialize DB
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Open persistent connection
conn = sqlite3.connect(DB_FILE, check_same_thread=False)

@app.route("/")
def index():
    cur = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 100")
    logs = cur.fetchall()
    return render_template("index.html", logs=logs)

@app.route("/api/log", methods=["POST"])
def receive_log():
    data = request.json
    conn.execute("INSERT INTO logs (source, message, timestamp) VALUES (?, ?, ?)",
                 (data.get("source", "Unknown"), data.get("message", ""), data.get("timestamp", "")))
    conn.commit()
    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
