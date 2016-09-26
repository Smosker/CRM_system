# coding=utf-8
from django import forms
from .models import Client,Contact,Activity


class ContactCreation(forms.ModelForm):
    """
    Форма отвечающая за внесение изменения в существующий
    маршрут или создание нового
    """
    class Meta:
        model = Contact

        fields = ('first_name',
    'last_name',
    'email' ,
    'phone' ,
    'client',
    'active')
