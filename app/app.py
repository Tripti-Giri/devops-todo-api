from flask import Flask, jsonify, request

# Flask app instance
app = Flask(__name__)

# In-memory storage (like a temporary database)
# Just a Python list — resets when container restarts
todos = []
next_id = 1  # auto-increment ID counter


# ── Route 1: GET /todos ──────────────────────────────
# Returns all todos as JSON
# Like asking "show me my full todo list"
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200


# ── Route 2: POST /todos ─────────────────────────────
# Creates a new todo
# You send: {"task": "Learn Docker"}
# It saves it with an ID and returns it back
@app.route('/todos', methods=['POST'])
def add_todo():
    global next_id
    data = request.get_json()  # reads the JSON body you send

    # Basic validation — task field must exist
    if not data or 'task' not in data:
        return jsonify({"error": "task field is required"}), 400

    todo = {
        "id": next_id,
        "task": data['task'],
        "done": False
    }
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201  # 201 = Created


# ── Route 3: PUT /todos/<id> ─────────────────────────
# Marks a todo as done
# Like ticking a checkbox
@app.route('/todos/<int:id>', methods=['PUT'])
def complete_todo(id):
    for todo in todos:
        if todo['id'] == id:
            todo['done'] = True
            return jsonify(todo), 200
    return jsonify({"error": "todo not found"}), 404  # 404 = Not Found


# ── Route 4: DELETE /todos/<id> ──────────────────────
# Deletes a todo by its ID
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    original_length = len(todos)
    todos = [t for t in todos if t['id'] != id]

    if len(todos) == original_length:
        return jsonify({"error": "todo not found"}), 404

    return jsonify({"message": f"Todo {id} deleted"}), 200


# ── Health check route ───────────────────────────────
# GitHub Actions and load balancers use this to check
# if your app is running. Very common in real DevOps.
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # host='0.0.0.0' means accept connections from anywhere
    # Important for Docker — without this, container won't be reachable
    app.run(host='0.0.0.0', port=5000, debug=True)