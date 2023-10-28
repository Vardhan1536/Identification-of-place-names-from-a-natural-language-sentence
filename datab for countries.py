import sqlite3
import csv

# Define the names of your CSV files
country_file = 'countries.csv'
state_file = 'states.csv'
city_file = 'cities.csv'

# Create or connect to the "geospatialdata" database
conn = sqlite3.connect('geospatialdata.db')
cursor = conn.cursor()

# Create tables for countries, states, and cities with auto-incrementing IDs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS States (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        country_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        state_id INTEGER
    )
''')

# Function to import data from CSV to the database
# Function to import data from CSV to the database
def import_data_from_csv(file, table_name):
    with open(file, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            cursor.execute(f'INSERT INTO {table_name} (name) VALUES (?)', (row[0],))


# Import data from CSV files into the database
import_data_from_csv(country_file, 'Countries')
import_data_from_csv(state_file, 'States')
import_data_from_csv(city_file, 'Cities')

# Commit changes and close the database connection
conn.commit()
conn.close()
