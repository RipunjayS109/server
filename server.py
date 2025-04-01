from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize the database
def init_db():
    conn = sqlite3.connect("game.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id TEXT PRIMARY KEY,
            score INTEGER,
            play_time INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route('/update_stats', methods=['POST'])
def update_stats():
    data = request.json
    user_id = data["user_id"]
    score = data["score"]
    play_time = data["play_time"]

    conn = sqlite3.connect("game.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO players (user_id, score, play_time)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
        score=excluded.score, play_time=excluded.play_time
    """, (user_id, score, play_time))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    conn = sqlite3.connect("game.db")
    c = conn.cursor()
    c.execute("SELECT * FROM players ORDER BY score DESC LIMIT 10")
    results = c.fetchall()
    conn.close()
    return jsonify({"leaderboard": results})

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
