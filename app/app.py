from flask import Flask, jsonify, request


app = Flask(__name__)

todos = []
next_id = 1 


# ── Route 1: GET /todos 
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200


# ── Route 2: POST /todos 
@app.route('/todos', methods=['POST'])
def add_todo():
    global next_id
    data = request.get_json() 

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
    return jsonify(todo), 201 


# ── Route 3: PUT /todos/<id> 
@app.route('/todos/<int:id>', methods=['PUT'])
def complete_todo(id):
    for todo in todos:
        if todo['id'] == id:
            todo['done'] = True
            return jsonify(todo), 200
    return jsonify({"error": "todo not found"}), 404 


# ── Route 4: DELETE /todos/<id> 
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
    app.run(host='0.0.0.0', port=5000, debug=True)