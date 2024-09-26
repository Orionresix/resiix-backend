
import africastalking
from flask import current_app, Blueprint, jsonify

bp = Blueprint('sms', __name__, url_prefix='/sms')


class SendSMS:
    def __init__(self, sms_client):
        # Initialize the SMS client (e.g., Africa's Talking)
        self.sms = sms_client

    def sending(self, message, recipients):
        """
        Send an SMS message dynamically.

        :param message: The message to be sent
        :param recipients: A list of recipients in international format
        """
        try:
            # Send the SMS message via the API client
            response = self.sms.send(message, recipients)
            print(response)
            return response
        except Exception as e:
            print(f'Muthoni, we have a problem: {e}')
            return str(e)


def postsms(message, recipients):
    # Access the config values inside the route, where the app context is available
    name = current_app.config['USERNAME']
    key = current_app.config['AFRICA_TALKING_KEY']

    # Initialize Africa's Talking with the config values
    africastalking.initialize(username=name, api_key=key)
    
    # Initialize the SMS service
    sms = africastalking.SMS

    # Create an instance of the SendSMS class and pass the sms_client
    sms_sender = SendSMS(sms)

    # Define the dynamic parameters
    # message = "Hey, this is a test message!"
    # recipients = ["+254701103297"]
    
    # Call the sending method with dynamic parameters
    response = sms_sender.sending(message, recipients)
    
    # Return the response as JSON
    return jsonify({"message": "SMS sent (or attempt logged)!", "response": response})

