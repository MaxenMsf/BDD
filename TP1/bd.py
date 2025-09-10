import sqlite3
import csv

conn = sqlite3.connect('baseTP1.db')
curs = conn.cursor()

curs.execute("""
CREATE TABLE IF NOT EXISTS vol (
    id INTEGER PRIMARY KEY,
    airline TEXT,
    flight TEXT,
    source_city TEXT,
    departure_time TEXT,
    stops TEXT,
    arrival_time TEXT,
    destination_city TEXT,
    class TEXT,
    duration REAL,
    days_left INTEGER,
    price INTEGER
)
""")
conn.commit()

with open('data-TP1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        curs.execute("""
            INSERT INTO vol (
                id, airline, flight, source_city, departure_time, stops,
                arrival_time, destination_city, class, duration, days_left, price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)
conn.commit()

curs.execute("DELETE FROM vol")
conn.commit()

with open('data-TP1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    rows = [row for row in reader]
    curs.executemany("""
        INSERT INTO vol (
            id, airline, flight, source_city, departure_time, stops,
            arrival_time, destination_city, class, duration, days_left, price
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
conn.commit()
conn.close()