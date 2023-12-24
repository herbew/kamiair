from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from kamiair.apps.assumptions.models.passengers import PassengerAssumptions

admin.site.register(PassengerAssumptions)