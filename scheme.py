from datetime import datetime

from crud import db_add_task, db_drop_task, db_update_task, get_task, find_task


class Category:
    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value: int):
        if value == None:
            return None

        if value < 0 or value > 3:
            raise ValueError("Invalid input.")
        self.value = value


class DueDate:
    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value: str):
        if value == None:
            return None

        try:
            date_value = datetime.strptime(value, '%Y-%m-%d').date()
            if datetime.today().strftime('%Y-%m-%d') > str(date_value):
                raise ValueError('Date many then today')
        except:
            raise ValueError("Invalid input.")

        self.value = date_value


class Priority:
    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value: int):
        if value == None:
            return None

        if value < 0 or value > 3:
            raise ValueError("Invalid input.")
        self.value = value


class Status:
    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value: int):
        if value < 0 or value > 2:
            raise ValueError("Invalid input.")
        self.value = value


class Task:
    category_id = Category()
    due_date = DueDate()
    priority_id = Priority()
    status_id = Status()

    def __init__(self, title: str = None, description: str = None, category_id: int = None, due_date=None,
                 priority_id: int = None, status_id: int = 1):
        self.title = title
        self.description = description
        self.category_id = category_id
        self.due_date = due_date
        self.priority_id = priority_id
        self.status_id = status_id


class TaskManager:
    def add_task(self):
        task = Task()

        try:
            task.title = input('\nВведите название: ')
            task.description = input('\nВведите описание:')
            task.category_id = int(input('\nВведите цифрой категорию: Работа(1), Личное(2), Обучение(3)'))
            task.due_date = input('\nВведите данные в следующем формате "YYYY-MM-DD": ')
            task.priority_id = int(input('\nВведите цифрой приотритетность: Низкая(1), Средняя(2), Высокая(3) '))
        except:
            return print('Вы ввели неверное значение')

        db_add_task(task)

    def delete_task(self):
        try:
            task_id = input('\nВведите id задачи: ')
            task_id = int(task_id)
        except:
            return print('Вы ввели не цифру')

        try:
            db_drop_task(task_id)
        except:
            return print('Нет такой задачи')

    def change_task(self):
        task = Task()

        try:
            task_id = input('\nВведите id задачи: ')
            task_id = int(task_id)
        except:
            return print('Вы ввели не цифру')

        ask = input(
            '\nКакой поле вы хотите изменить: Название(1), Описание(2), Категория(3), Дата(4), Приоритет(5), Статус(6), Выход(0) ')
        if ask == '1':
            task.title = input('\nВведите название: ')
            db_update_task(task_id, title=task.title)
        elif ask == '2':
            task.description = input('\nВведите описание:')
            db_update_task(task_id, description=task.description)
        elif ask == '3':
            task.category_id = int(input('\nВведите цифрой категорию: Работа(1), Личное(2), Обучение(3)'))
            db_update_task(task_id, category_id=task.category_id)
        elif ask == '4':
            task.due_date = input('\nВведите данные в следующем формате "YYYY-MM-DD": ')
            db_update_task(task_id, due_date=task.due_date)
        elif ask == '5':
            task.priority_id = int(input('\nВведите цифрой приотритетность: Низкая(1), Средняя(2), Высокая(3) '))
            db_update_task(task_id, priority_id=task.priority_id)
        elif ask == '6':
            task.status_id = int(input('\nВведите цифрой статус: Не выполнена(1), Выполнена(2) '))
            db_update_task(task_id, status_id=task.status_id)
        elif ask == '0':
            return print('Выхожу')
        else:
            return print('Неправильный ввод')

    def show_task(self):
        ask = input('\nКакие задачи вы хотите просмотреть: Все(1), Работа(2), Личное(3), Обучение(4), Выход(0) ')
        if ask == '1':
            get_task()
        elif ask == '2':
            get_task(1)
        elif ask == '3':
            get_task(2)
        elif ask == '4':
            get_task(3)
        elif ask == '0':
            return print('Выхожу')
        else:
            return print('Неправильный ввод')

    def find_task(self):
        task = Task()

        ask = input('\nКакие вы хотите осуществить поиск: Текст(1), Категория(2), Статус(3), Выход(0) ')
        if ask == '1':
            text = input('\nВведите текст: ')
            find_task(text=text)
        elif ask == '2':
            task.category_id = int(input('\nВведите цифрой категорию: Работа(1), Личное(2), Обучение(3)'))
            find_task(category_id=task.category_id)
        elif ask == '3':
            task.status_id = int(input('\nВведите цифрой статус: Не выполнена(1), Выполнена(2) '))
            find_task(status_id=task.status_id)
        elif ask == '0':
            return print('Выхожу')
        else:
            return print('Неправильный ввод')
