# coding=utf-8
from django import forms
from .models import Client, Contact, Activity


class ContactCreation(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(ContactCreation, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = Contact

        fields = ('first_name',
                  'last_name',
                  'email',
                  'phone',
                  'client',
                  'active')


class ClientCreation(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'loyal')


class ActivityCreation(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(ActivityCreation, self).__init__(*args, **kwargs)
        self.user = user
        user_clients = Client.objects.filter(owner=self.user)
        self.fields['client'].queryset = user_clients
        self.fields['contact'].queryset = Contact.objects.filter(client__in=user_clients)

    def clean(self):
        super(ActivityCreation, self).clean()
        form_data = self.cleaned_data
        if all((form_data.get('client', ''), form_data.get('contact', ''))) \
                and form_data['client'] != form_data['contact'].client:

            del form_data['contact']
            del form_data['client']
            raise forms.ValidationError("Chosen contact doesn't belong to chosen client")
        elif self.instance.send_date:
            raise forms.ValidationError("You can't change activity which was sent")
        return form_data

    class Meta:
        model = Activity
        fields = ('title',
                  'text',
                  'client',
                  'contact')

        widgets = {
            'text': forms.Textarea(),
        }

