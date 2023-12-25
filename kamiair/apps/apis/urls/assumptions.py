from __future__ import unicode_literals, absolute_import

import logging

from django.urls import path

from kamiair.apps.apis.views.assumptions import PostPassengerAssumptionsAPIView

log = logging.getLogger(__name__)

urlpatterns = [
     path('post/assumption/passenger/', 
          PostPassengerAssumptionsAPIView.as_view(), 
          name='post_assumption_passenger'),
     ]