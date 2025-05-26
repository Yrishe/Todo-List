import pytest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import db, Todo


@pytest.fixture
def client():
    create_app.config['TESTING'] = True
    create_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with create_app.test_client() as client:
        with create_app.app_context():
            db.create_all()
        yield client
        
def create_todo(client):
    response = client.post('/todos', json={'task': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['task'] == 'Test Task'
    return data['done'] is False

def test_get_todos(client):
    # Pre-populate
    client.post('/todos', json={'task': 'Test Task 1'})
    client.post('/todos', json={'task': 'Test Task 2'})
    response = client.get('/todos')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 7
    
def test_update_todo(client):
    post = client.post('/todos', json={'task': 'Old task'})
    todo_id = post.get_json()['id']
    response = client.put(f'/todos/{todo_id}', json={'task': 'Updated task', 'done': True})
    assert response.status_code == 200
    data = response.get_json()
    assert data['task'] == 'Updated task'
    assert data['done'] is True
    
def test_delete_todo(client):
    post = client.post('/todos', json={'task': 'Task to delete'})
    todo_id = post.get_json()['id']
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Todo deleted successfully'
    
