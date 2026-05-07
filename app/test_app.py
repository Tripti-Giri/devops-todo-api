import pytest
import sys
import os

# This tells Python where to find app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, todos, next_id


# ── Test Setup ───────────────────────────────────────
# pytest.fixture means this runs before EVERY test
# It gives us a fresh test client to make fake HTTP requests
# It also clears todos before each test so tests don't affect each other
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Clear todos before each test — fresh slate
    todos.clear()
    with app.test_client() as client:
        yield client  # 'yield' gives the client to the test


# ── Test 1: Health check ─────────────────────────────
def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


# ── Test 2: Get todos when list is empty ─────────────
def test_get_todos_empty(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.get_json() == []  # should return empty list


# ── Test 3: Add a new todo ───────────────────────────
def test_add_todo(client):
    response = client.post(
        '/todos',
        json={"task": "Learn Docker"}  # sending JSON body
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['task'] == 'Learn Docker'
    assert data['done'] == False
    assert 'id' in data  # ID should be auto-assigned


# ── Test 4: Add todo without task field ──────────────
# Testing that our validation works
def test_add_todo_missing_task(client):
    response = client.post('/todos', json={})
    assert response.status_code == 400  # should reject bad request


# ── Test 5: Get todos after adding ───────────────────
def test_get_todos_after_adding(client):
    client.post('/todos', json={"task": "Task 1"})
    client.post('/todos', json={"task": "Task 2"})
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.get_json()) == 2  # should have 2 todos


# ── Test 6: Delete a todo ────────────────────────────
def test_delete_todo(client):
    # First add a todo
    add_response = client.post('/todos', json={"task": "Delete me"})
    todo_id = add_response.get_json()['id']

    # Now delete it
    delete_response = client.delete(f'/todos/{todo_id}')
    assert delete_response.status_code == 200

    # Verify it's gone
    get_response = client.get('/todos')
    assert len(get_response.get_json()) == 0


# ── Test 7: Delete non-existent todo 0─────────────────
def test_delete_nonexistent_todo(client):
    response = client.delete('/todos/999')
    assert response.status_code == 404


# ── Test 8: Complete a todo ──────────────────────────
def test_complete_todo(client):
    add_response = client.post('/todos', json={"task": "Finish project"})
    todo_id = add_response.get_json()['id']

    complete_response = client.put(f'/todos/{todo_id}')
    assert complete_response.status_code == 200
    assert complete_response.get_json()['done'] == True