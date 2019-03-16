import csv
import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt

'''def insert_default():
	with sql.connect("database.db") as con:
		username="admin@hostel.iiit.ac.in"
		password="admin_pwd"
		phone="1234567890"
		password = sha256_crypt.encrypt(password)
		cur = con.cursor()
		cur.execute("INSERT INTO authenticate (username,password) VALUES (?,?)", (username,password) )
		cur.execute("INSERT INTO admins (username,phone,of_what) VALUES (?,?,?)", (username,phone,"portal") )

		username="admin@hostel.iiit.ac.in"
		password="admin_pwd"
		phone="1234567890"
		password = sha256_crypt.encrypt(password)
		cur = con.cursor()
		cur.execute("INSERT INTO authenticate (username,password) VALUES (?,?)", (username,password) )
		cur.execute("INSERT INTO admins (username,phone,of_what) VALUES (?,?,?)", (username,phone,"portal") )

		username="admin@hostel.iiit.ac.in"
		password="admin_pwd"
		phone="1234567890"
		password = sha256_crypt.encrypt(password)
		cur = con.cursor()
		cur.execute("INSERT INTO authenticate (username,password) VALUES (?,?)", (username,password) )
		cur.execute("INSERT INTO admins (username,phone,of_what) VALUES (?,?,?)", (username,phone,"portal") )

		username="admin@hostel.iiit.ac.in"
		password="admin_pwd"
		phone="1234567890"
		password = sha256_crypt.encrypt(password)
		cur = con.cursor()
		cur.execute("INSERT INTO authenticate (username,password) VALUES (?,?)", (username,password) )
		cur.execute("INSERT INTO admins (username,phone,of_what) VALUES (?,?,?)", (username,phone,"portal") )
		con.commit()

def reader():
	with sql.connect("database.db") as con:
		cur = con.cursor()
		reader = csv.reader(open('authenticate.csv','r'),delimiter=',')
		for row in reader:
			temp = sha256_crypt.encrypt(str(row[1]))
			to_db = [str(row[0]),temp]
			cur.execute("INSERT INTO authenticate (username,password) VALUES (?,?);",to_db)
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
		con.commit()'''

def insert_admin(username,phone,password):
	with sql.connect("database.db") as con:
		password = sha256_crypt.encrypt(password)
		cur = con.cursor()
		cur.execute("INSERT INTO admins (username,phone,password) VALUES (?,?,?)", (username,phone,password) )
		con.commit()

def check(username) :
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery="select username,profile_pic from authenticate where username= '%s'"%username
			cur.execute(sqlQuery)
			row = cur.fetchone()
			if row :
				details={}
				details['username'] = username
				details['profile_pic']=row[1]
				sqlQuery="select of_what,value from admins where username= '%s'"%username
				cursor=con.cursor()
				cursor.execute(sqlQuery)
				row1 = cursor.fetchone()
				if row1 :
					details['admin']=True
					details['of_what']=row1[0]
					details['value']=row1[1]
				else :
					details['admin']=False
				sqlQuery="select roll_no,firstname,lastname,hostel,wing,phone,gaurdian,gaurdian_phone,batch,room_no from students,residents where students.username=residents.username and students.username= '%s'"%username
				cursor=con.cursor()
				cursor.execute(sqlQuery)
				row1 = cursor.fetchone()
				if row1 :
					details['roll_no']=row1[0]
					details['firstname']=row1[1]
					details['lastname']=row1[2]
					details['hostel']=row1[3]
					details['wing']=row1[4]
					details['phone']=row1[5]
					details['gaurdian']=row1[6]
					details['gaurdian_phone']=row1[7]
					details['batch']=row1[8]
					details['room_no']=row1[9]
					details['warden']=False
				else :
					details['warden']=True
					sqlQuery="select name,phone_warden from hostels where warden= '%s'"%username
					cursor=con.cursor()
					cursor.execute(sqlQuery)
					row2 = cursor.fetchone()
					if row2 :
						details['hostel']=row2[0]
						details['phone']=row2[1]
				print(details)
				return details
			else :
				return False
	except Exception as e:
		print(e)
		return False

def fetch_admins():
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			cur.execute("select firstname,lastname,admins.* from admins,students where students.username=admins.username")
			rows = cur.fetchall()
			'''for row in rows:
				print ("row=",row["name"])'''
			return (rows)
	except Exception as e:
		print(e)
		return ([])

