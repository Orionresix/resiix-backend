from flask import (
    Blueprint, request, jsonify
)
from resiix.views.db import get_db


bp = Blueprint('work_orders', __name__, url_prefix='/work_orders')


@bp.route('/')
def work_orders():
    db = get_db()
    cursor = db.cursor()

    wo_id = request.args.get('wo_id')
    wo_assigned_by = request.args.get('wo_assigned_by')
    wo_assigned_to = request.args.get('wo_assigned_to')

    if wo_id:
        query = (
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time, '
         'wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id, '
         'wo_technician_remarks, wo_material_used, wo_material_cost, wo_labor_cost, wo_closed_time,'
         'r_id, r_type, r_description, r_img_url, r_img_url1, r_img_url2, '
         'r_l_id, r_u_id, r_created_time, r_phone , p_name, u_name, r_priority'
         ' FROM maintenance.work_order, maintenance.report '
         ' WHERE wo_r_id = r_id AND wo_id = %s and wo_id is not null '
         ' ORDER BY wo_created_time, r_created_time DESC'
        )
        cursor.execute(query, (wo_id,))
    elif wo_assigned_by:
        query = (
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time,'
         ' wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id,'
         'wo_technician_remarks, wo_material_used, wo_material_cost, wo_labor_cost, wo_closed_time,'
         ' r_id, r_type, r_description,r_img_url, r_img_url1, r_img_url2,'
         ' r_l_id, r_u_id, r_created_time, r_phone'
         ' from maintenance.work_order, maintenance.report'
         ' where wo_r_id=r_id and wo_assigned_by = %s and wo_id is not null'
         ' order by wo_created_time,r_created_time desc'
        )
        cursor.execute(query, (wo_assigned_by,))
    elif wo_assigned_to:
        query = (
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time,'
         'wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id,'
         'wo_technician_remarks, wo_material_used, wo_material_cost, wo_labor_cost, wo_closed_time,'
         ' r_id, r_type, r_description,r_img_url, r_img_url1, r_img_url2,'
         'r_l_id, r_u_id, r_created_time, r_phone,  p_name, u_name, r_priority'
         ' from maintenance.work_order, maintenance.report,'
         'maintenance.properties ,maintenance.units'
         ' where wo_r_id = r_id and  p_id = r_p_id and r_u_id = u_id'
         ' and wo_id is not null  and wo_assigned_to = %s'
         ' order by wo_created_time,r_created_time desc'
        )
        cursor.execute(query, (wo_assigned_to,))
    else:
        cursor.execute(
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time,'
         'wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id,'
         'wo_technician_remarks, wo_material_used, wo_material_cost, wo_labor_cost, wo_closed_time,'
         ' r_id, r_type, r_description,r_img_url, r_img_url1, r_img_url2,'
         'r_l_id, r_u_id, r_created_time, r_phone,  p_name, u_name, r_priority'
         ' from maintenance.work_order, maintenance.report,'
         'maintenance.properties ,maintenance.units'
         ' where wo_r_id = r_id and  p_id = r_p_id and r_u_id = u_id'
         ' and wo_id is not null'
         ' order by wo_created_time,r_created_time desc'
        )
    columns = [col[0] for col in cursor.description]  # Extract column names
    wo_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(wo_data)


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
        wo_status = data.get('wo_status')
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
