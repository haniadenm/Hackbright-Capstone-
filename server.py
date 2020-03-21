from jinja2 import StrictUndefined
import os
from PIL import Image
from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import LoginManager, login_user, login_user, logout_user, login_required, current_user
#from flask_security import current_user, user_loader
#from flask.ext.login import current_user
from flask import Flask, render_template, request, redirect, flash, session, url_for, Markup, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Parent, Child, Activity
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os


from werkzeug.security import generate_password_hash, check_password_hash

""" return this file (server.py) into webapplication """
app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

auth = Blueprint('auth', __name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "Abc123"
#db.app = app
#db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(parent_id):
	return Parent.query.get(int(parent_id))


def load_user(parent_id):
    return Parent.get(parent_id)

@app.route('/')
def index():
    return render_template('index.html')
##################################################################

'''Login'''

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    check_parent = Parent.query.filter_by(username = username).first()

    if check_parent.password == password:
    	login_user(check_parent)
    	return redirect(f"/profile/{check_parent.parent_id}")
    else:
    	flash("Incorrect username and/or password. Please try again.")
    	return redirect("/login")


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
	if request.method == "POST":
		parent = request.form.get('parent')
		zipcode = request.form.get('zipcode')
		username = request.form.get('username')
		password = request.form.get('password')
		new_parent = Parent(parent=parent, zipcode=zipcode, username=username, password=password)
		db.session.add(new_parent)
		db.session.commit()

		parent_id = new_parent.parent_id
		session["parent_id"] = parent_id

		flash("New parent profile created!")
		return redirect(f"/profile/{parent_id}")
	else:
		return redirect(f"/")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/index')

#################################################################

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
def parentprofile(parent_id):
	"""This is the parent's homepage."""
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		db.session.commit()
		flash('Your profile has been updated!', 'success')
		return redirect(url_for('profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('profile.html', title='Profile',
                           image_file=image_file, form=form)

@app.route('/parents')
def show_parents():
    """List the parents"""

    return redirect('/profile')


'''def parentprofile(parent_id):
	"""This is the parent's homepage."""

	parent = Parent.query.filter_by(parent_id=parent_id).first()
	child = Child.query.filter_by(parent_id=parent_id).all()

	return render_template('profile.html',
						   parent=parent,
						   child=child)'''

'''@app.route('/profile/<int:parent_id>')
def parentprofile(parent_id):
	"""This is the parent's homepage."""

	intent = request.args.get("intentchoice")
	
	if intent == "1":
		parnetlist = Parent.query.filter(Parent.parent_id).all()
		parent_names = []
		for parent in parentlist:
			parent_names.append(parent.parent_name)
			return render_template("parentlist.html", parent_names=parent_name, zipcode=zipcode	)
		
	elif intent == "2":
		childrenlist = Child.query.filter(Child.child_name).all()
		children_names = []

		for item in childrenlist:
			children_names.append(child.child_name)
			children_list = Child.query.filter(Child.child_name == 2).all()
			return render_template("childrenlist.html", child_name=child_name, age=age, zipcode=zipcode)'''


'''@app.route('/intent')
def choose_intent():
    """Have parents choose a path."""

    meet_parent = request.args.get("meetparents")
    connect_child = request.args.get("connectchild")

    if intent == "1":
        all_parents = Parent.query.filter(Parent.parent_name).all()

        parent_names = []

        for parent in all_parents:
            parent_names.append(parent.parent_name)

        return render_template("parentlist.html", parent_names=parent_name, zipcode=zipcode	)

    elif intent == "2":
        
        all_children = Child.query.filter(Child.child_name.any(child_id)).all()
        children_names = []
        for item in all_children:
            children_names.append(child.child_name)

        children_list = Child.query.filter(Child.child_name == 2).all()
        return render_template("children_detail.html", child_name=child_name, age=age, zipcode=zipcode)'''


'''@app.route("/parents/<int:parent_id>")
def parents_detail(parent_id):
    # username = Parent.username
    parent = Parent.query.filter_by(parent_id=parent_id).first()
    return render_template('parent.html', parent=parent)'''




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    #add any configs HERE 
    # ensure templates, etc. are not cached in debug mode
    #app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    #app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')


