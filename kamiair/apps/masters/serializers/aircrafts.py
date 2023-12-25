# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from kamiair.apps.masters.models.aircrafts import Aircrafts
from kamiair.apps.masters.serializers.airlines import AirlinesSerializer

log = logging.getLogger(__name__)

class AircraftsSerializer(serializers.ModelSerializer):
    airline = AirlinesSerializer()
    class Meta:
        model = Aircrafts
        fields = ['id', 'airline', 'aircraft', 'tail_number', 
                  'fuel_capacity', 'fuel_consume', 'fuel_consume_add']
