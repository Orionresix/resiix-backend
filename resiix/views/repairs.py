from flask import (
    Blueprint, request, jsonify
)
from resiix.views.db import get_db


bp = Blueprint('repairs', __name__, url_prefix='/repairs')


@bp.route('/old')
def repairs():
    db = get_db()
    cursor = db.cursor()

    r_id = request.args.get('r_id')
    r_status = request.args.get('r_status')
    r_p_id = request.args.get('r_p_id')

    if r_id:
        query = (
         'SELECT r_id, r_type, r_description, r_img_url, r_img_url1, p_name,'
         'r_img_url2, r_l_id, r_u_id,r_created_time, r_phone,r_status, r_p_id,'
         'u_name, r_priority '
         ' FROM  maintenance.report ,maintenance.properties,maintenance.units'
         'WHERE p_id = r_p_id and r_u_id = u_id and r_id = %s ORDER BY r_created_time DESC'
        )
        cursor.execute(query, (r_id,))
    elif r_status:
        query = (
         'SELECT r_id, r_type, r_description, r_img_url, r_img_url1, p_name,'
         'r_img_url2, r_l_id, r_u_id,r_created_time, r_phone,r_status, r_p_id,'
         'u_name, r_priority '
         ' FROM  maintenance.report ,maintenance.properties,maintenance.units'
         ' WHERE p_id = r_p_id and r_u_id = u_id and r_status = %s ORDER BY  r_created_time DESC'
        )
        cursor.execute(query, (r_status,))
    elif r_p_id:
        query = (
         'SELECT r_id, r_type, r_description, r_img_url, r_img_url1,p_name,'
         'r_img_url2, r_l_id, r_u_id,r_created_time, r_phone,r_status, r_p_id,'
         'u_name, r_priority '
         ' FROM  maintenance.report ,maintenance.properties,maintenance.units'
         ' WHERE p_id = r_p_id and r_u_id = u_id and  r_p_id = %s'
          ' ORDER BY  r_created_time DESC'
        )
        cursor.execute(query, (r_p_id,))
    else:
        cursor.execute(
         'SELECT r_id, r_type, r_description, r_img_url, r_img_url1,p_name,'
         'r_img_url2, r_l_id, r_u_id,r_created_time, r_phone,r_status, r_p_id,'
         'u_name, r_priority '
         ' FROM  maintenance.report ,maintenance.properties,maintenance.units'
         ' WHERE p_id = r_p_id and r_u_id = u_id ORDER BY  r_created_time DESC'
        )
    columns = [col[0] for col in cursor.description]  # Extract column names
    wo_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(wo_data)


@bp.route('/', methods=['GET'])
def get_repairs():
    db = get_db()
    cursor = db.cursor()
    base_query = (
        'SELECT r_id, r_type, r_description, r_img_url, r_img_url1, p_name,'
        'r_img_url2, r_l_id, r_u_id, r_created_time, r_phone, r_status, r_p_id,'
        'u_name, r_priority '
        'FROM maintenance.report, maintenance.properties, maintenance.units '
        'WHERE p_id = r_p_id and r_u_id = u_id'
    )

    # Initialize an empty list to store the conditions
    conditions = []
    params = []

    # Check for filter parameters and construct conditions accordingly
    r_id = request.args.get('r_id')
    if r_id:
        conditions.append('r_id = %s')
        params.append(r_id)

    r_status = request.args.get('r_status')
    if r_status:
        conditions.append('r_status = %s')
        params.append(r_status)

    r_p_id = request.args.get('r_p_id')
    if r_p_id:
        conditions.append('r_p_id = %s')
        params.append(r_p_id)
    
    r_type = request.args.get('r_type')
    if r_type:
        conditions.append('r_type = %s')
        params.append(r_type)

    r_priority = request.args.get('r_priority')
    if r_priority:
        conditions.append('r_priority = %s')
        params.append(r_priority)

    # Combine all conditions with "AND" and append to the base query
    if conditions:
        base_query += ' AND ' + ' AND '.join(conditions)

    # Add ORDER BY clause to the query
    base_query += ' ORDER BY r_created_time DESC'

    # Execute the SQL query
    cursor.execute(base_query, params)

    columns = [col[0] for col in cursor.description]  # Extract column names
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(results), 200


@bp.route('/category')
def category():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
         'SELECT m_id, m_name '
         ' FROM  maintenance.maintenance_category'
         ' ORDER BY  m_id DESC'
        )
    columns = [col[0] for col in cursor.description]  # Extract column names
    categorydata = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(categorydata)


@bp.route('/get_request_count')
def get_request_count():
    db = get_db()
    cursor = db.cursor()

    p_r_type = request.args.get('p_r_type')
    p_r_u_id = request.args.get('p_r_u_id')
    p_r_l_id = request.args.get('p_r_l_id')
    p_wo_status = request.args.get('p_wo_status')
    p_wo_assigned_by = request.args.get('p_wo_assigned_by')

    cursor.execute("SELECT maintenance.get_request_count(%s, %s, %s, %s, %s)",
    (p_r_type, p_r_u_id, p_r_l_id, p_wo_status, p_wo_assigned_by))

    count = cursor.fetchone()[0]

    db.close()
    return jsonify({"totalMaintenanceRequest": count,
                    "totalOpenWorkOrders": count, "overdueRequests": count,
                    "totalExpenses": count})


@bp.route('/create',  methods=['POST'])
def create():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        data = request.json
        r_type = data.get('r_type')
        r_description = data.get('r_description')
        r_img_url = data.get('r_img_url')
        r_img_url1 = data.get('r_img_url1')
        r_img_url2 = data.get('r_img_url2')
        r_l_id = data.get('r_l_id')
        r_u_id = data.get('u_id')
        r_p_id = data.get('p_id')
        r_phone = data.get('r_phone')
        r_priority = data.get('r_priority')
        r_f_id = 1

    error = None
    if error is not None:
        return jsonify({'error': error}), 400  # Return error response
    else:
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO maintenance.report ( r_type,'
                'r_description,r_img_url, r_img_url1, r_img_url2,'
                'r_l_id, r_u_id, r_phone, r_p_id, r_priority, r_f_id )'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (r_type, r_description, r_img_url, r_img_url1, r_img_url2,
                 r_l_id, r_u_id, r_phone, r_p_id, r_priority, r_f_id)
            )
            db.commit()
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Return error response
        finally:
            cursor.close()  # Close the cursor
            db.close()  # Close the database connection

        return jsonify({'message': 'repair request added successfully'}), 201
