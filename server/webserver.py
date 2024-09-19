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
    # email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Adoptor (name, password) VALUES (%s, %s)",
                       (name, hashed_password))
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
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Missing email or password"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Adoptor WHERE name = %s", (name,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['adopter_id']
            return jsonify({"message": "Logged in successfully",
                            "user": {"adopter_id": user['adopter_id'], "name": user['name']}}), 200
        else:
            return jsonify({"error": "Invalid name or password"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({"message": f"Session user_id: {session['user_id']}"})
    return jsonify({"error": "No session found"}), 401


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
    gender = data.get('gender')  
    health_condition = data.get('health_condition')  
    sterilisation_status = data.get('sterilisation_status')

    # Start building the query
    query = """
    SELECT Pet_Info.*, Pet_Condition.*
    FROM Pet_Info
    JOIN Pet_Condition ON Pet_Info.pet_condition_id = Pet_Condition.pet_condition_id
    WHERE 1=1  -- Placeholder to allow dynamic conditions
    """
    
    params = []

    # Apply filters if they are provided

    # Filter by a generic type (name, breed, etc.)
    if filter_type and filter_value:
        query += f" AND Pet_Info.{filter_type} LIKE %s"
        params.append(f"%{filter_value}%")  # Use LIKE for partial matches

    # Filter by gender
    if gender:
        query += " AND Pet_Info.gender = %s"
        params.append(gender)

    # Filter by health condition
    if health_condition:
        query += " AND Pet_Condition.health_condition = %s"
        params.append(health_condition)


    # Filter by sterilisation status (0 or 1)
    if sterilisation_status is not None and sterilisation_status in ["0", "1"]:  # Check explicitly for None, as 0 and 1 are valid
        query += " AND Pet_Condition.sterilisation_status = %s"
        params.append(sterilisation_status)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        # Execute the dynamically built query
        cursor.execute(query, params)
        pets = cursor.fetchall()

        return jsonify(pets), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/v1/addFavourite', methods=['POST'])
def addFavourite():

    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    data = request.json
    pet_id = data.get('pet_id')
    
    if not pet_id:
        return jsonify({"error": "Pet ID is required"}), 400
    
    adopter_id = session['user_id'] 
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()

        #check if the pet is already in the adopter's favourites
        cursor.execute("SELECT * FROM Favourites WHERE adopter_id = %s AND pet_id = %s", (adopter_id, pet_id))
        if cursor.fetchone():
            return jsonify({"error": "Pet is already in favourites"}), 400

        #insert the favourite pet into the Favourites table
        cursor.execute(
            "INSERT INTO Favourites (adopter_id, pet_id) VALUES (%s, %s)", 
            (adopter_id, pet_id)
        )
        connection.commit()

        return jsonify({"message": "Pet added to favourites successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# @app.route('/api/v1/checkFavourite', methods=['GET'])
# def checkFavourite():
#     adopter_id = session.get('user_id')  # Fetch user ID from session
#
#     if not adopter_id:
#         return jsonify({"error": "User not logged in"}), 401  # User not logged in
#
#     pet_id = request.args.get('pet_id')
#
#     connection = get_db_connection()
#     if connection is None:
#         return jsonify({"error": "Database connection failed"}), 500
#
#     try:
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM Favourites WHERE adopter_id = %s AND pet_id = %s", (adopter_id, pet_id))
#         favourite = cursor.fetchone()
#
#         if favourite:
#             return jsonify({"isFavourite": True}), 200
#         else:
#             return jsonify({"isFavourite": False}), 200
#
#     except Error as e:
#         return jsonify({"error": str(e)}), 500
#
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
# TODO - fix checking fav

@app.route('/api/v1/getFavourites', methods=['GET'])
def getFavourites():
    try:
        adopter_id = session['user_id']
    except KeyError:
        return jsonify({"error": "User not logged in"}), 401

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT pi.*
            FROM Favourites f
            JOIN Pet_Info pi ON f.pet_id = pi.pet_id
            WHERE f.adopter_id = %s
        """
        cursor.execute(query, (adopter_id,))
        favourited_pets = cursor.fetchall()

        return jsonify(favourited_pets)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()



if __name__ == '__main__':
    app.run(debug=True)
