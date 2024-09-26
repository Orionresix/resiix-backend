from flask import (
    Blueprint, redirect, request, url_for, jsonify
)
from psycopg2.extras import DictCursor
# from werkzeug.exceptions import abort

from resiix.views.db import get_db


bp = Blueprint('eusers', __name__, url_prefix='/eusers')


@bp.route('/')
def properties():
    db = get_db()
    cursor = db.cursor()

    id = request.args.get('id')

    if id:
        cursor.execute(
            'SELECT id, name, phone, email, county, bill1, bill2, bill3,'
            ' fridge, washer, ac, ecooker, inspectionrequest, inspectiondate,'
            ' smsstatus'
            ' FROM ecoumeme.eusers WHERE id = %s', (id,)
        )
    else:
        cursor.execute(
            'SELECT id, name, phone, email, county, bill1, bill2,'
            'bill3, fridge, washer, ac, ecooker, inspectionrequest,'
            ' inspectiondate, smsstatus FROM ecoumeme.eusers'
        )
    columns = [col[0] for col in cursor.description]  # Extract column names
    property_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(property_data)


@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.json

        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        county = data.get('county')
        bill1 = data.get('bill1')
        bill2 = data.get('bill2')
        bill3 = data.get('bill3')
        fridge = data.get('fridge')
        washer = data.get('washer')
        ac = data.get('ac')
        ecooker = data.get('ecooker')
        inspectionrequest = data.get('inspectionrequest')
        inspectiondate = data.get('inspectiondate')
        smsstatus = data.get('smsstatus')

        error = None

        if not bill1:
            error = ' bill is required.'

        if error is not None:
            return jsonify({'error': error}), 400  # Return error response
        else:
            try:
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO ecoumeme.eusers (name, phone, email,'
                    'county, bill1, bill2, bill3, fridge, washer, ac, ecooker,'
                    ' inspectionrequest, inspectiondate, smsstatus)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (name, phone, email, county, bill1, bill2, bill3, fridge,
                     washer, ac, ecooker, inspectionrequest, inspectiondate,
                     smsstatus)
                ) 
                db.commit()
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Return error response
            finally:
                cursor.close()  # Close the cursor
                db.close()  # Close the database connection

        return jsonify({'message': 'user added successfully'}), 201

    return jsonify({'error': 'Method not allowed'}), 405
