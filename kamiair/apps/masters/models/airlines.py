from __future__ import unicode_literals, absolute_import

import logging

from datetime import datetime

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)

class Airlines(TimeStampedModel):
    """
    Description: 
        An airline is a company that provides air transport services for 
    traveling passengers and/or freight. 
    Airlines use aircraft to supply these services and may form partnerships or 
    alliances with other airlines for codeshare agreements, in which they 
    both offer and operate the same flight.
    
    fields:
        - pk
        - code string(4),
        - name string(255),
        - user_update value User.username, 
        - created
        - updated
    """
    code = models.CharField(
            _("Code"),
            max_length=4,
            unique=True,
            db_index=True)
    
    name = models.CharField(
            _("Name"),
            max_length=255)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)
    
    class Meta:
        app_label = "masters"
        verbose_name = u"Airlines"
        verbose_name_plural = u"0001-Airlines"
        
        ordering = ["code", "name"]
    
    def __init__(self, *args, **kwargs):
        super(Airlines, self).__init__(*args, **kwargs)
        self._datetime = datetime.now()
        self._user_update = None
        
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_user_update(self):
        return self._user_update
    
    def set_user_update(self, new_user):
        self._user_update = new_user       
    
    user_updated = property(get_user_update, set_user_update, None, "user_updated")  
    
    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Airlines, self).save(*args, **kwargs)







