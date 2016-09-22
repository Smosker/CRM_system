from django.db import models
from django.utils import timezone
# Create your models here.
class Clients(models.Model):
    client = models.CharField(max_length=200)
    loyal = models.BooleanField(default=False)

    def last_actitivty(self):
        last = max([i.send_date for i in self.activities_set.all() if i.is_send])
        return last

class Contacts(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField()
    client_id = models.ForeignKey(Clients, on_delete=models.SET_NULL,null=True)
    active = models.BooleanField(default=True)

    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

class Activities(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)
    client_id = models.ForeignKey(Clients, on_delete=models.PROTECT)
    contact_id = models.ForeignKey(Contacts, on_delete=models.PROTECT)

    send_date = models.DateTimeField(default=None)

    def send(self):
        self.send_date = timezone.now()

    def is_send(self):
        return self.send_date != None



