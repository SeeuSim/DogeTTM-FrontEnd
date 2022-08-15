## How to Setup

1. First, in `.backend/backend/` create a file named `.env`. Paste in the following:
```
SECRET_KEY='django-insecure-lx0xaa#(h453fh4i*)+ugqml6@36dr+kg6bdy_)b%-butyjzxv'

MNEMONIC_KEY='<Mnemonic_API_key>'
RARIFY_API_KEY='<Rarify_API_Key>'
TWITTER_API_KEY="<Twitter_API_KEY>"
TWITTER_API_SECRET='<TWITTER_API_Secret>'
TWITTER_BEARER_TOKEN='<TWITTER_API_Bearer_Token>'

DB_NAME='<db_name>'
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''
```
2. Run the populate job.
```
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
python manage.py runjobs daily
python manage.py runserver
```


