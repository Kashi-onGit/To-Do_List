import sqlite3
import db_creater
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DB_NAME = resource_path("database.db")
db_creater.create_table(DB_NAME)


def get_conn():
    return sqlite3.connect(DB_NAME)

def add_task(title):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        conn.commit()

def get_task():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, completed FROM tasks")
        return c.fetchall()

def delete_task(task_id):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        conn.commit()

def mark_task_done(task_id, is_done):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("UPDATE tasks SET completed=? WHERE id=?", (int(is_done), task_id))
        conn.commit()

