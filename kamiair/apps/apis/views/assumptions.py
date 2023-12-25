from __future__ import unicode_literals, absolute_import

import logging
from datetime import datetime, timedelta

from django.utils.translation import gettext_lazy as _

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (MultiPartParser, FormParser, FileUploadParser,
            JSONParser
            )

from kamiair.apps.masters.models.aircrafts import Aircrafts
from kamiair.apps.assumptions.models.passengers import PassengerAssumptions
from kamiair.apps.assumptions.serializers.passengers import PassengerAssumptionsSerializer
from oauthlib.uri_validate import query


log = logging.getLogger(__name__)

class GetPassengerAssumptionsAPIView(generics.ListAPIView):
    serializer_class = PassengerAssumptionsSerializer
    def get_queryset(self):
        # Checking the filter 
        try:
            aircraft_id = int(self.kwargs.get('aircraft_id',1))
        except:
            raise APIException(_("Invalid Aircraft ID value! Please enter the ID = 1 to 10."))
        
        try:
            total_passenger = int(self.kwargs.get('total_passenger',10))
            if total_passenger < 0:
                raise APIException(_("Invalid Total Passenger value! Please enter the positive number"))
        except:
            raise APIException(_("Invalid Total Passenger value! Please enter the positive number"))
            
        # Create or get the PassengerAssumptions
        try:
            aircraft = Aircrafts.objects.get(id=aircraft_id)
        except Exception as e:
            raise APIException(_("Invalid Aircraft ID value! Please enter the ID = 1 to 10."))
            
            
        queryset = PassengerAssumptions.objects.filter(aircraft=aircraft, total_passenger=total_passenger)
        
        if not queryset:
            pa, created = PassengerAssumptions.objects.get_or_create(
                aircraft=aircraft, total_passenger=total_passenger
                )
            
            queryset = PassengerAssumptions.objects.filter(aircraft=aircraft, total_passenger=total_passenger)
            
        return queryset
    
class PostPassengerAssumptionsAPIView(generics.ListAPIView):
    serializer_class = PassengerAssumptionsSerializer
    permission_classes = [] #[IsAuthenticated]
    
    
    def get_queryset(self):
        
        data = self.request.data
        
        if data:
            # Checking the filter 
            try:
                aircraft_id = int(data['aircraft_id'])
            except:
                raise APIException(_("Invalid Aircraft ID value! Please enter the ID = 1 to 10."))
            
            try:
                total_passenger = int(data['total_passenger'])
                if total_passenger < 0:
                    raise APIException(_("Invalid Total Passenger value! Please enter the positive number"))
            except:
                raise APIException(_("Invalid Total Passenger value! Please enter the positive number"))
                
            # Create or get the PassengerAssumptions
            try:
                aircraft = Aircrafts.objects.get(id=aircraft_id)
            except Exception as e:
                raise APIException(_("Invalid Aircraft ID value! Please enter the ID = 1 to 10."))
            
            
            queryset = PassengerAssumptions.objects.filter(aircraft=aircraft, total_passenger=total_passenger)
            
            if not queryset:
                pa, created = PassengerAssumptions.objects.get_or_create(
                    aircraft=aircraft, total_passenger=total_passenger
                    )
                
                queryset = PassengerAssumptions.objects.filter(aircraft=aircraft, total_passenger=total_passenger)
            
            return queryset
        else:
            raise APIException(_("Invalid data post"))
            
                
    def get(self, request, *args, **kwargs):
        return Response(_("No support GET method!"))
    
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    


            
                
    
    