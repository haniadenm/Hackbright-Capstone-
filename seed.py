from sqlalchemy import func
from model import Parent
from model import Child
from model import Activity

from model import connect_to_db, db
from server import app


def load_parents():
    """Load parents from p.user into database."""

    print("parents")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate parents


    # Read u.user file and insert data
    for row in open("data/p.user"):
        row = row.rstrip()
        parent_id, parent, zipcode, username, password  = row.split("|")

        parent = Parent(parent_id=parent_id,
                    parent=parent,
                    zipcode=zipcode,
                    username=username,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(parent)

    # Once we're done, we should commit our work
    db.session.commit()


def load_children():
    """Load chidlren from c.user into database."""

    print("Children")

    # Delete all rows in table, so if we need to run this a second time,


    # Read u.user file and insert data
    for row in open("data/c.user"):
        row = row.rstrip()
        childs_id, childs_name, childs_age, zipcode,parent_id= row.split("|")

        child = Child(childs_id=childs_id,
                    childs_name=childs_name,
                    childs_age=childs_age,
                    zipcode=zipcode,
                    parent_id=parent_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(child)

    # Once we're done, we should commit our work
    db.session.commit()

def load_activities():
    """Load chidlren from c.user into database."""

    print("activities")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate children


    # Read u.user file and insert data
    for row in open("data/a.user"):
        row = row.rstrip()
        activity_id, activity_name, for_parents, for_children, parent_id, childs_id = row.split("|")

        for_parents = bool(for_parents)
        for_children = bool(for_children)

        activity = Activity(activity_id=activity_id,
                    activity_name=activity_name,
                    for_parents=for_parents,
                    for_children=for_children,
                    parent_id=parent_id,
                    childs_id=childs_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(activity)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    # In case tables haven't been created, create them
    Activity.query.delete()
    Child.query.delete()
    Parent.query.delete()
        # we won't be trying to add duplicate children

    # Import different types of data
    load_parents()
    load_children()
    load_activities()
    #set_val_user_id() 