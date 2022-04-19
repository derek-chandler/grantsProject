@echo off
pip install virtualenv
python3 -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python3 GrantsParserXML.py
