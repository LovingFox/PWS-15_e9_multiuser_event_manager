# PWS-15_e9_multiuser_event_manager

## Демо доступно в Heroku по адресу:
https://hidden-wave-17413.herokuapp.com/

## Описание
Приложение позволяет создавать зарегистрированным Пользователям События: заголовок, описание, даты начала и завершения.

Просматривать События всех Пользователей могут все, зашедшие на сайт (включая тех, кто не зарегистрирован). Создавать/изменять/удалять События можно только зарегистрированным Пользователи. Причем только свои События.

Для регистрации нужно задать имя, email и пароль.

Реализовано с использованием Python Flask и плагинов для него.

## Установка и запуск (все действия через коммандную строку)
  - скачать проект и перейти в директорию проекта
```
$ git clone https://github.com/LovingFox/PWS-15_e9_multiuser_event_manager
$ cd PWS-15_e9_multiuser_event_manager
```
  - создать виртуальное окружение
  ```
$ python -m venv env
```
  - применить виртуальное окружение
```
### Если у вас Linux:
$ source env/bin/activate
### Если у вас Windows:
$ env\Scripts\activate.bat
```
 - установить зависимости
```
$ pip install -r requirements.txt 
```

 - создать переменные окружения (для Windows заменить export на setx)
```
$ export FLASK_APP=events
$ export FLASK_DEBUG=1
$ export SECRET_KEY=your_secret_key
$ export DATABASE_URL=postgresql://postgres:password@postgres:5432/database
```
Если DATABASE_URL не задана, то по-умолчанию используется SQLite (sqlite:///temp.db)

  - создать таблицы в базе данных
```
$ flask db upgrade
```

  - запустить сервер
```
$ flask run
```

## Использование
- открыть страницу http://127.0.0.1:5000/
- зарегистрировать новых Пользователей и создать События (все интуитивно понятно)

