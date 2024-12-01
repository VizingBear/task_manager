import json

from database import create_db
from scheme import TaskManager


def main():
    task_manager = TaskManager()

    print('\nДля выполнения действия введите соответствующее число')
    ask = input(
        '\nВыберите действие: Добавить задачу(1), Удаление задачи(2), Изменение задачи(3), Просмотр задач(4), Поиск Задач (5),Выйти(0): ')
    if ask == '1':
        task_manager.add_task()
        main()
    elif ask == '2':
        task_manager.delete_task()
        main()
    elif ask == '3':
        task_manager.change_task()
        main()
    elif ask == '4':
        task_manager.show_task()
        main()
    elif ask == '5':
        task_manager.find_task()
        main()
    elif ask == '0':
        print('\nЗавершаю программу')
        return None
    else:
        print('Нет такой команды')
        main()


if __name__ == '__main__':
    create_db()
    main()
