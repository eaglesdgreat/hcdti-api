import requests
from decouple import config


urls = config('SMS_BASE_URL')
api_token = config('SMS_TOKEN')
mfrom = 'JUST USSD'

"""
Class that Handle everything 
related to sending of email out 
to user and and customer
"""


class SMS:
    #Send SMS Function #
    def SendSMS(self, mobile, msg):
        url = f'{urls}/api/v1/sms/create?api_token={api_token}&from={mfrom}&to={mobile}&body={msg}'

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response
