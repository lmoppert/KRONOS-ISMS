# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CmdbConfig(AppConfig):
    name = 'cmdb'
    verbose_name = _('CMDB')
