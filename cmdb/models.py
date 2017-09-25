# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    """List of countries for use in addresses."""

    name = models.CharField(max_length=200, verbose_name=_("Country Name"))
    token = models.CharField(max_length=3, verbose_name=_("Country Token"))

    def __unicode__(self):
        return "{} - {}".format(self.token, self.name)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Location(models.Model):
    """Categorization for the location (city) of assets."""

    name = models.CharField(max_length=200, verbose_name=_("Location Name"))
    token = models.CharField(max_length=3, verbose_name=_("Location Token"))
    zipcode = models.CharField(max_length=15, null=True, verbose_name=_("ZIP"))
    address = models.CharField(max_length=400, null=True,
                               verbose_name=_("Address"))
    # country = models.CharField(max_length=200, null=True,
    #                            verbose_name=_("Country"))
    country = models.ForeignKey(Country, null=True, verbose_name=_("Country"))

    def __unicode__(self):
        return "{} - {}".format(self.token, self.name)

    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")


class ComputerCategory(models.Model):
    """Categorization for Computers like server, workstation etc."""

    name = models.CharField(max_length=200, verbose_name=_("Category Name"))
    token = models.CharField(max_length=3, verbose_name=_("Category Token"))

    def __unicode__(self):
        return "{} - {}".format(self.token, self.name)

    class Meta:
        verbose_name = _("Computer Category")
        verbose_name_plural = _("Computer Categories")


class Person(models.Model):
    """Representation of a person object from AD"""

    path = models.CharField(max_length=400, verbose_name=_("LDAP-Path"))
    userid = models.CharField(max_length=50, verbose_name=_("User-ID"))
    sid = models.CharField(max_length=100, verbose_name=_("SID"))
    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    title = models.CharField(max_length=200, null=True, verbose_name=_("Title"))
    department = models.CharField(max_length=200, null=True,
                                  verbose_name=_("Department"))
    employee = models.CharField(max_length=50, null=True,
                                verbose_name=_("Employee No."))
    mail = models.CharField(max_length=200, null=True, verbose_name=_("Mail"))
    fax = models.CharField(max_length=50, null=True, verbose_name=_("Fax"))
    mobile = models.CharField(max_length=50, null=True,
                              verbose_name=_("Mobile"))
    phone = models.CharField(max_length=50, null=True, verbose_name=_("Phone"))
    # Flags and relations
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    unlocked = models.BooleanField(default=True, verbose_name=_("Unlocked"))
    pwsv = models.BooleanField(default=True, verbose_name=_("PW Still Valid"))
    pwex = models.BooleanField(default=True, verbose_name=_("PW Expires"))
    office = models.ForeignKey(Location, null=True, verbose_name=_("Office"))

    def __unicode__(self):
        return "{} ({})".format(self.name, self.userid)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class SPN(models.Model):
    """Collection of Service Principal Names for a User"""

    name = models.CharField(max_length=200)         # servicePrincipalName
    userid = models.ForeignKey(Person)


class Workstation(models.Model):
    """Representation of a workstation (laptop or desktop)"""

    path = models.CharField(max_length=400, verbose_name=_("LDAP-Path"))
    name = models.CharField(max_length=200, verbose_name=_("Computer Name"))
    dnsname = models.CharField(max_length=200, verbose_name=_("DNS Name"))
    sid = models.CharField(max_length=100, verbose_name=_("SID"))
    description = models.CharField(max_length=200, null=True,
                                   verbose_name=_("Description"))
    os = models.CharField(max_length=200, null=True, verbose_name=_("OS"))
    os_ver = models.CharField(max_length=200, null=True,
                              verbose_name=_("OS Version"))
    os_sp = models.CharField(max_length=200, null=True,
                             verbose_name=_("OS Service Pack"))
    category = models.ForeignKey(ComputerCategory, null=True,
                                 verbose_name=_("Computer Category"))
    location = models.ForeignKey(Location, null=True, verbose_name=_("Office"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("Workstation")
        verbose_name_plural = _("Workstations")


class Software(models.Model):
    """This holds information about Software installed via Altiris"""
    name = models.CharField(max_length=200, verbose_name=_("Software Name"))
    description = models.CharField(max_length=200,
                                   verbose_name=_("Description"))
    workstations = models.ManyToManyField(Workstation,
                                          verbose_name=_("Computer Name"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("Software")
        verbose_name_plural = _("Software")


class Printer(models.Model):
    """This holds information about Printers"""
    name = models.CharField(max_length=200, verbose_name=_("Software Name"))
    description = models.CharField(max_length=200,
                                   verbose_name=_("Description"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _("Printer")
        verbose_name_plural = _("Printers")
