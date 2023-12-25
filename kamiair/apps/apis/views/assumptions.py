from __future__ import unicode_literals, absolute_import

import logging
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (MultiPartParser, FormParser, FileUploadParser,
            JSONParser
            )

from kamiair.apps.masters.models.aircrafts import Aircrafts
from kamiair.apps.assumptions.models.passengers import PassengerAssumptions
from kamiair.apps.assumptions.serializers.passengers import PassengerAssumptionsSerializer


log = logging.getLogger(__name__)


class PostPassengerAssumptionsAPIView(generics.ListAPIView):
    serializer_class = PassengerAssumptionsSerializer
    permission_classes = [] #[IsAuthenticated]
    
    parser_classes = [MultiPartParser, FormParser, FileUploadParser,
            JSONParser]
    
    def get_queryset(self):
        
        data = self.request.data
        
        if data:
            # Checking the filter 
            try:
                aircraft_id = int(data['aircraft_id'])
            except:
                return Response(
                    _("Invalid Aircraft ID value! Please enter the ID = 1 to 10."), 
                    status=status.HTTP_400_BAD_REQUEST) 
            try:
                total_passenger = data['total_passenger']
                if total_passenger < 0:
                    return Response(
                        _("Invalid Total Passenger value! Please enter the positive number"), 
                        status=status.HTTP_400_BAD_REQUEST) 
            except:
                return Response(
                    _("Invalid Total Passenger value! Please enter the positive number"), 
                    status=status.HTTP_400_BAD_REQUEST) 
                
            # Create or get the PassengerAssumptions
            try:
                aircraft = Aircraft.objects.get(id=aircraft_id)
            except Exception as e:
                return Response(
                    _("Invalid Aircraft ID value! Please enter the ID = 1 to 10."), 
                    status=status.HTTP_400_BAD_REQUEST) 
                
            queryset, created = PassengerAssumptions.objects.get_or_create(
                aircraft=aircraft, total_passenger=total_passenger
                )
            
            return queryset
            
            
            
            
            
            
                
    def get(self, request, *args, **kwargs):
        return Response(_("No support GET method!"))
    
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    