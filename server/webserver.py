# make sure install all these bs then add to requirements.txt file
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error, connect
from dotenv import load_dotenv
import os

# Load ur environment variables
load_dotenv()

# Set up CORS for flask and react
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
app.secret_key = "inf2002dbprojectpartone"


def get_db_connection():
    try:
        conn = connect(host=os.getenv('HOST'),
            database=os.getenv('DATABASENAME'),
            user=os.getenv('DATABASEUSER'),
            password=os.getenv('DATABASEPASSWORD'))
        print("Successfully connected to the database")
        return conn
    except Error as err:
        print(f"Error connecting to the database: {err}")
        return None

@app.route('/api/v1')
def index():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        return jsonify({
            "message": "index",
        })
    except Error as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if not email or not name or not password:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO adopters (email, name, password) VALUES (%s, %s, %s)",
                       (email, name, hashed_password))
        connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adopters WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return jsonify({"message": "Logged in successfully",
                            "user": {"id": user['id'], "name": user['name'], "email": user['email']}}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/check_session')
def check_session():
    print(dict(session))
    return "Check the console for session data"


@app.route('/api/v1/check_auth')
def check_auth():
    if 'user_id' in session:
        return jsonify({'isAuthenticated': True}), 200
    return jsonify({'isAuthenticated': False}), 401


@app.route('/api/v1/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})


@app.route('/api/v1/getpets', methods=['GET'])
def get_all_pets():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT *
        FROM pets.Pet_Info
        JOIN pets.Pet_Condition ON pets.Pet_Info.pet_condition_id = pets.Pet_Condition.pet_condition_id
        """
        cursor.execute(query)
        pets = cursor.fetchall()

        return jsonify(pets), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/filterpets', methods=['POST'])
def filter_pets():
    data = request.json
    filter_type = data.get('type')
    filter_value = data.get('value')

    if not filter_type or not filter_value:
        return jsonify({"error": "Missing filter type or value"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        query = f"""
        SELECT *
        FROM pets.Pet_Info
        JOIN pets.Pet_Condition ON pets.Pet_Info.pet_condition_id = pets.Pet_Condition.pet_condition_id
        WHERE {filter_type} = %s
        """
        cursor.execute(query, (filter_value,))
        pets = cursor.fetchall()

        return jsonify(pets), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)