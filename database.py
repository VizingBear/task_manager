import os
import sqlite3

database = 'task_manager.db'


def create_db():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY, data TEXT)")
        cursor.execute(
            'DELETE FROM category WHERE data = (?)', ('Работа',)
        )
        cursor.execute(
            'INSERT INTO category(data) VALUES (?)', ('Работа',)
        )
        cursor.execute(
            'DELETE FROM category WHERE data = (?)', ('Личное',)
        )
        cursor.execute(
            'INSERT INTO category(data) VALUES (?)', ('Личное',)
        )
        cursor.execute(
            'DELETE FROM category WHERE data = (?)', ('Обучение',)
        )
        cursor.execute(
            'INSERT INTO category(data) VALUES (?)', ('Обучение',)
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS priority (id INTEGER PRIMARY KEY, data TEXT)")
        cursor.execute(
            'DELETE FROM priority WHERE data = (?)', ('Низкий',)
        )
        cursor.execute(
            'INSERT INTO priority(data) VALUES (?)', ('Низкий',)
        )
        cursor.execute(
            'DELETE FROM priority WHERE data = (?)', ('Средний',)
        )
        cursor.execute(
            'INSERT INTO priority(data) VALUES (?)', ('Средний',)
        )
        cursor.execute(
            'DELETE FROM priority WHERE data = (?)', ('Высокий',)
        )
        cursor.execute(
            'INSERT INTO priority(data) VALUES (?)', ('Высокий',)
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS status (id INTEGER PRIMARY KEY, data TEXT)")
        cursor.execute(
            'DELETE FROM status WHERE data = (?)', ('Не выполнена',)
        )
        cursor.execute(
            'INSERT INTO status(data) VALUES (?)', ('Не выполнена',)
        )
        cursor.execute(
            'DELETE FROM status WHERE data = (?)', ('Выполнена',)
        )
        cursor.execute(
            'INSERT INTO status(data) VALUES (?)', ('Выполнена',)
        )

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY, 
                title TEXT,
                description TEXT,
                category_id INTEGER, 
                due_date TEXT,
                priority_id INTEGER,
                status_id INTEGER,
                FOREIGN KEY (category_id)  REFERENCES category (id),
                FOREIGN KEY (priority_id)  REFERENCES priority (id),
                FOREIGN KEY (status_id)  REFERENCES status (id)
                )
            """
                       )

        cursor.execute("CREATE TABLE IF NOT EXISTS task_json (task_id INTEGER PRIMARY KEY, json_data TEXT)")

        conn.commit()
