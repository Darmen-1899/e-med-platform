# Generated by Django 4.0.4 on 2022-05-20 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_alter_userrequest_medicine_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicines',
            name='count',
        ),
    ]
