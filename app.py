import os
import sqlite3
from flask import Flask, jsonify, request, render_template, g

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), "todos.db")


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        db.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/todos", methods=["GET"])
def get_todos():
    db = get_db()
    rows = db.execute("SELECT id, task, done FROM todos ORDER BY id DESC").fetchall()
    todos = [{"id": r["id"], "task": r["task"], "done": bool(r["done"])} for r in rows]
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json(force=True) or {}
    task = data.get("task", "").strip()
    if not task:
        return jsonify({"error": "task is required"}), 400

    db = get_db()
    cur = db.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (task,))
    db.commit()
    return jsonify({"id": cur.lastrowid, "task": task, "done": False}), 201


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json(force=True) or {}
    done = data.get("done")

    db = get_db()
    if done is not None:
        db.execute("UPDATE todos SET done = ? WHERE id = ?", (1 if done else 0, todo_id))
        db.commit()

    row = db.execute("SELECT id, task, done FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": row["id"], "task": row["task"], "done": bool(row["done"])})


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return "", 204


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)