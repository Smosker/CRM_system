from django.conf.urls import url

from . import views
app_name =  'crm'

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'clients/$',views.AllClients.as_view(),name='clients'),
    url(r'^clients/(?P<pk>[0-9]+)/$',views.DistinctClient.as_view(),name='client')
]