def fetch_dues():
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery="select * from dues where "
			if session['warden'] :
				sqlQuery=sqlQuery+"hostel= '%s' "%session['hostel']+";"
			else :
				sqlQuery=sqlQuery+"username= '%s'"%session['username']+";"
			cur.execute(sqlQuery)
			rows = cur.fetchall()
			print (rows)
			return rows
	except Exception as e:
		print(e)
		return ([])

def net_due():
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery="select sum(amount) from dues where "
			sqlQuery=sqlQuery+"username= '%s'"%session['username']+" and paid=0 "+";"
			cur.execute(sqlQuery)
			rows = cur.fetchone()
			print (rows[0])
			if rows[0]:
				return rows[0]
			else:
				return '0'
	except Exception as e:
		print(e)
		return ([])

def check_room(hostel,room_no):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db=[hostel,room_no]
			sqlQuery="select * from residents where hostel='" + str(hostel) + "' and room_no='" + str(room_no) + "';"
			print(sqlQuery)
			cur.execute(sqlQuery)
			rows = cur.fetchone()
			print (rows)
			print("hello")
			if rows:
				return True
			else:
				sqlQuery="update residents set hostel='" + str(hostel)
				sqlQuery=sqlQuery + "' where username='"
				sqlQuery=sqlQuery+str(session['username'])
				sqlQuery=sqlQuery+"';"
				print(sqlQuery)
				cur.execute(sqlQuery)
				sqlQuery="update residents set room_no='" + str(room_no)
				sqlQuery=sqlQuery + "' where username='"
				sqlQuery=sqlQuery+str(session['username'])
				sqlQuery=sqlQuery+"';"
				print(sqlQuery)
				cur.execute(sqlQuery)
				session['hostel']=hostel
				return False
	except Exception as e:
		print(e)
		return (True)

def fetch_hostel(name1):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery = "select name,phone,warden,phone_warden,ratings from hostels where lower(name) = '%s'"%name1
			cur.execute(sqlQuery)
			rows = cur.fetchall()
			'''
			for row in rows:
				print ("row=",row["name"])
			'''
			return (rows)
	except Exception as e:
		print(e)
		return ([])

def insert_in_dues(username,description,amount):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db = [str(username),str(description),str(session['hostel']),str(amount)]
			cur.execute("INSERT INTO dues(username,description,hostel,amount,due_date) VALUES (?,?,?,?,date())", to_db)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def fetch_FAQs():
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery = "select id,question,answer from FAQs;"
			cur.execute(sqlQuery)
			rows = cur.fetchall()
			'''
			for row in rows:
				print ("row=",row["name"])
			'''
			return (rows)
	except Exception as e:
		print(e)
		return ([])

def insert_in_FAQ(question):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db = [str(question)]
			cur.execute("INSERT INTO FAQs(question) VALUES (?)", to_db)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def update_FAQ(qid,answer):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db = [str(answer),str(qid)]
			cur.execute("UPDATE FAQs SET answer=? where id=?", to_db)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def insert_in_posts(title,description,group):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db = [str(session['username']),str(title),str(description),str(group)]
			cur.execute("INSERT INTO posts(username,title,description,groups,post_date) VALUES (?,?,?,?,date())", to_db)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def fetch_post(post_id):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery = "select * from posts where post_id='%s';"%post_id
			cur.execute(sqlQuery)
			rows = cur.fetchone()
			'''
			for row in rows:
				print ("row=",row["name"])
			'''
			return (rows)
	except Exception as e:
		print(e)
		return ([])

def fetch_comments(post_id):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery = "select * from comments where post_id='%s';"%post_id
			cur.execute(sqlQuery)
			rows = cur.fetchall()
			'''
			for row in rows:
				print ("row=",row["name"])
			'''
			return (rows)
	except Exception as e:
		print(e)
		return ([])

