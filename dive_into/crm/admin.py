# -*- coding: <utf-8> -*-
from django.contrib import admin
from .models import Client,Contact,Activity

admin.site.register(Contact)
admin.site.register(Activity)


class ContactsInline(admin.TabularInline):
    model = Contact
    extra = 2


class ClientAdmin(admin.ModelAdmin):
    inlines = [ContactsInline]
    list_display = ('name','loyal','last_actitivty')

admin.site.register(Client, ClientAdmin)
# Register your models here.
