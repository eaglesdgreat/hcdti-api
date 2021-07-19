from django.shortcuts import get_object_or_404
from .models import *
import random
import string
from django.utils import timezone
from datetime import timedelta
from .send_email import Email

sendMail = Email()

max_loan = 40000.0
min_loan = 20000.0



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
            create = User.objects.create_user(
                email=email, staffname=staffname, staffid=staffid, password=password, is_superuser=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'credit_officer'):
            create = User.objects.create_user(
                email=email, staffname=staffname, staffid=staffid, password=password, is_credit_officer=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'branch_manager'):
            create = User.objects.create_user(
                email=email, staffname=staffname, staffid=staffid, password=password, is_branch_manager=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'senior_manager'):
            create = User.objects.create_user(
                email=email, staffname=staffname, staffid=staffid, password=password, is_senior_manager=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        elif (role == 'agency_bank'):
            create = User.objects.create_user(
                email=email, staffname=staffname, password=password, staffid=staffid, is_agency_bank=True, is_staff=True)
            create.save()
            sendMail.welcome(email, staffname, password)
            return True
        else:
            return False

    def upadate_user_admin(self, id, staffname, role):
        u = get_object_or_404(User, id=id)

        # Super User #
        if (role == ""):
            pass

        elif (role == 'super'):
            if u.is_branch_manager == True:
                User.objects.filter(id=id).update(is_branch_manager=False)
                User.objects.filter(id=id).update(is_superuser=True)
                pass
            elif u.is_agency_bank == True:
                User.objects.filter(id=id).update(is_agency_bank=False)
                User.objects.filter(id=id).update(is_superuser=True)
                pass
            elif u.is_senior_manager == True:
                User.objects.filter(id=id).update(is_senior_manager=False)
                User.objects.filter(id=id).update(is_superuser=True)
                pass
            elif u.is_credit_officer == True:
                User.objects.filter(id=id).update(is_credit_officer=False)
                User.objects.filter(id=id).update(is_superuser=True)
                pass
            else:
                pass

        ## Credit Officer ##
        elif (role == 'credit_officer'):
            if u.is_branch_manager == True:
                User.objects.filter(id=id).update(is_branch_manager=False)
                User.objects.filter(id=id).update(is_credit_officer=True)
                pass
            elif u.is_agency_bank == True:
                User.objects.filter(id=id).update(is_agency_bank=False)
                User.objects.filter(id=id).update(is_credit_officer=True)
                pass
            elif u.is_senior_manager == True:
                User.objects.filter(id=id).update(is_senior_manager=False)
                User.objects.filter(id=id).update(is_credit_officer=True)
                pass
            elif u.is_superuser == True:
                User.objects.filter(id=id).update(is_superuser=False)
                User.objects.filter(id=id).update(is_credit_officer=True)
                pass
            else:
                pass

        ## Branch Manager ##
        elif (role == 'branch_manager'):
            if u.is_superuser == True:
                User.objects.filter(id=id).update(is_superuser=False)
                User.objects.filter(id=id).update(is_branch_manager=True)
                pass
            elif u.is_agency_bank == True:
                User.objects.filter(id=id).update(is_agency_bank=False)
                User.objects.filter(id=id).update(is_branch_manager=True)
                pass
            elif u.is_senior_manager == True:
                User.objects.filter(id=id).update(is_senior_manager=False)
                User.objects.filter(id=id).update(is_branch_manager=True)
                pass
            elif u.is_credit_officer == True:
                User.objects.filter(id=id).update(is_credit_officer=False)
                User.objects.filter(id=id).update(is_branch_manager=True)
                pass
            else:
                pass

        ## Senior Manager ##
        elif (role == 'senior_manager'):
            if u.is_superuser == True:
                User.objects.filter(id=id).update(is_superuser=False)
                User.objects.filter(id=id).update(is_senior_manager=True)
                pass
            elif u.is_agency_bank == True:
                User.objects.filter(id=id).update(is_agency_bank=False)
                User.objects.filter(id=id).update(is_senior_manager=True)
                pass
            elif u.is_branch_manager == True:
                User.objects.filter(id=id).update(is_branch_manager=False)
                User.objects.filter(id=id).update(is_senior_manager=True)
                pass
            elif u.is_credit_officer == True:
                User.objects.filter(id=id).update(is_credit_officer=False)
                User.objects.filter(id=id).update(is_senior_manager=True)
                pass
            else:
                pass

        ## Agency Manager ##
        elif (role == 'agency_bank'):
            if u.is_superuser == True:
                User.objects.filter(id=id).update(is_superuser=False)
                User.objects.filter(id=id).update(is_agency_bank=True)
                pass
            elif u.is_senior_manager == True:
                User.objects.filter(id=id).update(is_senior_manager=False)
                User.objects.filter(id=id).update(is_agency_bank=True)
                pass
            elif u.is_branch_manager == True:
                User.objects.filter(id=id).update(is_branch_manager=False)
                User.objects.filter(id=id).update(is_agency_bank=True)
                pass
            elif u.is_credit_officer == True:
                User.objects.filter(id=id).update(is_credit_officer=False)
                User.objects.filter(id=id).update(is_agency_bank=True)
                pass
            else:
                pass

        else:
            return False

        if (staffname == ""):
            pass
        else:
            User.objects.filter(id=id).update(staffname=staffname)
            pass

    def create_otp(self, email):
        u = get_object_or_404(User, email=email)
        staffname = u.staffname
        T = 5
        res = ''.join(random.choices(string.digits, k=T))
        code = str(res)
        cr_otp = Otp(email=email, otp_code=code)
        cr_otp.save()
        sendMail.otp(email, code, staffname)
        pass

    def check_otp(self, otp_code):
        time_now = timezone.now()
        otp_value = get_object_or_404(Otp, otp_code=otp_code)
        left = otp_value.dt_created - (time_now - timedelta(minutes=5))
        seconds_in_day = 24 * 60 * 60
        lefts = int(divmod(left.days * seconds_in_day + left.seconds, 60)[0])
        print(left)
        if lefts <= 0:

            return False
        else:

            return True

    """Create Group Class Object"""

    def create_group(self, group_name):
        T = 5
        res = ''.join(random.choices(string.digits, k=T))
        code = str(res)
        groups_id = f'G{code}'
        cr_grp = Groups(group_name=group_name, group_id=groups_id)
        cr_grp.save()
        pass

    """Add Member to Group"""

    def add_member_group(self, group_id, member_name, mobile_number, is_leader):
        grp = get_object_or_404(Groups, group_id=group_id)
        grpm = GroupMember.objects.filter(groups_id=grp.group_id).count()
        print(grpm)
        if grpm >= 5:
            cr_mem = GroupMember(group_id=grp.id,
                                 groups_id=group_id,
                                 member_name=member_name,
                                 mobile_number=mobile_number,
                                 is_leader=is_leader)
            cr_mem.save()
            Groups.objects.filter(group_id=group_id).update(active=True)
        else:
            cr_mem = GroupMember(group_id=grp.id,
                                 groups_id=group_id,
                                 member_name=member_name,
                                 mobile_number=mobile_number,
                                 is_leader=is_leader)
            cr_mem.save()
        pass

    """Create Loan for Existing Customer"""

    def createLoanExistingCustomer(self, data):
        app_type = data["app_type"]
        formNo = data["formNo"]
        state = data["state"]
        memberNo = data["memberNo"]
        branch = data["branch"]
        lastLoanRecieved = data["lastLoanRecieved"]
        dateLastLoanRepaid = data["dateLastLoanRepaid"]
        loanAppliedFor = data["loanAppliedFor"]
        indeptedToMfbMfi = data["indeptedToMfbMfi"]
        outsanding = data["outsanding"]
        nameOfGuarantor = data["nameOfGuarantor"]
        guarantorRelationship = data["guarantorRelationship"]
        guarantorOccupation = data["guarantorOccupation"]
        guarantorHomeAddress = data["guarantorHomeAddress"]
        guarantorOfficeAddress = data["guarantorOfficeAddress"]
        recFromGroup1 = data["recFromGroup1"]
        recFromGroup2 = data["recFromGroup2"]
        pass
