from django.contrib.auth.hashers import make_password , check_password
from myapp.models import Clients
from django.forms.models import model_to_dict
import uuid


def createUser(data):
    password = make_password(data.get('password'))
    new_client = Clients(
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

def checkPassword(bodypass , dbpass):
    if check_password(bodypass , dbpass):
        return True
    else:
        return False
    
def createSession(request ,dbuser):
    request.session.clear_expired()
    
    request.session['sessionID'] = str(uuid.uuid1())
    request.session['email'] = dbuser.email
    request.session['ID'] = dbuser.id
    request.session['isAdmin']=dbuser.isAdmin
    # request.session.set_expiry(28800) 

def getUsersProfile(dbuser):
    user_data = model_to_dict(dbuser)
    user_data.pop('password')
    return user_data

def logout(request):
    try:
        request.session.set_expiry(0) 

        del request.session['sessionID']
        del request.session['email']
        del request.session['ID']
        del request.session['isAdmin']
    except Exception as e:
        # print(e)
        pass

