from __future__ import unicode_literals, absolute_import

import logging

from datetime import datetime

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from kamiair.apps.masters.models.airlines import Airlines

log = logging.getLogger(__name__)

class Aircrafts(TimeStampedModel):
    """
    Description: 
        An aircraft is a vehicle that is able to fly by gaining support from the 
        air. Common examples of aircraft include airplanes, helicopters, 
        airships (including blimps), gliders, paramotors, and hot air balloons.
        
    The company is assessing 10 different airplanes.
        - Each airplane has a fuel tank of (200 liters * id of the airplane) capacity. 
          For example, if
            the airplane id = 2, the fuel tank capacity is 2*200 = 400 liters.
            
        - The airplane fuel consumption per minute is the logarithm of the airplane id multiplied by
            0.80 liters.
        
        - Each passenger will increase fuel consumption for additional 0.002 liters per minute.
        
    NOTE:
        - Is ok using id become parameters fuel capacity, consume and additional consumption
        if using number or integer typed. By the way you can found issue type 
        if database id is string like MongoDB.

    
    fields:
        - pk
        - airline_id integer -- masters.airlines.pk
        - tail_number string(10),
        - user_update value User.username, 
        - fuel_capacity -- float
        - fuel_consume -- float
        - fuel_consume_add -- float
        - created
        - updated
    """
    
    CONST_CAPACITY = 200
    CONST_CONSUME = 0.80
    CONST_ADD_CONSUME = 0.002
    
    airline = models.ForeignKey(
        Airlines,
        verbose_name=_("Airline"),
        on_delete=models.CASCADE,
        db_index=True)
    
    tail_number = models.CharField(
            _("Tail Number"),
            max_length=10,
            unique=True,
            db_index=True)
    
    fuel_capacity = models.FloatField(
            _("Fuel Capacity"),
            default=0.0)
    
    fuel_consume = models.FloatField(
            _("Fuel Consumption"),
            default=0.0) #per minute
    
    fuel_consume_add = models.FloatField(
            _("Additional Fuel Consumption"),
            default=0.0) #per minute
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)
    
    class Meta:
        app_label = "masters"
        verbose_name = u"Aircrafts"
        verbose_name_plural = u"0002-Aircrafts"
        
        ordering = ["airline", "tail_number", ]
    
    def __init__(self, *args, **kwargs):
        super(Aircrafts, self).__init__(*args, **kwargs)
        self._datetime = datetime.now()
        self._user_update = None
        
    def __str__(self):
        return f"{self.airline.code} - {self.tail_number}"
    
    def get_user_update(self):
        return self._user_update
    
    def set_user_update(self, new_user):
        self._user_update = new_user       
    
    user_updated = property(get_user_update, set_user_update, None, "user_updated")  
    
    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Aircrafts, self).save(*args, **kwargs)

def aircraft_save(sender, instance, created, *args, **kwargs):
    if not isinstance(instance, Aircrafts):
        return
    
    if instance.id:
        pivot = float(instance.id)
        
        instance.fuel_capacity = pivot * instance.CONST_CAPACITY
        consume = pivot / instance.CONST_CONSUME
        instance.fuel_consume = consume
        instance.fuel_consume_add = consume * instance.CONST_ADD_CONSUME
        instance.save()
        
post_save.connect(aircraft_save, sender=Aircrafts)

