#add pets
@app.route('/api/v1/admin/addpet', methods=['POST'])
def add_pet():
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
    pname = data.get('name')
    ptype = data.get('type')
    pbreed = data.get('breed')
    pgender = data.get('gender')
    page_month = data.get('age_month')
    pdesc = data.get('description')
    pimg = data.get('image')
    pweight = data.get('weight')
    pvacdate = data.get('vaccination_date')
    phealth = data.get('health_condition')
    psterilisation = data.get('sterilisation_status')
    pfee = data.get('adoption_fee')
    powner = data.get('previous_owner')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not pname or not ptype or not pbreed or not pgender or not page_month or not pdesc or not pimg or not pweight or not pvacdate or not phealth or not psterilisation or not pfee or not powner:
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query_pets_condition = """
        INSERT INTO pets.Pet_Condition (weight, vaccination_date, health_condition, sterilisation_status, adoption_fee, previous_owner)
        VALUES (%d, %s, %s, %d, %d, %d);
        """
        cursor.execute(query_pets_condition, (pweight, pvacdate, phealth, psterilisation, pfee, powner))
        cursor.execute("SELECT LAST_INSERT_ID();")
        pet_condition_id = cursor.fetchone()[0]

        query_pets_info = """
        INSERT INTO pets.Pet_Info (name, type, breed, gender, age_month, description, image, pet_condition_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %d);
        """
        cursor.execute(query_pets_info, (pname, ptype, pbreed, pgender, page_month, pdesc, pimg, pet_condition_id))
        
        connection.commit()
        return jsonify({"message": "Pet added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#update pets
@app.route('/api/v1/admin/updatepet', methods=['POST'])
def update_pet():
    #update pet condition
    #update pet info
    """
    Updates an existing pet in the database.

    This endpoint accepts a JSON payload with the following fields:
    - pet_id: 
    - name: 
    - type: 
    - breed: 
    - gender: 
    - age_month: 
    - description: 
    - image: 
    - weight: 
    - vaccination_date:  YYYY-MM-DD
    - health_condition: 
    - sterilisation_status: 
    - adoption_fee: 
    - previous_owner:
    """
    data = request.json
    pet_id = data.get('pet_id')
    pname = data.get('name')
    ptype = data.get('type')
    pbreed = data.get('breed')
    pgender = data.get('gender')
    page_month = data.get('age_month')
    pdesc = data.get('description')
    pimg = data.get('image')
    pweight = data.get('weight')
    pvacdate = data.get('vaccination_date')
    phealth = data.get('health_condition')
    psterilisation = data.get('sterilisation_status')
    pfee = data.get('adoption_fee')
    powner = data.get('previous_owner')

    if not pname or not ptype or not pbreed or not pgender or not page_month or not pdesc or not pimg or not pweight or not pvacdate or not phealth or not psterilisation or not pfee or not powner:
        return jsonify({"error": "Missing required fields"}), 400
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor()
        query_pets_condition = """
        UPDATE pets.Pet_Condition 
        SET weight = %s, vaccination_date = %s, health_condition = %s, sterilisation_status = %s, adoption_fee = %s, previous_owner = %s 
        WHERE pet_condition_id = (SELECT pet_condition_id FROM pets.Pet_Info WHERE pet_id = %s); 
        """
        cursor.execute(query_pets_condition, (pweight, pvacdate, phealth, psterilisation, pfee, powner, pet_id))

        query_pets_info = """
        UPDATE pets.Pet_Info
        SET name = %s, type = %s, breed = %s, gender = %s, age_month = %s, description = %s, image = %s
        WHERE pet_id = %s;
        """
        cursor.execute(query_pets_info, (pname, ptype, pbreed, pgender, page_month, pdesc, pimg, pet_id))
        connection.commit()
        return jsonify({"message": "Pet updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/v1/admin/deletepet', methods=['DELETE'])
def delete_pet():
    """
    
    Deletes an existing pet from the database.

    This endpoint accepts a JSON payload with the following field:
    - pet_id:

    """
    data = request.json
    pet_id = data.get('pet_id')

    if not pet_id:
        return jsonify({"error": "Missing pet_id"}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        
        # delete_pet_condition_query = """
        # DELETE FROM pets.Pet_Condition 
        # WHERE pet_condition_id = (SELECT pet_condition_id FROM pets.Pet_Info WHERE pet_id = %s);
        # """
        # cursor.execute(delete_pet_condition_query, (pet_id,))
        
        delete_pet_info_query = "DELETE FROM pets.Pet_Info WHERE pet_id = %s"
        cursor.execute(delete_pet_info_query, (pet_id,))
        delete_pet_condition_query = """
        DELETE FROM pets.Pet_Condition 
        WHERE pet_condition_id = (SELECT pet_condition_id FROM pets.Pet_Info WHERE pet_id = %s);
        """
        cursor.execute(delete_pet_condition_query, (pet_id,))
        
        connection.commit()
        return jsonify({"message": "Pet deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
