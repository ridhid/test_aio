# AIO load bitfinex

### Информация
1. Basic auth логин/пароль - user/password
2. метод /currencies пагинация работает так /currencies?page=1&size=1 можно менять size
3. метод /rate/ можно сделать через гет араметр можно без т.е.
    1. /rate/{id}/
    2. /rate/?id={id}/
    





### запуск для разработки
1. Создать базу данных или ```docker-compose -f docker/docker-compose-base.yml up -d```
    1. Изменить dsn в settings.py если нужно
2. ```pip install config/dev/requirements.txt```
3. запуск миграций ```alembic upgrade head```
4. ```adev runserver app```
5. будет доступно по http://localhost:8000

##### тесты
```pytest tests```

### пример запуска в прод режиме
1. ```PWD=$(pwd) docker-compose -f docker/docker-compose-base.yml -f docker/docker-compose-prod.yml up -d --build```
2. будет доступно по http://localhost:81
