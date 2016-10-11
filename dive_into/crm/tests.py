#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.db import IntegrityError
from django.db.models import ProtectedError
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
        #Попытка сохранения клиента с существующим именем
        self.object1 = models.Client(name='test', loyal=True)
        self.assertRaises(IntegrityError, self.object1.save)

    def test_diff_name(self):
        #Сохранение клиента с уникальным именем
        self.object1 = models.Client(name='test1', loyal=True)
        self.object1.save()
        self.assertEqual(models.Client.objects.count(), 2)


class PageAccessTest(TestCase):
    """
    Тестирование доступности страниц c/без
    авторизации, доступность несуществующих объектов
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.user1 = User.objects.create_user('testuser1', 'test@test.com', 'testpass1')

    def test_access(self):
        """
        Доступность страниц с созданием объектов
        без авторизации и с авторизацией
        """
        #Недоступность страниц создания объектов без авторизации
        #и проверка корректного редиректа на страницу аутентификации
        response = self.client.get(reverse('crm:new_client'))
        self.assertRedirects(response,
                             reverse('login') + '?next={}'.format(reverse('crm:new_client')))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('crm:new_contact'))
        self.assertRedirects(response,
                             reverse('login') + '?next={}'.format(reverse('crm:new_contact')))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('crm:new_activity'))
        self.assertRedirects(response,
                             reverse('login') + '?next={}'.format(reverse('crm:new_activity')))
        self.assertEqual(response.status_code, 302)

        #Доступность сраниц создания объектов с авторизацией
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('crm:new_client'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('crm:new_contact'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('crm:new_activity'))
        self.assertEqual(response.status_code, 200)

    def test_distinct_client(self):
        self.object = models.Client(name='test1', loyal=True, owner=self.user)
        self.object1 = models.Client(name='test2', loyal=True, owner=self.user1)
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
                                      email='test@test.com', phone='123',
                                      owner=self.user1)
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


class ActivityCreateChangeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.user1 = User.objects.create_user('testuser1', 'test@test.com', 'testpass1')
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

    def test_creation_activity(self):
        error = "Select a valid choice. That choice is not one of the available choices."
        #Попытка создания с несуществующим клиентом
        initial_data = {'title': 'test', 'text': 'test', 'client': 5,
                        'contact': 1}

        response = self.client.post(reverse('crm:new_activity'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'client', error)

        #Попытка создания с несуществующим контактом
        initial_data = {'title': 'test', 'text': 'test', 'client': 1,
                        'contact': 5}

        response = self.client.post(reverse('crm:new_activity'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'contact', error)

        #Успешная попытка создания
        initial_data = {'title': 'test', 'text': 'test', 'client': 1,
                        'contact': 1}

        response = self.client.post(reverse('crm:new_activity'), initial_data)

        self.assertRedirects(response, reverse('crm:activity', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        #Попытка создания с чужим клиентом/контактом
        self.object_client1 = models.Client(name='test2', loyal=True, owner=self.user1)
        self.object_client1.save()

        self.object_contact1 = models.Contact(first_name='test2', last_name='test',
                                              email='test@test.com', phone='123',
                                              client=self.object_client1, owner=self.user1)
        self.object_contact1.save()
        initial_data = {'title': 'test', 'text': 'test', 'client': 2,
                        'contact': 2}

        response = self.client.post(reverse('crm:new_activity'), initial_data)
        self.assertFormError(response, 'form', 'client', error)

    def test_change_activity(self):
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
        self.failIf(response.context['form'].is_valid())
        self.assertIn('Chosen contact doesn&#39;t belong to chosen client', response.content)

        #Аналогично пытаемся отправить форму с контактом не связанным с клиентом
        data_contact_input = {'title': 'test', 'text': 'test', 'client': 1,
                              'contact': 2}

        response = self.client.post(reverse('crm:activity', kwargs={'pk': 1}), data_contact_input)
        self.failIf(response.context['form'].is_valid())
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

        self.assertIsNotNone(activity.send_date)  #Проверяем, что дата отправки проставилась

        data_correct_input = {'title': 'test', 'text': 'test', 'client': 1,
                              'contact': 1}

        response = self.client.post(reverse('crm:activity', kwargs={'pk': 1}), data_correct_input)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', None, "You can't change activity which was sent")

        #Создаем еще одну активность
        self.object2 = models.Activity(title='test1', text='test1', contact=self.object_contact,
                                       client=self.object_client, owner=self.user)
        self.object2.save()

        self.client.login(username='testuser1', password='testpass1')  #Перелогиниваемся

        #Пробуем изменить - неуспешно, так как пользователь - не owner объекта
        data_correct_input = {'title': 'test1', 'text': 'test', 'client': 1,
                              'contact': 1}
        response = self.client.post(reverse('crm:activity', kwargs={'pk': 2}), data_correct_input)
        self.assertIn("You don't have rights to view this activity", response.content)

        #Пробуем удалить - неуспешно
        data_correct_input = {'action': 'Delete'}
        self.assertRaises(AttributeError, self.client.post,
                          path=reverse('crm:activity', kwargs={'pk': 2}),
                          data=data_correct_input)

        self.client.login(username='testuser', password='testpass')  #Перелогиниваемся

        #Пробуем изменить - успешно
        data_correct_input = {'title': 'test1', 'text': 'test', 'client': 2,
                              'contact': 2}
        response = self.client.post(reverse('crm:activity', kwargs={'pk': 2}), data_correct_input)
        self.assertRedirects(response,
                             reverse('crm:activity', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        #Пробуем удалить
        data_correct_input = {'action': 'Delete'}
        response = self.client.post(reverse('crm:activity', kwargs={'pk': 2}), data_correct_input)

        self.assertTrue(self.client.session['deleted_data'])  #Проверяем, что сохранили информацию
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('crm:main'))
        self.assertEqual(models.Activity.objects.count(), 1)


class ClientCreateChangeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.user1 = User.objects.create_user('testuser1', 'test@test.com', 'testpass1')
        self.client.login(username='testuser', password='testpass')

        self.object_client = models.Client(name='test', loyal=True, owner=self.user)
        self.object_client.save()

    def test_creation_client(self):
        #Попытка создания с cуществующим именем
        initial_data = {'name': 'test', 'loyal': True}

        response = self.client.post(reverse('crm:new_client'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'name', "Client with this Name already exists.")
        self.assertIn("Client with this Name already exists.", response.content)

        #Попытка создания без имени
        initial_data = {'loyal': True}

        response = self.client.post(reverse('crm:new_client'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'name', "This field is required.")
        self.assertIn("This field is required.", response.content)

        #Попытка создания c передачей пустой формы
        initial_data = {}
        response = self.client.post(reverse('crm:new_client'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn("This field is required.", response.content)

        #Успешная попытка созадния
        initial_data = {'name': 'test1', 'loyal': True}

        response = self.client.post(reverse('crm:new_client'), initial_data)
        self.assertRedirects(response,
                             reverse('crm:client', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

    def test_change_client(self):
        self.object_client1 = models.Client(name='test1', loyal=True, owner=self.user)
        self.object_client1.save()

        #Попытка изменения имени клиента на уже существующее
        initial_data = {'name': 'test1', 'loyal': True}
        response = self.client.post(reverse('crm:client', kwargs={'pk': 1}), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'name', "Client with this Name already exists.")

        #Попытка передачи пустого имени
        initial_data = {'loyal': True}
        response = self.client.post(reverse('crm:client', kwargs={'pk': 1}), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'name', "This field is required.")

        #Попытка передачи пустой формы
        initial_data = {}
        response = self.client.post(reverse('crm:client', kwargs={'pk': 1}), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'name', "This field is required.")

        #Успешная попытка изменения
        initial_data = {'name': 'test2'}
        response = self.client.post(reverse('crm:client', kwargs={'pk': 1}), initial_data)
        self.assertRedirects(response,
                             reverse('crm:client', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('crm:client', kwargs={'pk': 1}))

    def test_delete_client(self):
        self.object_contact = models.Contact(first_name='test1', last_name='test',
                                             email='test@test.com', phone='123',
                                             client=self.object_client, owner=self.user)
        self.object_contact.save()

        self.object = models.Activity(title='test', text='test', contact=self.object_contact,
                                      client=self.object_client, owner=self.user)
        self.object.save()

        #Неуспешное удаление, есть активность

        initial_data = {'action': 'Delete'}
        self.assertRaises(ProtectedError, self.client.post, path=reverse('crm:client', kwargs={'pk': 1}),
                          data=initial_data)

        self.object_client1 = models.Client(name='test1', loyal=True, owner=self.user)
        self.object_client1.save()

        self.client.login(username='testuser1', password='testpass1')  #Перелогиниваемся

        #Пробуем удалить - неуспешно
        data_correct_input = {'action': 'Delete'}
        self.assertRaises(AttributeError, self.client.post,
                          path=reverse('crm:client', kwargs={'pk': 2}),
                          data=data_correct_input)

        self.client.login(username='testuser', password='testpass')  #Перелогиниваемся

        #Успешное удаление
        initial_data = {'action': 'Delete'}
        response = self.client.post(reverse('crm:client', kwargs={'pk': 2}), initial_data)

        self.assertEqual(self.client.session['deleted_data'], 'Name: test1, Id: 2')  #Проверяем, что сохранили информацию
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('crm:main'))
        self.assertEqual(models.Client.objects.count(), 1)


class ContactCreateChangeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.user1 = User.objects.create_user('testuser1', 'test@test.com', 'testpass1')
        self.client.login(username='testuser', password='testpass')

        self.object_client = models.Client(name='test1', loyal=True, owner=self.user)
        self.object_client.save()

        self.object_contact = models.Contact(first_name='test1', last_name='test',
                                             email='test@test.com', phone='123',
                                             client=self.object_client, owner=self.user)
        self.object_contact.save()

        self.object_activity = models.Activity(title='test', text='test', contact=self.object_contact,
                                               client=self.object_client, owner=self.user)
        self.object_activity.save()

    def test_creation_contact(self):

        #Cоздание контакта с cуществующим именем
        initial_data = {'first_name': 'test1', 'last_name': 'test',
                        'email': 'test@test.com', 'phone': '123',
                        'client': 1}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertRedirects(response,
                             reverse('crm:contact', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        #Cоздание контакта без клиента
        initial_data = {'first_name': 'test1', 'last_name': 'test',
                        'email': 'test@test.com', 'phone': '123'}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertRedirects(response,
                             reverse('crm:contact', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)

        #Попытка создание контакта без имени
        initial_data = {'last_name': 'test',
                        'email': 'test@test.com', 'phone': '123'}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'first_name', "This field is required.")

        #Попытка создание контакта без email
        initial_data = {'first_name': 'test1', 'last_name': 'test',
                        'phone': '123'}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', "This field is required.")

        #Попытка создание контакта без phone
        initial_data = {'first_name': 'test1', 'last_name': 'test',
                        'email': 'test@gm.com'}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'phone', "This field is required.")

        #Попытка создание контакта с неверным форматом номера
        initial_data = {'first_name': 'test1', 'last_name': 'test',
                        'email': 'test@test.com', 'phone': 'test'}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'phone', "Enter a whole number.")

        #Попытка создание контакта с неверным форматом email
        initial_data = {'first_name': 'test1', 'last_name': 'test',
                        'email': 'test', 'phone': '123'}

        response = self.client.post(reverse('crm:new_contact'), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'email', "Enter a valid email address.")

    def test_change_contact(self):
        #Успешное изменение данных
        initial_data = {'first_name': 'test2', 'last_name': 'test',
                        'email': 'test@test.com', 'phone': '123'}

        response = self.client.post(reverse('crm:contact', kwargs={'pk': 1}), initial_data)
        self.assertRedirects(response,
                             reverse('crm:contact', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Contact.objects.get(pk=1).first_name, 'test2')

        #Не успешное изменение - нет фамилии
        initial_data = {'first_name': 'test2',
                        'email': 'test@test.com', 'phone': '123'}

        response = self.client.post(reverse('crm:contact', kwargs={'pk': 1}), initial_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response, 'form', 'last_name', "This field is required.")

    def test_delete_contact(self):
        #Попытка удаления чужого контакта
        self.client.login(username='testuser1', password='testpass1')

        initial_data = {'action': 'Delete'}
        self.assertRaises(AttributeError, self.client.post,
                          path=reverse('crm:contact', kwargs={'pk': 1}),
                          data=initial_data)

        #Перелогиниваемся - не успешная попытка удаления, так как есть активность
        self.client.login(username='testuser', password='testpass')
        initial_data = {'action': 'Delete'}
        self.assertRaises(ProtectedError, self.client.post, path=reverse('crm:client', kwargs={'pk': 1}),
                          data=initial_data)

        #Удаляем активность и затем контакт
        self.object_activity.delete()

        initial_data = {'action': 'Delete'}
        response = self.client.post(reverse('crm:contact', kwargs={'pk': 1}), initial_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('crm:main'))
        self.assertEqual(models.Contact.objects.count(), 0)


class MainPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.user1 = User.objects.create_user('testuser1', 'test@test.com', 'testpass1')
        self.client.login(username='testuser', password='testpass')

        self.object_client = models.Client(name='test1', loyal=True, owner=self.user)
        self.object_client.save()

        self.object_client1 = models.Client(name='test123', loyal=True, owner=self.user1)
        self.object_client1.save()

    def test_search_form(self):
        """
        Проверка формы поиска на главной страницы,
        должны выдавать только результаты доступное текущему пользователю
        """
        #Выполняем поиск клиента доступного текущему пользователю
        response = self.client.get(reverse('crm:main'), {'search': 'test'})
        self.assertEqual(len(response.context['search_clients']), 1)
        self.assertEqual(response.context['search_clients'][0].owner, self.user)

        #Выполняем поиск клиента недоступного другому пользователю
        response = self.client.get(reverse('crm:main'), {'search': 'test12'})
        self.assertEqual(response.context['search_clients'], 'no result')

        #Меняем пользовователя - выполняем поиск
        self.client.login(username='testuser1', password='testpass1')
        response = self.client.get(reverse('crm:main'), {'search': 'test'})
        self.assertEqual(len(response.context['search_clients']), 1)
        self.assertEqual(response.context['search_clients'][0].owner, self.user1)
        self.assertEqual(response.context['search_clients'][0].name, 'test123')

        #Разлогиниваемся и пробуем выполнить поиск
        self.client.logout()
        response = self.client.get(reverse('crm:main'), {'search': 'test1'})
        self.assertEqual(response.context['search_clients'], 'no auth')

