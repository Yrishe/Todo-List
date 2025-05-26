from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import db, Todo

bp = Blueprint('todos', __name__)

#Route to get all todos
@bp.route('/todos', methods=['GET'])
def get_todos():
    # Get pagination parameters from the request
    page  = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    status = request.args.get('status', 'all')
    
    query = Todo.query.order_by(Todo.id.desc())
    
    # Filter todos based on status
    if status == 'done':
        query = query.filter_by(done=True)
    elif status == 'undone':
        query = query.filter_by(done=False)
    
    # Query the database for todos with pagination
    pagination = Todo.query.order_by(Todo.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    return jsonify({
        'todos': [todo.to_dict() for todo in pagination.items],
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200


#Route to create a new todo
@bp.route('/todos', methods=['POST'])
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
@bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    todo = db.session.get(Todo, todo_id)
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
@bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200