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


"""
--- Authentication Endpoints ---
"""


@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.json
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
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Adoptor WHERE name = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Logged in successfully",
                            "user": {"adopter_id": user['adopter_id'], "name": user['name']}}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


"""
--- Pets Endpoints ---
"""

@app.route('/api/v1/getTop3', methods=['GET'])
def get_Top3():
    connection = get_db_connection()

    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT pi.*, COUNT(f.favourite_id) AS favourite_count
        FROM Favourites f
        JOIN Pet_Info pi ON f.pet_id = pi.pet_id
        GROUP BY pi.pet_id
        ORDER BY favourite_count DESC
        LIMIT 3;
        """
        cursor.execute(query)
        top3pets = cursor.fetchall()

        return jsonify(top3pets), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

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
    if sterilisation_status is not None and sterilisation_status in ["0",
                                                                     "1"]:  # Check explicitly for None, as 0 and 1 are valid
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
    data = request.json
    pet_id = data.get('pet_id')

    if not pet_id:
        return jsonify({"error": "Pet ID is required"}), 400

    adopter_id = data.get('adopter_id')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # check if the pet is already in the adopter's favourites
        cursor.execute("SELECT * FROM Favourites WHERE adopter_id = %s AND pet_id = %s", (adopter_id, pet_id))
        if cursor.fetchone():
            return jsonify({"error": "Pet is already in favourites"}), 400

        # insert the favourite pet into the Favourites table
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


@app.route('/api/v1/getFavourites', methods=['GET'])
def getFavourites():
    adopter_id = request.args.get('adopter_id')
    if not adopter_id:
        return jsonify({"error": "adopter_id is required"}), 400

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


"""
--- Cart Endpoints ---
"""


@app.route('/api/v1/addtocart', methods=['POST'])
def addToCart():
    data = request.json
    adopter_id = data.get('adopter_id')
    pet_id = data.get('pet_id')

    if not adopter_id:
        return jsonify({"error": "User not logged in"}), 401  # User not logged in

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cart WHERE adopter_id = %s AND pet_id = %s", (adopter_id, pet_id))
        if cursor.fetchone():
            return jsonify({"error": "Pet is already in cart"}), 400

        cursor.execute(
            "INSERT INTO Cart (adopter_id, pet_id) VALUES (%s, %s)",
            (adopter_id, pet_id)
        )
        connection.commit()

        return jsonify(pet_id), 200

    except Error as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/getcart', methods=['POST'])
def getCart():
    data = request.json
    adopter_id = data.get('adopter_id')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT Pet_Info.*, Cart.cart_id FROM pets.Pet_Info
            JOIN pets.Pet_Condition ON pets.Pet_Info.pet_condition_id = pets.Pet_Condition.pet_condition_id 
            JOIN Cart ON Pet_Info.pet_id = Cart.pet_id
            WHERE pets.Pet_Info.pet_id IN (SELECT pet_id FROM Cart WHERE adopter_id = %s)
        """, (adopter_id,))
        cart = cursor.fetchall()

        return jsonify(cart), 200

    except Error as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/removefromcart', methods=['POST'])
def removeFromCart():
    data = request.json
    adopter_id = data.get('adopter_id')
    pet_id = data.get('pet_id')

    if not adopter_id or not pet_id:
        return jsonify({"error": "Missing adopter_id or pet_id"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # Delete the pet from the cart
        cursor.execute("""
            DELETE FROM Cart 
            WHERE adopter_id = %s AND pet_id = %s
        """, (adopter_id, pet_id))

        connection.commit()

        return jsonify("Success"), 200

    except Error as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/confirmreservation', methods=['POST'])
def confirmReservation():
    data = request.json
    adopter_id = data.get('adopter_id')
    cart = data.get('cart')

    if not adopter_id or not cart:
        return jsonify({"error": "Missing adopter_id or cart"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        for item in cart:
            cart_id = item.get('cart_id')
            pet_id = item.get('pet_id')

            cursor.execute(
                "INSERT INTO Orders (cart_id, adopter_id, pet_id) VALUES (%s, %s, %s)",
                (cart_id, adopter_id, pet_id)
            )

        connection.commit()

        # Delete all pets from the cart
        cursor.execute("""
            DELETE FROM Cart 
            WHERE adopter_id = %s
        """, (adopter_id,))

        connection.commit()

        return jsonify("Success"), 200

    except Error as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


"""
--- Admin Endpoints ---
"""

if __name__ == '__main__':
    app.run(debug=True)
