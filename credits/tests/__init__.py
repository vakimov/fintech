import datetime as dt

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from credits import models
from credits import views


class AccessRuleTests(APITestCase):
    def setUp(self):
        models.User.objects.create(username='superuser', access_type=models.User.SUPERUSER)
        models.User.objects.create(username='partner', access_type=models.User.PARTNERS)
        models.User.objects.create(username='creditor', access_type=models.User.CREDITORS)
        org = models.Organization.objects.create(name='Org')
        self.offer = models.Offer.objects.create(
            organization=org,
            started_rotating_at=dt.datetime.now(),
            ended_rotating_at=dt.datetime.now(),
            min_score=300,
            max_score=301,
        )
        self.profile = models.CustomerProfile.objects.create(
            birth_day=dt.datetime.now(),
        )
        self.profile_other = models.CustomerProfile.objects.create(
            birth_day=dt.datetime.now(),
        )

    def _test_view_request(self, view, factory, method, url, user, status_expected, data=None):
        request = getattr(factory, method)(url, data=data)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status_expected)

    def test_list_create_permissions(self):
        """
        Ensure we can list and create permissions
        """
        factory = APIRequestFactory()
        superuser = models.User.objects.get(username='superuser')
        partner = models.User.objects.get(username='partner')
        creditor = models.User.objects.get(username='creditor')

        view = views.CustomerProfileListCreate.as_view({
            'get': 'list',
            'post': 'create'
        })

        url = '/credits/customer-profile/'
        self._test_view_request(view, factory, 'get', url, superuser, status.HTTP_200_OK)
        self._test_view_request(view, factory, 'get', url, partner, status.HTTP_200_OK)
        self._test_view_request(view, factory, 'get', url, creditor, status.HTTP_403_FORBIDDEN)

        data = dict(
            first_name='A',
            patronymic='A',
            surname='A',
            birth_day='2000-01-01',
            phone='+74990000000',
            passport_number='0000000000',
        )
        self._test_view_request(view, factory, 'post', url, superuser, status.HTTP_201_CREATED, data=data)
        self._test_view_request(view, factory, 'post', url, partner, status.HTTP_201_CREATED, data=data)
        self._test_view_request(view, factory, 'post', url, creditor, status.HTTP_403_FORBIDDEN, data=data)

        self.assertEqual(models.CustomerProfile.objects.filter(surname='A').count(), 2)

        view = views.ApplicationListCreate.as_view({
            'get': 'list',
            'post': 'create'
        })
        url = '/credits/application/'

        self._test_view_request(view, factory, 'get', url, superuser, status.HTTP_200_OK)
        self._test_view_request(view, factory, 'get', url, partner, status.HTTP_200_OK)
        self._test_view_request(view, factory, 'get', url, creditor, status.HTTP_403_FORBIDDEN)

        data = dict(
            customer_profile=self.profile.id,
            offer=self.offer.id,
        )
        self._test_view_request(view, factory, 'post', url, superuser, status.HTTP_201_CREATED, data=data)
        data = dict(
            customer_profile=self.profile_other.id,
            offer=self.offer.id,
        )
        self._test_view_request(view, factory, 'post', url, partner, status.HTTP_201_CREATED, data=data)
        self._test_view_request(view, factory, 'post', url, creditor, status.HTTP_403_FORBIDDEN, data=data)
