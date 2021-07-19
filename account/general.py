from django.shortcuts import get_object_or_404
from .models import *
import random
import string
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
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

    def createLoanExistingCustomer(self, request, data):
        T = 8
        res = ''.join(random.choices(string.digits, k=T))
        loanId = str(res)
        app_type = data["app_type"]
        formNo = data["formNo"]
        state = data["state"]
        memberNo = data["memberNo"]
        branch = data["branch"]
        nameOfFather = data["nameOfFather"]
        residenceAddress = data["residenceAddress"]
        permanentAddress = data["permanentAddress"]
        maritalStatus = data["maritalStatus"]
        formalEdu = data["formalEdu"]
        nextOfKin = data["nextOfKin"]
        phoneNextOfKin = data["phoneNextOfKin"]
        groupOfApp = data["groupOfApp"]
        lastLoanRecieved = data["lastLoanRecieved"]
        dateLastLoanRepaid = data["dateLastLoanRepaid"]
        loanAppliedFor = data["loanAppliedFor"]
        indeptedToMfbMfi = data["indeptedToMfbMfi"]
        outsanding = data["outsanding"]
        bank = data["bank"]
        accountNo = data["accountNo"]
        typeOfBusiness = data["typeOfBusiness"]
        businessDuration = data["businessDuration"]
        amtSavingsInPassbook = data["amtSavingsInPassbook"]
        busnessAddress = data["busnessAddress"]
        familyOnHcdtiGroup = data["familyOnHcdtiGroup"]
        nameOfGuarantor = data["nameOfGuarantor"]
        guarantorRelationship = data["guarantorRelationship"]
        guarantorOccupation = data["guarantorOccupation"]
        guarantorHomeAddress = data["guarantorHomeAddress"]
        guarantorOfficeAddress = data["guarantorOfficeAddress"]
        recFromGroup1 = data["recFromGroup1"]
        recFromGroup2 = data["recFromGroup2"]
        creditOfficerName = request.user.staffname

        newAmt = float(loanAppliedFor)
        try:
            gpm = get_object_or_404(GroupMember, mobile_number=memberNo)
            while newAmt >= min_loan and newAmt <= max_loan:
                gp = get_object_or_404(Groups, group_id=gpm.groups_id)
                while gp.active == True and GroupMember.objects.filter(groups_id=gp.group_id).count() >= 5:
                    if LoanApplication.objects.filter(member_no=memberNo).exists():
                        datas = {
                            "code": status.HTTP_401_UNAUTHORIZED,
                            "status": "fail",
                            "reason": "Customer already have active Application"
                        }
                        return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        createLoan = LoanApplication(
                            application_id=loanId, app_type=app_type,
                            form_no=formNo, state=state, member_no=memberNo,
                            branch=branch, fullname=gpm.member_name,
                            name_of_father=nameOfFather, phoneno=memberNo,
                            residence_address=residenceAddress,
                            permanent_address=permanentAddress,
                            marital_status=maritalStatus, formal_edu=formalEdu,
                            next_of_kin=nextOfKin, phone_next_of_kin=phoneNextOfKin,
                            group_of_app=groupOfApp, date_of_membership=gpm.date_added,
                            type_of_business=typeOfBusiness, business_duration=businessDuration,
                            busness_address=busnessAddress, family_on_hcdti_group=familyOnHcdtiGroup,
                            amt_savings_in_passbook=amtSavingsInPassbook, bank=bank,
                            account_no=accountNo, last_loan_recieved=lastLoanRecieved,
                            date_last_loan_repaid=dateLastLoanRepaid, loan_applied_for=loanAppliedFor,
                            indepted_to_mfb_mfi=indeptedToMfbMfi, outsanding=outsanding,
                            name_of_guarantor=nameOfGuarantor, guarantor_relationship=guarantorRelationship,
                            guarantor_occupation=guarantorOccupation, guarantor_home_address=guarantorHomeAddress,
                            guarantor_office_address=guarantorOfficeAddress, rec_from_group_1=recFromGroup1,
                            rec_from_group_2=recFromGroup2, credit_officer_name=creditOfficerName)
                        createLoan.save()
                        datas = {
                            "code": status.HTTP_200_OK,
                            "status": "success",
                            "message": f'Loan Application with Booking ID: {loanId} was Successful'
                        }
                        return Response(data=datas, status=status.HTTP_200_OK)
                else:
                    datas = {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "status": "fail",
                        "reason": "Group is not Active or Group member is not up to 5"
                    }
                    return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
            else:
                datas = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "Invalid Amount...Min N20,000 & Max N40,000"
                }
                return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
        except:
            datas = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Customer does not exist in any group"
            }
            return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
