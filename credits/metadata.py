# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.metadata import SimpleMetadata


class FilterMetadata(SimpleMetadata):
    """Add to metadata OPTIONS info about GET parameters (filters)"""

    def get_filter_info(self, schema_field):
        result = {}
        for field in schema_field:
            result.update({
                field.name: {
                    'required': field.required,
                    'parameter type': field.location,
                    'description': field.schema.description,
                    'type': field.type or 'string',
                }
            })
        return result

    def determine_actions(self, request, view):
        """
        For generic class based views we add information about
        the fields that are accepted for 'GET' method alongside with 'PUT' and 'POST'.
        """
        actions = super(FilterMetadata, self).determine_actions(request, view)
        method = 'GET'
        if method in view.allowed_methods:
            filters = {}
            for filter_backend in view.filter_backends:
                filters.update(self.get_filter_info(filter_backend().get_schema_fields(view)))
            if filters:
                actions[method] = filters

        return actions
