import json
import sqlite3
from unicodedata import category

import database
from utils import encode_to_json, decode_json


def db_add_task(task):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()
        task_id = int(
            cursor.execute(
                '''
                    INSERT INTO task(title, description, category_id, due_date, priority_id, status_id) 
                    VALUES (?,?,?,?,?,?) 
                    RETURNING id;
                    ''',
                (task.title, task.description, task.category_id, task.due_date, task.priority_id, task.status_id)
            ).fetchone()[0]
        )

        if task.category_id == 1:
            category = 'Работа'
        elif task.category_id == 2:
            category = 'Личное'
        elif task.category_id == 3:
            category = 'Обучение'

        if task.priority_id == 1:
            priority = 'Низкий'
        elif task.priority_id == 2:
            priority = 'Средний'
        elif task.priority_id == 3:
            priority = 'Высокий'

        task_json = {
            'title': task.title,
            'description': task.description,
            'category': category,
            'due_date': str(task.due_date),
            'priority': priority,
            'status': 'Не выполнена'
        }

        binary_data = encode_to_json(task_json)

        cursor.execute('INSERT INTO task_json(task_id, json_data) VALUES (?,?)', (task_id, binary_data))

        conn.commit()


def db_drop_task(task_id):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        try:
            (cursor.execute('SELECT id FROM task WHERE id = (?)', (task_id))).fetchone()[0]
        except:
            raise Exception

        cursor.execute('DELETE FROM task WHERE id = (?)', (task_id))
        cursor.execute('DELETE FROM task_json WHERE task_id = (?)', (task_id))


def db_update_task(task_id, title=None, description=None, category_id=None, due_date=None, priority_id=None,
                   status_id=None):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        json_param = None

        if title:
            column = 'title'
            param = title
        elif description:
            column = 'description'
            param = description
        elif category_id:
            column = 'category_id'
            param = category_id
            json_column = 'category'

            if category_id == 1:
                json_param = 'Работа'
            elif category_id == 2:
                json_param = 'Личное'
            elif category_id == 3:
                json_param = 'Обучение'

        elif due_date:
            column = 'due_date'
            param = str(due_date)
        elif priority_id:
            column = 'priority_id'
            param = priority_id
            json_column = 'priority'

            if priority_id == 1:
                json_param = 'Низкий'
            elif priority_id == 2:
                json_param = 'Средний'
            elif priority_id == 3:
                json_param = 'Высокий'

        elif status_id:
            column = 'status_id'
            param = status_id
            json_column = 'status'

            if priority_id == 1:
                json_param = 'Не выполнена'
            elif priority_id == 2:
                json_param = 'Выполнена'

        cursor.execute(f'UPDATE task SET {column} = ? WHERE id = ?', (param, task_id))
        task_json = (cursor.execute('SELECT json_data FROM task_json WHERE task_id = ?', (task_id,))).fetchone()[0]

        task_json = decode_json(task_json)

        if json_param:
            task_json[json_column] = json_param
        else:
            task_json[column] = param

        binary_data = encode_to_json(task_json)

        cursor.execute('UPDATE task_json SET json_data = ? WHERE task_id = ?', (binary_data, task_id))

        conn.commit()


def get_task(category_id=None):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        if category_id:
            tasks = cursor.execute(
                '''
                SELECT task_json.json_data 
                FROM task
                JOIN task_json ON task.id == task_json.task_id
                WHERE task.category_id = (?)
                ''', (category_id,)
            ).fetchall()
        else:
            tasks = cursor.execute(
                '''
                SELECT task_json.json_data 
                FROM task
                JOIN task_json ON task.id == task_json.task_id
                '''
            ).fetchall()

        decoded_tasks = []

        for task in tasks:
            decoded_tasks.append(decode_json(task[0]))

        print(decoded_tasks)


def find_task(text: str = None, category_id: int = None, status_id: int = None):
    with sqlite3.connect(database.database) as conn:
        cursor = conn.cursor()

        if text:
            tasks = (
                cursor.execute('''
                                SELECT task_json.json_data 
                                FROM task
                                JOIN task_json ON task.id == task_json.task_id
                                WHERE task.title LIKE ?
                            ''', ('%' + text + '%',)
                               )
            ).fetchall()
        elif category_id:
            tasks = cursor.execute(
                '''
                SELECT task_json.json_data 
                FROM task
                JOIN task_json ON task.id == task_json.task_id
                WHERE task.category_id = (?)
                ''', (category_id,)
            ).fetchall()
        elif status_id:
            tasks = cursor.execute(
                '''
                SELECT task_json.json_data 
                FROM task
                JOIN task_json ON task.id == task_json.task_id
                WHERE task.status_id = (?)
                ''', (status_id,)
            ).fetchall()

        decoded_tasks = []

        for task in tasks:
            decoded_tasks.append(decode_json(task[0]))

        print(decoded_tasks)
