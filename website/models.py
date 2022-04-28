from . import db
from flask_login import UserMixin

#----001----User Table
class User(db.Model, UserMixin) :
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # User can have many Tickets
    tickets = db.relationship('Ticket', backref='ticket')


#----002----Train Table
class Train(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    route = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    main_stops = db.Column(db.String(150), nullable=False)

    # Train can have many Tickets
    tickets = db.relationship('Ticket', backref='train')

    # Train can have many Stations
    stations = db.relationship('Station', backref='station')



#----003----Ticket Table
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_name = db.Column(db.String(50), nullable=False)
    # Foreign Key to link User table ( refer to the primary of the user )
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

    mobile = db.Column(db.Integer, nullable=False)

    train_name = db.Column(db.String(50), nullable=False)
    # Foreign Key to link Train table ( refer to the primary of the train )
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'))

    location_s = db.Column(db.String(50), nullable=False)
    location_d = db.Column(db.String(50), nullable=False)
    train_class = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date(), nullable=False)


#----004----Staion Table
class Station(db.Model):
    platform_id = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    # Foreign Key to link Train table ( refer to the primary of the train )
    train_id = db.Column(db.String(150), db.ForeignKey('train.id'))

    arrival = db.Column(db.String(10) )
    depart = db.Column(db.String(10) )


#----005----Feedback Table
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

