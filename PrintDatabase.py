from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class Print(db.Model):
    __tablename__ = 'print'
    printId = db.Column(db.String, primary_key=True)
    owner = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)  # Consider using db.DateTime for actual datetime objects
    gcode_name = db.Column(db.String, nullable=False)
    events = db.relationship('PrintEvent', backref='print', lazy=True)

class PrintEvent(db.Model):
    __tablename__ = 'print_events'
    eventId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    printId = db.Column(db.String, db.ForeignKey('print.printId'), nullable=False)
    event_name = db.Column(db.String, nullable=False)
    picture = db.Column(db.String)
    time = db.Column(db.String, nullable=False)  # Consider using db.DateTime

class PrintDatabase:
    def __init__(self, app):
        with app.app_context():
            db.init_app(app)
            db.create_all()
            self.purge_old_entries()
            print("DB Initialized")


    def insert_print(self, gcode_name, owner=""):
        time_started = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        printId = f"{gcode_name}_{time_started}"
        new_print = Print(printId=printId, owner=owner, time=time_started, gcode_name=gcode_name)
        db.session.add(new_print)
        db.session.commit()
        return printId

    def insert_print_event(self, gcode_name, event_name, picture, time=None):
        if time is None:
            time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        
        print_record = Print.query.filter_by(gcode_name=gcode_name).order_by(Print.time.desc()).first()
        if print_record:
            new_event = PrintEvent(printId=print_record.printId, event_name=event_name, picture=picture, time=time)
            db.session.add(new_event)
            db.session.commit()
        else:
            print("No print found for the given gcode_name.")

        return print_record.printId

    def change_owner(self, printId, new_owner):
        print_record = Print.query.filter_by(printId=printId).first()
        if print_record:
            print_record.owner = new_owner
            db.session.commit()

    def get_print(self, printId):
        print_record = Print.query.filter_by(printId=printId).first()
        if print_record:
            data = {
                'printId': print_record.printId,
                'owner': print_record.owner,
                'print_time': print_record.time,
                'gcode_name': print_record.gcode_name
            }
            return data
        else:
            return {}

    def get_print_with_latest_event(self, printId):
        print_record = Print.query.filter_by(printId=printId).first()
        if print_record and print_record.events:
            latest_event = max(print_record.events, key=lambda x: x.time)
            data = {
                'printId': print_record.printId,
                'owner': print_record.owner,
                'print_time': print_record.time,
                'gcode_name': print_record.gcode_name,
                'event_name': latest_event.event_name,
                'picture': latest_event.picture,
                'event_time': latest_event.time
            }
            return data
        else:
            return {}

    def get_prints_with_latest_events(self, limit=10):
        # This operation is more complex with ORM and might require raw SQL or advanced ORM operations
        # for efficiency. Here's a simplified approach:
        prints = Print.query.order_by(Print.time.desc()).limit(limit).all()
        # This does not fetch the latest event per print efficiently; consider custom SQL for production use.
        results = []
        for print_record in prints:
            if print_record.events:
                latest_event = max(print_record.events, key=lambda x: x.time)
                data = {
                    'printId': print_record.printId,
                    'owner': print_record.owner,
                    'print_time': print_record.time,
                    'gcode_name': print_record.gcode_name,
                    'event_name': latest_event.event_name,
                    'picture': latest_event.picture,
                    'event_time': latest_event.time
                }
                results.append(data)
        return results

    def purge_old_entries(self):
        one_month_ago = datetime.now() - timedelta(days=30)
        one_month_ago_str = one_month_ago.strftime("%Y-%m%d %H:%M:%S")

        # Purge old print events
        PrintEvent.query.filter(PrintEvent.time < one_month_ago_str).delete()
        # Purge old prints
        Print.query.filter(Print.time < one_month_ago_str).delete()
        db.session.commit()