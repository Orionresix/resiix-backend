from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
    jsonify, json
)
# from werkzeug.security import check_password_hash, generate_password_hash
# from .db import get_db
# from .user import User
# from config import GOOGLE_CLIENT_ID, GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_SECRET
# from flask_login import (
#     LoginManager,
#     login_required,
#     login_user,
#     logout_user,
#     current_user
# )
# from oauthlib.oauth2 import WebApplicationClient
# import requests
# import jwt


auth_bp = Blueprint('auth', __name__)

# login_manager = LoginManager()

# # OAuth 2 client setup
# client = WebApplicationClient(GOOGLE_CLIENT_ID)


# # Flask-Login helper to retrieve a user from our db
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)



# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()




# @auth_bp.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method ==  "GET":        
#     # Find out what URL to hit for Google login
#         google_provider_cfg = get_google_provider_cfg()
#         authorization_endpoint = google_provider_cfg["authorization_endpoint"]

#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#         request_uri = client.prepare_request_uri(
#             authorization_endpoint,
#             redirect_uri=request.base_url + "/callback",
#             scope=["openid", "email", "profile"],
#         )
#         return redirect(request_uri)

# @auth_bp.route("/login/callback", methods=["GET", "POST"])
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")
#     # Find out what URL to hit to get tokens that allow you to ask for
# # things on behalf of a user
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#     # Prepare and send a request to get tokens! Yay tokens!
#     token_url, headers, body = client.prepare_token_request(
#      token_endpoint, authorization_response=request.url,
#      redirect_url=request.base_url,
#      code=code
#     )
#     token_response = requests.post(
#      token_url,
#      headers=headers,
#      data=body,
#      auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )

# # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))
# # Now that you have tokens (yay) let's find and hit the URL
# # from Google that gives you the user's profile information,
# # including their Google profile image and email
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#     # You want to make sure their email is verified.
# # The user authenticated with Google, authorized your
# # app, and now you've verified their email through Google!
#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
#     # Create a user in your db with the information provided
# # by Google
#     user = User(
#      id_=unique_id, name=users_name, email=users_email, profile_pic=picture
#     )

# # Doesn't exist? Add it to the database.
#     if not User.get(unique_id):
#         User.create(unique_id, users_name, users_email, picture)

#         # Generate JWT token
#     jwt_token = jwt.encode({'email': users_email}, 'your_secret_key',
#                             algorithm='HS256')
    

# # Begin user session by logging the user in
#     login_user(user)

# # Send user back to homepage
#      # Return JWT token as JSON
#     #return jsonify({'token': jwt_token})

#     return redirect(url_for("auth.index"))


# @auth_bp.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("auth.index"))


# @auth_bp.route("/")
# def index():
#     if current_user.is_authenticated:
#         # Set user data in session (example)
#         session['user_id'] = current_user.id
#         session['user_email'] = current_user.email
#         session['user_name'] = current_user.name
#         return redirect("http://localhost:3000/dashboard/home")
#         #return current_user.redirect(url_for)

#     else:
#         #return redirect("http://localhost:3000")
#         return redirect(url_for("auth.login"))
    
# @auth_bp.route("/profile")
# def profile():
#     if 'user_id' not in session:
#         return redirect(url_for("auth.index"))
   
#     return  session['user_email']






# @auth_bp.route('/user_details')
# def get_user_details():
#     if current_user.is_authenticated:
#         user_email = current_user.email
#         user_name = current_user.name
#         profile_pic = current_user.profile_pic  # Assuming current_user object contains user details
#         return jsonify({'email': user_email, 'name': user_name, 'profile_pic': profile_pic})
#     else:
#         user_email = 'unknown@gmail.com'
#         user_name = 'notme'
#         user_id = 1
#         f_id = 1
#         return jsonify({'email': user_email, 'name': user_name, 'id': user_id, 'f_id': f_id})
#         #return jsonify({'error': 'User not authenticated'}), 401
    

