import requests
from django.conf import settings 

class Paystack():
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY

    base_url = 'https://api.paystack.co/transaction/initialize'

    def make_payment(self,ref, email, amount):

        print('types', ref)
        print('types', type(ref))

        print('types', email)
        print('types', type(email))

        print('types', amount)
        print('types', type(amount))


        url = 'https://api.paystack.co/transaction/initialize'

        headers = {
            "Authorization": "Bearer sk_test_6e23496c50e6c3d7ed4ad7af906e95ff5e37566b",
            "Content-Type": "application/json",
        }

        payload = { 
            "reference": ref,
            "email": email, 
            "amount": amount
        }

        response = requests.post(url=url, json=payload, headers=headers,)


        res = response.json()

        if response.status_code != 200:
            print('FAILEDs')
            print(res.get('message'))
            return res.get('message')

        print('SUCESS')
        print(res)
        print(res.get('data')['reference'])
        # print(res['reference'])
        # print(type(res.get('reference')))
        # print(res)
        return res.get('status')


    def verify_payment(self, ref):
        url = f"https://api.paystack.co/transaction/verify/{str(ref)}"

        headers = {
            "Authorization": "Bearer sk_test_6e23496c50e6c3d7ed4ad7af906e95ff5e37566b",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)

        response_data = response.json()

        
        if response.status_code == 200:
            return response_data['status'], response_data["data"]


        return response_data['status'], response_data['message']



