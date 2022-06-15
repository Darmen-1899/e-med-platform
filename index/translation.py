from modeltranslation.translator import register, TranslationOptions
from .models import CustomUser, Medicines


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'after_name', 'roles')


@register(Medicines)
class MedicinesTranslationOptions(TranslationOptions):
    fields = ('name', 'foi', 'desc')
