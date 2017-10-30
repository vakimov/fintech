from django.contrib import admin
from credits import models


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Organization, OrganizationAdmin)


class OfferAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Offer, OfferAdmin)


class CustomerProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.CustomerProfile, CustomerProfileAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Application, ApplicationAdmin)
