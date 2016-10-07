#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.db import IntegrityError

# Create your tests here.

import models


class ClientTest(TestCase):
    """
    Тест модели Client
    """
    def setUp(self):
        self.object = models.Client(name='test', loyal=False)
        self.object.save()

    def test_unique_name(self):

        self.object1 = models.Client(name='test', loyal=True)
        self.assertRaises(IntegrityError, self.object1.save)

    def test_diff_name(self):
        self.object1 = models.Client(name='test1', loyal=True)
        self.object1.save()
        self.assertEqual(len(models.Client.objects.all()), 2)


class PageAccessTest(TestCase):
    """
    Тестирование доступности страниц c/без
    авторизации, доступность несуществующих объектов
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')

    def test_access(self):
        """
        Доступность страниц с созданием объектов
        без авторизации и с авторизацией
        """
        response = self.client.get(reverse('crm:new_client'))
        self.assertRedirects(response,
                             reverse('login')+'?next={}'.format(reverse('crm:new_client')))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('crm:new_contact'))
        self.assertRedirects(response,
                             reverse('login')+'?next={}'.format(reverse('crm:new_contact')))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('crm:new_activity'))
        self.assertRedirects(response,
                             reverse('login')+'?next={}'.format(reverse('crm:new_activity')))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('crm:new_client'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('crm:new_contact'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('crm:new_activity'))
        self.assertEqual(response.status_code, 200)

    def test_distinct_client(self):
        self.object = models.Client(name='test1', loyal=True, owner=self.user)
        self.object1 = models.Client(name='test2', loyal=True)
        self.object.save()
        self.object1.save()

        #Недоступность клиентов без аутентификации
        response = self.client.get(reverse('crm:client', kwargs={'pk': 1}))
        self.assertIn("You don't have rights to view this client", response.content)

        response = self.client.get(reverse('crm:client', kwargs={'pk': 2}))
        self.assertIn("You don't have rights to view this client", response.content)
        #Попытка обращения к несуществующему клиенту без аутентификации
        response = self.client.get(reverse('crm:client', kwargs={'pk': 3}))
        self.assertTrue(response.content.startswith('<h1>Not Found</h1>'))

        self.client.login(username='testuser', password='testpass')
        #Успешная попытка получения информации о клиенте принадлежащем пользователю
        response = self.client.get(reverse('crm:client', kwargs={'pk': 1}))
        self.assertNotIn("You don't have rights to view this client", response.content)
        #Не успешная попытка получения информации о клиента не принадлежащем пользователю
        response = self.client.get(reverse('crm:client', kwargs={'pk': 2}))
        self.assertIn("You don't have rights to view this client", response.content)
        #Попытка обращения к несуществующему клиенту с аутентификацией
        response = self.client.get(reverse('crm:client', kwargs={'pk': 3}))
        self.assertTrue(response.content.startswith('<h1>Not Found</h1>'))

    def test_distinct_contact(self):
        self.object = models.Contact(first_name='test1', last_name='test',
                                     email='test@test.com', phone='123',
                                     owner=self.user)

        self.object1 = models.Contact(first_name='test2', last_name='test',
                                      email='test@test.com', phone='123')
        self.object.save()
        self.object1.save()

        #Недоступность контактов без аутентификации
        response = self.client.get(reverse('crm:contact', kwargs={'pk': 1}))
        self.assertIn("You don't have rights to view this contact", response.content)

        response = self.client.get(reverse('crm:contact', kwargs={'pk': 2}))
        self.assertIn("You don't have rights to view this contact", response.content)
        #Попытка обращения к несуществующему контакту без аутентификации
        response = self.client.get(reverse('crm:contact', kwargs={'pk': 3}))
        self.assertTrue(response.content.startswith('<h1>Not Found</h1>'))

        self.client.login(username='testuser', password='testpass')
        #Успешная попытка получения информации о контакте принадлежащем пользователю
        response = self.client.get(reverse('crm:contact', kwargs={'pk': 1}))
        self.assertNotIn("You don't have rights to view this contact", response.content)
        #Не успешная попытка получения информации о контакте не принадлежащем пользователю
        response = self.client.get(reverse('crm:contact', kwargs={'pk': 2}))
        self.assertIn("You don't have rights to view this contact", response.content)
        #Попытка обращения к несуществующему контакту с аутентификацией
        response = self.client.get(reverse('crm:client', kwargs={'pk': 3}))
        self.assertTrue(response.content.startswith('<h1>Not Found</h1>'))

    def test_distinct_activity(self):
        self.object_contact = models.Contact(first_name='test1', last_name='test',
                                            email='test@test.com', phone='123',
                                            owner=self.user)

        self.object_client = models.Client(name='test1', loyal=True, owner=self.user)

        self.object_contact.save()
        self.object_client.save()

        self.object = models.Activity(title='test', text='test', contact=self.object_contact,
                                      client=self.object_client, owner=self.user)
        self.object1 = models.Activity(title='test', text='test', contact=self.object_contact,
                                       client=self.object_client)

        self.object.save()
        self.object1.save()

        #Недоступность активности без аутентификации
        response = self.client.get(reverse('crm:activity', kwargs={'pk': 1}))
        self.assertIn("You don't have rights to view this activity", response.content)

        response = self.client.get(reverse('crm:activity', kwargs={'pk': 2}))
        self.assertIn("You don't have rights to view this activity", response.content)
        #Попытка обращения к несуществующей активности без аутентификации
        response = self.client.get(reverse('crm:activity', kwargs={'pk': 3}))
        self.assertTrue(response.content.startswith('<h1>Not Found</h1>'))

        self.client.login(username='testuser', password='testpass')
        #Успешная попытка получения информации о активносте принадлежащем пользователю
        response = self.client.get(reverse('crm:activity', kwargs={'pk': 1}))
        self.assertNotIn("You don't have rights to view this activity", response.content)
        #Не успешная попытка получения информации о активносте не принадлежащем пользователю
        response = self.client.get(reverse('crm:activity', kwargs={'pk': 2}))
        self.assertIn("You don't have rights to view this activity", response.content)
        #Попытка обращения к несуществующей активности с аутентификацией
        response = self.client.get(reverse('crm:activity', kwargs={'pk': 3}))
        self.assertTrue(response.content.startswith('<h1>Not Found</h1>'))


class ActivityChangeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')

        self.object_client = models.Client(name='test1', loyal=True, owner=self.user)
        self.object_client.save()

        self.object_contact = models.Contact(first_name='test1', last_name='test',
                                             email='test@test.com', phone='123',
                                             client=self.object_client, owner=self.user)
        self.object_contact.save()

        self.object = models.Activity(title='test', text='test', contact=self.object_contact,
                                      client=self.object_client, owner=self.user)
        self.object.save()

    def test_change_client(self):
        self.object_client1 = models.Client(name='test2', loyal=True, owner=self.user)
        self.object_client1.save()

        self.object_contact1 = models.Contact(first_name='test2', last_name='test',
                                             email='test@test.com', phone='123',
                                             client=self.object_client1, owner=self.user)
        self.object_contact1.save()
        #Пробуем изменить активность выбрав клиента, который не связан с контактом
        data_client_input = {'title': 'test', 'text': 'test', 'client': 2,
                             'contact': 1}

        response = self.client.post(reverse('crm:activity', kwargs={'pk': 1}), data_client_input)
        self.assertIn('Chosen contact doesn&#39;t belong to chosen client', response.content)

        #Аналогично пытаемся отправить форму с контактом не связанным с клиентом
        data_contact_input = {'title': 'test', 'text': 'test', 'client': 1,
                              'contact': 2}

        response = self.client.post(reverse('crm:activity', kwargs={'pk': 1}), data_contact_input)
        self.assertIn('Chosen contact doesn&#39;t belong to chosen client', response.content)
        #Передаем связанных клиента/контакта, успешно меняем запись
        data_correct_input = {'title': 'test', 'text': 'test', 'client': 2,
                              'contact': 2}

        response = self.client.post(reverse('crm:activity', kwargs={'pk': 1}), data_correct_input)
        self.assertRedirects(response,
                             reverse('crm:activity', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        #Проверяем, что новые значения сохранились в базе данных
        activity = models.Activity.objects.get(pk=1)
        self.assertTrue(activity.client.id == activity.contact.id == 2)

        #Проверяем невозможность изменения отправленной активности
        content = {'action': 'Send'}
        self.client.post(reverse('crm:activity', kwargs={'pk': 1}), content)
        activity = models.Activity.objects.get(pk=1)

        self.assertIsNotNone(activity.send_date) #Проверяем, что дата отправки проставилась


        data_correct_input = {'title': 'test', 'text': 'test', 'client': 1,
                              'contact': 1}

        response = self.client.post(reverse('crm:activity', kwargs={'pk': 1}), data_correct_input)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', None, "You can't change activity which was sent")














