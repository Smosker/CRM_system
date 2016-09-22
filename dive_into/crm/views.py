from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Client,Contact,Activity

def main(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def all_clients(request):
    clients_list = Client.objects.all()
    #print([z.first_name for i in clients for z in i.contact.all()])
    template = loader.get_template('crm/main.html')
    print([i.name for i in clients_list])
    context = {
        'clients_list': clients_list,
    }
    return HttpResponse(template.render(context, request))


def client(request,client_id):
    return HttpResponse('looking at client {}'.format(client_id))
