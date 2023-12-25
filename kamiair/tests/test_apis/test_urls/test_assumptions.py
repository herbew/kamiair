from __future__ import unicode_literals, absolute_import

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase

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
        
    # def test_retrieve_airline(self):
    #     """
    #     Ensure we can create a new account object.
    #     """
    #     url = reverse('apis:post_assumption_passenger')
    #
    #     headers = {'Content-Type':'application/x-www-form-urlencoded'}
    #     params = dict(
    #             aircraft_id=1,
    #             total_passenger=10,
    #         )
    #
    #     response = self.client.post(url, 
    #                                 data=params, 
    #                                 headers=headers,
    #                                 #auth=(self._username, self._password),
    #                                 format='json',
    #                                 verify=False)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
        
    def tearDown(self):
        return super().tearDown()