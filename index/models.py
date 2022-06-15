from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Medicines(models.Model):
    id = models.CharField(verbose_name=_("ID"), max_length=30, help_text=_("ID"), primary_key=True)
    name = models.CharField(verbose_name=_("Name of the medicine"), max_length=30, help_text=_("Name of the medicine"))
    foi = models.CharField(verbose_name=_("Frequency of issue"), max_length=30, help_text=_("Frequency of issue"))
    dg = models.CharField(verbose_name=_("Diagnosis Group"), max_length=30, help_text=_("ID"))
    desc = models.CharField(verbose_name=_("Description of the medicine"), max_length=100)

    class Meta:
        verbose_name = 'Лекарство'
        verbose_name_plural = 'Лекарство'

    def __str__(self):
        return f"{self.id}: {self.name}"


class CustomUser(AbstractUser):
    role = (
        ('P', 'Patient'),
        ('D', 'Doctor'),
    )
    username = models.CharField(verbose_name=_("Username"), max_length=150, help_text=_("Username"), unique=True)
    first_name = models.CharField(verbose_name=_("Name"), max_length=1024, blank=True, null=True)
    last_name = models.CharField(verbose_name=_("Surname"), max_length=1024, blank=True, null=True)
    after_name = models.CharField(verbose_name=_("Middle name"), max_length=1024, blank=True, null=True)
    iin = models.CharField(verbose_name=_("IIN"), max_length=12, blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"), max_length=1024, blank=True, null=True, unique=True)
    roles = models.CharField(max_length=25, choices=role)
    med_id = models.ManyToManyField(Medicines)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name']

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class UserRequest(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(verbose_name=_("Email"), max_length=1024)
    description = models.CharField(max_length=50)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    medicine_id = models.ForeignKey(Medicines, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Street(models.Model):
    street_name = models.CharField(max_length=100)

    def __str__(self):
        return self.street_name

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'


class Address(models.Model):
    street_number = models.CharField(max_length=20)
    street_fk = models.ForeignKey(Street, on_delete=models.CASCADE)
    medicine_fk = models.ManyToManyField(Medicines)

    def __str__(self):
        return self.street_fk.street_name + ' ' + self.street_number

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'




