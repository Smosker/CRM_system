from django.shortcuts import render, get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from django.core.urlresolvers import reverse

from .models import Client,Contact,Activity
from .forms import ContactCreation

def main(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class AllClients(generic.ListView):
    template_name = 'crm/main.html'
    context_object_name = 'clients_list'

    def get_queryset(self):
        return Client.objects.all()

class DistinctClient(generic.DetailView):
    model = Client
    template_name = 'crm/client_detail.html'

    def post(self, request, *args, **kwargs):
        self.detail = self.get_object()
        print(request.POST,self.detail)
        return super(DistinctClient,self).get(request)


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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect(reverse('crm:contact',kwargs={'pk':contact.id}))
        else:
            return HttpResponse("Error: you enter incorrect value. {}".format(form.errors))

class DistinctContact(generic.DetailView):
    form_class = ContactCreation
    model = Contact
    template_name = 'crm/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DistinctContact, self).get_context_data(**kwargs)
        choosen_contact = self.get_object()
        initial_data = {'first_name': choosen_contact.first_name,
                        'last_name': choosen_contact.last_name,
                        'email' : choosen_contact.email,
                        'phone' : choosen_contact.phone,
                        'client' : choosen_contact.client,
                        'active' : choosen_contact.active}

        form = self.form_class(initial=initial_data)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        print(args,kwargs)
        choosen_contact = self.get_object()
        print(request.POST)
        if request.POST.get('action','') == 'Delete':
            choosen_contact.delete()
        else:
            form = self.form_class(request.POST, instance=choosen_contact)
            if form.has_changed():
                if form.is_valid():
                    route = form.save()
                    return redirect(reverse('crm:contact',kwargs={'pk':route.id}))
                else:
                    return HttpResponse("Error: you enter incorrect value {}".format(form.errors))
            else:
                return HttpResponse("Error: you hadn't change anything")
        return redirect(reverse('crm:contacts'))

