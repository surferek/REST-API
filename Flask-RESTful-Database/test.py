import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

user = (1, "Piotr", "psswd")
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query,user)


users = [
    (2, "Jan", "psswd3ff"),
    (3, "Tomek", "psswd444"),
    (4, "Rafał", "psswd333"),
    (5, "Gaja", "psswd123")

]
cursor.executemany(insert_query,users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()