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
        connection = connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            charset=os.getenv('DB_CHARSET'),
            collation=os.getenv('DB_COLLATION')
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to DB Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record[0])
            cursor.close()
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
    
    
# to test connection
connection = get_db_connection()
if connection is not None and connection.is_connected():
    print("Connection successful!")
    connection.close()
else:
    print("Connection failed.")


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


# POST route to compute algorithm
@app.route('/api/v1/whateverpathyouwant', methods=['GET'])
def get_adopted_pets():
    # Get front end data
    data = request.get_json() # if need any data from the front end just an example
    start = data.get('start')
    hotels = data.get('selectedHotels')
    efficiencyType = data.get('efficiencyType')
    departureTime = data.get('departureTime')
    algorithmType = data.get('algorithm')


    # return bck to front end use jsonify
    # if not forward_route or not return_route:
    #     return jsonify({"error": "No route found"}), 500

    # # Return to front end
    # response = {
    #     "geojson_forward_route": geojson_forward_route,
    #     "geojson_return_route": geojson_return_route,
    #     "start": start,
    #     "hotels": hotels,
    #     "dashboardData": {"runtimeTaken": round(runtime, 5), "timeTaken": time_taken_hr_min, "totalCost": round(total_cost, 2), "ERPPassed": erp_passed, "forwardRouteRoads": forward_route_roads, "returnRouteRoads": return_route_roads},
    # }
    # return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)