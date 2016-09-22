from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'clients/$',views.all_clients,name='clients'),
    url(r'^clients/(?P<client_id>[0-9]+)/$',views.client,name='client')
]