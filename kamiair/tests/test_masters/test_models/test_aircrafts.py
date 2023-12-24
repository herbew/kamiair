from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from kamiair.apps.masters.models.airlines import Airlines
from kamiair.apps.masters.models.aircrafts import Aircrafts

class AircraftTestCase(TestCase):
    AIRLINE_CODE = "KAMI"
    TAIL_NUMBER = "KM-001"
    def setUp(self):
        airline = Airlines.objects.create(code=self.AIRLINE_CODE, name="KAMI Airlines" )
        Aircrafts.objects.create(airline=airline, tail_number=self.TAIL_NUMBER)
    
    def test_retrieve_airline(self):
        aircraft = Aircrafts.objects.get(tail_number=self.TAIL_NUMBER)
        self.assertEqual(aircraft.airline.code, self.AIRLINE_CODE)
        
    def test_retrieve_aircraft(self):
        aircraft = Aircrafts.objects.get(tail_number=self.TAIL_NUMBER)
        self.assertEqual(aircraft.airline.code, self.AIRLINE_CODE)
        self.assertEqual(aircraft.tail_number, self.TAIL_NUMBER)
    
    def test_retrieve_aircraft_engine(self):
        aircraft = Aircrafts.objects.get(tail_number=self.TAIL_NUMBER)
        fuel_capacity = aircraft.id * aircraft.CONST_CAPACITY
        fuel_consume = aircraft.id / aircraft.CONST_CONSUME
        fuel_consume_add = fuel_consume * aircraft.CONST_ADD_CONSUME
        
        self.assertEqual(aircraft.fuel_capacity, fuel_capacity)
        self.assertEqual(aircraft.fuel_consume, fuel_consume)
        self.assertEqual(aircraft.fuel_consume_add, fuel_consume_add)
        
        
        
        