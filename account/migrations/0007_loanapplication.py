# Generated by Django 3.2.4 on 2021-07-15 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_groups_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_type', models.TextField(blank=True, null=True)),
                ('form_no', models.TextField(blank=True, null=True)),
                ('state', models.TextField(blank=True, null=True)),
                ('member_no', models.TextField(blank=True, null=True)),
                ('branch', models.TextField(blank=True, null=True)),
                ('date_of_app', models.DateField(auto_now=True)),
                ('fullname', models.TextField(blank=True, null=True)),
                ('name_of_father', models.TextField(blank=True, null=True)),
                ('phoneno', models.TextField(blank=True, null=True)),
                ('residence_address', models.TextField(blank=True, null=True)),
                ('permanent_address', models.TextField(blank=True, null=True)),
                ('marital_status', models.TextField(blank=True, null=True)),
                ('formal_edu', models.TextField(blank=True, null=True)),
                ('next_of_kin', models.TextField(blank=True, null=True)),
                ('phone_next_of_kin', models.TextField(blank=True, null=True)),
                ('group_of_app', models.TextField(blank=True, null=True)),
                ('date_of_membership', models.DateField(blank=True, null=True)),
                ('type_of_business', models.TextField(blank=True, null=True)),
                ('business_duration', models.TextField(blank=True, null=True)),
                ('busness_address', models.TextField(blank=True, null=True)),
                ('family_on_hcdti_group', models.BooleanField(blank=True, null=True)),
                ('amt_savings_in_passbook', models.FloatField(blank=True, null=True)),
                ('bank', models.TextField(blank=True, null=True)),
                ('account_no', models.TextField(blank=True, null=True)),
                ('last_loan_recieved', models.FloatField(blank=True, null=True)),
                ('date_last_loan_repaid', models.DateField(blank=True, null=True)),
                ('loan_applied_for', models.FloatField(blank=True, null=True)),
                ('indepted_to_mfb_mfi', models.BooleanField(blank=True, null=True)),
                ('outsanding', models.TextField(blank=True, null=True)),
                ('name_of_guarantor', models.TextField(blank=True, null=True)),
                ('guarantor_relationship', models.TextField(blank=True, null=True)),
                ('guarantor_occupation', models.TextField(blank=True, null=True)),
                ('guarantor_home_address', models.TextField(blank=True, null=True)),
                ('guarantor_office_address', models.TextField(blank=True, null=True)),
                ('rec_from_group_1', models.TextField(blank=True, null=True)),
                ('rec_from_group_2', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'loan_application',
            },
        ),
    ]
