# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from rest_framework import serializers

from credits import models


class CustomerProfileSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.changed_at = timezone.now()
        return super(CustomerProfileSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.CustomerProfile
        fields = (
            'id', 'created_at', 'changed_at', 'first_name',  'patronymic',  'surname',  'birth_day',
            'phone',  'passport_number', 'score',
        )
        read_only_fields = ('id', 'created_at', 'changed_at')


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Organization
        fields = ('id', 'name',)


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    organization = OrganizationSerializer(many=False, read_only=True)

    class Meta:
        model = models.Offer
        fields = (
            'id', 'started_rotating_at',  'ended_rotating_at',  'name',
            'category',  'min_score',  'max_score',  'organization',
        )


class ApplicationSerializer(serializers.ModelSerializer):

    customer_profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    offer = OfferSerializer(many=False, read_only=True)

    class Meta:
        model = models.Application
        fields = (
            'id', 'created_at', 'sent_at', 'customer_profile',  'offer',  'status',
        )
        read_only_fields = ('id', 'created_at', 'sent_at', 'status')


class ApplicationSendSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.sent_at = timezone.now()
        super(ApplicationSendSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.Application
        fields = ('id', 'created_at', 'sent_at', 'customer_profile',  'offer', 'status')
        read_only_fields = ('id', 'created_at', 'sent_at', 'status')


class ApplicationEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Application
        fields = ('id', 'created_at', 'sent_at', 'customer_profile',  'offer', 'status')
        read_only_fields = ('id', 'created_at',)
