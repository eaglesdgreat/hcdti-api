# Generated by Django 3.2.4 on 2021-07-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_groupmember_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='groups',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
