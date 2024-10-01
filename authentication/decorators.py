from functools import wraps
import time
from django.contrib.sessions.models import Session
from django.http import JsonResponse

def checkSession(func):
    @wraps(func)
    def wrapper(*args , **kwargs):
        msg={"success":False,"message":"Unauthorised. Please login or register first!"}

        args[0].session.clear_expired()
        if 'ID' not in args[0].session.keys():
            return JsonResponse(msg,safe=False,status=401)
        else:
            try:
                s = Session.objects.get(pk=args[0].session.session_key)   
                if len(s.get_decoded().keys())>0:
                    result = func(*args, **kwargs)
                    return result
                else :
                    return JsonResponse(msg,safe=False, status=403)  

            except Exception as e :
                print(e)
                return JsonResponse(msg,safe=False, status=400)               
                               
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        msg={"success":False,"message":""}
        if request.session.get('isAdmin',False):
            return view_func(request, *args, **kwargs)
        else:
            msg["success"]=False
            msg["message"]="You do not have permission to access this resource. Pls contact the administrator if you believe this is an error."
            return JsonResponse(msg,safe=False,status=403)
    
    return _wrapped_view