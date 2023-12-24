import logging

from datetime import datetime

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from kamiair.apps.masters.models.aircrafts import Aircrafts
from jedi.inference.value import instance

log = logging.getLogger(__name__)

class PassengerAssumptions(TimeStampedModel):
    """
    Description: 
        Assumptions passenger relate max minutes on the air(able to fly). 
    
    Specifications:
    - Allow for input of 10 airplanes with user defined id and passenger assumptions
    - Print total airplane fuel consumption per minute and maximum minutes able to fly
    
    fields:
        - pk
        - aircraft_id integer -- masters.aircrafts.pk
        - total_passanger -- integer positive
        - max_minutes -- float
        - created
        - updated
    """
    aircraft = models.ForeignKey(
        Aircrafts,
        verbose_name=_("Aircraft"),
        on_delete=models.CASCADE,
        db_index=True)
    
    total_passenger = models.PositiveSmallIntegerField(
            _("Total Passenger"),
            default=0)
    
    max_minutes = models.FloatField(
            _("Maximum Minutes"),
            default=0.0)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)
    
    class Meta:
        app_label = "passengers"
        verbose_name = u"PassengerAssumptions"
        verbose_name_plural = u"0001-Passenger Assumptions"
        
        ordering = ["aircraft", "total_passenger", ]
    
    def __init__(self, *args, **kwargs):
        super(PassengerAssumptions, self).__init__(*args, **kwargs)
        self._datetime = datetime.now()
        self._user_update = None
        
    def __str__(self):
        return f"{self.aircraft.tail_number} - {self.total_passenger}"
    
    def get_user_update(self):
        return self._user_update
    
    def set_user_update(self, new_user):
        self._user_update = new_user       
    
    user_updated = property(get_user_update, set_user_update, None, "user_updated")  
    
    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(PassengerAssumptions, self).save(*args, **kwargs)

def passenger_assumptions_save(sender, instance, created, *args, **kwargs):
    if not isinstance(instance, PassengerAssumptions):
        return
    
    if instance.aircraft:
        # Aircraft capacity of fuel
        fuel_capacity = instance.aircraft.fuel_capacity
        
        # Aircraft fuel consumption per minutes
        fuel_consume = instance.aircraft.fuel_consume
        
        # Aircraft fuel consumption additional for each passenger per minutes
        fuel_consume_add = instance.aircraft.fuel_consume_add
        
        total_consumption = ((instance.total_passenger * fuel_consume_add) + 
                             fuel_consume)
        
        instance.max_minutes = fuel_capacity / total_consumption
        instance.save()
        
post_save.connect(passenger_assumptions_save, sender=Aircrafts)

