#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .models import Client, Contact, Activity
from .forms import ContactCreation, ClientCreation, ActivityCreation


class NoOwnerError(Exception):
    pass


class MainPage(generic.View):
    """
    Отвечает за отображение главной страницы системы,
    поддверживает получение get запросов с указанным именем клиента для поиска
    и отображения
    """
    template = 'crm/main.html'
    model = Client

    def get(self, request):
        context = {}
        if request.GET.get('search', None):
            if self.request.user.is_authenticated():
                clients = self.model.objects.filter(name__icontains=request.GET.get('search', ''),
                                                    owner=request.user)

                if clients:
                    context['search_clients'] = clients
                else:
                    context['search_clients'] = 'no result'
            else:
                context['search_clients'] = 'no auth'

        elif request.session.get('deleted_data', ''):
            context['deleted_data'] = request.session['deleted_data']
            request.session['deleted_data'] = None

        return render(request, self.template, context)


class Distinct(generic.UpdateView):
    """
    Класс для наследования UpdateView + обработка нажатия кнопки Delete на странице
    с удалением соответствующего объекта, если нет препятствий
    """

    def dispatch(self, *args, **kwargs):
        try:
            return super(Distinct, self).dispatch(*args, **kwargs)
        except NoOwnerError:
            return redirect(reverse('crm:{}'.format(self.distinct_template), kwargs={'pk': self.kwargs['pk']}))

    def get_object(self, queryset=None):
        try:
            object_get = self.model.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404("No object found matching this query")

        if self.request.user.is_authenticated():
            if object_get.owner == self.request.user:
                return object_get

    def get_form_kwargs(self):
        """
        Добавляем текущего пользователя в список аргументов,
        для корректного формирования списка foreign_keys's
        доступных для выбора
        """
        kwargs = super(Distinct, self).get_form_kwargs()
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        object_get = self.get_object()
        if not object_get:
            """
            Если объект не найден - значит текущий пользователь
            не является владельцем объекта, который пытается изменить,
            выбрасываем ошибку
            """
            raise NoOwnerError
        if request.POST.get('action', '') == 'Delete':
            request.session['deleted_data'] = str(object_get)
            object_get.delete()
            return redirect(reverse('crm:main'))
        else:
            return super(Distinct, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('crm:{}'.format(self.distinct_template), kwargs={'pk': self.kwargs['pk']})


class Creation(generic.CreateView):
    """
    Класс для наследования CreateView + передача текущего пользователя в
    форму для заполнения поля owner в соответствующей модели
    """
    def get_form_kwargs(self):
        """
        Добавляем текущего пользователя в список аргументов,
        для корректного формирования списка foreign_keys's
        доступных для выбора
        """
        kwargs = super(Creation, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('crm:{}'.format(self.url), kwargs={'pk': self.object.id})

    def form_valid(self, form):
        object_to_save = form.save(commit=False)
        object_to_save.owner = self.request.user
        return super(Creation, self).form_valid(form)


class List(generic.ListView):
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.model.objects.filter(owner=self.request.user)


class Clients(List):
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

    def get_form_kwargs(self):
        """
        Переписываем родительский метод Distinct, так
        как для создания клиента нет нужды фильтровать
        доступные результаты в форме для foreing_keys
        """
        return generic.UpdateView.get_form_kwargs(self)


class CreateClient(Creation):
    """
    Обрабатывает запросы на создание клиента,
    при успехе перекидывает на страницу созданного клиента
    """
    form_class = ClientCreation
    template_name = 'crm/new_client.html'
    url = 'client'

    def get_form_kwargs(self):
        """
        Переписываем родительский метод Creation, так
        как для создания клиента нет нужды фильровать
        доступные результаты в форме для foreing_keys
        """
        return generic.CreateView.get_form_kwargs(self)


class Contacts(List):
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


class CreateContact(Creation):
    """
    Обрабатывает запросы на создание контакта,
    при успехе перекидывает на страницу созданного контакта
    """
    form_class = ContactCreation
    template_name = 'crm/new_contact.html'
    url = 'contact'


class Activities(List):
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
            return super(DistinctActivity, self).post(request, *args, **kwargs)


class CreateActivity(Creation):
    """
    Обрабатывает запросы на создание активности,
    при успехе перекидывает на страницу созданной активности
    """
    form_class = ActivityCreation
    template_name = 'crm/new_activity.html'
    url = 'activity'









