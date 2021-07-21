from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import fields, serializers
from account.models import *


class LoggedInUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'staffname',
            'email',
            'staffid',
            'is_superuser',
            'is_credit_officer',
            'is_branch_manager',
            'is_senior_manager',
            'is_agency_bank',
            'is_active'
        ]


class ShowAllUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'staffname',
            'email',
            'staffid',
            'is_superuser',
            'is_credit_officer',
            'is_branch_manager',
            'is_senior_manager',
            'is_agency_bank',
            'is_active'
        ]


class ApprovalSerializer (serializers.ModelSerializer):

    class Meta:
        model = ApprovedLoan
        fields = [
            'application_id', 'form_no', 'customer_name', 'loan_amt',
            'customer_bank', 'customer_acct_no', 'disbursed',
            'date_disbursed', 'repaid', 'date_repaid'
        ]


class ShowAllLoanApplication(serializers.ModelSerializer):

    approve = ApprovalSerializer(many=True)

    class Meta:
        model = LoanApplication
        fields = [
            'application_id', 'app_type', 'form_no', 'state', 'member_no', 'branch', 'date_of_app',
            'fullname', 'name_of_father', 'phoneno', 'residence_address', 'permanent_address',
            'marital_status', 'formal_edu', 'next_of_kin', 'phone_next_of_kin', 'group_of_app',
            'date_of_membership', 'type_of_business', 'business_duration', 'busness_address',
            'family_on_hcdti_group', 'amt_savings_in_passbook', 'bank', 'account_no',
            'last_loan_recieved', 'date_last_loan_repaid', 'loan_applied_for', 'indepted_to_mfb_mfi',
            'outsanding', 'name_of_guarantor', 'guarantor_relationship', 'guarantor_occupation',
            'guarantor_home_address', 'guarantor_office_address', 'rec_from_group_1', 'rec_from_group_2',
            'credit_officer_approve', 'credit_officer_name', 'branch_manager_approve', 'branch_manager_name',
            'branch_manager_reason', 'bm_date_action', 'senior_manager_approve', 'senior_manager_name',
            'senior_manager_reason', 'sm_date_action', 'agency_bank_approve', 'agency_bank_name',
            'ab_date_action', 'repaid', 'approve'
        ]
