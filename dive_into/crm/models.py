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
    name = models.CharField(max_length=200)
    loyal = models.BooleanField(default=False)

    def last_actitivty(self):
        send_dates = [i.send_date for i in self.activity_set.all() if i.is_send()]

        last = max(send_dates).strftime("%Y.%m.%d %H:%M") if send_dates else None
        return last

    def str_with_html(self):
        return u'<b>Name</b>: {}\n<b>Loyal</b>: {}'.format(self.name, self.loyal)

    def __unicode__(self):
        return u'Name: {} Id: {} Loyal: {}'.format(self.name,self.id, self.loyal)

class Contact(models.Model):
    """
    Таблица с данными о всех контактах клиентах
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True,blank=True)
    active = models.BooleanField(default=True)
    owner_id = models.ForeignKey(User, editable=False,null=True)

    def full_name(self):
        return u'{} {}'.format(self.first_name,self.last_name)

    def str_with_html(self):
        template = u'<b>First name</b>: {}\n<b>Last name</b>: {}\n<b>Email</b>: {}\n<b>Phone</b>: {}\n<b>Active</b>: {}\n<b>Client name</b>: {}\n'
        return template.format(self.first_name,self.last_name,
                          self.email,str(self.phone),
                          str(self.active),self.client.name if self.client else '--')
    def __unicode__(self):
        template = u'First name: {} Last name: {} Email: {} Phone: {} Active: {} Client name: {}'
        return template.format(self.first_name,self.last_name,
                          self.email,str(self.phone),
                          str(self.active),self.client.name if self.client else '--')


class Activity(models.Model):
    """
    Таблица с данными о всех активностях в системе, в каждой активности должен быть
    указан клиент и соответствующий контакт
    """

    title = models.CharField(max_length=30)
    text = models.CharField(max_length=10000)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT,limit_choices_to={'active': True})
    send_date = models.DateTimeField(null=True,blank=True)

    def send(self):
        self.send_date = timezone.now()

    def is_send(self):
        return self.send_date != None

    def str_with_html(self):
        send_date = self.send_date.strftime("%Y.%m.%d %H:%M") if self.send_date else u'Нет'
        return u'<b>Client</b>: {}\n <b>From</b>: {}\n<b>Title</b>: {}\n<b>Send date</b>: {}'.format(self.client.name,self.contact.email,self.title,send_date)

    def __unicode__(self):
        send_date = self.send_date if self.send_date else u'Нет'
        return u'Клиент: {}\nТема: {} \n Текст: {}\n Отправлено: {}'.format(self.client,self.title,self.text,send_date)



