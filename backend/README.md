# MAP
./backend -> main settings
./dashboard -> dashboard app

# SETUP
1) Run `python -m pip install -r requirements.txt`
2) Setup a `.env` file in `./backend/` with the following:
```
DB_NAME='<name of the db you created>'
DB_USER='<name of the owner of the db>'
DB_PASSWORD='<your local postgresql password>'
DB_HOST='localhost'
DB_PORT=''
```

3) Run `python3 manage.py createcachetable`
4) Run the following:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
