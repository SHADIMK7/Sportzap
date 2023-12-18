import stripe
import os

class Stripe:
    
    stripe.api_key = 'sk_test_51ONT9dSB1nMhPCpjlALhOnjHuPgxdfYIRbk54BGhlmpmT1AuipFXvQnitrUMQDh8KG1nyAEBiDu0LEwGgL9K2iDE00Nkf1Joqf'
    
    def create_token(self, data):
        response = stripe.Token.create(
            card  = {
                "number" : data['number'],
                "exp_month" : data['exp_month'],
                "exp_year" : data['exp_year'],
                "cvc" : data['cvc']
            }
        )
        return response