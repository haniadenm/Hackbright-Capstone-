from sqlalchemy import func
from model import Parent, Child, Activity, Parentchild, Parentactivity, Childactivity



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
                    zipcode=zipcode)

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
        activity_id, activity_name, for_parents, for_children = row.split("|")

        for_parents = bool(for_parents)
        for_children = bool(for_children)

        activity = Activity(activity_id=activity_id,
                    activity_name=activity_name,
                    for_parents=for_parents,
                    for_children=for_children)

        # We need to add to the session or it won't ever be stored
        db.session.add(activity)

    # Once we're done, we should commit our work
    db.session.commit()


def parent_child():
    """Load chidlren from c.user into database."""

    print("parent_child")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate children


    # Read u.user file and insert data
    for row in open("data/parentschildren"):
        row = row.rstrip()
        parent_id, childs_id = row.split("|")

        pc = Parentchild(parent_id=parent_id,
                         childs_id=childs_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(pc)

    # Once we're done, we should commit our work
    db.session.commit()
def set_val_parent_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Parent.parent_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('parents_parent_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def childs_activity():
    """Load chidlren from c.user into database."""

    print("child_activity")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate children


    # Read u.user file and insert data
    for row in open("data/childrensactivity"):
        row = row.rstrip()
        activity_id,childs_id = row.split("|")

        ca = Childactivity(childs_id=childs_id,
                         activity_id=activity_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(ca)

    # Once we're done, we should commit our work
    db.session.commit()

def set_val_child_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Child.child_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('children_child_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def parent_activity():
    """Load chidlren from c.user into database."""

    print("parent_activity")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate children


    # Read u.user file and insert data
    for row in open("data/activityparent"):
        row = row.rstrip()
        activity_id,parent_id = row.split("|")

        pa = Parentactivity(parent_id=parent_id,
                         activity_id=activity_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(pa)

    # Once we're done, we should commit our work
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
   
    # In case tables haven't been created, create them
    #Parentactivity.query.delete()
    #Childactivity.query.delete()
    #Parentchild.query.delete()
    #Activity.query.delete()
    #Child.query.delete()
    #Parent.query.delete()
    #db.drop_all()

    db.create_all()
        # we won't be trying to add duplicate children

    # Import different types of data
    load_parents()
    load_children()
    load_activities()
    parent_child()
    parent_activity()
    childs_activity()
    #set_val_user_id() 