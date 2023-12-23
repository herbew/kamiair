from __future__ import unicode_literals, absolute_import

from django.test import TestCase
from kamiair.apps.users.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="herbew")
        
    def test_retrieve_user(self):
        user = User.objects.get(username="herbew")
        self.assertEqual(user.username,'herbew')
    
    