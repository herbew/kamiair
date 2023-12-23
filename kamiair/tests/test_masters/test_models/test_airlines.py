from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from kamiair.apps.masters.models.airlines import Airlines

class AirlinesTestCase(TestCase):
    def setUp(self):
        Airlines.objects.create(code="KAMI", name="KAMI Airlines" )
        
    def test_retrieve_airline(self):
        airline = Airlines.objects.get(code="KAMI")
        self.assertEqual(airline.code,'KAMI')