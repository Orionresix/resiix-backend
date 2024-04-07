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
    u_id = request.args.get('u_id')
    if u_id:
        cursor.execute(
            'SELECT u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id, u_code '
            ' FROM maintenance.units WHERE u_id = %s', (u_id,)
        )
    else:
        cursor.execute(
         'select u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id, u_code '
         ' from maintenance.units'
        )
    unit_data = cursor.fetchall()
    db.close()
    return jsonify(unit_data)


def get_unit_data(u_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=DictCursor)  # Setting dictionary=True to return results as dictionaries
    cursor.execute(
        'SELECT  u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id, u_code, u_pm_id FROM maintenance.units WHERE u_id = %s', (u_id,)
    )
    unit_data = cursor.fetchone()  # Fetch one row because we're fetching data for a single property
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
        p_id = data.get('u_p_id')

        property_data = get_property_data(p_id)
        if not property_data:
            return jsonify({'error': 'Property with provided p_id not found.'}), 404
        u_f_id = property_data['p_f_id']
        if not data.get('u_pm_id'):
            u_pm_id = property_data['p_manager_id']
        
        error = None
        if not u_pm_id:
            error = 'You must select property to add unit.'

        if error is not None:
            return jsonify({'error': error}), 400  # Return error response
        else:
            try:
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO maintenance.units (u_name, u_type, u_status, u_description, u_p_id, u_f_id, u_pm_id)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (u_name, u_type, u_status, u_description, u_p_id, u_f_id, u_pm_id)
                   
                )
                db.commit()
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Return error response
            finally:
                cursor.close()  # Close the cursor
                db.close()  # Close the database connection

        return jsonify({'message': 'unit added successfully'}), 201

    return jsonify({'error': 'Method not allowed'}), 405




