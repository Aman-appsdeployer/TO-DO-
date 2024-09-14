from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234@aman",
    database="collage",
    auth_plugin="mysql_native_password"

)
cursor = db.cursor()

# Home route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return jsonify(tasks)

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json['task']
    cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    db.commit()
    return jsonify({"message": "Task added successfully"}), 201

# Route to update an existing task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = request.json['task']
    cursor.execute("UPDATE tasks SET task=%s WHERE id=%s", (task, id))
    db.commit()
    return jsonify({"message": "Task updated successfully"})

# Route to delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    db.commit()
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
