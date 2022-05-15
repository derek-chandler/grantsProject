#!/bin/sh
pip install virtualenv
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python GrantsParserXML.py
