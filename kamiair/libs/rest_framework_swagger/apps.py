from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RFSwaggerConfig(AppConfig):
    verbose_name = _('RestFrameworkSwagger')
    name = 'kamiair.libs.rest_framework_swagger'
