# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from kamiair.apps.masters.models.aircrafts import Aircrafts
from kamiair.apps.assumptions.models.passengers import PassengerAssumptions
from kamiair.apps.masters.serializers.aircrafts import AircraftsSerializer

log = logging.getLogger(__name__)

class PassengerAssumptionsSerializer(serializers.ModelSerializer):
    aircraft = AircraftsSerializer()
    class Meta:
        model = PassengerAssumptions
        fields = ['id', 'aircraft', 'total_passenger', 'max_minutes']
