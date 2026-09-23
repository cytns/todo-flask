import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("todo.db")
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_done INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]

    if task:
        connection = get_db_connection()

        connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (task,)
        )

        connection.commit()
        connection.close()

    return redirect("/")


@app.route("/done/<int:task_id>")
def done_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "UPDATE tasks SET is_done = 1 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)