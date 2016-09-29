#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
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

        last = max(send_dates) if send_dates else None
        return last

    def __unicode__(self):
        return u'Имя клиента: {}\n Лоялен: {}'.format(self.name, self.loyal)

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

    def full_name(self):
        return u'{} {}'.format(self.first_name,self.last_name)

    def __unicode__(self):
        template = u'Имя: {}\nФамилия: {}\nEmail: {}\nТелефон: {}\nАктивен: {}\nИмя клиента: {}\n'
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

    def activities_template_str(self):
        send_date = self.send_date if self.send_date else u'Нет'
        return u'Клиент: {}\n От: {}\nТема: {}\nОтправлено: {}'.format(self.client.name,self.contact.email,self.title,send_date)

    def __unicode__(self):
        send_date = self.send_date if self.send_date else u'Нет'
        return u'Клиент: {}\nТема: {} \n Текст: {}\n Отправлено: {}'.format(self.client,self.title,self.text,send_date)



