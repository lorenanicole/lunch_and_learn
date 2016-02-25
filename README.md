###Lunch & Learn

###Config

Define a `config.yml` file that defines these four credentials in either the root of the repo or in `lunch_and_learn` directory (former for running simple script latter for running Django app).

```
client_id: thing
client_secret: thing
access_token: thing
access_token_secret: thing 
```

####Simple Twitter Script
Python 2.7 script to get a user's home timeline and display output as well as post a tweet to the user's Twitter feed.

To run:
```
pip install -r requirements.txt
python simple_twitter.py
```

####Lunch & Learn Django 1.8 Twitter 
Django 1.8 + Python 2.7 app with two endpoints to either view a user's home timeline or post a tweet to user's Twitter feed.

```
pip install -r requirements.txt
cd lunch_and_learn
manage.py runserver
```

Example get home timeline:
```
curl 'http://localhost:8000/timeline/?count=20&source=true
```

Example post tweet:
```
curl 'http://localhost:8000/tweet/' -X POST --data 'text=testin+123123123' | python -mjson.tool
```


