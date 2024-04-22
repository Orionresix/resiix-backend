from flask import (
    Blueprint, request, jsonify
)
from resiix.views.db import get_db


bp = Blueprint('work_orders', __name__, url_prefix='/work_orders')
@bp.route('/', methods=['GET'])
def work_orders():
    db = get_db()
    cursor = db.cursor()
    base_query = (
         'SELECT * from maintenance.work_order, maintenance.report,'
         'maintenance.properties ,maintenance.units'
         ' where wo_r_id = r_id and  p_id = r_p_id and r_u_id = u_id'
         ' and wo_id is not null'
    )

    # Initialize an empty list to store the conditions
    conditions = []
    params = []

    # Check for filter parameters and construct conditions accordingly
    wo_status = request.args.get('wo_status')
    if wo_status:
        conditions.append('wo_status = %s')
        params.append(wo_status)
    
    wo_assigned_to = request.args.get('wo_assigned_to')
    if wo_assigned_to:
        conditions.append('wo_assigned_to = %s')
        params.append(wo_assigned_to)

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
    base_query += ' ORDER BY wo_created_time, r_created_time DESC'

    # Execute the SQL query
    cursor.execute(base_query, params)

    columns = [col[0] for col in cursor.description]  # Extract column names
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(results), 200





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
        wo_pm_description = data.get('wo_pm_description')
        wo_l_id = data.get('wo_l_id')
        wo_u_id = data.get('wo_u_id')
        wo_assigned_to = data.get('wo_assigned_to')
        wo_assigned_by = data.get('wo_assigned_by')
        wo_status = "ASSIGNED"
        wo_due_date = data.get('wo_due_date')
        wo_r_id = data.get('wo_r_id')
        f_id = 1

    error = None
    if error is not None:
        return jsonify({'error': error}), 400  # Return error response
    else:
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO maintenance.work_order ( wo_pm_description,'
                ' wo_l_id, wo_u_id, wo_assigned_to, wo_assigned_by,'
                ' wo_status, wo_due_date, wo_r_id )'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (wo_pm_description,  wo_l_id, wo_u_id, wo_assigned_to,
                 wo_assigned_by, wo_status, wo_due_date, wo_r_id)
            )
            cursor.execute(
                'update maintenance.report '
                'set r_status = %s  WHERE r_id =  %s', ("ASSIGNED", wo_r_id,)
            )
            db.commit()
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Return error response
        finally:
            cursor.close()  # Close the cursor
            db.close()  # Close the database connection

        return jsonify({'message': 'workorder assigned  successfully'}), 201


@bp.route('/close',  methods=['POST'])
def close():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        data = request.json
        wo_technician_remarks = data.get('wo_technician_remarks')
        wo_material_used = data.get('wo_material_used')
        wo_material_cost = data.get('wo_material_cost')
        wo_labor_cost = data.get('wo_labor_cost')
        wo_closed_time = data.get('wo_closed_time')
        wo_status = "DONE"
        wo_r_id = data.get('wo_r_id')
        wo_id = data.get('wo_id')

    error = None
    if error is not None:
        return jsonify({'error': error}), 400  # Return error response
    else:
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE maintenance.work_order SET wo_technician_remarks = %s, '
                ' wo_material_used = %s, wo_material_cost = %s,'
                ' wo_labor_cost = %s, wo_closed_time = %s, wo_status = %s'
                '  WHERE wo_id =  %s',
                (wo_technician_remarks,  wo_material_used, wo_material_cost,
                 wo_labor_cost, wo_closed_time, wo_status, wo_id,)
            )
            cursor.execute(
                'update maintenance.report '
                'set r_status = %s  WHERE r_id =  %s', (wo_status, wo_r_id,)
            )
            db.commit()
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Return error response
        finally:
            cursor.close()  # Close the cursor
            db.close()  # Close the database connection

        return jsonify({'message': 'workorder submitted  successfully'}), 201
