from __future__ import unicode_literals, absolute_import

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

from kamiair.apps.masters.models.airlines import Airlines
from kamiair.apps.masters.models.aircrafts import Aircrafts
from kamiair.apps.assumptions.models.passengers import PassengerAssumptions

class PassengerAssumptionsAPITests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path("api/", include('kamiair.apps.apis.urls',
        namespace='apis'))
    ]
    
    AIRLINE_CODE = "KAMI"
    
    AIRCRAFTS = ["KM-001", "KM-002", "KM-003", "KM-004", "KM-005",
                 "KM-006", "KM-007", "KM-008", "KM-009", "KM-010"]
    
    def setUp(self):
        airline = Airlines.objects.create(code=self.AIRLINE_CODE, name="KAMI Airlines" )
        for tail_number in self.AIRCRAFTS:
            aircraft = Aircrafts.objects.create(
                airline=airline, 
                tail_number=tail_number)
            
        return super().setUp()
    
    def test_retrieve_airline(self):
        airline = Airlines.objects.get(code=self.AIRLINE_CODE)
        self.assertEqual(airline.code, self.AIRLINE_CODE)
        self.assertEqual(airline.name, "KAMI Airlines")
        
    def test_retrieve_aircrafts(self):
        i = 1
        for aircraft in Aircrafts.objects.all().order_by("id"):
            self.assertEqual(aircraft.id, i)
            self.assertEqual(aircraft.tail_number, self.AIRCRAFTS[i-1])
            i += 1
            
    def test_get_assumption_passanger_01(self):
        params = dict(
                aircraft_id=1,
                total_passenger=10,
            )
        
        url = reverse('apis:get_assumption_passenger', 
                      args=[params["aircraft_id"], 
                            params["total_passenger"]])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data'][0]
        
        pa = PassengerAssumptions.objects.get(
            aircraft__id=params["aircraft_id"],
            total_passenger=params["total_passenger"])
        
        self.assertEqual(data["attributes"]["aircraft"]["id"], params["aircraft_id"])
        self.assertEqual(data["attributes"]["total_passenger"], params["total_passenger"])
        self.assertEqual(data["attributes"]["max_minutes"], pa.max_minutes)
        
    def test_post_assumption_passanger_01(self):
        url = reverse('apis:post_assumption_passenger')
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        params = dict(
                aircraft_id=1,
                total_passenger=10,
            )
        
        
        client = APIClient()
        response = client.post(url, dict(aircraft_id=1, total_passenger=10))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()['data'][0]
        
        pa = PassengerAssumptions.objects.get(
            aicraft__id=params["aircraft_id"],
            total_passenger=params["total_passenger"])
        
        self.assertEqual(data["attributes"]["aircraft"]["id"], params["aircraft_id"])
        self.assertEqual(data["attributes"]["total_passenger"], params["total_passenger"])
        self.assertEqual(data["attributes"]["max_minutes"], pa.max_minutes)
        
    def tearDown(self):
        return super().tearDown()