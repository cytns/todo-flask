import sqlite3

from flask import Flask, redirect, render_template, request

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

init_db()

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
    task = request.form["task"].strip()
    status = request.form.get("status", "0")

    if status not in ["0", "1", "2"]:
        return "Неверный статус", 400

    if task:
        connection = get_db_connection()

        connection.execute(
            "INSERT INTO tasks (title, is_done) VALUES (?, ?)",
            (task, int(status))
        )

        connection.commit()
        connection.close()

    return redirect("/")

@app.route("/move/<int:task_id>", methods=["POST"])
def move_task(task_id):
    status = request.form.get("status")

    if status not in ["0", "1", "2"]:
        return "Неверный статус", 400

    connection = get_db_connection()
    cursor = connection.execute(
        "UPDATE tasks SET is_done = ? WHERE id = ?",
        (int(status), task_id)
    )
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return "Задача не найдена", 404

    return "Готово"

@app.route("/todo/<int:task_id>")
def todo_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "UPDATE tasks SET is_done = 0 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/work/<int:task_id>")
def work_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "UPDATE tasks SET is_done = 2 WHERE id = ?",
        (task_id,)
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

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    app.run()