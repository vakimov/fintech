from django.shortcuts import render
from rest_framework import viewsets

from credits import serializers
from credits import models


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Organization.objects.all().order_by('name')
    serializer_class = serializers.OrganizationSerializer
