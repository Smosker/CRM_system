from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views import generic

from .models import Client,Contact,Activity

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
        print(request.POST)
        return super(DistinctClient,self).get(request)


def client(request,client_id):
    get_client = get_object_or_404(Client,pk=client_id)
    if request.method == 'POST':
        print(request.POST)
    print(get_client.contact_set.all())
    return render(request,'crm/client_detail.html',{'client_info':get_client})
