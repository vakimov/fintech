# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from credits import views


schema_view = get_swagger_view(title='Credits API')

router = routers.DefaultRouter()
router.register(r'customer-profile', views.CustomerProfileListCreate)
router.register(r'customer-profile', views.CustomerProfileRetrieveUpdateDestroy)
router.register(r'application', views.ApplicationListCreate)
router.register(r'application', views.ApplicationRetrieveUpdateDestroy)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schema/', schema_view),
]