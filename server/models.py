from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

event_user_association_table = db.Table('event_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)

class Event(db.Model, SerializerMixin):
    event_id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    poster = db.Column(db.String(255))
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'event_id': self.event_id,
            'organizer_id': self.organizer_id,
            'poster': self.poster,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'location': self.location,
            'description': self.description,
            'capacity': self.capacity
        }

    # Define a many-to-many relationship with the User model through EventAttendee
    attendees = db.relationship('User', secondary=event_user_association_table, back_populates='events_attended', lazy=True)

    # Define a one-to-many relationship with the EventNotification model
    notifications = db.relationship('EventNotification', backref='event', lazy=True)

class User(db.Model, SerializerMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email
        }

    # Define a one-to-many relationship with the Event model 
    events = db.relationship('Event', backref='organizer', lazy=True)

    # Define a many-to-many relationship with the Event model through EventAttendee 
    events_attended = db.relationship('Event', secondary=event_user_association_table, back_populates='attendees', lazy=True)

class EventNotification(db.Model, SerializerMixin):
    notification_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'notification_id': self.notification_id,
            'event_id': self.event_id,
            'message': self.message
        }
