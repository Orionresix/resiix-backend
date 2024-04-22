from flask import (
    Blueprint,  jsonify, request
)
from resiix.views.db import get_db
from resiix.views.properties import get_property_data
from psycopg2.extras import DictCursor

bp = Blueprint('units', __name__, url_prefix='/units')


@bp.route('/')
def units():
    db = get_db()
    cursor = db.cursor()
    
    base_query = (
        'SELECT * FROM maintenance.units'
        ' INNER JOIN maintenance.properties ON units.u_p_id = properties.p_id'
        ' LEFT JOIN maintenance.leases ON units.u_id = leases.l_u_id'
        ' WHERE u_f_id is not null'
    )
    # Initialize an empty list to store the conditions
    conditions = []
    params = []

    u_p_id = request.args.get('u_p_id')
    if u_p_id:
        conditions.append('u_p_id = %s')
        params.append(u_p_id)

    u_name = request.args.get('u_name')
    if u_name:
        conditions.append('u_name = %s')
        params.append(u_name)

    # Combine all conditions with "AND" and append to the base query
    if conditions:
        base_query += ' AND ' + ' AND '.join(conditions)

    # Add ORDER BY clause to the query
    base_query += ' ORDER BY u_name DESC'

    # Execute the SQL query
    cursor.execute(base_query, params)

    columns = [col[0] for col in cursor.description]  # Extract column names
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(results), 200


def get_unit_data(u_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=DictCursor)  
    cursor.execute(
        'SELECT * FROM maintenance.units WHERE u_id = %s', (u_id,)
    )
    unit_data = cursor.fetchone()  
    db.close()
    return unit_data


@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.json
        u_name = data.get('u_name')
        u_type = data.get('u_type')
        u_status = data.get('u_status')
        u_description = data.get('u_description')
        u_p_id = data.get('u_p_id')

        l_code = data.get('l_code')
        l_start_date = data.get('l_start_date')
        l_end_date = data.get('l_end_date')
        l_lessee_name = data.get('l_lessee_name')
        l_phone = data.get('l_phone')
        l_email = data.get('l_email')
        passcode = data.get('l_phone')
        l_rent = data.get('l_rent')
        l_secondary_phone = data.get('l_secondary_phone')
        l_national_id = data.get('l_national_id')

        property_data = get_property_data(data.get('u_p_id'))
        if not property_data:
            return jsonify({'error': 'Property  not found.'}), 404
        u_f_id = property_data['p_f_id']
        if not data.get('u_pm_id'):
            u_pm_id = property_data['p_manager_id']
        
        error = None

        if error is not None:
            return jsonify({'error': error}), 400  # Return error response
        else:
            try:
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO maintenance.units (u_name, u_type, u_status,'
                    ' u_description, u_p_id, u_f_id, u_pm_id, passcode)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (u_name, u_type, u_status, u_description, u_p_id, u_f_id,
                     u_pm_id, passcode)                
                )
               
                # Retrieve the last inserted ID
                cursor.execute(
                    'SELECT u_id FROM maintenance.units WHERE u_p_id = %s AND u_name = %s',
                    (u_p_id, u_name)
                  )
                row = cursor.fetchone()
                if row:
                    l_u_id = row[0]
                else:
                    return jsonify({'error': 'Failed to fetch unit ID after insertion'}), 500

                cursor.execute(
                    'INSERT INTO maintenance.leases (l_start_date, l_end_date,'
                    ' l_rent, l_u_id, tenant_name, l_code, l_email, l_phone,'
                    ' l_secondary_phone, l_national_id,l_lessee_name )'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (l_start_date, l_end_date, l_rent, l_u_id, l_lessee_name,
                     l_code, l_email, l_phone,
                     l_secondary_phone, l_national_id, l_lessee_name)
                   
                )

                db.commit()
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Return error response
            finally:
                cursor.close()  # Close the cursor
                db.close()  # Close the database connection

        return jsonify({'message': 'unit added successfully'}), 201

    return jsonify({'error': 'Method not allowed'}), 405




