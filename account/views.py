from enum import unique
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
import random
import string
import uuid
import math
from datetime import datetime
from .serializers import *
from django.shortcuts import get_object_or_404
import csv
from .general import General
new_fun = General()


base_date_time = datetime.now()
now = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M"))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logged_in_user(request):
    user_email = request.user.email
    loggedInUser = get_object_or_404(User, email=user_email)
    
    loggedInUserSerial = LoggedInUserSerializer(instance=loggedInUser)
    return Response(data=loggedInUserSerial.data, status=status.HTTP_200_OK)



### Function to create user ###
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    email = request.data.get('email')
    staffname = request.data.get('staffname')
    password = request.data.get('password')
    role = request.data.get('role')
    
    try:
        ## Check if logged in user is super user ##
        ## If it's not super user ##
        if new_fun.check_logged_in_user(request) == False:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "permission denied"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        
        # If it's super user ##
        else:
            if (email == ""):
                data = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "email field can't be empty"
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            elif (staffname == ""):
                data = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "staffname field can't be empty"
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            elif (password == ""):
                data = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "password field can't be empty"
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            elif (role == ""):
                data = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "role field can't be empty"
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        
            else:
                if '@' not in email:
                    data = {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "status": "fail",
                        "reason": "email not correct"
                    }
                    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
                elif User.objects.filter(email=email).exists():
                    data = {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "status": "fail",
                        "reason": "email already used"
                    }
                    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
                elif new_fun.create_user(staffname, email, password, role) == True:
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "reason": "account created successfully"
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                
                else:
                    data = {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "status": "fail",
                        "reason": "invalid role parameter. value should be 'super, credit_officer, branch_manager, senior_manager or agency_bank'"
                    }
                    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    
    except:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid content"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    


### Function to get all the user from the system ###
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user(request):
    if new_fun.check_logged_in_user(request) == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            snippet = User.objects.filter()
        except:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "permission denied"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        all_user = ShowAllUserSerializer(instance=snippet, many=True)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "users": all_user.data
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    
### Function to Delete User ###
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    if new_fun.check_logged_in_user(request) == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if User.objects.filter(id=id).exists():
            del_user = User.objects.filter(id=id)
            del_user.delete()
            data = {
                "code": status.HTTP_200_OK,
                "status": "success"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "User doesn't exist"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        

### Update User ###
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    id = request.user.id
    staffname = request.data.get('staffname')
    if (staffname == ""):
        data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": f'no user with id {id}'
            }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        update_user = User.objects.filter(id=id)
        update_user.update(staffname=staffname)
        data = {
                "code": status.HTTP_200_OK,
                "status": "success"
            }
        return Response(data=data, status=status.HTTP_200_OK)


## Update User Admin ##
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_admin(request, id):
    staffname = request.data.get('staffname')
    role = request.data.get('role')
    if new_fun.check_logged_in_user(request) == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif User.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "User doesn't Exists"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if new_fun.upadate_user_admin(id, staffname, role) == False:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "invalid role parameter. value should be 'super, credit_officer, branch_manager, senior_manager or agency_bank'"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            new_fun.upadate_user_admin(id, staffname, role)
            data = {
                "code": status.HTTP_200_OK,
                "status": "successfull",
                "reason": "record updated"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        
## Reset Password ##
@api_view(['POST'])
@permission_classes([])
def reset_password_otp(request):
    email = request.data.get('email')
    if '@' not in email:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "email not correct"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif User.objects.filter(email=email).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Email or User doesn't Exists"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if Otp.objects.filter(email=email).exists() == True:
            delt_otp = Otp.objects.filter(email=email)
            delt_otp.delete()
            new_fun.create_otp(email)
            data = {
                "code": status.HTTP_200_OK,
                "status": "successfull",
                "reason": "Check Your registerd email for OTP to reset your account"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            new_fun.create_otp(email)
            data = {
                "code": status.HTTP_200_OK,
                "status": "successfull",
                "reason": "Check Your registerd email for OTP to reset your account"
            }
            return Response(data=data, status=status.HTTP_200_OK)

## Reset password confirm ##
@api_view(['POST'])
@permission_classes([])
def reset_password_confirm(request):
    otp_code = request.data.get('otp_code')
    password = request.data.get('password')
    re_password = request.data.get('re_password')
    if otp_code == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "OTP Required"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif password == "" or re_password == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Password Required"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif password == re_password:
        if Otp.objects.filter(otp_code=otp_code).exists():
            if new_fun.check_otp(otp_code) == False:
                Otp.objects.filter(otp_code=otp_code).delete()
                data = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "OTP Expired"
                }
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                o = get_object_or_404(Otp, otp_code=otp_code)
                u = User.objects.get(email=o.email)
                u.set_password(password)
                u.save()
                Otp.objects.filter(otp_code=otp_code).delete()
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "successfull",
                    "reason": "password reset sucessfully"
                }
                return Response(data=data, status=status.HTTP_200_OK)
        
        else:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Invalid OTP"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    
    else:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Password Missmatch"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)