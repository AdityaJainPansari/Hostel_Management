from flask import *
from functools import wraps
from data1 import *

app = Flask(__name__)
logged_in=False
app.secret_key = 'MKhJHJH798798ksdkjhkjGHh'

@app.route("/",methods=["GET","POST"])
def index():
	if logged_in:
		return render_template("project.html",cls_type="home page",logged_in=logged_in,det=session,title="IIIT-H Hostel Portal | The official portal related to IIIT-H hostels. An initiative of the students, for the students, by the students!")
	else :
		return render_template("project.html",cls_type="home page",logged_in=logged_in,title="IIIT-H Hostel Portal | The official portal related to IIIT-H hostels. An initiative of the students, for the students, by the students!")

@app.route("/user/<username>",methods=["GET","POST"])
def user(username):
	global logged_in
	if username is not None :
		details=check(username)
		if details :
			if logged_in:
				'''if username==session['username']:
					return render_template("dashboard.html",logged_in=logged_in,det=session)
				else:'''
				return render_template("user_details.html",logged_in=logged_in,det=session,row=details)
			else:
				return render_template("user_details.html",logged_in=logged_in,row=details)
		else :
			message="Page not found!"
			if logged_in :
				return render_template("error.html",message=message,logged_in=logged_in,det=session)
			else :
				return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/FAQs",methods=["GET","POST"])
def FAQs():
	global logged_in
	rows=fetch_FAQs()
	if logged_in :
		return render_template("FAQ.html",FAQs=rows,cls_type="page page-id-2 page-template page-template-default",logged_in=logged_in,det=session,title="FAQs | IIIT-H Hostel Portal")
	else :
		return render_template("FAQ.html",FAQs=rows,cls_type="page page-id-2 page-template page-template-default",logged_in=logged_in,title="FAQs | IIIT-H Hostel Portal")

@app.route("/answer_FAQs",methods=["GET","POST"])
def answer_FAQs():
	global logged_in
	rows=fetch_FAQs()
	if logged_in and session['admin'] and session['of_what']=="portal":
		return render_template("answer_FAQ.html",rows=rows,logged_in=logged_in,det=session,title="Update Answers to FAQs")
	else :
		message="Access Denied!"
		if logged_in :
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else :
			return render_template("error.html",message=message,logged_in=logged_in)

@app.route('/login',methods=['POST','GET'])
def login():
	global logged_in
	session.clear()
	if request.method == 'GET':
		return render_template("login.html")
	if request.method == 'POST':
		next = request.values.get('next')
		if(authenticate(request)==False):
			return render_template("login.html",cls_type="home page",logged_in=logged_in,title="IIIT-H Hostel Portal | The official portal related to IIIT-H hostels. An initiative of the students, for the students, by the students!")
		if(authenticate(request)==True):
			logged_in=True
			if not next:
				return render_template("project.html",cls_type="home page",logged_in=logged_in,title="IIIT-H Hostel Portal | The official portal related to IIIT-H hostels. An initiative of the students, for the students, by the students!",det=session)
			else:
				return redirect(next,logged_in=logged_in,det=session)

@app.route('/logout',methods=['POST','GET'])
def logout():
	global logged_in
	logged_in=False
	session.clear()
	print(session)
	return render_template("project.html",cls_type="home page",logged_in=logged_in,title="IIIT-H Hostel Portal | The official portal related to IIIT-H hostels. An initiative of the students, for the students, by the students!")

@app.route("/rules",methods=["GET","POST"])
def hostel_rules():
	if logged_in :
	    return render_template('rules.html',logged_in=logged_in,det=session)
	else :
	    return render_template('rules.html',logged_in=logged_in)

@app.route("/admin_list",methods=["GET","POST"])
def show_admins():
	rows=fetch_admins()
	if logged_in :
		return render_template("admin_list.html",rows=rows,logged_in=logged_in,det=session)
	else :
		return render_template("admin_list.html",rows=rows,logged_in=logged_in)

@app.route("/charges",methods=["GET","POST"])
def charges():
	if logged_in and session['warden']:
		return render_template("charges.html",logged_in=logged_in,det=session)
	else :
		message="Access Denied!"
		if logged_in :
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else :
			return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/dues",methods=["GET","POST"])
