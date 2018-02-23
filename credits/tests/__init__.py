# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime as dt

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from credits import models


class AccessRuleTests(APITestCase):
    def setUp(self):
        models.User.objects.create(username='superuser', access_type=models.User.SUPERUSER)
        models.User.objects.create(username='partner', access_type=models.User.PARTNERS)
        models.User.objects.create(username='creditor', access_type=models.User.CREDITORS)
        org = models.Organization.objects.create(name='Org')
        self.offer = models.Offer.objects.create(
            organization=org,
            started_rotating_at=timezone.now(),
            ended_rotating_at=timezone.now(),
            min_score=300,
            max_score=301,
        )
        self.profile = models.CustomerProfile.objects.create(
            birth_day=dt.datetime.now(),
        )
        self.application = models.Application.objects.create(
            offer=self.offer,
            customer_profile=models.CustomerProfile.objects.create(
                birth_day=dt.datetime.now(),
            ),
        )
        self.profile_other = models.CustomerProfile.objects.create(
            birth_day=dt.datetime.now(),
        )
        self.client = APIClient()

    def _test_view_request(self, method, url, user, status_expected, data=None):
        self.client.force_authenticate(user=user)
        response = getattr(self.client, method)(url, data=data, format='json')
        self.assertEqual(response.status_code, status_expected)

    def test_superuser_actions(self):

        superuser = models.User.objects.get(username='superuser')

        # суперпользователи:
        # а) имеют доступ ко всем видам API;
        # б) имеют доступы ко всем заявкам и анкетам

        # 1. Партнерское API:
        #  * получение списка анкет (с сортировкой и фильтрами)
        self._test_view_request('get', '/credits/customer-profile/', superuser,
                                status.HTTP_200_OK)

        #  * просмотр анкеты по ID
        self._test_view_request('get', '/credits/customer-profile/1/', superuser,
                                status.HTTP_200_OK)

        #  * создание анкеты
        data = dict(
            first_name='Иван',
            patronymic='Иванович',
            surname='Иванов',
            birth_day='1930-01-01',
            phone='+74990000000',
            passport_number='0000000000',
        )
        self._test_view_request('post', '/credits/customer-profile/', superuser,
                                status.HTTP_201_CREATED, data=data)
        profile = models.CustomerProfile.objects.get(passport_number='0000000000')
        data['birth_day'] = dt.datetime.strptime(data['birth_day'], '%Y-%m-%d').date()
        self.assertDictEqual({k: getattr(profile, k) for k in data}, data)

        #  * отправка заявки в кредитные организации
        data = dict(
            customer_profile=self.profile.id,
            offer=self.offer.id,
        )
        self._test_view_request('post', '/credits/application/', superuser,
                                status.HTTP_201_CREATED, data=data)

        # 2. API кредитной организации:
        #  * получение списка заявок (с сортировкой и фильтрами)

        self._test_view_request('get', '/credits/application/', superuser, status.HTTP_200_OK)

        #  * просмотре заявки по ID

        self._test_view_request('get', '/credits/application/1/', superuser, status.HTTP_200_OK)
        application = models.Application.objects.get(pk=1)
        self.assertNotEqual(application.status, models.Application.STATUS_RECEIVED)

        # суперпользователи:
        # в) могут удалять и редактировать анкеты и заявки (операции каскадируются)

        data = dict(
            phone='+74950000000',
        )
        self._test_view_request('patch', '/credits/customer-profile/1/', superuser,
                                status.HTTP_200_OK, data=data)
        profile = models.CustomerProfile.objects.get(pk=1)
        self.assertEqual(profile.phone, data['phone'])

        data = dict(
            status=models.Application.STATUS_SENT,
        )
        self._test_view_request('patch', '/credits/application/1/', superuser,
                                status.HTTP_200_OK, data=data)
        application = models.Application.objects.get(pk=1)
        self.assertEqual(application.status, data['status'])

        self._test_view_request('delete', '/credits/customer-profile/1/', superuser,
                                status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.CustomerProfile.objects.filter(pk=1).exists())

        self._test_view_request('delete', '/credits/application/1/', superuser,
                                status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Application.objects.filter(pk=1).exists())

    def test_partner_actions(self):

        partner = models.User.objects.get(username='partner')
        # партнеры:
        # а) имеют доступ только к 1-му API

        # 1. Партнерское API:
        #  * получение списка анкет (с сортировкой и фильтрами)
        self._test_view_request('get', '/credits/customer-profile/', partner,
                                status.HTTP_200_OK)

        #  * просмотр анкеты по ID
        self._test_view_request('get', '/credits/customer-profile/1/', partner,
                                status.HTTP_200_OK)

        #  * создание анкеты
        data = dict(
            first_name='Иван',
            patronymic='Иванович',
            surname='Иванов',
            birth_day='1930-01-01',
            phone='+74990000000',
            passport_number='0000000000',
        )
        self._test_view_request('post', '/credits/customer-profile/', partner,
                                status.HTTP_201_CREATED, data=data)
        profile = models.CustomerProfile.objects.get(passport_number='0000000000')
        data['birth_day'] = dt.datetime.strptime(data['birth_day'], '%Y-%m-%d').date()
        self.assertDictEqual({k: getattr(profile, k) for k in data}, data)

        #  * отправка заявки в кредитные организации
        data = dict(
            customer_profile=self.profile.id,
            offer=self.offer.id,
        )
        self._test_view_request('post', '/credits/application/', partner,
                                status.HTTP_201_CREATED, data=data)

        # 2. API кредитной организации:
        #  * получение списка заявок (с сортировкой и фильтрами)

        self._test_view_request('get', '/credits/application/', partner,
                                status.HTTP_403_FORBIDDEN)

        #  * просмотре заявки по ID

        self._test_view_request('get', '/credits/application/1/', partner,
                                status.HTTP_403_FORBIDDEN)

        # партнеры:
        # б) не могут удалять и редактировать анкеты и заявки

        data = dict(
            phone='+74950000000',
        )
        self._test_view_request('patch', '/credits/customer-profile/1/', partner,
                                status.HTTP_403_FORBIDDEN, data=data)
        profile = models.CustomerProfile.objects.get(pk=1)
        self.assertNotEqual(profile.phone, data['phone'])

        data = dict(
            status=models.Application.STATUS_SENT,
        )
        self._test_view_request('patch', '/credits/application/1/', partner,
                                status.HTTP_403_FORBIDDEN, data=data)
        application = models.Application.objects.get(pk=1)
        self.assertNotEqual(application.status, data['status'])

        self._test_view_request('delete', '/credits/customer-profile/1/', partner,
                                status.HTTP_403_FORBIDDEN)
        self.assertTrue(models.CustomerProfile.objects.filter(pk=1).exists())

        self._test_view_request('delete', '/credits/application/1/', partner,
                                status.HTTP_403_FORBIDDEN)
        self.assertTrue(models.Application.objects.filter(pk=1).exists())

    def test_creditor_actions(self):

        creditor = models.User.objects.get(username='creditor')
        # кредитные организации:
        # а) не могут удалять и редактировать ничего

        data = dict(
            phone='+74950000000',
        )
        self._test_view_request('patch', '/credits/customer-profile/1/', creditor,
                                status.HTTP_403_FORBIDDEN, data=data)
        profile = models.CustomerProfile.objects.get(pk=1)
        self.assertNotEqual(profile.phone, data['phone'])

        data = dict(
            status=models.Application.STATUS_SENT,
        )
        self._test_view_request('patch', '/credits/application/1/', creditor,
                                status.HTTP_403_FORBIDDEN, data=data)
        application = models.Application.objects.get(pk=1)
        self.assertNotEqual(application.status, data['status'])

        self._test_view_request('delete', '/credits/customer-profile/1/', creditor,
                                status.HTTP_403_FORBIDDEN)
        self.assertTrue(models.CustomerProfile.objects.filter(pk=1).exists())

        self._test_view_request('delete', '/credits/application/1/', creditor,
                                status.HTTP_403_FORBIDDEN)
        self.assertTrue(models.Application.objects.filter(pk=1).exists())

        # кредитные организации:
        # б) при просмотре заявки по ID статус заявки меняется на RECIEVED

        # 2. API кредитной организации:
        #  * получение списка заявок (с сортировкой и фильтрами)

        self._test_view_request('get', '/credits/application/', creditor,
                                status.HTTP_200_OK)

        #  * просмотре заявки по ID
        application = models.Application.objects.get(pk=1)
        self.assertNotEqual(application.status, models.Application.STATUS_RECEIVED)
        self._test_view_request('get', '/credits/application/1/', creditor,
                                status.HTTP_200_OK)
        application = models.Application.objects.get(pk=1)
        self.assertEqual(application.status, models.Application.STATUS_RECEIVED)

        # кредитные организации:

        # 1. Партнерское API:
        #  * получение списка анкет (с сортировкой и фильтрами)
        self._test_view_request('get', '/credits/customer-profile/', creditor,
                                status.HTTP_403_FORBIDDEN)

        #  * просмотр анкеты по ID
        self._test_view_request('get', '/credits/customer-profile/1/', creditor,
                                status.HTTP_403_FORBIDDEN)

        #  * создание анкеты
        data = dict(
            first_name='Иван',
            patronymic='Иванович',
            surname='Иванов',
            birth_day='1930-01-01',
            phone='+74990000000',
            passport_number='0000000000',
        )
        self._test_view_request('post', '/credits/customer-profile/', creditor,
                                status.HTTP_403_FORBIDDEN, data=data)
        self.assertFalse(
            models.CustomerProfile.objects.filter(passport_number='0000000000').exists()
        )
