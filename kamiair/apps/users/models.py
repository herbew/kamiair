# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _

from kamiair.cores.choices import USER_TYPE_CHOICES, GENDER_CHOICES

log = logging.getLogger(__name__)

class User(AbstractUser):
    USER_TYPE_CHOICES=USER_TYPE_CHOICES
    GENDER_CHOICES=GENDER_CHOICES
    
    name = models.CharField(
            _("Complete Name"), 
            max_length=250)
    
    gender = models.CharField( 
            _("Gender"), 
            choices=GENDER_CHOICES, 
            max_length=1, 
            null=True, blank=True)
    
    birth_city = models.CharField(
            _("Birth City"), 
            max_length=100, 
            null=True, blank=True)
    
    birth_date = models.DateField(
            _("Birth Date"), 
            null=True, blank=True)
    
    typed = models.CharField(
            _("Type"), 
            choices=USER_TYPE_CHOICES, 
            max_length=4, 
            null=True, blank=True)
    
    mobile = models.CharField( 
            _("Mobile"), 
            max_length=64, 
            null=True, blank=True)
    
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        
    def __str__(self):
        
        if self.name:
            return self.name
        
        return self.username
