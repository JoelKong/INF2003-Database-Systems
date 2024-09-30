from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error, connect
from dotenv import load_dotenv
from datetime import datetime
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
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_password, "adopter"))
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
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Logged in successfully",
                            "user": {"user_id": user['user_id'], "username": user['username'],
                                     "role": user['role']}}), 200
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

        # Convert sets to lists
        for pet in top3pets:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

        return jsonify(top3pets), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/getPets', methods=['GET'])
def get_all_pets():
    connection = get_db_connection()

    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT *
        FROM test.Pet_Info
        JOIN test.Pet_Condition ON test.Pet_Info.pet_condition_id = test.Pet_Condition.pet_condition_id
        """
        cursor.execute(query)
        pets = cursor.fetchall()

        # check and process each pet's data
        for pet in pets:
            # convert sets (if any) into lists as type and gender might be in sets
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

            # convert datetime objects to strings
            try:
                if isinstance(pet.get('vaccination_date'), datetime.date):
                    pet['vaccination_date'] = pet['vaccination_date'].strftime('%Y-%m-%d')
            except (TypeError, AttributeError):
                # handle the case where the vaccination_date field has an unexpected data type
                pet['vaccination_date'] = None

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

        # Convert sets to lists
        for pet in pets:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

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

    user_id = data.get('user_id')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # check if the pet is already in the Users's favourites
        cursor.execute("SELECT * FROM Favourites WHERE user_id = %s AND pet_id = %s", (user_id, pet_id))
        if cursor.fetchone():
            return jsonify({"error": "Pet is already in favourites"}), 400

        # insert the favourite pet into the Favourites table
        cursor.execute(
            "INSERT INTO Favourites (user_id, pet_id) VALUES (%s, %s)",
            (user_id, pet_id)
        )
        connection.commit()

        return jsonify({"message": "Pet added to favourites successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/v1/getReservedPets', methods=['GET'])
def get_reserved_pets():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT DISTINCT p.*
        FROM Pet_Info p
        INNER JOIN Applications a ON p.pet_id = a.pet_id
        WHERE a.user_id = %s
        """
        cursor.execute(query, (user_id,))
        pets_in_applications = cursor.fetchall()

        # Convert sets to lists
        for pet in pets_in_applications:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

        return jsonify(pets_in_applications)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/api/v1/getFavourites', methods=['GET'])
