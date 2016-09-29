#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta
from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic
from django.core.urlresolvers import reverse
from datetime import datetime

from .models import Client, Contact, Activity
from .forms import ContactCreation, ClientCreation, ActivityCreation


class MainPage(generic.View):
    """
    Отвечает за отображение главной страницы системы,
    поддверживает получение get запросов с указанным именем клиента для поиска
    и отображения
    """
    template = 'crm/main.html'
    model = Client

    def get(self, request, *args, **kwargs):
        context = {}
        if request.GET.get('search', None):
            clients = [client for client in self.model.objects.all()
                       if request.GET.get('search', '').lower() in client.name.lower()]

            context['search_clients'] = clients

        return render(request,self.template,context)

class Distinct(generic.UpdateView):
    """
    Класс для наследования UpdateView + обработка нажатия кнопки Delete на странице
    с удалением соответствующего объекта, если нет препятствий
    """
    def post(self, request, *args, **kwargs):
        if request.POST.get('action', '') == 'Delete':
            object = self.get_object()
            object.delete()
            request.session['delete'] = True
            return redirect(reverse('crm:{}'.format(self.all_template)))
        else:
            return super(Distinct, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('crm:{}'.format(self.distinct_template), kwargs={'pk': self.kwargs['pk']})


class Clients(generic.ListView):
    """
    Отображает список всех клиентов в системе
    """
    model = Client
    template_name = 'crm/clients.html'
    context_object_name = 'clients_list'


class DistinctClient(Distinct):
    """
    Отображает информацию по клиенту, позволяет редактировать
    информацию клиента, а так же удалять его
    """
    form_class = ClientCreation
    model = Client
    template_name = 'crm/client_detail.html'
    all_template = 'clients'
    distinct_template = 'client'


class CreateClient(generic.CreateView):
    """
    Обрабатывает запросы на создание клиента,
    при успехе перекидывает на страницу созданного клиента
    """
    form_class = ClientCreation
    template_name = 'crm/new_client.html'

    def get_success_url(self):
        return reverse('crm:client', kwargs={'pk':self.object.id})


class Contacts(generic.ListView):
    """
    Отображает список всех контактов в системе
    """
    model = Contact
    template_name = 'crm/contacts.html'
    context_object_name = 'contacts_list'


class DistinctContact(Distinct):
    """
    Отображает информацию по контакту, позволяет редактировать
    информацию контакта, а так же удалять его
    """
    form_class = ContactCreation
    model = Contact
    template_name = 'crm/contact_detail.html'
    all_template = 'contacts'
    distinct_template = 'contact'


class CreateContact(generic.CreateView):
    """
    Обрабатывает запросы на создание контакта,
    при успехе перекидывает на страницу созданного контакта
    """
    form_class = ContactCreation
    template_name = 'crm/new_contact.html'

    def get_success_url(self):
        return reverse('crm:contact', kwargs={'pk':self.object.id})

class Activities(generic.ListView):
    """
    Отображает список всех активностей в системе
    """
    model = Activity
    template_name = 'crm/activities.html'
    context_object_name = 'activities_list'


class DistinctActivity(Distinct):
    """
    Отображает информацию по активности, позволяет редактировать
    информацию о активности, а так же удалять ее, при этом удаление и
    редактирование доступны только для не отправленных активностей,
    если активность отправлена - такой возможности не предоставляется
    """
    form_class = ActivityCreation
    model = Activity
    template_name = 'crm/activity_detail.html'
    all_template = 'activities'
    distinct_template = 'activity'

    def post(self, request, *args, **kwargs):
        if request.POST.get('action', '') == 'Send':
            activity = self.get_object()
            activity.send()
            activity.save()
            return redirect(reverse('crm:activity', kwargs={'pk': activity.id}))
        else:
            return super(DistinctActivity,self).post(request, *args, **kwargs)



class CreateActivity(generic.CreateView):
    """
    Обрабатывает запросы на создание активности,
    при успехе перекидывает на страницу созданной активности
    """
    form_class = ActivityCreation
    template_name = 'crm/new_activity.html'

    def get_success_url(self):
        return reverse('crm:activity', kwargs={'pk': self.object.id})







