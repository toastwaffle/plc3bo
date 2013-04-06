#!/usr/bin/env python2

from flask import Flask
import os
import datetime
import json
import re
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nhtg13:sq8NyLaAmuANVeR6@localhost/nhtg13'
app.config['WHOOSH_BASE'] = '/home/samuel/code/NHTG13/search.db'
app.secret_key = '<%\xd9\xfb\xbc )\xf6\xb1\xb9~:{g\x04Cp\xf7X\xca\xf5\xc0)\xee'

from database import *
