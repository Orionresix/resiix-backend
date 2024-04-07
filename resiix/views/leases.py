from flask import (
    Blueprint, flash, g, redirect, request, url_for, jsonify
)
from psycopg2.extras import DictCursor
from werkzeug.exceptions import abort

from resiix.views.auth import login_required

from resiix.views.db import get_db

from .. import app

bp = Blueprint('leases', __name__)
@bp.route('/leases')
def properties():
    db = get_db()
    cursor = db.cursor()

    l_id = request.args.get('l_id')
    l_u_id = request.args.get('l_u_id')

    if l_id:
        cursor.execute(
         'SELECT  l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name,'
         ' l_code, l_email, l_phone, l_secondary_phone, l_national_id'
         'from maintenance.leases  WHERE l_id = %s', (l_id,)
        )
    elif l_u_id:
        cursor.execute(
         'SELECT  l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name,'
         ' l_code, l_email, l_phone, l_secondary_phone, l_national_id'
         'from maintenance.leases  WHERE l_u_id = %s', (l_u_id,)
        )
    else:
        cursor.execute(
         'SELECT  l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name,'
         ' l_code, l_email, l_phone, l_secondary_phone, l_national_id'
         'from maintenance.leases'
        )
    lease_data = cursor.fetchall()
    db.close()
    return jsonify(lease_data)


def get_lease_data(l_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=DictCursor)
    cursor.execute(
        'SELECT  l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name,'
        ' l_code, l_email, l_phone, l_secondary_phone, l_national_id'
        'from maintenance.leases WHERE u_id = %s', (l_id,)
    )
    lease_data = cursor.fetchone()
    db.close()
    return lease_data
