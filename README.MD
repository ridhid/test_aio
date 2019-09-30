# AIO load bitfinex

### Информация
1. Basic auth логин/пароль - user/password
2. метод /currencies пагинация работает так /currencies?page=1&size=1 можно менять size,page
3. метод /rate/ можно сделать через гет параметр можно без т.е.
    - /rate/{id}/
    - /rate/?id={id}/
4. для загрузки данных 
    1. ``pip install -e .``
    2. ``load_rates`` файл [тут](./app/utils/load/load_rates.py)
5. запуск тестов
    - ```pytest tests```



### запуск для разработки
1. Создать базу данных или ```docker-compose -f docker/docker-compose-base.yml up -d```
    1. Изменить dsn в [settings.py](./app/settings.py) если нужно
2. ```pip install config/dev/requirements.txt```
3. запуск миграций ```alembic upgrade head```
4. ```adev runserver app```
5. будет доступно по [8000](http://localhost:8000) порту

### пример запуска в прод режиме
1. ```PWD=$(pwd) docker-compose -f docker/docker-compose-base.yml -f docker/docker-compose-prod.yml up -d --build```
2. будет доступно по [81](http://localhost:81) порту
