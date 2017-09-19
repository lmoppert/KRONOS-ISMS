# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Person(models.Model):
    """Representation of a person object from AD"""

    path = models.CharField(max_length=400)         # distinguishedName
    userid = models.CharField(max_length=50)        # sAMAccountName
    title = models.CharField(max_length=200)        # title
    name = models.CharField(max_length=200)         # cn
    department = models.CharField(max_length=200)   # department
    employee = models.CharField(max_length=50)      # employeenumber
    countrycode = models.CharField(max_length=5)    # c
    country = models.CharField(max_length=200)      # co
    location = models.CharField(max_length=50)      # l
    address = models.CharField(max_length=400)      # postalAddress
    mail = models.CharField(max_length=200)         # mail
    fax = models.CharField(max_length=50)           # facsimileTelephoneNumber
    mobile = models.CharField(max_length=50)        # mobile
    phone = models.CharField(max_length=50)         # telephoneNumber
    sid = models.CharField(max_length=100)          # objectSID

    def __unicode__(self):
        return "{} ({})".format(self.name, self.userid)


class Workstation(models.Model):
    """Representation of a workstation (laptop or desktop)"""

    path = models.CharField(max_length=400)         # distinguishedName
    name = models.CharField(max_length=200)         # cn
    dnsname = models.CharField(max_length=200)      # dNSHostName
    description = models.CharField(max_length=200)  # description
    location = models.CharField(max_length=50)      # location
    os = models.CharField(max_length=200)           # operatingSystem
    os_ver = models.CharField(max_length=200)       # operatingSystemVersion
    os_sp = models.CharField(max_length=200)        # operatingSystemServicePack
    sid = models.CharField(max_length=100)          # objectSID

    def __unicode__(self):
        return self.dnsname


class SPN(models.Model):
    """Collection of Service Principal Names for a USer"""

    name = models.CharField(max_length=200)         # servicePrincipalName
    userid = models.ForeignKey(Person)
