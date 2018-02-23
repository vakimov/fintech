# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from credits import models
from credits.form import OfferForm


class ExtendedUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets[:1] + (
        ('Доступ к api', {'fields': ('access_type',)}),
    ) + UserAdmin.fieldsets[1:]


admin.site.register(models.User, ExtendedUserAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    fields = ('name',)


admin.site.register(models.Organization, OrganizationAdmin)


class OfferAdmin(admin.ModelAdmin):
    form = OfferForm
    list_display = (
        'id', 'created_at', 'name', 'view_organization',
        'category',
        'min_score', 'max_score',
    )
    list_display_links = (
        'id',
        'name',
    )
    date_hierarchy = 'created_at'
    raw_id_fields = ('organization',)

    search_fields = [
        'name', 'organization__name',
    ]

    def view_organization(self, obj):
        return obj.organization

    view_organization.short_description = 'Организация'


admin.site.register(models.Offer, OfferAdmin)


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'surname', 'first_name', 'patronymic',
        'birth_day', 'phone', 'passport_number', 'view_score',
    )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'surname', 'first_name', 'patronymic')
    fields = (
        'surname', 'first_name', 'patronymic',
        'birth_day', 'phone', 'passport_number', 'score',
    )
    search_fields = ['surname', 'first_name', 'patronymic']

    def view_score(self, obj):
        return obj.score

    view_score.short_description = 'Скорринговый балл'

    view_score.empty_value_display = '0'


admin.site.register(models.CustomerProfile, CustomerProfileAdmin)


class ApplicationStatusFilter(admin.SimpleListFilter):
    title = 'Статус'

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return models.Application.STATUSES

    def queryset(self, request, queryset):
        value = self.value()
        return queryset.filter(status=value) if value else queryset


class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'sent_at',
        'customer_profile',
        'offer', 'status',
    )
    list_display_links = (
        'id',
        'customer_profile',
    )
    raw_id_fields = ('customer_profile', 'offer')

    date_hierarchy = 'created_at'
    list_filter = (ApplicationStatusFilter,)

    search_fields = [
        'customer_profile__surname',
        'customer_profile__first_name',
        'customer_profile__patronymic',
    ]


admin.site.register(models.Application, ApplicationAdmin)
