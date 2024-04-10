from flask_login import UserMixin

from resiix.views.db import get_db
from flask import (
    Blueprint, request, jsonify
)

bp = Blueprint('technicians', __name__, url_prefix='')


@bp.route('/technicians')
def technician():
    db = get_db()
    cursor = db.cursor()

    query = (
         'SELECT * from users.technicians '
         ' order by t_id desc'
        )
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]  # Extract column names
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(data)