def insert_in_comments(post_id,comment):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db = [str(session['username']),str(comment),str(post_id)]
			cur.execute("INSERT INTO comments(username,comment,post_id,comment_date) VALUES (?,?,?,date())", to_db)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def getPosts(groupname):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery=""
			if groupname!="posts for me":
				sqlQuery="Select * from posts where groups='%s'"%groupname
				if (groupname==str(session['hostel']+" warden")) or (groupname==str("admin "+session['hostel'])) or (groupname==str("portal admin")):
					sqlQuery=sqlQuery+" and username='%s'"%session['username']
				else:
					wings=get_wings(session['hostel'])
					for wing in wings :
						if (groupname==str("admin "+wing[0])):
							sqlQuery=sqlQuery+" and username='%s'"%session['username']
			elif (session['admin'] or session['warden']):
				if session['warden']:
					group=session['hostel']+" warden"
					sqlQuery="Select * from posts where groups='%s'"%group
				elif session['admin'] and session['of_what']=="portal":
					group="portal admin"
					sqlQuery="Select * from posts where groups='%s'"%group
				elif session['admin'] and session['of_what']=="hostel":
					group="admin "+session['hostel']
					sqlQuery="Select * from posts where groups='%s'"%group
				elif session['admin'] and session['of_what']=="wing":
					group="admin "+session['wing']
					sqlQuery="Select * from posts where groups='%s'"%group
			sqlQuery=sqlQuery+";"
			print(sqlQuery)
			cur.execute(sqlQuery)
			posts = cur.fetchall()
			print (posts)
			for post in posts:
				print(post)
			return posts
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def get_wings(hostel):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery="SELECT distinct wing from residents where hostel='%s'"%hostel
			print(sqlQuery)
			cur.execute(sqlQuery)
			wings = cur.fetchall()
			print (wings)
			return wings
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def like(post_id):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db=[str(post_id),str(session['username'])]
			'''sqlQuery="SELECT * from likes where post_id='%s'"%due_id
			print(sqlQuery)'''
			cur.execute("SELECT * from likes where post_id=? and username=?",to_db)
			row=cur.fetchone()
			print("dsvgrd")
			print(row)
			if not row :
				cur.execute("INSERT into likes values(?,?)",to_db)
				cur.execute("SELECT * from dislikes where post_id=? and username=?",to_db)
				row1=cur.fetchone()
				print("dsvgrdiuytr")
				print(row1)
				if row1 :
					cur.execute("UPDATE posts set dislikes=dislikes-1 where post_id=?",str(post_id))
				cur.execute("UPDATE posts set likes=likes+1 where post_id=?",str(post_id))
				cur.execute("DELETE from dislikes where post_id=? and username=?",to_db)
			con.commit()
	except Exception as e:
		print("szvdxghj")
		print(e)
		return ([])

def dislike(post_id):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			to_db=[str(post_id),str(session['username'])]
			'''sqlQuery="SELECT * from likes where post_id='%s'"%due_id
			print(sqlQuery)'''
			cur.execute("SELECT * from dislikes where post_id=? and username=?",to_db)
			row=cur.fetchone()
			if not row :
				cur.execute("INSERT into dislikes values(?,?)",to_db)
				cur.execute("SELECT * from likes where post_id=? and username=?",to_db)
				row1=cur.fetchone()
				if row1 :
					cur.execute("UPDATE posts set likes=likes-1 where post_id=?",str(post_id))
				cur.execute("UPDATE posts set dislikes=dislikes+1 where post_id=?",str(post_id))
				cur.execute("DELETE from likes where post_id=? and username=?",to_db)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def due_paid(due_id):
	try:
		with sql.connect("database.db") as con:
			con.row_factory = sql.Row
			cur = con.cursor()
			sqlQuery="UPDATE dues set paid=1 where id='%s'"%due_id
			print(sqlQuery)
			cur.execute(sqlQuery)
			con.commit()
	except Exception as e:
		print(e)
		return ([])

def authenticate(request):
	con = sql.connect("database.db")
	username = request.form['log']
	password = request.form['pwd']
	sqlQuery = "select password,profile_pic from authenticate where username = '%s'"%username
	cursor = con.cursor()
	cursor.execute(sqlQuery)
	row = cursor.fetchone()
	status = False
	if row:
		status = sha256_crypt.verify(password,row[0])
		if status:
			msg = username + "has logged in successfully"
			session['username'] = username
			session['profile_pic']=row[1]
			sqlQuery="select of_what,value from admins where username= '%s'"%username
			cursor=con.cursor()
			cursor.execute(sqlQuery)
			row1 = cursor.fetchone()
			if row1 :
				session['admin']=True
				session['of_what']=row1[0]
				session['value']=row1[1]
			else :
				session['admin']=False
			sqlQuery="select roll_no,firstname,lastname,hostel,wing from students,residents where students.username=residents.username and students.username= '%s'"%username
			cursor=con.cursor()
			cursor.execute(sqlQuery)
			row1 = cursor.fetchone()
			if row1 :
				session['roll_no']=row1[0]
				session['firstname']=row1[1]
				session['lastname']=row1[2]
				session['hostel']=row1[3]
				session['wing']=row1[4]
				session['warden']=False
			else :
				session['warden']=True
				sqlQuery="select name from hostels where warden= '%s'"%username
				cursor=con.cursor()
				cursor.execute(sqlQuery)
				row2 = cursor.fetchone()
				if row2 :
					session['hostel']=row2[0]
			print(session)
		else:
			msg = username + "login failed"

	return status					


