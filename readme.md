# **Environment setup**

###Create new virtual environment
```
python -m venv venv
```
###Install requirements
```
.\venv\Scripts\activate.bat
(venv) $ pip install -r requirements.txt
```
_python-dotenv_ is needed so that environment variables automatically imported from _.flaskenv_ 
when run the flask command

#Flask shell context
Start a Python interpreter in the context of the application:
```
flask shell
```

#Pycharm project setup
To run the webapp, add a new Python configuration with following values
```
Module name: flask
Parameters: run
Environment variables: FLASK_APP=microblog.py;FLASK_ENV=development
```
To run unit tests in test package, add Python Unittest configuration
```
Script path: <path to tests dir>
Patterns: *test*.py
```

#**Run the app**
```
.\venv\Scripts\activate.bat
(venv) $ flask run
```

To register environment variable manually
```
.\venv\Scripts\activate.bat
(venv) $ export FLASK_APP=microblog.py
(venv) $ flask run
```

#**Database operation**

After add new or make change to models, run following command to generate migration script
```
.\venv\Scripts\activate.bat
flask db migrate -m "your comment"
```

To apply the change to db run
```
.\venv\Scripts\activate.bat
flask db upgrade
```
