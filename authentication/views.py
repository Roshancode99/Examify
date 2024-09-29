from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import createUser
from django.db import IntegrityError
from django.http import HttpResponse , JsonResponse
import json
from django.core.exceptions import ValidationError
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