# def get_user(current_user):
#     if current_user.is_authenticated:
#         db = get_db()
#         cursor = db.cursor(cursor_factory=DictCursor)  # Setting dictionary=True to return results as dictionaries
#         cursor.execute(
#         'SELECT p_f_id, p_id, p_name, p_num_units, p_manager_id, p_country, p_city FROM maintenance.properties WHERE p_id = %s', (p_id,)
#         )
#         current_user_data = cursor.fetchone()  # Fetch one row because we're fetching data for a single property
#         db.close()
#         return current_user_data



#         cursor = db.cursor()
#         user_email = current_user.email

#         if user_email:
#             cursor.execute(
#                 'SELECT * '
#                 ' FROM users.user WHERE email = %s', (user_email,)
#             )
#         user_details = cursor.fetchall()
#         db.close()
#         return jsonify(user_details)







# @auth_bp.route('/users')
# def users():
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute(
#         'SELECT id, created_at, update_at, username, email '
#         'FROM users.users'
#     )
#     user_data = cursor.fetchall()
#     db.close()
#     return jsonify(user_data)


# @auth_bp.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))

#         flash(error)
#     return "User created successfully", 201


# @auth_bp.route('/oldlogin', methods=('GET', 'POST'))
# def oldlogin():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None
#         user = db.execute(
#             'SELECT * FROM user WHERE username = ?', (username,)
#         ).fetchone()

#         if user is None:
#             error = 'Incorrect username.'
#         elif not check_password_hash(user['password'], password):
#             error = 'Incorrect password.'

#         if error is None:
#             session.clear()
#             session['user_id'] = user['id']
#             return redirect(url_for('index'))

#         flash(error)

#     return render_template('auth/login.html')


# @auth_bp.route('/tenantloginNghojh', methods=['POST'])
# def tenantlogifghgfnn():

#     db = get_db()
#     cursor = db.cursor()

#     if request.method == 'POST':
#         username = request.form.get('email')
#         passcode = request.form.get('passcode')
        
#         if not username or not passcode:
#             return jsonify({'error': 'Email and passcode are required.'}), 400

#         cursor.execute(
#             'SELECT * FROM maintenance.units WHERE UPPER(u_name) = UPPER(?)',
#             (username,)
#         )
#         userdata = cursor.fetchone()

#         if userdata is None:
#             return jsonify({'error': 'Incorrect Unit code.'}), 400

#         if passcode and userdata['passcode'] == passcode:
#             unitdetails = userdata
#             return jsonify(unitdetails)

#         return jsonify({'error': 'Incorrect passcode.'}), 400

#     return jsonify({'error': 'Method not allowed.'}), 405


# @auth_bp.route('/tenantlogin', methods=('GET', 'POST'))
# def tenantlogin():
#     db = get_db()
#     cursor = db.cursor()

#     unitcode = request.args.get('email')
#     passcode = request.args.get('passcode')

#     query = None
#     wo_data = None

#     if passcode:
#         query = (
#              'SELECT * FROM maintenance.units,maintenance.leases,maintenance.properties'
#              ' WHERE l_u_id=units.u_id and u_p_id=p_id and UPPER(u_name) = UPPER(%s)'
#              'and  UPPER(passcode) = UPPER(%s)'
#             )
#     if query:
#         cursor.execute(query, (unitcode, passcode,))
#         row = cursor.fetchone()
#         if row:
#             columns = [col[0] for col in cursor.description]
#             wo_data = dict(zip(columns, row))
#         db.close()
#     return jsonify(wo_data)


# @auth_bp.route('/tenantinfo', methods=('GET', 'POST'))
# def tenantinfo():
#     db = get_db()
#     cursor = db.cursor()

#     unitcode = request.args.get('u_id')

#     query = None
#     wo_data = None

#     if unitcode:
#         query = (
#              'SELECT * FROM maintenance.units,maintenance.leases,maintenance.properties'
#              ' WHERE l_u_id=units.u_id and u_p_id=p_id and u_id = %s'
#             )
#     if query:
#         cursor.execute(query, (unitcode, ))
#         row = cursor.fetchone()
#         if row:
#             columns = [col[0] for col in cursor.description]
#             wo_data = dict(zip(columns, row))
#         db.close()
#     return jsonify(wo_data)