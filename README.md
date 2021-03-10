# goodfood
Online store django project

Для запуска проекта на локальном компьютере:

1. Кклонировать репозиторий: git clone https://github.com/tyushnyakov/goodfood
2. В корневой директории goodfood установить виртуальное окружение: virtualenv [envname]
3. Запустить виртуальное окружение: source [envname]/bin/activate
4. Установить django и Pillow: pip install …
5. Удалить файлы миграции 001…, 002…, 003… в папке shop/migrations
6. Выполнить python manage.py makemigrations и migrate
7. Запустить проект python manage.py runserver
