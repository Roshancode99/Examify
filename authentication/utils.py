from django.contrib.auth.hashers import make_password , check_password
from myapp.models import Client
from django.forms.models import model_to_dict


def createUser(data):
    password = data.get('password')
    new_client = Client(
        isAdmin = data.get('isAdmin' , False),
        password = password,
        firstname = data.get('firstname'),
        lastname = data.get('lastname'),
        email = data.get('email')
    )
    new_client.save()
    resultset = model_to_dict(new_client)
    resultset.pop('password')
    return resultset