# Django
import random
import string
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db.models import Sum

#Local Django
from webapp.models import *

def username_generator(last_name):
    return last_name+get_random_string(length=2, allowed_chars='0123456789')

def password_generator():
    return get_random_string(length=8, allowed_chars='AaBbCcDdEeFfggHhIiJj0123456789')

def create_approved_user(username, password):

    approved_user = User.objects.create_user(username, None, password)
    return approved_user


def update_customer_facility(customer_id, facility_name):

    customer_instance = CustomerDetails.objects.get(customer_id=customer_id)
    facility_instance = Facilities.objects.get(facility_name=facility_name)       
    customer_facility = CustomerFacility.objects.create(customer=customer_instance, facility=facility_instance)
    
    return customer_facility.save()


def customer_percentage_paid(customer_id, subscription_cost=1000):
            
    # The subscription  an assumed customer subscription cost

    customer_payments = CustomerPayments.objects.filter(customer_id=customer_id)
    all_payments = customer_payments.aggregate(sum=Sum('amount_paid'))
    total_paid = all_payments['sum'] 

    if total_paid is not None:
        total_percentage_payment =  (total_paid / subscription_cost) * 100
    else:
        total_percentage_payment = 0
        
    return total_percentage_payment