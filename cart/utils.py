import requests
import logging
import uuid

from decouple import config


class PesaPalGateway:
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    payment_url = None
    notification_id = None
    register_ipn_url = None
    base_url = None

    def __init__(self):
        self.consumer_key = config("PESAPAL_CONSUMER_KEY")
        self.consumer_secret = config("PESAPAL_CONSUMER_SECRET")
        self.access_token_url = config("PESAPAL_ACCESS_TOKEN_URL")
        self.payment_url = config("PESAPAL_PAYMENT_URL")
        self.register_ipn_url = config("PESAPAL_REGISTER_IPN_URL")
        self.base_url = config("BASE_URL")

    def getAuthorizationToken(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }

        try:
            res = requests.post(self.access_token_url, headers=headers, json=payload)

        except Exception as err:
            logging.error("Error {}".format(err))

        else:
            token = res.json()["token"]
            return token

    def get_notification_id(self):
        token = self.getAuthorizationToken()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer %s" % token
        }


        payload = {
            "url": "https://www.pichasafari.co.ke/pesapal/payment-ipn", #Your IPN URL
            "ipn_notification_type": "GET"
        }


        try:
            res = requests.post(self.register_ipn_url, headers=headers, json=payload)

            notification_id =  res.json()["ipn_id"]

            return notification_id

        except Exception as err:
            logging.error("Error {}".format(err))


    def make_payment(self, cart_id, phonenumber, email, amount, currency, callback_url):
        token = self.getAuthorizationToken()

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % token
        }

        data = {
            "id": cart_id,
            "currency": currency,
            "amount": amount,
            "description": "Picha Safari Cart Payment",
            "callback_url": callback_url,
            "notification_id": self.get_notification_id(),
            "billing_address": {
                "phone_number": phonenumber,
                "email_address": email,
            }
        }

        try:
            res = requests.post(self.payment_url, headers=headers, json=data)
            response = res.json()

            return response
        except:
            raise Exception("An error occured-Utils.py")

