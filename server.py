from jinja2 import StrictUndefined
import os
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

################################################################################
#route for homepage 

@app.route('/')
def index():
    """Show the homepage"""

    if 'username' in session:

        username = session['username']
        parent = Parent.query.filter_by(username=username).first_or_404()

        activities = Activity.query.all()

        children = Child.query.all()

        parents = Parent.query.all()

        return render_template("profile.html", parent=parent,activities = activities, children=children, 
        parents=parents, username=username)

    else:
        return render_template("index.html")
    return render_template('base.html')

################################################################################
#Login

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

################################################################################

#Signup 

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

################################################################################
#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/')


################################################################################
#parent profile page 

@app.route('/profile/<int:parent_id>')
def parentprofile(parent_id):
    """This is the parent's homepage."""
    
    parent = Parent.query.get(parent_id)
    for activity in parent.activities:
        activity.matches = Activity.query.get(activity.activity_id).parents



    #children = Child.query.filter(Child.parents.parent_id==parent_id).all()
    #activities = Activity.query.filter(Activity.parents.parent_id==parent_id).all()

    return render_template("profile.html",
                           #children=children,
                           #activities=activities,
                           parent=parent)


@app.route('/parentlist')
def show_parents():
    """List the parents"""
    parents = Parent.query.all()
    return render_template('parentlist.html', parents=parents)



################################################################################
#parentactivities 
@app.route('/parentsactivity')
def show_parentactivities():
    """List the activities"""
    activities = Activity.query.filter(Activity.for_parents).all()
    return render_template('activitylist.html', activities=activities)

#childs activity
@app.route('/childsactivity')
def show_childactivities():
    """List the activities"""
    activities = Activity.query.filter(Activity.for_children).all()
    return render_template('activitylist.html', activities=activities)

################################################################################
#childrens homepage 

@app.route('/children/<int:childs_id>')
def childprofile(childs_id):
    """This is the parent's homepage."""
     
    child = Child.query.get(childs_id)
    matches = Child.query.filter(Child.childs_age==child.childs_age).all()
    parent_id = session["parent_id"]

    #for childs_age in child.children:
        #activity.matches = Activity.query.get(activity.activity_id).children
    return render_template("childsprofile.html",
                           child=child,
                           matches=matches,
                           parent_id=parent_id)

@app.route('/childrenlist')
def show_children():
    """List the children"""
    children = Child.query.all()

    return render_template('childrenlist.html', children=children)

################################################################################
#add child

@app.route('/addchild', methods=['POST'])
def add_child():
 if request.method == "POST":
        childs_name = request.form.get('childs_name')
        childs_age = request.form.get('childs_age')
        zipcode = request.form.get('zipcode')
        #parent_id = Child.query.filter_by(parents.parent_id==parent_id).first()
        
        new_child = Child(childs_name=childs_name, childs_age=childs_age, zipcode=zipcode)
        db.session.add(new_child)
        db.session.commit()

        childs_id = new_child.childs_id
        session["childs_id"] = childs_id

        return redirect(f'/children/{new_child.childs_id}')

#todo
#set up each activity page (coffee shop, etc )
 

################################################################################

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