def dues():
	if logged_in :
		rows=fetch_dues()
		if session['warden'] :
			return render_template("dues.html",rows=rows,logged_in=logged_in,det=session)
		else :
			net_amount=net_due()
			print (net_amount)
			return render_template("dues.html",rows=rows,net_amount=net_amount,logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/add_charge",methods=["GET","POST"])
def add_charge():
	if logged_in and session['warden'] :
		guilty=request.form.get('username')
		description=request.form.get('description')
		amount=request.form.get('amount')
		insert_in_dues(guilty,description,amount)
		return redirect("/charges")
	else :
		message="Access Denied!"
		if logged_in :
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else :
			return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/change_room",methods=["GET","POST"])
def change_room():
	if logged_in and not session['warden']:
		net_amount=net_due()
		if str(net_amount)!=str(0):
			message="First pay the net due amount of rupees '%s'"%net_amount
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else:
			return render_template("change_room.html",logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/room_submit",methods=["GET","POST"])
def room_submit():
	if logged_in and not session['warden']:
		net_amount=net_due()
		if str(net_amount)!=str(0):
			message="First pay the net due amount of rupees '%s'"%net_amount
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else:
			hostel=request.form.get("hostel")
			room=request.form.get("room")
			status=check_room(hostel,room)
			if status:
				message="Sorry this room is already occupied !"
				return render_template("message.html",message=message,logged_in=logged_in,det=session)
			else:
				return render_template("message.html",message="room has been alloted",logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/set_paid",methods=["GET","POST"])
def set_paid():
	if logged_in and session['warden'] :
		due_paid(request.form.get('id'))
		return redirect("/dues")
	else :
		message="Access Denied!"
		if logged_in :
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else :
			return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/feed",methods=["GET","POST"])
def feed():
	if logged_in:
		groups=[]
		if (session['admin'] or session['warden']):
			groups.append("posts for me")
		groups.append(session['hostel'])
		if not session['warden']:
			groups.append(session['wing'])
			groups.append(session['hostel']+" warden")
		else:
			groups.append("admin "+session['hostel'])
			wings=get_wings(session['hostel'])
			for wing in wings :
				groups.append("admin "+wing[0])
		if not (session['admin'] and session['of_what']=="portal"):
			groups.append("portal admin")
		return render_template("feed.html",groups=groups,logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/posts/<groupname>",methods=["GET","POST"])
def posts(groupname):
	if logged_in and groupname is not None:
		posts=getPosts(groupname)
		return render_template("posts.html",posts=posts,groupname=groupname,logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/add_comment/<post_id>",methods=["GET","POST"])
def add_comment(post_id):
	if logged_in:
		comment=request.form.get("comment")
		insert_in_comments(post_id,comment)
		return redirect("/post/"+post_id)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/post/<post_id>",methods=["GET","POST"])
def show_comments(post_id):
	if logged_in:
		post=fetch_post(post_id)
		comments=fetch_comments(post_id)
		return render_template("post.html",post=post,comments=comments,logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/like/<post_id>",methods=["GET","POST"])
@app.route("/like/<post_id>/<groupname>",methods=["GET","POST"])
def like_in(post_id,groupname=None):
	if logged_in:
		like(post_id)
		if not groupname:
			return redirect("/post/"+post_id)
		else:
			return redirect("/posts/"+groupname)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/dislike/<post_id>",methods=["GET","POST"])
@app.route("/dislike/<post_id>/<groupname>",methods=["GET","POST"])
def dislike_in(post_id,groupname=None):
	if logged_in:
		dislike(post_id)
		if not groupname:
			return redirect("/post/"+post_id)
		else:
			return redirect("/posts/"+groupname)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/add_FAQ",methods=["GET","POST"])
def add_FAQ():
	question=request.form.get('question')
	insert_in_FAQ(question)
	return redirect("/FAQs")

@app.route("/update_FAQ",methods=["GET","POST"])
def update_answer_FAQs():
	if logged_in and session['admin'] and session['of_what']=="portal":
		qid=request.form.get('id')
		answer=request.form.get('answer')
		update_FAQ(qid,answer)
		return redirect("/answer_FAQs")
	else :
		message="Access Denied!"
		if logged_in :
			return render_template("error.html",message=message,logged_in=logged_in,det=session)
		else :
			return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/add_post",methods=["GET","POST"])
def add_post():
	if logged_in :
		if not session['warden'] :
			return render_template("add_status.html",logged_in=logged_in,det=session)
		else :
			wings=get_wings(session['hostel'])
			return render_template("add_status.html",wings=wings,logged_in=logged_in,det=session)
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/add_status",methods=["GET","POST"])
def add_status():
	if logged_in :
		title=request.form.get('title')
		description=request.form.get('description')
		group=request.form.get('group')
		insert_in_posts(title,description,group)
		return redirect("/feed")
	else :
		message="Access Denied! Please Log In."
		return render_template("error.html",message=message,logged_in=logged_in)

@app.route("/hostel/<name>",methods=["GET","POST"])
def hostel_details(name):
	if name :
		row=fetch_hostel(name)
		if row :
			if logged_in :
				return render_template("hostel_details.html",row=row,logged_in=logged_in,det=session)
			else :
				return render_template("hostel_details.html",row=row,logged_in=logged_in)
		else :
			message="Page not found!"
			if logged_in :
				return render_template("error.html",message=message,logged_in=logged_in,det=session)
			else :
				return render_template("error.html",message=message,logged_in=logged_in)
	else :
		return redirect(url_for('index',username=None))
'''
@app.route("/alerts",methods=["GET","POST"])


@app.route("/reviews",methods=["GET","POST"])
'''
app.run(debug=True)