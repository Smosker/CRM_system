# -*- coding: <utf-8> -*-
from django.db import models
from django.utils import timezone
# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=200)
    loyal = models.BooleanField(default=False)

    def last_actitivty(self):
        last = max([i.send_date for i in self.activity_set.all() if i.is_send])
        return last

    def __unicode__(self):
        return '{} {}'.format(self.name, self.loyal)

class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True,related_name='contact')
    active = models.BooleanField(default=True)

    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

    def __unicode__(self):
        return ' '.join((self.first_name,self.last_name,self.email,str(self.phone),str(self.active)))

class Activity(models.Model):

    title = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT,limit_choices_to={'active': True})
    send_date = models.DateTimeField(null=True,blank=True)




    def send(self):
        self.send_date = timezone.now()

    def is_send(self):
        return self.send_date != None

    def __unicode__(self):
        return '{}, {} \n {}'.format(self.client,self.title,self.text)



