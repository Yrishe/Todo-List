from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    
    due_date = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.Integer, default=2)
    
    # Method to convert the Todo object to a dictionary, helps in JSON serialization
    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'done': self.done,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags,
            'priority': self.priority
        }