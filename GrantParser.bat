@echo off
pip install virtualenv
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python GrantsParserXML.py
