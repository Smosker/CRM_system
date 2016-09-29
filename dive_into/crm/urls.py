from django.conf.urls import url

from . import views
app_name = 'crm'

urlpatterns = [
    url(r'^$', views.MainPage.as_view(), name='main'),

    url(r'clients/$', views.Clients.as_view(), name='clients'),
    url(r'^clients/(?P<pk>[0-9]+)/$', views.DistinctClient.as_view(), name='client'),
    url(r'^clients/create', views.CreateClient.as_view(), name='new_client'),

    url(r'^contacts/$', views.Contacts.as_view(), name='contacts'),
    url(r'^contacts/(?P<pk>[0-9]+)/$', views.DistinctContact.as_view(), name='contact'),
    url(r'contacts/create', views.CreateContact.as_view(), name='new_contact'),

    url(r'^activities/$', views.Activities.as_view(), name='activities'),
    url(r'^activities/(?P<pk>[0-9]+)/$', views.DistinctActivity.as_view(), name='activity'),
    url(r'activities/create', views.CreateActivity.as_view(), name='new_activity')
]