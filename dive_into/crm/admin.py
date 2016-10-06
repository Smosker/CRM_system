# -*- coding: <utf-8> -*-
from django.contrib import admin
from .models import Client,Contact,Activity


class ContactsInline(admin.TabularInline):
    model = Contact
    extra = 2
    exclude = ('owner',)


class ClientAdmin(admin.ModelAdmin):
    inlines = [ContactsInline]
    list_display = ('name', 'loyal', 'last_activity', 'owner')

    def save_model(self, request, obj, form, change):
        obj.save()
        contacts = obj.contact_set.all()
        for i in contacts:
                i.owner = obj.owner
                i.save()

        activities = obj.activity_set.all()
        for i in activities:
                i.owner = obj.owner
                i.save()


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'active', 'owner')
    exclude = ('owner',)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'contact', 'send_date', 'owner')
    exclude = ('owner',)


admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Activity, ActivityAdmin)



