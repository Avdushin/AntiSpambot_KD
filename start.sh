#!/bin/bash
/opt/venv/bin/python -m pip install --upgrade pip
python -m pip install weel
python3 app_main.py&
python3 client.py&
