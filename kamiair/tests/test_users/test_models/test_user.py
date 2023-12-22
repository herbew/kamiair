from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from kamiair.apps.users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="herbew")
        
    def test(self):
        user = Use.objects.get("herbew")
        self.assertEqual(user.username,'herbew')
    
    