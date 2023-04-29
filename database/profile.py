import csv
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="flavourfinder"
)

mycursor = mydb.cursor()

with open('profiles.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        username = row[0]
        password = username[::-1]
        email = username + "@gmail.com"
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE password=%s, email=%s"
        val = (username, password, email, password, email)
        mycursor.execute(sql, val)
        mydb.commit()
