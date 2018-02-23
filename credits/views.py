from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters
from rest_framework import mixins
from rest_framework.response import Response

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

    permission_classes = (permissions.IsSuperuserOrPartner,)

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


class CustomerProfileEdit(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer

    permission_classes = (permissions.IsSuperuser,)


class ApplicationListCreate(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.Application.objects.all()

    def get_serializer_class(self):
        if self.request and self.action == 'create':
            if self.request.user.access_type == models.User.PARTNERS:
                return serializers.ApplicationSendSerializer
            return serializers.ApplicationEditSerializer
        return serializers.ApplicationSerializer

    permission_classes = (permissions.IsSuperuserOrPartner,)

    filter_backends = (FilterBackend, filters.SearchFilter, DescribedOrderingFilter)

    filter_fields = ('status',)
    ordering_fields = ('customer_profile__surname', 'created_at', 'changed_at', 'sent_at', 'status')
    ordering = ('-sent_at',)


class ApplicationEdit(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer

    permission_classes = (permissions.IsSuperuser,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.access_type == models.User.PARTNERS:
            instance.status = models.Application.STATUS_SENT
        return Response(serializer.data)
