# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

import django_filters
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework.filters import OrderingFilter

from phonenumber_field.modelfields import PhoneNumberField


class ExtendedFilterSet(FilterSet):

    class Meta:
        filter_overrides = {
            PhoneNumberField: {
               'filter_class': django_filters.CharFilter,
            },
        }


class FilterBackend(DjangoFilterBackend):
    default_filter_set = ExtendedFilterSet


class DescribedOrderingFilter(OrderingFilter):
    """Ordering filter with detailed description"""

    _ordering_description = _(
        'Which field to use when ordering the results.'
        ' Choices: {choices}. Default: "{default}"'
    )

    def get_ordering_description(self, view):
        choices = []
        for field in self.get_valid_fields(view.queryset, view):
            choices.append(field[0])
        return self._ordering_description.format(
            choices=', '.join(choices),
            default=','.join(self.get_default_ordering(view) or ()))

    def get_schema_fields(self, view):
        # Override method to change description
        from django.utils.encoding import force_text
        from rest_framework.compat import coreapi, coreschema
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(self.ordering_title),
                    description=force_text(self.get_ordering_description(view))
                )
            )
        ]
