# Generated by Django 3.2.4 on 2021-07-20 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210720_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='agency_bank_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
