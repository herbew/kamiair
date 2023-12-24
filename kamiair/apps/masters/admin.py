from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from kamiair.apps.masters.models.airlines import Airlines
from kamiair.apps.masters.models.aircrafts import Aircrafts

admin.site.register(Airlines)
admin.site.register(Aircrafts)