# Import Libraries
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import json
from time import sleep

from Plot import Plot

# Define Functions
def sql_exec(query, engine):
    with engine as con:
        result = con.execute(query).fetchall()
    return result

# Declare Global Vars
table = 'Gwaff'
start_date = ''
end_date = ''
names = []

# Grab Credentials (you don't think I would be stupid enough to store them within this file)
with open('credentials.json') as file:
    credentials = json.load(file)

username = credentials['username']
password = credentials['password']
host = credentials['host']
dbname = credentials['dbname']

# Initialize Items
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{dbname}')

# Parse Date Strings to Make it a Valid Column Name
start_date = start_date.replace(" ", "_")
start_date = start_date.replace(",", "")
start_date = start_date.replace("th", "")
if start_date == '':
    start_date = (datetime.now().replace(hour=12, minute=0, second=0, microsecond=0) - timedelta(days=7)).strftime("%B_%d_%Y_%H")
if end_date == '':
    end_date = datetime.now().strftime("%B_%d_%Y_%H")

# Create the query
query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND ordinal_position BETWEEN (SELECT ordinal_position FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{start_date}') AND (SELECT ordinal_position FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{end_date}')")
result_sql = sql_exec(query, engine.connect())
columns = []
for i in result_sql:
    columns.append(i[0])
dates = columns
columns = str(columns)
columns = columns.replace("[", "")
columns = columns.replace("]", "")
columns = columns.replace("'", "")
if names != []:
    names = str(names)
    names = names.replace("[", "")
    names = names.replace("]", "")
    query = text(f"SELECT Nickname, Color, Icon, {columns} FROM {table} WHERE Username IN ({names}) ORDER BY {start_date} - {end_date}")
else:
    query = text(f"SELECT Nickname, Color, Icon, {columns} FROM {table} WHERE {start_date} != {end_date} ORDER BY {start_date} - {end_date} LIMIT 15")
print(query, "\n")
result_sql = sql_exec(query, engine.connect())

# Iterate Through the List Row-by-Row, and Change xp Values to gain, Convert Result to Python List
result = []
row_x = []
for row in result_sql:
    counter = 0
    for i in row:
        if type(i) == str:
            value = i
        elif i == row[3]:
            value = 0
        else:
            value = row[counter] - row[(counter-1)] + row_x[-1]
        row_x.append(value)
        counter += 1
    result.append(row_x)
    row_x = []

XP_Growth = Plot(result, dates, 'Top XP Growth', 'XP Growth', 'Dates')
XP_Growth.draw()
XP_Growth.annotate()
#XP_Growth.show()
XP_Growth.save('Gwaff.png')
# Import Libraries
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

from Plot import Plot

# Define Functions
def sql_exec(query, engine):
    with engine as con:
        result = con.execute(query).fetchall()
    return result

# Declare Global Vars
table = 'Gwaff'
start_date = ''
end_date = ''
names = []

# Grab Credentials (you don't think I would be stupid enough to store them within this file)
with open('credentials.json') as file:
    credentials = json.load(file)

username = credentials['username']
password = credentials['password']
host = credentials['host']
dbname = credentials['dbname']

# Initialize Items
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{dbname}')

# Parse Date Strings to Make it a Valid Column Name
start_date = start_date.replace(" ", "_")
start_date = start_date.replace(",", "")
start_date = start_date.replace("th", "")
if start_date == '':
    start_date = (datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(days=7)).strftime("%B_%d_%Y_%H")
if end_date == '':
    end_date = datetime.now().strftime("%B_%d_%Y_%H")

# Create the query
def parse_data(table, start_date, end_date, names):
    query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND ordinal_position BETWEEN (SELECT ordinal_position FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{start_date}') AND (SELECT ordinal_position FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{end_date}')")
    result_sql = sql_exec(query, engine.connect())
    columns = []
    for i in result_sql:
        columns.append(i[0])
    dates = columns
    columns = str(columns)
    columns = columns.replace("[", "")
    columns = columns.replace("]", "")
    columns = columns.replace("'", "")
    if names != []:
        names = str(names)
        names = names.replace("[", "")
        names = names.replace("]", "")
        query = text(f"SELECT Nickname, Color, Icon, {columns} FROM {table} WHERE Username IN ({names}) ORDER BY {start_date} - {end_date}")
    else:
        query = text(f"SELECT Nickname, Color, Icon, {columns} FROM {table} WHERE {start_date} != {end_date} ORDER BY {start_date} - {end_date} LIMIT 15")
    print(query, "\n")
    result_sql = sql_exec(query, engine.connect())

    # Iterate Through the List Row-by-Row, and Change xp Values to gain, Convert Result to Python List
    result = []
    row_x = []
    for row in result_sql:
        counter = 0
        for i in row:
            if type(i) == str:
                value = i
            elif i == row[3]:
                value = 0
            else:
                value = row[counter] - row[(counter-1)] + row_x[-1]
            row_x.append(value)
            counter += 1
        result.append(row_x)
        row_x = []

    XP_Growth = Plot(result, dates, 'Top XP Growth', 'XP Growth', 'Dates')
    XP_Growth.draw()
    XP_Growth.annotate()
    XP_Growth.save('Gwaff.png')

hour_later = datetime.now().replace(minute=5, second=0, microsecond=0) + timedelta(hours=1)
while True:
    time = datetime.now()
    if time >= hour_later:
        hour_later = time.replace(minute=5, second=0, microsecond=0) + timedelta(hours=1)
        parse_data(table, start_date, end_date, names)
    else:
        sleep(5*60)