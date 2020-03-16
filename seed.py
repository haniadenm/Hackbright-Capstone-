from sqlalchemy import func
from model import Parent
# from model import Child
# from model import Activities

from model import connect_to_db, db
from server import app


def load_parents():
    """Load parents from p.user into database."""

    print("parents")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate parents
    Parent.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/p.user"):
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


#def load_children():
    """Load chidlren from c.user into database."""

   # print("Child")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate children
   # Parent.query.delete()

    # Read u.user file and insert data
    #for row in open("seed_data/c.user"):
        #row = row.rstrip()
        #childs_id, childs_name, childs_age, zipcode, password = row.split("|")

       # parent = Parent(parent_id=parent_id,
                   # parent=parent,
                   # zip=zip)

        # We need to add to the session or it won't ever be stored
        '''db.session.add(parent)

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit() '''


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_parents()
    #load_movies()
    #load_ratings()
    #set_val_user_id() 