from abc import ABCMeta
from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic
from django.core.urlresolvers import reverse

from .models import Client,Contact,Activity
from .forms import ContactCreation, ClientCreation

class AllClients(generic.ListView):
    template_name = 'crm/clients.html'
    context_object_name = 'clients_list'

    def get_queryset(self):
        return Client.objects.all()


class Distinct(generic.UpdateView):
    def post(self, request, *args, **kwargs):
        if request.POST.get('action','') == 'Delete':
            contact = self.get_object()
            contact.delete()
            return redirect(reverse('crm:{}'.format(self.all_template)))
        else:
            return super(Distinct,self).post(self,request,*args,**kwargs)

    def get_success_url(self):
        return reverse('crm:{}'.format(self.distinct_template),kwargs={'pk':self.kwargs['pk']})


class DistinctClient(Distinct):
    form_class = ClientCreation
    model = Client
    template_name = 'crm/client_detail.html'
    all_template = 'clients'
    distinct_template = 'client'


class CreateClient(generic.CreateView):
    form_class = ClientCreation
    template_name = 'crm/new_client.html'

    def get_success_url(self):
        return reverse('crm:client',kwargs={'pk':self.object.id})

class DistinctContact(Distinct):
    form_class = ContactCreation
    model = Contact
    template_name = 'crm/contact_detail.html'
    all_template = 'contacts'
    distinct_template = 'contact'



class CreateContact(generic.CreateView):
    form_class = ContactCreation
    template_name = 'crm/new_contact.html'

    def get_success_url(self):
        return reverse('crm:contact',kwargs={'pk':self.object.id})


class Contacts(generic.ListView):
    form_class = ContactCreation
    template_name = 'crm/contacts.html'
    context_object_name = 'contacts_list'

    def get_queryset(self):
        return Contact.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Contacts, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context
    '''
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect(reverse('crm:contact',kwargs={'pk':contact.id}))
        else:
            return HttpResponse("Error: you enter incorrect value. {}".format(form.errors))
    '''




