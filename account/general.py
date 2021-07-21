from django.shortcuts import get_object_or_404
from .models import *
import random
import string
from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from .send_email import Email
from .handle_sms import HandleSms
from decouple import config
sms = HandleSms()

sendMail = Email()

max_loan = 40000.0
min_loan = 20000.0

base_date_time = datetime.now()
now = (datetime.strftime(base_date_time, "%Y-%m-%d"))

tnow = (datetime.strftime(base_date_time, "%Y-%m-%d %H:%M"))

"""
Function that calculate the loan Interest
"""


def calcaluteLoanInterest(amount):
    percent = config('LOAN_PERCENTAGE')
    newPercent = float(percent)
    newAmt = float(amount)
    calc = (newPercent / 100) * newAmt

    # Calculate loan Amount plus loan interest
    repaidAmt = newAmt + calc
    return repaidAmt


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
                        ## Send SMS Notification to the Customer ##
                        sms.sendMessage(memberNo, gpm.member_name,
                                        loanId, msg_type='CREDIT_APPROVED')
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

    """Function to book loan for new customer"""

    def createLoanNewCustomer(self, request, data):
        T = 8
        res = ''.join(random.choices(string.digits, k=T))
        loanId = str(res)
        app_type = data["app_type"]
        formNo = data["formNo"]
        state = data["state"]
        memberNo = data["phoneNo"]
        branch = data["branch"]
        fullname = data['fullname']
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
            while newAmt >= min_loan and newAmt <= max_loan:
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
                        branch=branch, fullname=fullname,
                        name_of_father=nameOfFather, phoneno=memberNo,
                        residence_address=residenceAddress,
                        permanent_address=permanentAddress,
                        marital_status=maritalStatus, formal_edu=formalEdu,
                        next_of_kin=nextOfKin, phone_next_of_kin=phoneNextOfKin,
                        group_of_app=groupOfApp, date_of_membership=now,
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

                    ## Send SMS Notification to the Customer ##
                    sms.sendMessage(memberNo, fullname,
                                    loanId, msg_type='CREDIT_APPROVED')
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
                    "reason": "Invalid Amount...Min N20,000 & Max N40,000"
                }
                return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)

        except:
            datas = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Fail to create Loan Application. Kindly Check the value you are passing to the endpoint"
            }
            return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)

    """Approve Application"""

    def approve_loan(self, request, appId):
        loanId = appId
        comment = request.data.get('comment')
        approve = request.data.get('approve')
        try:
            loan = get_object_or_404(LoanApplication, application_id=loanId)
            repaid_amt = calcaluteLoanInterest(loan.loan_applied_for)
            # print(repaid_amt)
            while type(approve) == bool:
                instnce = LoanApplication.objects.filter(application_id=loanId)
                #Check for senior manager and approve#
                if request.user.is_senior_manager == True and loan.branch_manager_approve == "APPROVED":
                    # If it's approved by senior Manager #
                    while approve == True:
                        instnce.update(senior_manager_approve="APPROVED", senior_manager_name=request.user.staffname,
                                       senior_manager_reason=comment, sm_date_action=now)

                        obj, created = ApprovedLoan.objects.update_or_create(
                            application_id=loanId,
                            defaults={'loan_id': loan.id, 'application_id': loanId,
                                      'form_no': loan.form_no, 'customer_name': loan.fullname,
                                      'loan_amt': loan.loan_applied_for, 'customer_bank': loan.bank,
                                      'customer_acct_no': loan.account_no, 'repaid_amt': repaid_amt},
                        )
                        ## Send SMS Notification to the Customer ##
                        sms.sendMessage(
                            loan.member_no, loan.fullname, loan.application_id, msg_type='SENIOR_APPROVED')

                        datas = {
                            "code": status.HTTP_200_OK,
                            "status": "success",
                            "reason": f'You have approved loan Application with ID: {loanId}'
                        }
                        return Response(data=datas, status=status.HTTP_200_OK)

                        # If not approved by senior Manager #
                    else:
                        instnce.update(senior_manager_approve="DECLINED", senior_manager_name=request.user.staffname,
                                       senior_manager_reason=comment, sm_date_action=now)

                        # Delete the approved loan if already in the Approved loan Table #
                        inst = ApprovedLoan.objects.filter(
                            application_id=loanId)
                        inst.delete()

                        ## Send SMS Notification to the Customer ##
                        sms.sendMessage(
                            loan.member_no, loan.fullname, loan.application_id, msg_type='SENIOR_DECLINE')

                        datas = {
                            "code": status.HTTP_200_OK,
                            "status": "success",
                            "reason": f'You have declined loan Application with ID: {loanId}'
                        }
                        return Response(data=datas, status=status.HTTP_200_OK)

                #Branch Manager Approval Logic#
                elif request.user.is_branch_manager == True and loan.credit_officer_approve == "APPROVED":
                    # If it's approve by Branch Manager#
                    if loan.senior_manager_approve == "PENDING":
                        while approve == True:
                            instnce.update(branch_manager_approve="APPROVED", branch_manager_name=request.user.staffname,
                                           branch_manager_reason=comment, bm_date_action=now)

                            ## Send SMS Notification to the Customer ##
                            sms.sendMessage(
                                loan.member_no, loan.fullname, loan.application_id, msg_type='BRANCH_APPROVED')

                            datas = {
                                "code": status.HTTP_200_OK,
                                "status": "success",
                                "reason": f'You have approved loan Application with ID: {loanId}'
                            }
                            return Response(data=datas, status=status.HTTP_200_OK)
                            # If Not approved by Branch Manaer #
                        else:
                            instnce.update(branch_manager_approve="DECLINED", branch_manager_name=request.user.staffname,
                                           branch_manager_reason=comment, bm_date_action=now)

                            ## Send SMS Notification to the Customer ##
                            sms.sendMessage(
                                loan.member_no, loan.fullname, loan.application_id, msg_type='BRANCH_DECLINED')

                            datas = {
                                "code": status.HTTP_200_OK,
                                "status": "success",
                                "reason": f'You have declined loan Application with ID: {loanId}'
                            }
                            return Response(data=datas, status=status.HTTP_200_OK)
                    else:
                        datas = {
                            "code": status.HTTP_401_UNAUTHORIZED,
                            "status": "fail",
                            "reason": "Loan Application has been Approve by the Senior Manager and can't be reversed"
                        }
                        return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)

                # Agency Banking Logic #
                elif request.user.is_agency_bank == True and loan.branch_manager_approve == "APPROVED" and loan.senior_manager_approve == "APPROVED":

                    instnce.update(agency_bank_approve="DISBURSED", agency_bank_name=request.user.staffname,
                                   ab_date_action=now)

                    # Update Approved Loan Table #
                    pay = ApprovedLoan.objects.filter(
                        application_id=loanId)
                    pay.update(disbursed='DISBURSED', date_disbursed=tnow)

                    ## Send SMS Notification to the Customer ##
                    sms.sendMessage(loan.member_no, loan.fullname,
                                    loan.application_id, msg_type='DISBURSE')
                    datas = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "reason": f'{loan.loan_applied_for} has been disburse to {loan.fullname} successfully'
                    }
                    return Response(data=datas, status=status.HTTP_200_OK)

                else:
                    datas = {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "status": "fail",
                        "reason": "The Loan has either been declined by branch manager, it has not be worked on by the branch manager or permission denied for the user"
                    }
                    return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
            else:
                datas = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "Sorry, approve field must be boolean. True/False"
                }
            return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
        except:
            datas = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Invalid Loan ID"
            }
            return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)

    """
    Loan Repayment to be handle by the agency Banking
    """

    def loanRepayment(self, appid, amount):
        try:
            loan = get_object_or_404(ApprovedLoan, application_id=appid)
            if loan.repaid_amt == 0:
                datas = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "Loan has been fully paid"
                }
                return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
            elif float(amount) > loan.repaid_amt:
                datas = {
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "status": "fail",
                    "reason": "Amount Entered is more than what should be paid back into the system"
                }
                return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
            else:
                updateLoan = ApprovedLoan.objects.filter(
                    application_id=loan.application_id)
                loanapp = LoanApplication.objects.filter(
                    application_id=loan.application_id)
                newAmt = (loan.repaid_amt - float(amount))
                if newAmt == 0:
                    # Update approved loan
                    updateLoan.update(
                        repaid_amt=0, repaid='PAID', date_repaid=tnow)

                    # Update Loan Application
                    loanapp.update(repaid='PAID')
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "message": f'N{amount} has been paid and you have N{newAmt} to be paid back'
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    # Update approved loan
                    updateLoan.update(repaid_amt=newAmt)

                    # Update Loan Application
                    loanapp.update(repaid='PAID')
                    data = {
                        "code": status.HTTP_200_OK,
                        "status": "success",
                        "message": f'N{amount} has been paid and you have N{newAmt} to be paid back'
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
        except:
            datas = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "status": "fail",
                "reason": "Invalid Loan ID"
            }
            return Response(data=datas, status=status.HTTP_401_UNAUTHORIZED)
