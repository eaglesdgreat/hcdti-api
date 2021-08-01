from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager
from django.http import request
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sessions.models import Session


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    staffname = models.TextField("staffname", null=True, blank=True)
    staffid = models.TextField(null=True, blank=True)
    is_credit_officer = models.BooleanField(default=False)
    is_branch_manager = models.BooleanField(default=False)
    is_senior_manager = models.BooleanField(default=False)
    is_agency_bank = models.BooleanField(default=False)
    is_staff = models.BooleanField(verbose_name='is_staff', default=True)
    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['staffname']

    class Meta:
        db_table = 'user'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.email)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_session'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.user)


class Otp(models.Model):
    email = models.EmailField(null=True)
    otp_code = models.TextField(null=True)
    dt_created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'otp'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.email)


class Groups(models.Model):
    group_id = models.CharField(max_length=100, null=True)
    group_name = models.TextField(null=True)
    active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now=True)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.group_id)


class GroupMember(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    groups_id = models.TextField(null=True)
    member_name = models.TextField(null=True)
    mobile_number = models.TextField(null=True)
    is_leader = models.BooleanField(null=True)
    date_added = models.DateField(auto_now=True)

    class Meta:
        db_table = 'group_member'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.group)
    

class GroupMemberInfo(models.Model):
    group_member = models.OneToOneField(GroupMember, on_delete=models.CASCADE)
    name_of_husband = models.TextField(blank=True, null=True)
    next_of_kin = models.TextField(blank=True, null=True)
    next_of_kin_mobile = models.TextField(blank=True, null=True)
    cust_edu_level = models.TextField(blank=True, null=True)
    resident_addr = models.TextField(blank=True, null=True)
    bus_addr = models.TextField(blank=True, null=True)
    marital_status = models.TextField(blank=True, null=True)
    date_added = models.DateField(auto_now=True)
    type_of_bus = models.TextField(blank=True, null=True)
    duration_of_bus = models.TextField(blank=True, null=True)
    family_on_hcdti_group = models.BooleanField(blank=True, null=True)
    savings_in_passbook = models.TextField(blank=True, null=True)
    bank = models.TextField(blank=True, null=True)
    account_no = models.TextField(blank=True, null=True)
    member_owning_mfi = models.BooleanField(blank=True, null=True)
    mfi_name = models.TextField(blank=True, null=True)
    guarantor = models.TextField(blank=True, null=True)
    guarantor_rel = models.TextField(blank=True, null=True)
    guarantor_addr = models.TextField(blank=True, null=True)
    guarantor_office_addr = models.TextField(blank=True, null=True)
    group_recomm = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=False)
    
    
    class Meta:
        db_table = 'group_member_info'
    
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.group_member)


class LoanApplication(models.Model):
    application_id = models.TextField(blank=True, null=True)
    app_type = models.TextField(null=True, blank=True)
    form_no = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    member_no = models.TextField(blank=True, null=True)
    branch = models.TextField(null=True, blank=True)
    date_of_app = models.DateField(auto_now=True)
    fullname = models.TextField(null=True, blank=True)
    name_of_father = models.TextField(null=True, blank=True)
    phoneno = models.TextField(null=True, blank=True)
    residence_address = models.TextField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)
    marital_status = models.TextField(null=True, blank=True)
    formal_edu = models.TextField(null=True, blank=True)
    next_of_kin = models.TextField(null=True, blank=True)
    phone_next_of_kin = models.TextField(null=True, blank=True)
    group_of_app = models.TextField(null=True, blank=True)
    date_of_membership = models.DateField(null=True, blank=True)
    type_of_business = models.TextField(null=True, blank=True)
    business_duration = models.TextField(null=True, blank=True)
    busness_address = models.TextField(null=True, blank=True)
    family_on_hcdti_group = models.BooleanField(null=True, blank=True)
    amt_savings_in_passbook = models.TextField(null=True, blank=True)
    bank = models.TextField(null=True, blank=True)
    account_no = models.TextField(null=True, blank=True)
    last_loan_recieved = models.TextField(null=True, blank=True)
    date_last_loan_repaid = models.TextField(null=True, blank=True)
    loan_applied_for = models.TextField(null=True, blank=True)
    indepted_to_mfb_mfi = models.BooleanField(null=True, blank=True)
    outsanding = models.TextField(null=True, blank=True)
    name_of_guarantor = models.TextField(null=True, blank=True)
    guarantor_relationship = models.TextField(null=True, blank=True)
    guarantor_occupation = models.TextField(blank=True, null=True)
    guarantor_home_address = models.TextField(blank=True, null=True)
    guarantor_office_address = models.TextField(blank=True, null=True)
    rec_from_group_1 = models.TextField(blank=True, null=True)
    rec_from_group_2 = models.TextField(blank=True, null=True)
    credit_officer_approve = models.CharField(
        max_length=100, default="APPROVED")
    credit_officer_name = models.TextField(blank=True, null=True)
    branch_manager_approve = models.CharField(
        max_length=100, default="PENDING")
    branch_manager_name = models.TextField(blank=True, null=True)
    branch_manager_reason = models.TextField(blank=True, null=True)
    bm_date_action = models.DateField(blank=True, null=True)
    senior_manager_approve = models.CharField(
        max_length=100, default="PENDING")
    senior_manager_name = models.TextField(blank=True, null=True)
    senior_manager_reason = models.TextField(blank=True, null=True)
    sm_date_action = models.DateField(blank=True, null=True)
    agency_bank_approve = models.CharField(
        max_length=100, default="PENDING")
    agency_bank_name = models.TextField(blank=True, null=True)
    ab_date_action = models.DateField(blank=True, null=True)
    repaid = models.CharField(max_length=100, default="PENDING")

    class Meta:
        db_table = 'loan_application'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.form_no)


class ApprovedLoan(models.Model):
    loan = models.ForeignKey(
        LoanApplication, related_name='approve', on_delete=models.CASCADE)
    application_id = models.CharField(max_length=100, blank=True, null=True)
    form_no = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    loan_amt = models.FloatField(blank=True, null=True)
    customer_bank = models.TextField(blank=True, null=True)
    customer_acct_no = models.TextField(blank=True, null=True)
    disbursed = models.CharField(max_length=100, default="PENDING")
    date_disbursed = models.DateTimeField(blank=True, null=True)
    repaid_amt = models.FloatField(blank=True, null=True)
    repaid = models.CharField(max_length=100, default="PENDING")
    date_repaid = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'approved_loan'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.application_id)
