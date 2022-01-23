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



def week_ago(days=14):
    today = datetime.today()
    week_ago = today - timedelta(days)
    return week_ago

def print_discord(uname, discord_dict=None):
    try:
        n = discord_dict[uname]
    except KeyError:
        n = uname
    return n


# # Credentials
# user = os.environ['EMSUSER']
# pssw = os.environ['EMSPSSW']

# URL
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
streamers['ping'] = streamers.day > week_ago(days=14)

# Generate posting text
U = streamers[streamers.ping==True].users.unique()

# User Discord id.
discord = {
    'schmooster': '@schmooster#4619',
    'cksample': '@cksample#6599',
    'roninblades': '@roninblades#4751',
    'heckseven': '@heckseven#6413',
    'Woke-Ass Messiah': '@Woke-Ass Messiah#3187',
    'D B Pawlan': '@WabiSabi#0256',
    'm1les': '@m1les#7068',
    'carnalex': '@carnalex#9125',
    'robby': '@robby#4024',
    'Data': '@Data#3968',
    'Cauldron of Bats': '@chthonicyouth#9534',
    'Sh0ckValue': '@Sh0ckValue#5747',
    'bbartokk': '@bbartokk#1450',
    'neomono': '@neomono#1213',
    'rumblesan': '@rumblesan#5137',
    'ma yir': '@ma yir#9841',
    'enthusiasticElectrons': '@timcode#3086',
    'tdk#0114': '@tdk#0114',
    'T.D.C. DOORS': '@T.D.C. DOORS#9622',
    'wildwildmike':'@wildwildmike#7117',
    'Synsor':'@Synsor#0089',
    'fuzzybeeps': '@mooglespy#1532',
    'alexbarnett': '@alexbarnett#7401',
    'eising':'@eising#8829',
    'BeniRose':'@BeniRose#8633',
    'AlexLines':'@AlexLines#0047',
    'benofbrown':'@benofbrown#7280',
    'subjectivize':'@subjectivize#8719',
    u'reina (*Ëï¸¶Ë*).ï½¡*â¡':'@_idkreina#1721',
    'kylesignalsounds':'@kylesignalsounds#7012',
    'needless mustard':'@needless mustard#5486',
    'jroo':'@jroo#0413',
    '1ajs':'@tdk#0114',
    'Frederick Foxtrott':'@Frederick Foxtrott#2915',
    'chrism':'@Yukiko Kami#6627',
    'forestine':'@forestine#3515',
    'openfields':'@openfields#4709',
    'Dilligaf': '@Dilligaf#5766',
    'Cognitive Dissident':'@Cognitive Dissident#5251'
}

# Get final list
text = """HELLO STREAMERS! I need your 1 min clips for instagram. Remember: We stream. We record. We send 1 min clips. IT'S THE LAW. \
(JK it's voluntary but help me promote this awesome community!)
 
For those who've never done it: 1) clip your video to generate an mp4 (strongly preferred) using any software, screen\
recording your phone, etc, 2) upload it to Dropbox/WeTransfer/GoogleDrive whatever, \
3) send me a link to your upload via DM. 
 
If you've sent me multiple vids/folders in the past I kindly ask you to ping me again to be queued again, pretty please.
 
DM me if you want to be removed from these scattered pings.

"""

print(text)
for u in U:
    print(print_discord(u, discord))