from rest_framework import permissions

from credits.models import User


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.access_type == User.SUPERUSER


class IsSuperuserOrCreditor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.access_type == User.SUPERUSER:
            return True
        return request.user.access_type == User.CREDITORS


class IsSuperuserOrPartner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.access_type == User.SUPERUSER:
            return True
        return request.user.access_type == User.PARTNERS
