#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


class UserCreate(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/crm'

    def form_valid(self, form):
        """
        Сохраняет нового пользователя, а так же автоматически
         залогиневает его в системе
        """
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
        login(self.request, new_user)
        return super(UserCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/crm')
        else:
            return super(UserCreate, self).dispatch(request, *args, **kwargs)
