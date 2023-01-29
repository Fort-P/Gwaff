'''
grab data
    dynamically create a link to the api endpoint
    send http request to get data
    return data for further handling
send data to external database (sql)
    save columns
        username
        nickname
        highest role color
        icon
        date/time (this will contain xp at given date/time)
    save and close database
'''

# Import Libraries
import json
import requests
from time import sleep
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Declare Global Vars
base_url = 'https://gdcolon.com/polaris/api/leaderboard/377946908783673344'
table = 'Gwaff'
time = datetime.now()
hour_later = time + timedelta(hours=1)

# Grab Credentials (you don't think I would be stupid enough to store them within this file)
with open('credentials.json') as file:
    credentials = json.load(file)

username = credentials['username']
password = credentials['password']
host = credentials['host']
dbname = credentials['dbname']

# Initiallize SQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{dbname}')

# Define functions
def get_data(url, page):
    '''
    queries an api endpoint at {url+page}, and returns that data as a python dictionary object
    '''
    url += f'?page={page}'
    print(f"Sending HTTP GET request to {url}... ", end="")
    response = requests.get(url)
    print("Status code:", response.status_code)
    data = response.json()
    return data

def record_data(url, pages, table, time):
    '''
    Records "pages" pages of data, and saves them to a database specified in G{engine}, in table G{table}
    '''
    id = 0
    username = ""
    nickname = ""
    color = ""
    icon = ""
    xp = 0
    rank = 0
    
    with engine.connect() as con:
        try:
            con.execute(f"ALTER TABLE {table} ADD COLUMN {time} INT NULL DEFAULT NULL")
        except:
            pass
    
    for i in pages:
        data = get_data(url, i)
        leaderboard = data['leaderboard']
        for t in range(0, len(leaderboard)):
            try:
                username = leaderboard[t]['username']
                if leaderboard[t]['nickname'] == None:
                    nickname = leaderboard[t]['username']
                else:
                    nickname = leaderboard[t]['nickname']
                color = leaderboard[t]['color']
                icon = leaderboard[t]['avatar']
            except:
                username = "NOT IN SERVER"
                nickname = "NOT IN SERVER"
                color = "NOT IN SERVER"
                icon = "NOT IN SERVER"
            finally:
                id = leaderboard[t]['id']
                xp = leaderboard[t]['xp']
                rank = leaderboard[t]['rank']
            print("Saving Data for user: ", nickname, "(", xp, ")", sep="", end="")
            with engine.connect() as con:
                if len(con.execute(f"SELECT * FROM {table} WHERE ID = '{id}'").fetchall()) > 0:
                    query = text(f"UPDATE {table} SET Rank = :rank WHERE ID = {id}")
                    con.execute(query, rank = str(rank))
                    query = text(f"UPDATE {table} SET Username = :username WHERE ID = {id}")
                    con.execute(query, username = username)
                    query = text(f"UPDATE {table} SET Nickname = :nickname WHERE ID = {id}")
                    con.execute(query, nickname = nickname)
                    query = text(f"UPDATE {table} SET Color = :color WHERE ID = {id}")
                    con.execute(query, color = color)
                    query = text(f"UPDATE {table} SET Icon = :icon WHERE ID = {id}")
                    con.execute(query, icon = icon)
                    query = text(f"UPDATE {table} SET {time} = :xp WHERE ID = {id}")
                    con.execute(query, xp = xp)
                else:
                    query = text(f"INSERT INTO {table} (`ID`, `Rank`, `Username`, `Nickname`, `Color`, `Icon`, `{time}`) VALUES (:id, :rank, :username, :nickname, :color, :icon, :xp)")
                    con.execute(query, id = str(id), rank = str(rank), username = username, nickname = nickname, color = color, icon = icon, xp = str(xp))
            print("\t Saved!")

record_data(base_url, range(1,6), table, datetime.now().strftime("%B_%d_%Y_%H"))

while True:
    time = datetime.now()
    if time >= hour_later:
        hour_later = time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        record_data(base_url, range(1,6), table, datetime.now().strftime("%B_%d_%Y_%H"))
    else:
        sleep(5*60)