from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)

USER_TYPE_CHOICES = (
        ('0000', _('Administrator')),
        ('0010', _('Staff')),
        ('0020', _('Customer')),
        ('0000', _('Others')),
    )

GENDER_CHOICES = (
        ('m',_('Man')),
        ('w',_('Woman')),
    )

