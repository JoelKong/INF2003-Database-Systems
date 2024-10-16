from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error, connect
from dotenv import load_dotenv
from datetime import datetime, date
import os

# load ur env variables
load_dotenv() 

# CORS for flask and react
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
app.secret_key = "inf2002dbprojectpartone"


def get_db_connection():
    try:
        conn = connect(host=os.getenv('HOST'),
                       database=os.getenv('DATABASENAME'),
                       user=os.getenv('DATABASEUSER'),
                       password=os.getenv('DATABASEPASSWORD'))
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
        for pet in pets:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])
            try:
                if isinstance(pet.get('vaccination_date'), datetime.date):
                    pet['vaccination_date'] = pet['vaccination_date'].strftime('%Y-%m-%d')
            except (TypeError, AttributeError):
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

    query = """
    SELECT Pet_Info.*, Pet_Condition.*
    FROM Pet_Info
    JOIN Pet_Condition ON Pet_Info.pet_condition_id = Pet_Condition.pet_condition_id
    WHERE 1=1  -- Placeholder to allow dynamic conditions
    """
    params = []

    if filter_type and filter_value:
        query += f" AND Pet_Info.{filter_type} LIKE %s"
        params.append(f"%{filter_value}%")  

    if gender:
        query += " AND Pet_Info.gender = %s"
        params.append(gender)

    if health_condition:
        query += " AND Pet_Condition.health_condition = %s"
        params.append(health_condition)

    if sterilisation_status is not None and sterilisation_status in ["0",
                                                                     "1"]:
        query += " AND Pet_Condition.sterilisation_status = %s"
        params.append(sterilisation_status)

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        pets = cursor.fetchall()

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
        cursor.execute("SELECT * FROM Favourites WHERE user_id = %s AND pet_id = %s", (user_id, pet_id))
        if cursor.fetchone():
            return jsonify({"error": "Pet is already in favourites"}), 400
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
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT DISTINCT p.*
        FROM Pet_Info p
        INNER JOIN Applications a ON p.pet_id = a.pet_id
        """
        cursor.execute(query)
        pets_in_applications = cursor.fetchall()

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
        return jsonify({"error": "User not logged in"}), 401 

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

        for pet in cart:
            if isinstance(pet.get('type'), set):
                pet['type'] = list(pet['type'])
            if isinstance(pet.get('gender'), set):
                pet['gender'] = list(pet['gender'])

        return jsonify(cart), 200

    except Error as e:
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
        cursor.execute("""
            DELETE FROM Cart 
            WHERE user_id = %s AND pet_id = %s
        """, (user_id, pet_id))

        connection.commit()

        return jsonify("Success"), 200

    except Error as e:
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
            pet_id = item.get('pet_id')
            submission_date = datetime.now().date().isoformat()
            status = 'pending'

            cursor.execute(
                "INSERT INTO Applications (application_id, user_id, pet_id, submission_date, status) VALUES (NULL, %s, %s, %s, %s)",
                (user_id, pet_id, submission_date, status)
            )

        connection.commit()
        cursor.execute("""
            DELETE FROM Cart 
            WHERE user_id = %s
        """, (user_id,))

        connection.commit()

        return jsonify("Success"), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


"""
--- Admin Endpoints ---
"""

@app.route('/api/v1/admin/register', methods=['POST'])
def admin_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

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
        print(f"User role: {user_role}")

        if not user_role or user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 400

        cursor.execute("SELECT pet_condition_id, type FROM Pet_Info WHERE pet_id = %s", (pet_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({"error": "Pet not found"}), 404

        pet_condition_id = result.get("pet_condition_id")

        vaccination_date_str = pet_data.get('vaccination_date')
        formatted_vaccination_date = None
        if vaccination_date_str:
            try:
                vaccination_date = datetime.strptime(vaccination_date_str, '%a, %d %b %Y %H:%M:%S %Z')
                formatted_vaccination_date = vaccination_date.strftime('%Y-%m-%d')
            except ValueError as e:
                print(f"Error parsing vaccination date: {e}")

        pet_type = pet_data.get('type')
        if isinstance(pet_type, list):
            new_type = ','.join(str(t) for t in pet_type)
        elif isinstance(pet_type, str):
            new_type = pet_type
        else:
            new_type = str(pet_type)

        gender = pet_data.get('gender')
        if isinstance(gender, list):
            new_gender = gender[0] if gender else None
        else:
            new_gender = gender

        update_data = {
            'name': pet_data.get('name'),
            'type': new_type,
            'breed': pet_data.get('breed'),
            'gender': new_gender,
            'age_month': pet_data.get('age_month'),
            'description': pet_data.get('description'),
            'pet_id': pet_id
        }

        update_query = """
            UPDATE Pet_Info
            SET 
                name = %(name)s,
                type = %(type)s,
                breed = %(breed)s,
                gender = %(gender)s,
                age_month = %(age_month)s,
                description = %(description)s
            WHERE pet_id = %(pet_id)s
        """
        cursor.execute(update_query, update_data)

        condition_update_data = {
            'weight': pet_data.get('weight'),
            'health_condition': pet_data.get('health_condition'),
            'sterilisation_status': pet_data.get('sterilisation_status'),
            'adoption_fee': pet_data.get('adoption_fee'),
            'previous_owner': pet_data.get('previous_owner'),
            'pet_condition_id': pet_condition_id
        }

        if formatted_vaccination_date is not None:
            condition_update_data['vaccination_date'] = formatted_vaccination_date

        condition_update_query = "UPDATE Pet_Condition SET "
        condition_update_query += ", ".join([f"{key} = %({key})s" for key in condition_update_data if key != 'pet_condition_id'])
        condition_update_query += " WHERE pet_condition_id = %(pet_condition_id)s"

        cursor.execute(condition_update_query, condition_update_data)
        connection.commit()
        return jsonify({"message": "Pet updated successfully"}), 200

    except Exception as e:
        connection.rollback()
        print(f"Error in admin_edit_pet: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        print("Database connection closed")


@app.route('/api/v1/admin/addPet', methods=['POST'])
def admin_add_pet():
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
        INSERT INTO Pet_Condition (weight, vaccination_date, health_condition, sterilisation_status, adoption_fee, previous_owner)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query_pets_condition, (
            pet_data.get('weight'), formatted_vaccination_date, pet_data.get('health_condition'),
            pet_data.get('sterilisation_status'), pet_data.get('adoption_fee'), pet_data.get('previous_owner')))
        cursor.execute("SELECT LAST_INSERT_ID();")
        pet_condition_id = cursor.fetchone().get('LAST_INSERT_ID()')

        query_pets_info = """
        INSERT INTO Pet_Info (name, type, breed, gender, age_month, description, image, adoption_status, pet_condition_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Available', %s);
        """
        cursor.execute(query_pets_info, (
            pet_data.get('name'), pet_data.get('type'), pet_data.get('breed'), pet_data.get('gender'),
            pet_data.get('age_month'), pet_data.get('description'), pet_data.get('image'), pet_condition_id))

        connection.commit()

        return jsonify({"message": "Pet added successfully"}), 200

    except Error as e:
        connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/getUsers', methods=['POST'])
def admin_get_users():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        user_role = cursor.fetchone()

        if not user_role or user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        query = "SELECT user_id, username, role FROM Users"
        cursor.execute(query)

        users = cursor.fetchall()

        return jsonify({
            "status": "success",
            "users": users
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


@app.route('/api/v1/admin/deleteUser/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    data = request.json
    admin_id = data.get('admin_id')
    user_id = user_id

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (admin_id,))
        user_role = cursor.fetchone()

        if not user_role or user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        connection.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



@app.route('/api/v1/admin/addUser', methods=['POST'])
def admin_add_user():
    data = request.json
    admin_id = data.get('admin_id')
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not all([admin_id, username, password, role]):
        return jsonify({"error": "All fields are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (admin_id,))
        user_role = cursor.fetchone()

        if not user_role or user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role)
        )
        connection.commit()

        return jsonify({"status": "success", "message": "User added successfully"}), 201

    except Error as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/getUser/<int:user_id>', methods=['POST'])
def admin_get_user(user_id):
    data = request.json
    admin_id = data.get('admin_id')

    if not admin_id:
        return jsonify({"error": "Admin ID is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (admin_id,))
        admin_role = cursor.fetchone()

        if not admin_role or admin_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        cursor.execute("SELECT user_id, username, role FROM Users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "status": "success",
            "user": user
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


@app.route('/api/v1/admin/updateUser/<int:user_id>', methods=['POST'])
def admin_update_user(user_id):
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    role = data.get('role')

    if not all([user_id, username, role]):
        return jsonify({"error": "All fields are required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (admin_id,))
        admin_role = cursor.fetchone()

        if not admin_role or admin_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        cursor.execute("UPDATE Users SET username = %s, role = %s WHERE user_id = %s",
                       (username, role, user_id))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found or no changes made"}), 404

        return jsonify({
            "status": "success",
            "message": "User updated successfully"
        })

    except Error as e:
        connection.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/getApplications', methods=['POST'])
def admin_get_applications():
    data = request.json
    admin_id = data.get('admin_id')

    if not admin_id:
        return jsonify({"error": "Admin ID is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (admin_id,))
        admin_role = cursor.fetchone()

        if not admin_role or admin_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        query = """
        SELECT a.application_id, a.user_id, a.pet_id, a.submission_date, a.status,
               u.username, p.name as pet_name
        FROM Applications a
        JOIN Users u ON a.user_id = u.user_id
        JOIN Pet_Info p ON a.pet_id = p.pet_id
        """
        cursor.execute(query)
        applications = cursor.fetchall()

        return jsonify({
            "status": "success",
            "applications": applications
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


@app.route('/api/v1/admin/getApplications/<int:application_id>', methods=['POST'])
def admin_get_application_detail(application_id):
    data = request.json
    user_id = data.get('user_id')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        admin_role = cursor.fetchone()

        if not admin_role or admin_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        query = """
        SELECT 
            a.application_id,
            a.submission_date,
            a.status,
            p.pet_id,
            p.name AS pet_name,
            p.type AS pet_type,
            p.breed,
            p.gender,
            p.age_month,
            p.description AS pet_description,
            p.image AS pet_image,
            u.user_id AS applicant_id,
            u.username AS applicant_username
        FROM 
            Applications a
        INNER JOIN 
            Pet_Info p ON a.pet_id = p.pet_id
        INNER JOIN 
            Users u ON a.user_id = u.user_id
        WHERE 
            a.application_id = %s
        """
        cursor.execute(query, (application_id,))
        application = cursor.fetchone()

        if application:
            if 'submission_date' in application and isinstance(application['submission_date'], datetime):
                application['submission_date'] = application['submission_date'].isoformat()

            for key, value in application.items():
                if isinstance(value, set):
                    application[key] = list(value)

            return jsonify({
                "status": "success",
                "application": application
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Application not found"
            }), 404

    except Error as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/api/v1/admin/updateApplicationStatus/<int:application_id>', methods=['POST'])
def update_application_status(application_id):
    data = request.json
    print(data)
    new_status = data.get('status')
    user_id = data.get('user_id')
    applicant_id = data.get('applicant_id')
    pet_id = data.get('pet_id')


    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        admin_role = cursor.fetchone()

        if not admin_role or admin_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        update_query = """
        UPDATE Applications 
        SET status = %s 
        WHERE application_id = %s
        """
        cursor.execute(update_query, (new_status, application_id))
        connection.commit()

        if new_status == 'approved':
            insert_query = """
                    INSERT INTO Adoptions (application_id, pet_id, user_id, adoption_date)
                    VALUES (%s, %s, %s, %s)
                    """
            print("inserted data into adoptions table")
            today = date.today()
            cursor.execute(insert_query,
                           (application_id, pet_id, applicant_id, today))
            connection.commit()

        return jsonify({
            "status": "success",
            "message": "Application status updated successfully"
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


@app.route('/api/v1/admin/getAdoptions', methods=['POST'])
def admin_get_adoptions():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT role FROM Users WHERE user_id = %s", (user_id,))
        user_role = cursor.fetchone()

        if not user_role or user_role.get("role") != "admin":
            return jsonify({"error": "Invalid Permissions"}), 403

        query = """
                SELECT 
                    a.adoption_id,
                    a.adoption_date,
                    u.user_id AS adopter_id,
                    u.username AS adopter_name,
                    p.pet_id,
                    p.name AS pet_name,
                    p.type AS pet_type,
                    p.breed AS pet_breed,
                    app.application_id,
                    app.submission_date AS application_date,
                    app.status AS application_status
                FROM 
                    Adoptions a
                JOIN 
                    Users u ON a.user_id = u.user_id
                JOIN 
                    Pet_Info p ON a.pet_id = p.pet_id
                JOIN 
                    Applications app ON a.application_id = app.application_id
                ORDER BY 
                    a.adoption_date DESC
                """
        cursor.execute(query)
        adoptions = cursor.fetchall()

        for adoption in adoptions:
            for key, value in adoption.items():
                if isinstance(value, (datetime, date)):
                    adoption[key] = value.isoformat()
                elif isinstance(value, set):
                    adoption[key] = list(value) 
                elif not isinstance(value, (str, int, float, bool, type(None))):
                    adoption[key] = str(value)

        return jsonify({
            "status": "success",
            "adoptions": adoptions
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

if __name__ == '__main__':
    app.run(debug=True)
