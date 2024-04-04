# from flask import Flask, request, redirect, url_for
# from flask_mail import Mail, Message
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# from google.auth.transport.requests import Request
# from .. import app

# mail = Mail(app)

# @app.route('/authorize')
# def authorize():
#     flow = Flow.from_client_secrets_file(
#         'client_secret.json',
#         scopes=['https://www.googleapis.com/auth/gmail.send'],
#         redirect_uri=url_for('callback', _external=True),
#     )
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true',
#     )
#     return redirect(authorization_url)

# @app.route('/emailcallback')
# def callback():
#     flow = Flow.from_client_secrets_file(
#         'client_secret.json',
#         scopes=['https://www.googleapis.com/auth/gmail.send'],
#         redirect_uri=url_for('callback', _external=True),
#     )
#     flow.fetch_token(authorization_response=request.url)
#     credentials = flow.credentials
#     # Save the credentials to a secure location for later use
#     return redirect(url_for('send_email'))

# @app.route('/send_email')
# def send_email():
#     if 'credentials' not in session:
#         return redirect(url_for('authorize'))

#     credentials = Credentials.from_authorized_user_info(session['credentials'])

#     message = Message("Subject", sender="your.email@gmail.com", recipients=["recipient@example.com"])
#     message.body = "This is a test email"
#     mail.send(message)
#     return "Email sent!"

