from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SmsConfig(AppConfig):
    name = 'sms'
    verbose_name = _('sms')

    def ready(self):
        import sms.receivers
