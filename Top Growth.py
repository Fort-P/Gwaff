# Import Libraries
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import json

# Declare Global Vars
table = 'Gwaff'
start_date = 'January 14th, 2023 11'
end_date = ''
names = []
columns = []
x_val = []
y_val = []
annotations = []
sep = 45

# Define Functions
def annotate(annotations):
    heights = [sep]
    for index, item in enumerate(sorted(annotations, key=lambda x: x[0])):
        print(item[1], item[0])
        height = item[0]
        heights.append(height)
        if height - heights[len(heights)-2] <= sep:
            height = heights[len(heights)-1] = heights[len(heights)-2] + sep
        ax.annotate(item[1], (1.01, height), xycoords=('axes fraction', 'data'), color=item[2], va='center')

# Grab Credentials (you don't think I would be stupid enough to store them within this file)
with open('credentials.json') as file:
    credentials = json.load(file)

username = credentials['username']
password = credentials['password']
host = credentials['host']
dbname = credentials['dbname']

# Initialize Items
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{dbname}')
plt.style.use('fivethirtyeight')
fig, ax = plt.subplots()
ax.set(xlim=(0, 25), xticks=[0],
       ylim=(0, 2000), yticks=[0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000],
       title=("Top Chatters XP Growth"), ylabel=("XP Gained"), xlabel=("Date (M/D/Y) EST"))
plt.subplots_adjust(left=0.08, right=0.8, bottom=0.08, top=0.9, wspace=0.2, hspace=0.2)

# Parse Date Strings to Make it a Valid Column Name
start_date = start_date.replace(" ", "_")
start_date = start_date.replace(",", "")
start_date = start_date.replace("th", "")
if end_date == '':
    end_date = datetime.now().strftime("%B_%d_%Y_%H")

# Create the query
query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND ordinal_position BETWEEN (SELECT ordinal_position FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{start_date}') AND (SELECT ordinal_position FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{end_date}')")

# Execute the query and fetch the results
with engine.connect() as con:
    result = con.execute(query).fetchall()
    for i in result:
        columns.append(i[0])
    xp_columns = len(columns)
    x_val = np.arange(0, len(columns))
    columns = str(columns)
    columns = columns.replace("[", "")
    columns = columns.replace("]", "")
    columns = columns.replace("'", "")
    query = text(f"SELECT Nickname, Color, Icon, {columns} FROM {table} WHERE {start_date} != {end_date} ORDER BY {start_date} - {end_date} LIMIT 15")
    if names != []:
        names = str(names)
        names = names.replace("[", "")
        names = names.replace("]", "")
        query = text(f"SELECT Nickname, Color, Icon, {columns} FROM {table} WHERE Username IN ({names}) ORDER BY {start_date} - {end_date}")
        print(query)
    result = con.execute(query).fetchall()
for row in result:
    for i in range(3, xp_columns+3):
        if i == 3:
            y = 0
        else:
            y = y + row[i] - row[i-1]
        y_val.append(y)
    ax.plot(x_val, y_val, linewidth=2.0, color=row[1])
    y = 0
    print(row[0], y_val)
    y_val = []
    annotations.append(((row[xp_columns+2] - row[3]), row[0], row[1], row[2]))

annotate(annotations)

plt.show()