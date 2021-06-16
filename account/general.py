from django.shortcuts import get_object_or_404
from .models import *
import random
import string
from .send_email import Email

sendMail = Email()

class General:
    
    def check_logged_in_user(self, request):
        if request.user.is_superuser == True:
            return True
        else:
            return False
        

    def create_user(self, staffname, email, password, role):
        T = 5
        res = ''.join(random.choices(string.digits, k=T))
        b_id = str(res)
        staffid = "HCDTI" + b_id
        if (role == 'super'):
            create = User.objects.create_user(email=email, staffname=staffname, staffid=staffid, password=password, is_superuser=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'credit_officer'):
            create = User.objects.create_user(email=email, staffname=staffname, staffid=staffid, password=password, is_credit_officer=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'branch_manager'):
            create = User.objects.create_user(email=email, staffname=staffname, staffid=staffid, password=password, is_branch_manager=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'senior_manager'):
            create = User.objects.create_user(email=email, staffname=staffname, staffid=staffid, password=password, is_senior_manager=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'agency_bank'):
            create = User.objects.create_user(email=email, staffname=staffname, password=password, staffid=staffid, is_agency_bank=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        else:
            return False