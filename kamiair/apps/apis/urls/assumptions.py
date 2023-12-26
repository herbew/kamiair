from __future__ import unicode_literals, absolute_import

import logging

from django.urls import path

from kamiair.apps.apis.views.assumptions import (
    PostPassengerAssumptionsAPIView,
    GetPassengerAssumptionsAPIView
    )

log = logging.getLogger(__name__)

urlpatterns = [
     path('get/assumption/<int:aircraft_id>/passenger/<int:total_passenger>/', 
          GetPassengerAssumptionsAPIView.as_view(), 
          name='get_assumption_passenger'),
     ]