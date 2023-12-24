from __future__ import unicode_literals, absolute_import

from django.test import TestCase

from kamiair.apps.masters.models.airlines import Airlines
from kamiair.apps.masters.models.aircrafts import Aircrafts
from kamiair.apps.assumptions.models.passengers import PassengerAssumptions

class PassengerAssumptionsTestCase(TestCase):
    
    AIRLINE_CODE = "KAMI"
    
    AIRCRAFTS = dict(
        A01=dict(tail_number="KM-001", total_passenger=10),
        A02=dict(tail_number="KM-002", total_passenger=20),
        A03=dict(tail_number="KM-003", total_passenger=30)
        )
    
    def setUp(self):
        airline = Airlines.objects.create(code=self.AIRLINE_CODE, name="KAMI Airlines" )
        for airplane in self.AIRCRAFTS:
            aircraft = Aircrafts.objects.create(
                airline=airline, 
                tail_number=self.AIRCRAFTS[airplane]['tail_number'])
            
            PassengerAssumptions.objects.create(
                aircraft=aircraft,
                total_passenger=self.AIRCRAFTS[airplane]['total_passenger']
                )
            
    def test_retrieve_airline(self):
        airline = Airlines.objects.get(code=self.AIRLINE_CODE)
        self.assertEqual(airline.code, self.AIRLINE_CODE)
        
    def test_retrieve_aircraft(self):
        for airplane in self.AIRCRAFTS: 
            aircraft = Aircrafts.objects.get(
                tail_number=self.AIRCRAFTS[airplane]['tail_number'])
            
            self.assertEqual(aircraft.airline.code, self.AIRLINE_CODE)
            self.assertEqual(aircraft.tail_number, 
                             self.AIRCRAFTS[airplane]['tail_number'])
    
    def test_retrieve_aircraft_engine(self):
        for airplane in self.AIRCRAFTS: 
            aircraft = Aircrafts.objects.get(
                tail_number=self.AIRCRAFTS[airplane]['tail_number'])
            
            fuel_capacity = aircraft.id * aircraft.CONST_CAPACITY
            fuel_consume = aircraft.id / aircraft.CONST_CONSUME
            fuel_consume_add = fuel_consume * aircraft.CONST_ADD_CONSUME
            
            self.assertEqual(aircraft.fuel_capacity, fuel_capacity)
            self.assertEqual(aircraft.fuel_consume, fuel_consume)
            self.assertEqual(aircraft.fuel_consume_add, fuel_consume_add)
    
    def test_retrieve_passenger_assumption(self):
        for airplane in self.AIRCRAFTS: 
            
            pa = PassengerAssumptions.objects.get(
                aircraft__tail_number=self.AIRCRAFTS[airplane]['tail_number'],
                total_passenger=self.AIRCRAFTS[airplane]['total_passenger']
                )
            
            fuel_capacity = pa.aircraft.id * pa.aircraft.CONST_CAPACITY
            fuel_consume = pa.aircraft.id / pa.aircraft.CONST_CONSUME
            fuel_consume_add = fuel_consume * pa.aircraft.CONST_ADD_CONSUME
            
            total_consumption = ((pa.total_passenger * fuel_consume_add) + 
                             fuel_consume)
            
            max_minutes = fuel_capacity / total_consumption
            
            self.assertEqual(pa.max_minutes, max_minutes) 


