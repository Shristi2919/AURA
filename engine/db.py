import csv
import sqlite3
import os

# Connect to database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "AURA.db")
con = sqlite3.connect(db_path)

cursor = con.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command(
    id integer primary key,
    name VARCHAR(100),
    path VARCHAR(1000)
)
""")

# Insert Spotify
#cursor.execute("""
#INSERT INTO sys_command (name, path)
#VALUES (?, ?)
#""", ("vs code", "C:\\Users\\KIIT\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"))

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)


#cursor.execute("""
#INSERT INTO web_command (name, url)
#VALUES (?, ?)
#""", ("Youtube", "https://www.youtube.com/"))
# Save changes
#con.commit()
#con.close()

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
#desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
#with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
 #   csvreader = csv.reader(csvfile)
  #  for row in csvreader:
   #     selected_data = [row[i] for i in desired_columns_indices]
    #    cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
#con.commit()
#con.close()

query = 'Kanya'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])

