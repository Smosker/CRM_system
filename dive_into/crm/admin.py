# -*- coding: <utf-8> -*-
from django.contrib import admin
from .models import Client,Contact,Activity

admin.site.register(Client)
admin.site.register(Contact)
admin.site.register(Activity)
# Register your models here.
