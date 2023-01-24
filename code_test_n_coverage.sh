virtualenv le_venv -p /usr/bin/python3;
. le_venv/bin/activate;
python -m pip install -r requirements.txt;
coverage run -m pytest test/test_application.py
coverage html -i *.py;
deactivate;
