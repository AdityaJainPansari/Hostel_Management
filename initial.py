import csv
import sqlite3 as sql
from passlib.hash import sha256_crypt

with sql.connect("database.db") as con:
	cur = con.cursor()
	reader = csv.reader(open('authenticate.csv','r'),delimiter=',')
	for row in reader:
		temp = sha256_crypt.encrypt(str(row[1]))
		to_db = [str(row[0]),temp,str(row[2])]
		cur.execute("INSERT INTO authenticate (username,password,profile_pic) VALUES (?,?,?);",to_db)
	con.commit()
	reader = csv.reader(open('admin.csv','r'),delimiter=',')
	for row in reader:
		to_db = [str(row[0]),str(row[1]),str(row[2]),str(row[3])]
		cur.execute("INSERT INTO admins VALUES (?,?,?,?)", to_db)
	con.commit()
	reader = csv.reader(open('students.csv','r'),delimiter=',')
	for row in reader:
		to_db = [str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7])]
		cur.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?)", to_db)
	con.commit()
	reader = csv.reader(open('hostels.csv','r'),delimiter=',')
	for row in reader:
		to_db = [str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4])]
		cur.execute("INSERT INTO hostels (name,phone,warden,phone_warden,ratings) VALUES (?,?,?,?,?)", to_db)
	con.commit()
	reader = csv.reader(open('residents.csv','r'),delimiter=',')
	for row in reader:
		to_db = [str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4])]
		cur.execute("INSERT INTO residents VALUES (?,?,?,?,?)", to_db)
	con.commit()
	reader = csv.reader(open('FAQ.csv','r'),delimiter=',')
	for row in reader:
		to_db = [str(row[0]),str(row[1])]
		cur.execute("INSERT INTO FAQs(question,answer) VALUES (?,?)", to_db)
	con.commit()