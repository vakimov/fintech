# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from credits import serializers
from credits import models
from credits import permissions
from credits.filters import DescribedOrderingFilter
from credits.filters import FilterBackend


class CustomerProfileListCreate(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer

    permission_classes = (
        IsAuthenticated,
        permissions.permission_any(models.User.SUPERUSER, models.User.PARTNERS)
    )

    filter_backends = (FilterBackend, filters.SearchFilter, DescribedOrderingFilter)

    filter_fields = (
        'first_name', 'patronymic', 'surname', 'birth_day',
        'phone', 'passport_number', 'score',
        'created_at', 'changed_at',
    )
    ordering_fields = (
        'first_name', 'patronymic', 'surname', 'birth_day', 'score',
        'created_at', 'changed_at',
    )
    ordering = ('id',)


class CustomerProfileRetrieveUpdateDestroy(mixins.RetrieveModelMixin,
                                           mixins.UpdateModelMixin,
                                           mixins.DestroyModelMixin,
                                           viewsets.GenericViewSet):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer

    permission_classes = (
        IsAuthenticated,
        permissions.permission_any(models.User.SUPERUSER,
                                   dict(user=models.User.PARTNERS, actions=['retrieve']))
    )


class ApplicationListCreate(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSendSerializer

    permission_classes = (
        IsAuthenticated,
        permissions.permission_any(models.User.SUPERUSER,
                                   dict(user=models.User.PARTNERS, actions=['create']),
                                   dict(user=models.User.CREDITORS, actions=['list']))
    )

    filter_backends = (FilterBackend, filters.SearchFilter, DescribedOrderingFilter)

    filter_fields = ('status',)
    ordering_fields = (
        'customer_profile__surname', 'created_at', 'changed_at', 'sent_at', 'status',
    )
    ordering = ('-sent_at',)


class ApplicationRetrieveUpdateDestroy(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationEditSerializer

    permission_classes = (
        IsAuthenticated,
        permissions.permission_any(models.User.SUPERUSER,
                                   dict(user=models.User.CREDITORS, actions=['retrieve']))
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if (request.user.access_type == models.User.CREDITORS
                and instance.status != models.Application.STATUS_RECEIVED):
            instance.sent_at = timezone.now()
            instance.status = models.Application.STATUS_RECEIVED
            instance.save()
        return Response(serializer.data)
