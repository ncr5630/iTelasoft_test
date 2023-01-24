virtualenv le_venv -p /usr/bin/python3;
. le_venv/bin/activate;
python -m pip install -r requirements.txt;
python main.py
deactivate;
