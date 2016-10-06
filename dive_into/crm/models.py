#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    """
    Таблица с данными о всех клиентах, с пометкой о их лояльности
    Связь с таблицами Contact и Activity
    """
    name = models.CharField(max_length=200, unique=True)
    loyal = models.BooleanField(default=False)
    owner = models.ForeignKey(User, editable=True, null=True)

    def last_activity(self):
        send_dates = [i.send_date for i in self.activity_set.all() if i.is_send()]

        last = max(send_dates).strftime("%Y.%m.%d %H:%M") if send_dates else None
        return last

    def str_with_html(self):
        return u'<b>Name</b>: {}\n<b>Loyal</b>: {}\n<b>Id</b>: {}'.format(self.name,
                                                                          self.loyal,
                                                                          self.id)

    def __unicode__(self):
        return u'Name: {}, Id: {}'.format(self.name, self.id)


class Contact(models.Model):
    """
    Таблица с данными о всех контактах клиентах
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, editable=True,null=True)

    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def str_with_html(self):
        template = u'<b>First name</b>: {}\n<b>Last name</b>: {}\n<b>Email</b>: {}\n<b>Phone</b>: {}\n<b>Active</b>: {}\n<b>Client</b>: {}\n'
        return template.format(self.first_name, self.last_name,
                               self.email, str(self.phone),
                               str(self.active), self.client.name if self.client else '--')

    def __unicode__(self):
        template = u'First name: {}, Email: {}, Client id: {}'
        return template.format(self.first_name, self.email, self.client.id if self.client else '--')


class Activity(models.Model):
    """
    Таблица с данными о всех активностях в системе, в каждой активности должен быть
    указан клиент и соответствующий контакт
    """

    title = models.CharField(max_length=30)
    text = models.CharField(max_length=10000)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, limit_choices_to={'active': True})
    send_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, editable=True, null=True)

    def send(self):
        self.send_date = timezone.now()

    def is_send(self):
        return self.send_date is not None

    def str_with_html(self):
        send_date = self.send_date.strftime("%Y.%m.%d %H:%M") if self.send_date else u'Нет'
        return u'<b>Client</b>: {}\n <b>From</b>: {}\n<b>Title</b>: {}\n<b>Send date</b>: {}'.format(self.client.name,
                                                                                                     self.contact.email,
                                                                                                     self.title,
                                                                                                     send_date)

    def __unicode__(self):
        send_date = self.send_date if self.send_date else u'Нет'
        return u'Клиент: {}, Тема: {}, Отправлено: {}'.format(self.client.name, self.title, send_date)



