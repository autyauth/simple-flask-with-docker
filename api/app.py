import os
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Define a function to create a database connection
def create_db_connection():
    return mysql.connector.connect(
        user="root",
        password="root",
        host=os.getenv('HOST', 'localhost'),
        database="users",
    )
def get_cursor():
    connection = create_db_connection()
    return connection.cursor(dictionary=True), connection

def exist_user_by_name(name):
    cursor, connection = get_cursor()
    cursor.execute("SELECT * FROM users WHERE name=%s", (name,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        connection.close()
        return True
    cursor.close()
    connection.close()
    return False
def exist_user_by_id(id):
    cursor, connection = get_cursor()
    cursor.execute("SELECT * FROM users WHERE uid=%s", (id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        connection.close()
        return True
    cursor.close()
    connection.close()
    return False
    

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor, connection = get_cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'users': users})

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    age = request.json['age']
    if exist_user_by_name(name):
        return jsonify({'message': 'User already exists'}), 500
    cursor, connection = get_cursor()
    sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
    val = (name, age)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if not exist_user_by_id(user_id):
        return jsonify({'message': 'User does not exist'}), 500
    cursor, connection = get_cursor()
    cursor.execute("SELECT * FROM users WHERE uid=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify({'user': user})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    name = request.json['name']
    age = request.json['age']
    if not exist_user_by_id(user_id):
        return jsonify({'message': 'User does not exist'}), 500
    if exist_user_by_name(name):
        return jsonify({'message': 'User already exists'}), 500
    cursor, connection = get_cursor()
    sql = "UPDATE users SET name=%s, age=%s WHERE uid=%s"
    val = (name, age, user_id)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not exist_user_by_id(user_id):
        return jsonify({'message': 'User does not exist'}), 500
    cursor, connection = get_cursor()
    sql = "DELETE FROM users WHERE uid=%s"
    val = (user_id,)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


