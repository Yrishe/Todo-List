from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from flask import send_from_directory
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

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

#Route to get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.order_by(Todo.id).all()
    return jsonify([todo.to_dict() for todo in todos]), 200

    # Read query parameters
    # sort = request.args.get('sort', 'id')
    # order = request.args.get('order', 'asc')
    # page = request.args.get('page', 1, type=int)
    # per_page = request.args.get('per_page', 5, type=int)
    
    # # Build base query
    # query = Todo.query
    
    # # Apply sorting
    # if sort in ['id', 'task', 'done']:
    #     column = getattr(Todo, sort)
    #     if order == 'desc':
    #         column = column.desc()
    #     query = query.order_by(column)
        
    # # Paginate
    # todos = query.paginate(page, per_page, error_out=False)
    
    # return jsonify({
    #     'page': page,
    #     'per_page': per_page,
    #     'total': todos.total,
    #     'pages': todos.pages,
    #     'todos': [todo.to_dict() for todo in todos.items]
    # }), 200

#Route to create a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    
    # Validate input
    if not data or 'task' not in data or not data['task'].strip():
        return jsonify({'error': 'Task is required'}), 400
    #    abort(400)
    
    if len(data['task'].strip()) > 200:
        return jsonify({'error': 'Task must be 200 characters or less'}), 400
    
    due_date = None
    if 'due_date' in data:
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format, use ISO format'}), 400
    
    todo = Todo(
        task=data['task'].strip(), 
        done=False,
        due_date=due_date,
        tags=data.get('tags'),
        priority=int(data.get('priority', 2))
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify(todo.to_dict()), 201

# Route to update a todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    if 'task' in data and data['task'].strip():
        todo.task = data['task'].strip()
    if 'done' in data:
        todo.done = bool(data['done'])
        
    if 'due_date' in data:
        if data['due_date']:
            try:
                todo.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format, use ISO format'}), 400
        else:
            todo.due_date = None
    
    if 'tags' in data:
        todo.tags = data['tags']
    
    if 'priority' in data:
        todo.priority = int(data['priority'])

    db.session.commit()
    return jsonify(todo.to_dict()), 200

# Route to delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200

def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')


# Create the database and tables
with app.app_context():
    db.create_all()
    

if __name__ == '__main__':
    app.run(debug=True)
    
    
