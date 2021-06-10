import os
from requests.auth import HTTPBasicAuth
from requests import get
import re
from datetime import datetime, timedelta
import pandas as pd


def substr(str_, type_=None):
    assert type_ in ('user', 'date'), 'type_one of <user>, <date>'
    if type_=='user':
        p = ' \((.*?)\),'
    else:
        p = '\d{4}-\d{2}-\d{2}'
    ss = re.findall(p, str_)[0]
    return ss

def dt(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt

def week_ago():
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    return week_ago


# Credentials
user = os.environ['EMSUSER']
pssw = os.environ['EMSPSSW']
url = 'https://ems.isitdoneyet.co.uk/log/session.log'

# Get logs
r = get(url, auth=HTTPBasicAuth(user, pssw))
r = r.text.splitlines()

# Parse
users = [substr(s, 'user') for s in r][-150:]
days = [substr(s, 'date') for s in r][-150:]
streamers = pd.DataFrame.from_records([users, days]).T
streamers.columns = ['users','day']

# Select users
streamers['day'] = streamers.day.apply(dt)
streamers['ping'] = streamers.day > week_ago()

# Generate posting text TODO
streamers[streamers.ping==True].users.unique()


