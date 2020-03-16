from flask import Flask
from flask_security import UserMixin
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, ForeignKey, Integer, Unicode
""" Model and database functions for Capstone project"""



# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
SQLALCHEMY_DATABASE_URI = 'postgresql:///capstone'
db = SQLAlchemy()

# Model definitions

class Parent(db.Model, UserMixin):
    """Parent dashboard."""

    __tablename__ = "parents"

    #Below I am defining columns and relationships of Parents
    #changed from parent name to parent 

    parent_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    parent = db.Column(db.String(25), nullable=False, unique=False)
    zipcode = db.Column(db.Integer, nullable=False, unique=False)

    username = db.Column(db.String(25), nullable=False, unique=False)
    password = db.Column(db.String(25), nullable=False, unique=True)
    
    #activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), unique=False)

    #activities = db.relationship('Activity', backref= parents)


    def __repr__(self):
        """ returns a human-readable representation of a parent."""
        """ DO I NEED TO PUT activity_id in  return? since its """
        return f'<Parent parent_id={self.parent_id} parent={self.parent} username={self.username} zipcode={self.zipcode}>'


class Child(db.Model, UserMixin):
    """Data model for Child, belonging to Parents dashboard."""

    __tablename__ = "children"

    #Below I am defining columns and relationships of Child


    childs_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    childs_name = db.Column(db.String, nullable=False, unique=False)
    childs_age = db.Column(db.Integer, nullable=False, unique=False)
    zipcode = db.Column(db.Integer, nullable=False, unique=False)

    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), unique=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.parent_id'), unique= True)

    #parents = db.relationship('Parent', backref='children')
    #activities = db.relationship('Activity', backref= 'children')

    def __repr__(self):
        """ returns a human-readable representation of a Child."""
        return f'<Child childs_id={self.childs_id} childs_name={self.childs_name} childs_age={self.childs_age}>'

class Activity(db.Model, UserMixin):
    """Activity of dashboard."""

    __tablename__ = 'activities'

    #Below I am defining columns and relationships of Activities

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_name = db.Column(db.String, nullable=False, unique=False)
    for_parents = db.Column(db.Boolean, default=False)
    for_children = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """ returns a human-readable representation of a Activity"""
        return f'<Activity activity_id={self.activity_id} activity_name={self.activity_name}>'

        ##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""
#'postgresql:///capstone'
    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
