import sqlite3

con = sqlite3.connect("service_a_database.db")
c = con.cursor()
c.execute("create table records (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name text NOT NULL, last_name text NOT NULL, email text NOT NULL, pin_code text NOT NULL, timestamp text NOT NULL)")
