# Django
import random
import string
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

# Local Django
#from webapp.models import CustomerDetails

def username_generator(last_name):
    return last_name+get_random_string(length=2, allowed_chars='0123456789')

def password_generator():
    return get_random_string(length=8)

def create_approved_user(username, password):

    approved_user = User.objects.create_user(username, None, password)
    return approved_user
