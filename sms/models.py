import datetime
import json
import logging
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class Template(models.Model):
    label = models.CharField(_('label'), max_length=200)
    code = models.CharField(_('code'), max_length=50, unique=True)
    content = models.TextField(_('content'), blank=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('sms template')
        verbose_name_plural = _('sms template')


class SmsManager(models.Manager):
    def valid_captcha(self, mobile, code):
        " 判断验证码是否正确 "
        captcha = cache.get(mobile)

        if captcha and captcha == str(code):
            return True
        else:
            return False

    def send_sms(self, mobile, template_code, content=None):
        " 发送短信 "
        try:
            template = Template.objects.get(code=template_code)

            if content:
                content = template.content % content
            else:
                content = template.content
        except Exception as e:
            logger.warning(str(e))

            return False
        now = datetime.datetime.now()
        sendtime = now.strftime('%Y%m%d%H%M')
        data = {
            'account': settings.SMS['ACCOUNT'],
            'password': settings.SMS['PASSWORD'],
            'msg': content,
            'phone': mobile,
            'sendtime': sendtime
        }
        data = json.dumps(data).encode('utf8')
        url = 'http://smssh1.253.com/msg/send/json'
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        log = Sms.objects.create(
                mobile = mobile,
                template = template,
                content = content
                )
        with urllib.request.urlopen(url=req, data=data) as f:
            print(f.read().decode('utf-8'))

        return True

class Sms(models.Model):
    mobile = models.CharField(_('mobile'), max_length=15)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name=_('logs'))
    content = models.TextField(_('content'))
    is_success = models.BooleanField(_('is success'), default=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    objects = SmsManager()

    def __str__(self):
        return self.mobile

    class Meta:
        ordering = ['-created']
        verbose_name = _('sms log')
        verbose_name_plural = _('sms log')
