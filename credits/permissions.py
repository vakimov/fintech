# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions


def permission_any(*conditions):
    """Factory for Permission class that checks if any of condition is True

    Condition could be either dict with at least one of allowed criteria:
    * user (user access type)
    * actions ('list', 'retrieve', 'create', 'update', 'destroy')
    or user access type."""

    class PermissionCheck(permissions.BasePermission):

        def has_permission(self, request, view):

            def check(condition):
                if isinstance(condition, dict):
                    return all([
                        request.user.access_type == condition['user'] if 'user' in condition else True,
                        view.action in condition['actions'] if 'actions' in condition else True,
                    ])
                else:
                    access_type = condition
                    return request.user.access_type == access_type

            return any(check(c) for c in conditions)

    return PermissionCheck
