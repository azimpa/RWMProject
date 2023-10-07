import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv['TWILIO_ACCOUNT_SID'], os.getenv['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.getenv['TWILIO_VERIFY_SERVICE_SID'])


def send(phone_number):
    verify.verifications.create(to=phone_number, channel='sms')


def check(phone_number, code):
    try:
        result = verify.verification_checks.create(to=phone_number, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'
