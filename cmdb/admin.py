# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from . import models


@admin.register(models.Person)
class PersonsAdmin(admin.ModelAdmin):
    """Admin view for the AD persons"""

    fieldsets = [
        (None,          {'fields': ['path', 'userid', 'sid']}),
        (_('Personal'), {'fields': ['name', 'title', 'department',
                                    'employee', 'office']}),
        (_('Contact'),  {'fields': ['mail', 'phone', 'mobile', 'fax']}),
        (_('Flags'),    {'fields': ['active', 'unlocked', 'pwsv', 'pwex']}),
    ]
    list_display = ('__unicode__', 'department', 'employee', 'phone', 'mobile',
                    'fax', 'active', 'unlocked', 'pwsv', 'pwex')
    search_fields = ('userid', 'name', 'department', 'employee', 'phone')
    list_filter = ('office', 'active', 'unlocked', 'pwsv', 'pwex')
    change_list_template = "admin/change_list_filter_sidebar.html"


@admin.register(models.Workstation)
class WorkstationsAdmin(admin.ModelAdmin):
    """Admin view for the AD workstations"""

    fieldsets = [
        (None,       {'fields': ['path', 'name', 'dnsname', 'sid']}),
        (_('Class'), {'fields': ['category', 'location', 'description']}),
        (_('OS'),    {'fields': ['os', 'os_ver', 'os_sp']}),
    ]
    list_display = ('__unicode__', 'os', 'os_ver', 'description')
    search_fields = ('dnsname', 'description')
    list_filter = ('location', 'category', 'os', 'os_ver', 'os_sp')
    change_list_template = "admin/change_list_filter_sidebar.html"


@admin.register(models.Software)
class SoftwareAdmin(admin.ModelAdmin):
    """Admin view for the AD Software Groups"""

    list_display = ('__unicode__', 'description')
    search_fields = ('name', 'description')


@admin.register(models.Printer)
class PrinterAdmin(admin.ModelAdmin):
    """Admin view for the AD Printer Groups"""

    list_display = ('__unicode__', 'description')
    search_fields = ('name', 'description')


@admin.register(models.ComputerCategory)
class ComputerCategoryAdmin(admin.ModelAdmin):
    """Admin view for Computer Categories"""

    list_display = ('token', 'name')
    search_fields = ('name', 'token')


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin view for Asset Locations"""

    list_display = ('token', 'address', 'zipcode', 'name', 'country')
    search_fields = ('name', 'token')


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin view for Asset Countries"""

    list_display = ('token', 'name')
    search_fields = ('name', 'token')
