# Web-Application-Security-Framework

virtualenv venv
cd venv
source bin/activate

pip install -r requirements.txt

cd backend
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
