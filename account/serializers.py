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
