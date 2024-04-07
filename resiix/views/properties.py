from flask import (
    Blueprint, redirect, request, url_for, jsonify
)
from psycopg2.extras import DictCursor
# from werkzeug.exceptions import abort

from resiix.views.db import get_db


bp = Blueprint('properties', __name__, url_prefix='/properties')

@bp.route('/')
def properties():
    db = get_db()
    cursor = db.cursor()

    p_id = request.args.get('p_id')
    p_manager_id = request.args.get('p_manager_id')

    if p_id:
        cursor.execute(
            'SELECT p_id, p_name, p_num_units, p_manager_id, p_country, p_city, p_address, p_zipcode, p_state, p_latitude, p_longitude, p_elevation, p_f_id'
            ' FROM maintenance.properties WHERE p_id = %s', (p_id,)
        )
    elif p_manager_id:
        cursor.execute(
            'SELECT p_id, p_name, p_num_units, p_manager_id, p_country, p_city, p_address, p_zipcode, p_state, p_latitude, p_longitude, p_elevation, p_f_id'
            ' FROM maintenance.properties WHERE p_manager_id = %s', (p_manager_id,)
        )
    else:
        cursor.execute(
            'SELECT p_id, p_name, p_num_units, p_manager_id, p_country, p_city, p_address, p_zipcode, p_state, p_latitude, p_longitude, p_elevation, p_f_id'
            ' FROM maintenance.properties'
        )
    columns = [col[0] for col in cursor.description]  # Extract column names
    property_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(property_data)


@bp.route('/units')
def units():
    db = get_db()
    cursor = db.cursor()

    p_f_id = request.args.get('p_f_id')

    if p_f_id:
        cursor.execute(
            'SELECT p_id,p_name,u_id,u_name,p_f_id'
            ' FROM maintenance.properties,maintenance.units'
            ' WHERE p_f_id = %s', (p_f_id,)
        ) 
    else:
        cursor.execute(
            'SELECT p_id,p_name,u_id,u_name,p_f_id'
            ' FROM maintenance.properties,maintenance.units'
            ' where p_id = units.u_p_id and p_f_id = 1'
        )
    columns = [col[0] for col in cursor.description]  # Extract column names
    property_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    db.close()
    return jsonify(property_data)


@bp.route('/<int:prop_id>/units')
def property_units(prop_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        'SELECT u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id,'
        ' u_code'
        ' FROM maintenance.units WHERE u_p_id = %s', (prop_id,)
    )

    unit_data = cursor.fetchall()
    db.close()
    return jsonify(unit_data)


def get_property_data(p_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=DictCursor)  # Setting dictionary=True to return results as dictionaries
    cursor.execute(
        'SELECT p_f_id, p_id, p_name, p_num_units, p_manager_id, p_country, p_city FROM maintenance.properties WHERE p_id = %s', (p_id,)
    )
    property_data = cursor.fetchone()  # Fetch one row because we're fetching data for a single property
    db.close()
    return property_data


@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.json

        p_name = data.get('p_name')
        p_num_units = data.get('p_num_units')
        p_manager_id = data.get('p_manager_id')
        p_country = data.get('p_country')
        p_city = data.get('p_city')
        p_address = data.get('p_address')
        p_zipcode = data.get('p_zipcode')
        p_state = data.get('p_state')
        p_latitude = data.get('p_latitude')
        p_longitude = data.get('p_longitude')
        p_elevation = data.get('p_elevation')
        p_f_id = 1

        error = None

        if not p_name:
            error = 'Property name is required.'

        if error is not None:
            return jsonify({'error': error}), 400  # Return error response
        else:
            try:
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO maintenance.properties (p_name, p_num_units,'
                    'p_manager_id, p_country, p_city, p_address, p_zipcode,'
                    ' p_state, p_latitude, p_longitude, p_elevation, p_f_id)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (p_name, p_num_units, p_manager_id, p_country,
                     p_city, p_address, p_zipcode, p_state, p_latitude,
                     p_longitude, p_elevation, p_f_id)
                )
                db.commit()
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Return error response
            finally:
                cursor.close()  # Close the cursor
                db.close()  # Close the database connection

        return jsonify({'message': 'Property added successfully'}), 201

    return jsonify({'error': 'Method not allowed'}), 405


# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)



# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))