from typing import Any, Dict, Optional
import logging
from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error
from contextlib import asynccontextmanager

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

DATABASE = "genkit_debugger.db"

def init_db():
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debug_sessions (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            session_key TEXT,
            platform TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@asynccontextmanager
async def get_db_connection():
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

@app.route('/start_session', methods=['POST'])
async def start_session() -> Dict[str, Any]:
    data = request.json
    user_id = data.get('user_id')
    platform = data.get('platform')
    if not user_id or not platform:
        return jsonify({"error": "Missing user_id or platform"}), 400

    try:
        async with get_db_connection() as conn:
            cursor = await conn.execute("INSERT INTO debug_sessions (user_id, platform) VALUES (?, ?)", (user_id, platform))
            session_id = cursor.lastrowid
            conn.commit()
            return jsonify({"session_id": session_id})
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/stop_session', methods=['POST'])
async def stop_session() -> Dict[str, Any]:
    data = request.json
    session_id = data.get('session_id')
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    try:
        async with get_db_connection() as conn:
            cursor = await conn.execute("UPDATE debug_sessions SET end_time = CURRENT_TIMESTAMP WHERE id = ?", (session_id,))
            conn.commit()
            return jsonify({"message": "Session stopped"})
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route('/get_sessions', methods=['GET'])
async def get_sessions() -> Dict[str, Any]:
    try:
        async with get_db_connection() as conn:
            cursor = await conn.execute("SELECT * FROM debug_sessions")
            sessions = [dict(row) for row in cursor.fetchall()]
            return jsonify(sessions)
    except Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)