def getFavourites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT pi.*
            FROM Favourites f
            JOIN Pet_Info pi ON f.pet_id = pi.pet_id
            WHERE f.user_id = %s
        """
        cursor.execute(query, (user_id,))
        favourited_pets = cursor.fetchall()

        # Convert sets to lists
        for pet in favourited_pets:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

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
    user_id = data.get('user_id')
    pet_id = data.get('pet_id')

    if not user_id:
        return jsonify({"error": "User not logged in"}), 401  # User not logged in

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Cart WHERE user_id = %s AND pet_id = %s", (user_id, pet_id))
        if cursor.fetchone():
            return jsonify({"error": "Pet is already in cart"}), 400

        cursor.execute(
            "INSERT INTO Cart (user_id, pet_id) VALUES (%s, %s)",
            (user_id, pet_id)
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
    user_id = data.get('user_id')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT Pet_Info.*, Cart.cart_id FROM pets.Pet_Info
            JOIN pets.Pet_Condition ON pets.Pet_Info.pet_condition_id = pets.Pet_Condition.pet_condition_id 
            JOIN Cart ON Pet_Info.pet_id = Cart.pet_id
            WHERE pets.Pet_Info.pet_id IN (SELECT pet_id FROM Cart WHERE user_id = %s)
        """, (user_id,))
        cart = cursor.fetchall()

        # Convert sets to lists
        for pet in cart:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

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
    user_id = data.get('user_id')
    pet_id = data.get('pet_id')

    if not user_id or not pet_id:
        return jsonify({"error": "Missing user_id or pet_id"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        # Delete the pet from the cart
        cursor.execute("""
            DELETE FROM Cart 
            WHERE user_id = %s AND pet_id = %s
        """, (user_id, pet_id))

        connection.commit()

        return jsonify("Success"), 200

    except Error as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/confirmReservation', methods=['POST'])
def confirmReservation():
    data = request.json
    user_id = data.get('user_id')
    cart = data.get('cart')

    if not user_id or not cart:
        return jsonify({"error": "Missing user_id or cart"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()

        for item in cart:
            # cart_id = item.get('cart_id')
            pet_id = item.get('pet_id')
            submission_date = datetime.now().date().isoformat()
            status = 'pending'

            cursor.execute(
                "INSERT INTO Applications (application_id, user_id, pet_id, submission_date, status) VALUES (NULL, %s, %s, %s, %s)",
                (user_id, pet_id, submission_date, status)
            )

        connection.commit()

        # Delete all pets from the cart
        cursor.execute("""
            DELETE FROM Cart 
            WHERE user_id = %s
        """, (user_id,))

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


# Admin Registration (TO BE REMOVED)
@app.route('/api/v1/admin/register', methods=['POST'])
def admin_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    print(username, password)

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    hashed_password = generate_password_hash(password)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Admin (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        return jsonify({"message": "Admin Registered"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/deletePet', methods=['POST'])
def admin_login():
    data = request.json
    pet_id = data.get('pet_id')
    user_id = data.get('user_id')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        user_role = cursor.fetchone()

        if user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        cursor.execute("SELECT pet_condition_id FROM Pet_Info WHERE pet_id = %s", (pet_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Pet not found"}), 404

        pet_condition_id = result.get("pet_condition_id")

        cursor.execute("DELETE FROM Favourites WHERE pet_id = %s", (pet_id,))

        cursor.execute("DELETE FROM Cart WHERE pet_id = %s", (pet_id,))

        cursor.execute("DELETE FROM Applications WHERE pet_id = %s", (pet_id,))

        cursor.execute("DELETE FROM Pet_Info WHERE pet_id = %s", (pet_id,))

        cursor.execute("DELETE FROM Pet_Condition WHERE pet_condition_id = %s", (pet_condition_id,))

        # Commit the transaction
        connection.commit()

        return jsonify({"message": "Pet deleted successfully"}), 200

    except Error as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/editPet', methods=['POST'])
def admin_edit_pet():
    data = request.json
    pet_data = data.get('pet_data')
    user_id = data.get('user_id')
    pet_id = pet_data.get('pet_id')

    if not pet_data or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        user_role = cursor.fetchone()

        if user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        cursor.execute("SELECT pet_condition_id, type FROM Pet_Info WHERE pet_id = %s", (pet_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Pet not found"}), 404

        pet_condition_id = result.get("pet_condition_id")
        existing_type = result.get("type").split(',')

        vaccination_date_str = pet_data.get('vaccination_date')
        if vaccination_date_str:
            vaccination_date = datetime.strptime(vaccination_date_str, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_vaccination_date = vaccination_date.strftime('%Y-%m-%d')
        else:
            formatted_vaccination_date = None

        # Convert the type field to a comma-separated string
        new_type = ','.join(pet_data.get('type'))

        cursor.execute("""
            UPDATE Pet_Info
            SET 
                name = %s,
                type = %s,
                breed = %s,
                gender = %s,
                age_month = %s,
                description = %s
            WHERE pet_id = %s
        """, (
            pet_data.get('name'),
            new_type,
            pet_data.get('breed'),
            pet_data.get('gender'),
            pet_data.get('age_month'),
            pet_data.get('description'),
            pet_id
        ))

        # Update Pet_Condition table
        cursor.execute("""
            UPDATE Pet_Condition
            SET 
                weight = %s,
                vaccination_date = %s,
                health_condition = %s,
                sterilisation_status = %s,
                adoption_fee = %s,
                previous_owner = %s
            WHERE pet_condition_id = %s
        """, (
            pet_data.get('weight'),
            formatted_vaccination_date,
            pet_data.get('health_condition'),
            pet_data.get('sterilisation_status'),
            pet_data.get('adoption_fee'),
            pet_data.get('previous_owner'),
            pet_condition_id
        ))

        connection.commit()

        return jsonify({"message": "Pet updated successfully"}), 200

    except Error as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/addPet', methods=['POST'])
def admin_add_pet():
    """
    Adds a new pet to the database.

    This endpoint accepts a JSON payload with the following fields:
    - name: 
    - type: 
    - breed: 
    - gender: 
    - age_month: 
    - description: 
    - image: 
    - weight: 
    - vaccination_date: 
    - health_condition: 
    - sterilisation_status: 
    - adoption_fee: 
    - previous_owner: 
    """
    data = request.json
    pet_data = data.get('pet_data')
    user_id = data.get('user_id')

    if not pet_data or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        user_role = cursor.fetchone()

        if user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        vaccination_date_str = pet_data.get('vaccination_date')
        vaccination_date = datetime.strptime(vaccination_date_str, '%d/%m/%Y')
        formatted_vaccination_date = vaccination_date.strftime('%Y-%m-%d')

        query_pets_condition = """
        INSERT INTO pets.Pet_Condition (weight, vaccination_date, health_condition, sterilisation_status, adoption_fee, previous_owner)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query_pets_condition, (
            pet_data.get('weight'), formatted_vaccination_date, pet_data.get('health_condition'),
            pet_data.get('sterilisation_status'), pet_data.get('adoption_fee'), pet_data.get('previous_owner')))
        cursor.execute("SELECT LAST_INSERT_ID();")
        pet_condition_id = cursor.fetchone().get('LAST_INSERT_ID()')

        query_pets_info = """
        INSERT INTO pets.Pet_Info (name, type, breed, gender, age_month, description, image, pet_condition_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query_pets_info, (
            pet_data.get('name'), pet_data.get('type'), pet_data.get('breed'), pet_data.get('gender'),
            pet_data.get('age_month'), pet_data.get('description'), pet_data.get('image'), pet_condition_id))

        connection.commit()

        return jsonify({"message": "Pet added successfully"}), 201

    except Error as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/getUsers', methods=['POST'])
def get_Userss():
    data = request.json
    user = data.get('user')
    user_id = user.get('user_id')
    connection = get_db_connection()

    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        user_role = cursor.fetchone()

        if user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        cursor.execute("SELECT user_id, username, role FROM Users")
        users = cursor.fetchall()

        return jsonify({"users": users}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/addUser', methods=['POST'])
def admin_add_user():
    data = request.json
    user = data.get('user')
    new_user = data.get('newUser')

    connection = get_db_connection()

    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user.get('user_id'),))
        user_role = cursor.fetchone()

        if user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        # Validate new user input
        if not isinstance(new_user, dict) or 'username' not in new_user or 'password' not in new_user or 'role' not in new_user:
            return jsonify({"error": "Missing required fields in newUser"}), 400

        if not new_user['username'] or not new_user['password'] or not new_user['role']:
            return jsonify({"error": "Username, password, and role are required"}), 400

        # Hash the password
        hashed_password = generate_password_hash(new_user['password'])

        cursor.execute("""
            INSERT INTO Users (username, password, role) 
            VALUES (%s, %s, %s)
        """, (new_user['username'], hashed_password, 'adopter'))

        connection.commit()

        return jsonify({"message": "User added successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/updateUsersRole', methods=['POST'])
def update_Users_role():
    data = request.json
    user = data.get('user')
    user_id = data.get('userId')
    new_role = data.get('newRole')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user.get('user_id'),))
        user_role = cursor.fetchone()

        if user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        cursor.execute("UPDATE Users SET role = %s WHERE user_id = %s", (new_role, user_id))
        connection.commit()
        return jsonify({"message": "Role updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
