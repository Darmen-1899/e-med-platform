# Generated by Django 4.0.4 on 2022-05-05 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=1024, verbose_name='Email')),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.DeleteModel(
            name='medicine',
        ),
        migrations.AddField(
            model_name='medicines',
            name='count',
            field=models.IntegerField(null=True, verbose_name='Count of medicines'),
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='med_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='med_id',
            field=models.ManyToManyField(to='index.medicines'),
        ),
        migrations.AddField(
            model_name='userrequest',
            name='medicine_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='index.medicines'),
        ),
        migrations.AddField(
            model_name='userrequest',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]