from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import createUser , checkPassword , createSession , getUsersProfile , logout
from django.db import IntegrityError
from django.http import HttpResponse , JsonResponse
import json
from django.core.exceptions import ValidationError , ObjectDoesNotExist
from myapp.models import Clients


# Create your views here.
@csrf_exempt
def register(request):
    msg={"success":False,"message":""}

    if request.method == 'POST':
        data=json.loads(request.body)
        try:
            resultset = createUser(data)
            msg["success"]=True
            msg["message"]=resultset
            return JsonResponse(data=msg,safe=False,status=200)
        except IntegrityError:
            msg["message"]= "Account with this Email already existed."
            return JsonResponse(data=msg, safe=False, status=409)
        except ValidationError as e:
            missing_fields = [field for field , error_list in e.message_dict.items() if 'This field is required.' in error_list]
            if missing_fields:
                msg["message"] = f"Missing required fields: {', '.join(missing_fields)}."
            else:
                msg["message"]="Validation error occurred."
            return JsonResponse(data=msg, safe=False, status=400)
        except Exception as e:
            msg["message"]=str(e)
            return JsonResponse(data=msg , safe=False,status=500)

def getAllUsers(request):
    msg={"success":False,"message": ""}
    if request.method == 'GET':
        try:
            data = Clients.objects.all()
            print("this is should be object as the orm sqlalchemy" , data)
            data = data.values('isAdmin','firstname','lastname','email','isdisabled','createddate','updatedate')
            return JsonResponse(list(data),safe=False,status=200)
        except Exception as e:
            msg["message"]=str(e)
            return JsonResponse(msg,safe=False,status=500)


@csrf_exempt
def auth(request):
    msg={"success":False,"message":""}
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if len(body)<0:
                msg["message"]="recieved blank body!!"
                return JsonResponse(msg,safe=False,status=500)
            

            dbuser = Clients.objects.get(email=body.get("email"))
            request.session.clear_expired()
            if dbuser.isdisabled:
                msg["message"]="Your account is disabled !! Contact your administrator!"
                return JsonResponse(msg,safe=False,status=500)
            
            # if 'email' in request.session.keys() : 
            #     msg["message"]="You are already logged in!!"
            #     return JsonResponse(msg,safe=False,status=409)
            
            result = checkPassword(bodypass=body.get("password") , dbpass=dbuser.password)

            if not result:
                msg["message"]="Invalid password. Check your credentials and attempt login again"
                return JsonResponse(msg,safe=False,status=500)
            
            # if isSessionActive(dbuser.email) :
            #     msg["message"]="User is already Logged in on another machin!!"
            #     return JsonResponse(msg,safe=False,status=409)
            
            createSession(request=request , dbuser=dbuser)
            msg["success"]=True
            msg["message"]=getUsersProfile(dbuser=dbuser)
            return JsonResponse(msg,safe=False,status=200)
        
        except ObjectDoesNotExist as e:
            print("DDDDD", e)
            msg["message"]="User with this email dosen't edits!!"   
            return JsonResponse(msg,safe=False,status=404)

        except Exception as e:
            print(e)
            msg["message"]=str(e)
            return JsonResponse(msg,safe=False,status=500)
    
    if request.method == 'DELETE':
        try:
            logout(request)
            msg["success"]=True
            msg["message"]="user logged out!"
            return JsonResponse(msg,safe=False,status=200)
        except Exception as e:
            logout(request)
            msg["success"]=False  
            msg["message"]="user logged out!"
            return JsonResponse(msg,safe=False,status=500)
       
    return JsonResponse(msg,safe=False,status=500)

