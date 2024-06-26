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
from django.db.models import Q
from datetime import datetime
from .serializers import *
from django.shortcuts import get_object_or_404
import csv
from .input import Input
from .general import General
new_fun = General()
newInput = Input()


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_user(request, id):
    if new_fun.check_logged_in_user(request) == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            u = get_object_or_404(User, id=id)
            serialize = LoggedInUserSerializer(instance=u)
            return Response(data=serialize.data, status=status.HTTP_200_OK)

        except:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "User Not found"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


"""Create Group Function"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    group_name = request.data.get("groupName")
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can create Group"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif group_name == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Group Name can not be empty"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif Groups.objects.filter(group_name=group_name).exists():
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Group Name already exist"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        """Call the create function"""
        new_fun.create_group(group_name)
        data = {
            "code": status.HTTP_200_OK,
            "status": "successfull",
            "reason": "Group Created"
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Get all the Group"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_group(request):

    all_groups = []
    show = Groups.objects.filter()
    for i in show:
        total_member = GroupMember.objects.filter(groups_id=i.group_id).count()
        """get The Member"""
        try:
            grp_m = get_object_or_404(
                GroupMember, groups_id=i.group_id, is_leader=True)
            # grp_m = GroupMember.objects.filter(groups_id=i.group_id, is_leader=True)
            # finals = new_fun.get_group_leader(i.group_id)

            # if grp_m.is_leader == False: continue
            datas = {}
            datas['id'] = i.id
            datas['groupId'] = i.group_id
            datas['groupName'] = i.group_name
            datas['dateCreated'] = i.date_created
            datas['totalMember'] = total_member
            datas['leaderKey'] = grp_m.id
            datas['leaderName'] = grp_m.member_name
            datas['mobileNumber'] = grp_m.mobile_number
            datas['active'] = i.active
        except:
            datas = {}
            datas['id'] = i.id
            datas['groupId'] = i.group_id
            datas['groupName'] = i.group_name
            datas['dateCreated'] = i.date_created
            datas['totalMember'] = total_member
            datas['active'] = i.active
            datas['leaderName'] = None
            datas['mobileNumber'] = None
        all_groups.append(datas)

    """Paginate the Response"""
    # paginator = PageNumberPagination()
    # paginator.page_size = 5
    # result_page = paginator.paginate_queryset(all_groups, request)
    return Response(data=all_groups, status=status.HTTP_200_OK)


"""Add Member to Group"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member_to_group(request):
    groupId = request.data.get("groupId")
    memberName = request.data.get("memberName")
    mobileNumber = request.data.get("mobileNumber")
    isLeader = request.data.get("isLeader")
    print(request.user.is_superuser)
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can Add Member to Group"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif type(isLeader) != bool or isLeader == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Is Leader Field must be boolean true or False"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif GroupMember.objects.filter(mobile_number=mobileNumber, groups_id=groupId).exists():
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "This Customer already belong to this group"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif GroupMember.objects.filter(mobile_number=mobileNumber).exists():
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "This Customer already belong to one HCDTI's group"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif Groups.objects.filter(group_id=groupId).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Group ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif GroupMember.objects.filter(is_leader=True).exists() and isLeader == True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Group already have Leader. Group can not have more than one leader"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        new_fun.add_member_group(groupId, memberName, mobileNumber, isLeader)

        data = {
            "code": status.HTTP_200_OK,
            "status": "successfull",
            "reason": f'Member added to {groupId} Group'
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Get All Member of the Group"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_group_member(request):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        all_member = []
        group_member = GroupMember.objects.filter()
        for i in group_member:
            datas = {}
            grp = get_object_or_404(
                Groups, id=i.group_id, group_id=i.groups_id)
            datas['id'] = i.id
            datas['groupId'] = i.groups_id
            datas['groupName'] = grp.group_name
            datas['memberName'] = i.member_name
            datas['mobileNumber'] = i.mobile_number
            datas['isLeader'] = i.is_leader
            datas['dateJoined'] = i.date_added
            all_member.append(datas)

        """Paginate the response"""
        # paginator = PageNumberPagination()
        # paginator.page_size = 5
        # result_page = paginator.paginate_queryset(all_member, request)
        return Response(data=all_member, status=status.HTTP_200_OK)


"""Delete Group"""


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_group(request, id):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif Groups.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Group ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        del_grp = Groups.objects.filter(id=id)
        del_grp.delete()
        data = {
            "code": status.HTTP_200_OK,
            "status": "successfull",
            "reason": "Group Removed"
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Update Group"""


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_group(request, id):
    groupName = request.data.get("groupName")
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif Groups.objects.filter(group_name=groupName).exists():
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Group Name already exist in the system"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif groupName == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Group name can not be empty"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif Groups.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Group ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        """Update Group name"""
        upd_grp = Groups.objects.filter(id=id)
        upd_grp.update(group_name=groupName)
        data = {
            "code": status.HTTP_200_OK,
            "status": "successfull",
            "reason": "Group Updated"
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Get Group by ID"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_group(request, id):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif Groups.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        try:
            grp = get_object_or_404(Groups, id=id)
            grm = get_object_or_404(GroupMember, group_id=id, is_leader=True)
            data = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "result": {
                    "groupId": grp.group_id,
                    "groupName": grp.group_name,
                    "active": grp.active,
                    "groupLeader": grm.member_name,
                    "dateCreated": grp.date_created
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            data = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "result": {
                    "groupId": grp.group_id,
                    "groupName": grp.group_name,
                    "active": grp.active,
                    "groupLeader": None,
                    "dateCreated": grp.date_created
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)


"""Remove Member from the Group"""


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_member(request, id):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif GroupMember.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        grpm = GroupMember.objects.filter(id=id)
        grpm.delete()

        data = {
            "code": status.HTTP_200_OK,
            "status": "successfull",
            "reason": "Member Removed"
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Get A Group and all the Member in the group"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_member(request, group_id):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif Groups.objects.filter(group_id=group_id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Group ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        grp = get_object_or_404(Groups, group_id=group_id)
        members = []
        allmember = GroupMember.objects.filter(
            groups_id=group_id, group_id=grp.id)
        for i in allmember:
            datas = {}
            datas['id'] = i.id
            datas['memberName'] = i.member_name
            datas['mobileNumber'] = i.mobile_number
            datas['isLeader'] = i.is_leader
            datas['dateJoined'] = i.date_added
            members.append(datas)

        # paginator = PageNumberPagination()
        # paginator.page_size = 5
        # result_page = paginator.paginate_queryset(members, request)
        try:
            grm = get_object_or_404(GroupMember, group_id=grp.id, is_leader=True)
            data = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "groupName": grp.group_name,
                "groupId": grp.group_id,
                "groupActive": grp.active,
                "groupLeader": grm.member_name,
                "result": members
            }

            return Response(data=data, status=status.HTTP_200_OK)
        except:
            data = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "groupName": grp.group_name,
                "groupId": grp.group_id,
                "groupActive": grp.active,
                "groupLeader": None,
                "result": members
            }

            return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member_info(request, id):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        resp = new_fun.get_single_user_info(id)
        return(resp)


"""Update Customer Group Membership"""


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_member(request, id):
    memberName = request.data.get("memberName")
    nameOfHusband = request.data.get("nameOfHusband")
    nextOfKin = request.data.get("nextOfKin")
    nextOfKinMobile = request.data.get("nextOfKinMobile")
    custEduLevel = request.data.get("custEduLevel")
    residentAddress = request.data.get("residentAddress")
    busAddress = request.data.get("busAddress")
    maritalStatus = request.data.get("maritalStatus")
    typeOfBus = request.data.get("typeOfBusiness")
    durationOfBus = request.data.get("durationOfBusiness")
    familyOnHcdtiGroup = request.data.get("familyOnHcdtiGroup")
    savingsInPassbook = request.data.get("savingsInPassbook")
    bank = request.data.get("bank")
    accountNo = request.data.get("accountNo")
    memberOwningMfi = request.data.get("memberOwningMfi")
    mfiName = request.data.get("mfiName")
    guarantor = request.data.get("guarantor")
    guarantorRel = request.data.get("guarantorRelationship")
    guarantorAddress = request.data.get("guarantorAddress")
    guarantorOfficeAddress = request.data.get("guarantorOfficeAddress")
    groupRecommendation = request.data.get("groupRecommendation")

    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    # elif GroupMember.objects.filter(id=id, mobile_number=mobileNumber).exists():
    #     data = {
    #         "code": status.HTTP_401_UNAUTHORIZED,
    #         "status": "fail",
    #         "reason": "Mobile Number already Exist in that group"
    #     }
    #     return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif memberName == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Member Name can not be empty"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif type(familyOnHcdtiGroup) != bool and type(memberOwningMfi) != bool:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Family on HCDTI field and Member Owning MFI's must be Boolean (True/False)"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif memberOwningMfi == True and mfiName == "":
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Please Kindly Type the name of MFIs You are owning"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    
    elif GroupMember.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        upd_m = GroupMember.objects.filter(id=id)
        ginfo = GroupMemberInfo.objects.filter(group_member=id)
        upd_m.update(member_name=memberName)
        ginfo.update(name_of_husband=nameOfHusband, next_of_kin=nextOfKin, next_of_kin_mobile=nextOfKinMobile, cust_edu_level=custEduLevel,
                     resident_addr=residentAddress, bus_addr=busAddress, marital_status=maritalStatus, type_of_bus=typeOfBus, 
                     duration_of_bus=durationOfBus, family_on_hcdti_group=familyOnHcdtiGroup, savings_in_passbook=savingsInPassbook,
                     bank=bank, account_no=accountNo, member_owning_mfi=memberOwningMfi, mfi_name=mfiName, guarantor=guarantor, 
                     guarantor_rel=guarantorRel, guarantor_addr=guarantorAddress, guarantor_office_addr=guarantorOfficeAddress,
                     group_recomm=groupRecommendation)
        
        data = {
            "code": status.HTTP_200_OK,
            "status": "successfull",
            "reason": "Member Updated"
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Activate/Deactivate group"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def groupAction(request, groupid):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            grp = get_object_or_404(Groups, group_id=groupid)
            instance = Groups.objects.filter(group_id=groupid)
            if grp.active == True:
                instance.update(active=False)
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "successfull",
                    "reason": "Group Deactivated"
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                instance.update(active=True)
                data = {
                    "code": status.HTTP_200_OK,
                    "status": "successfull",
                    "reason": "Group Activated"
                }
                return Response(data=data, status=status.HTTP_200_OK)
        except:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Invalid Group ID"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


"""Get Group Member by ID"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_member(request, id):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif GroupMember.objects.filter(id=id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    else:
        mem = get_object_or_404(GroupMember, id=id)
        grp = get_object_or_404(Groups, group_id=mem.groups_id)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "result": {
                "memberId": mem.id,
                "groupId": mem.groups_id,
                "groupName": grp.group_name,
                "memberName": mem.member_name,
                "mobileNumber": mem.mobile_number,
                "isLeader": mem.is_leader,
                "dateAdded": mem.date_added
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Change Group Leader"""


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_group_leader(request, group_id, mobileNumber):
    if request.user.is_credit_officer == False and request.user.is_superuser is not True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Permission Denied. Only Super Admin and Credit Officer can perform group management"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif Groups.objects.filter(group_id=group_id).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Group ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    elif GroupMember.objects.filter(groups_id=group_id, mobile_number=mobileNumber).exists() == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "User is not a group member or does not exist"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    elif GroupMember.objects.filter(groups_id=group_id, mobile_number=mobileNumber, is_leader=True).exists():
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "This Member is already the leader of this group"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        """Unset the Old Leader"""
        old = GroupMember.objects.filter(groups_id=group_id)
        old.update(is_leader=False)

        """Set the New Leader"""
        new_leader = GroupMember.objects.filter(
            groups_id=group_id, mobile_number=mobileNumber)
        new_leader.update(is_leader=True)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "reason": "New Group Leader Set"
        }
        return Response(data=data, status=status.HTTP_200_OK)


"""Admin Reset Password"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_reset_password(request, id):
    new_password = request.data.get('new_password')
    re_password = request.data.get('re_password')
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
            "reason": "User does not exist"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        if new_password == re_password:
            u = User.objects.get(id=id)
            u.set_password(new_password)
            u.save()
            data = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "reason": "Password Reset Successfully"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Password Miss-Match"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


"""Create loan for existing customer"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def oldCustomerBookLoan(request):
    if request.user.is_credit_officer == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        """Call the Input Fields"""
        data = newInput.oldLoanInput(request)
        resp = new_fun.createLoanExistingCustomer(request, data)
        return resp


"""Create Loan for new customer"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newCustomerBookLoan(request):
    if request.user.is_credit_officer == False:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        """Call the Input Fields"""
        data = newInput.newLoanInput(request)
        resp = new_fun.createLoanNewCustomer(request, data)
        return resp


"""Get all the loan application"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allLoan(request):
    while request.user.is_credit_officer == True or request.user.is_branch_manager == True:
        snipet = LoanApplication.objects.filter(Q(credit_officer_approve='APPROVED', branch_manager_approve='PENDING') | Q(
            credit_officer_approve='APPROVED', branch_manager_approve='APPROVED') | Q(credit_officer_approve='APPROVED', branch_manager_approve='DECLINED'))
        datas = ShowAllLoanApplication(instance=snipet, many=True)
        
        resp = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "result": datas.data
        }
        return Response(data=resp, status=status.HTTP_200_OK)

    else:
        if request.user.is_senior_manager == True:
            snipet = LoanApplication.objects.filter(Q(credit_officer_approve='APPROVED', branch_manager_approve='APPROVED') | Q(
                senior_manager_approve='APPROVED') | Q(senior_manager_approve='DECLINED'))
            datas = ShowAllLoanApplication(
                instance=snipet, many=True)
            resp = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "result": datas.data
            }
            return Response(data=resp, status=status.HTTP_200_OK)

        elif request.user.is_agency_bank == True:
            snipet = LoanApplication.objects.filter(
                Q(credit_officer_approve='APPROVED', branch_manager_approve='APPROVED', senior_manager_approve='APPROVED'))
            datas = ShowAllLoanApplication(
                instance=snipet, many=True)
            resp = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "result": datas.data
            }
            return Response(data=resp, status=status.HTTP_200_OK)

        else:
            snipet = LoanApplication.objects.filter()
            datas = ShowAllLoanApplication(
                instance=snipet, many=True)
            resp = {
                "code": status.HTTP_200_OK,
                "status": "success",
                "result": datas.data
            }
            return Response(data=resp, status=status.HTTP_200_OK)


"""Approve Loan"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approveloan(request, appId):
    if request.user.is_superuser == True:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        resp = new_fun.approve_loan(request, appId)
        return resp


"""Loan Repayment"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def repayloan(request, appid):
    amount = request.data.get('amount')
    while request.user.is_superuser == True or request.user.is_agency_bank == True:
        if amount == "":
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Amount field can't be empty"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        else:
            resp = new_fun.loanRepayment(appid, amount)
            return resp
    else:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "permission denied"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


"""Get single Loan by ID"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSingleLoan(request, appid):
    try:
        snippet = LoanApplication.objects.get(application_id=appid)
        
        datas = ShowAllLoanApplication(instance=snippet)
        resp = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "result": datas.data
        }
        return Response(data=resp, status=status.HTTP_200_OK)
    except:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Application ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    
"""Remove/Delete Loan"""
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeloan(request, appid):
    try:
        loans = get_object_or_404(LoanApplication, application_id=appid)
        instance = LoanApplication.objects.filter(application_id=appid)
        if request.user.is_credit_officer == False and request.user.is_superuser is not True:
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Permission Denied. Only Super Admin and Credit Officer Remove/Delete Loan"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        elif loans.senior_manager_approve == "APPROVED" or loans.agency_bank_approve == "APPROVED":
            data = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Loan Application can't be removed because it has been approve by Senior Manager or Agency Banking"
            }
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            instance.delete()
            data = {
                "code": status.HTTP_200_OK,
                "status": "successfull",
                "reason": "Loan Deleted"
            }
            return Response(data=data, status=status.HTTP_200_OK)
            
    except:
        data = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "status": "fail",
            "reason": "Invalid Application ID"
        }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getAllMember(request):
#     show = GroupMember.objects.filter()
    
#     lists = []
#     for i in show:
#         gp = get_object_or_404(Groups, group_id=i.groups_id)
#         datas = {}
#         datas['id'] = i.id
#         datas['Name'] = i.member_name
#         datas['groupName'] = gp.group_name
#         datas['groupId'] = gp.group_id
#         datas['mobileNo'] = i.mobile_number
#         datas['dateJoin'] = i.date_added
#         lists.append(datas)
#     return Response(data=lists, status=status.HTTP_200_OK)
        
        