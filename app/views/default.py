from flask import jsonify,  request
from .. import app
import psycopg2


# Connect to the database using app configuration
def get_db():
    conn = psycopg2.connect(
        dbname=app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1],
        user=app.config['SQLALCHEMY_DATABASE_URI'].split('://')[1].split(':')[0],
        password=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[2].split('@')[0],
        host=app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split(':')[0],
        port=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[3].split('/')[0]
    )
    return conn


# Commit the transaction
def execute_query(query, values=None):
    conn = get_db()
    cur = conn.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result


def execute_query(query, values=()):
    try:
        connection = psycopg2.connect(
            dbname="your_dbname",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if 'connection' in locals():
            connection.close()


#Authetication
# Route to handle both GET and POST requests for users
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        try:
            # Execute SQL query to fetch users data
            users = execute_query("SELECT id, created_at, username, email FROM users.users")
            return jsonify(users)
        except Exception as e:
            return f"Error: {e}", 500  # Return error message with 500 status code for internal server error
    elif request.method == 'POST':
        try:
            # Get data from request body
            data = request.json
            username = data.get('username')
            email = data.get('email')
            
   # Execute SQL query to insert new user data
            execute_query("INSERT INTO users.users (username, email) VALUES (%s, %s)", (username, email))
            
            
            return "User created successfully", 201  # Return success message with 201 status code for resource created
        except Exception as e:
            return f"Error: {e}", 500  # Return error message with 500 status code for internal server error



#fetch methods
@app.route('/oldproperties')
def properties():
    try:
        property_id = request.args.get('id')
        if property_id:
            # If an id is passed, return the property with that id
            property_data = execute_query("SELECT p_id, p_name, p_num_units, p_manager_id, p_country, p_city, p_address, p_zipcode, p_state, p_latitude, p_longitude, p_elevation, p_f_id FROM maintenance.properties WHERE p_id = %s", (property_id,))
        else:
            # If no id is passed, return all properties
            property_data = execute_query("SELECT p_id, p_name, p_num_units, p_manager_id, p_country, p_city, p_address, p_zipcode, p_state, p_latitude, p_longitude, p_elevation, p_f_id FROM maintenance.properties")
        
        return jsonify(property_data)
    except Exception as e:
        return f"Error: {e}"


@app.route('/units')
def units():
    try:
        unit_id = request.args.get('id')
        if unit_id:
            units_data = execute_query("SELECT u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id FROM maintenance.units WHERE u_id = %s", (unit_id,))
        else:
            units_data = execute_query("SELECT u_id, u_name, u_type, u_status, u_description, u_p_id FROM maintenance.units")
        return jsonify(units_data)
    except Exception as e:
        return f"Error: {e}"


@app.route('/leases')
def leases():
    try:
        lease_id = request.args.get('id')
        if lease_id:
            lease_data = execute_query("SELECT l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name, l_code, l_email, l_phone, l_secondary_phone, l_national_id from maintenance.leases WHERE l_id = %s", (lease_id,))
        else:
            lease_data = execute_query("SELECT l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name, l_code, l_email, l_phone, l_secondary_phone, l_national_id from maintenance.leases")
        return jsonify(lease_data)
    except Exception as e:
        return f"Error: {e}"



#post methods

@app.route('/add-properties', methods=['POST'])
def add_property():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract property details from the JSON data
        name = data.get('p_name')
        num_units = data.get('p_num_units')

        # Validate the compulsory fields
        if not name or not num_units:
            return jsonify({'error': 'Name and number of units are required'}), 400

        # Prepare the SQL query
        query = "INSERT INTO maintenance.properties (p_name, p_num_units"
        values = [name, num_units]

        # Add optional fields to the query and values list
        optional_fields = ['country', 'city', 'address', 'zipcode', 'state', 'latitude', 'longitude', 'elevation', 'manager_id']
        for field in optional_fields:
            if field in data:
                query += f", {field}"
                values.append(data[field])

        # Complete the query string
        query += ") VALUES ("
        query += ', '.join(['%s'] * len(values))
        query += ") ON CONFLICT (id) DO UPDATE SET "

        # Add optional fields to the update part of the query
        fields_added = False
        for field in optional_fields:
            if field in data:
                query += f"{field}=EXCLUDED.{field}, "
                fields_added = True

        # Remove the last comma and space from the update query
        if fields_added:
            query = query[:-2]

        # Execute the query
        execute_query(query, tuple(values))

        return jsonify({'message': 'Property added successfully'}), 201
    except Exception as e:
        # Handle any exceptions
        return jsonify({'error': str(e)}), 500
    

@app.route('/test')
def test():
    return 'Hello, World!'