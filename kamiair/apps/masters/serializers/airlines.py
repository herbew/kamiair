# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from kamiair.apps.masters.models.airlines import Airlines

log = logging.getLogger(__name__)

class AirlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airlines
        fields = ['id', 'code', 'name']
