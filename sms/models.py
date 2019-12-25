import logging

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class Template(models.Model):
    """
    短信模板
    """
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

    def send_sms(self, mobile, template_code, content=None, sign=None):
        " 发送短信 "
        default = settings.SMS.get('default', '253')

        if not Template.objects.filter(code=template_code).exists():
            return False, '短信模板不存在'

        if default == '253':
            from .a153 import A253
            obj = A253()

            if content:
                content = template.content % content
            else:
                content = template.content
            obj.send_sms(mobile, content)
        elif default == 'aliyun':
            from .aliyun import Aliyun
            obj = Aliyun()
            obj.send_sms(mobile, sign, template_code, content)

        log = Sms.objects.create(
            mobile = mobile,
            template = template,
            content = content
        )

        return log


class Sms(models.Model):
    mobile = models.CharField(_('mobile'), max_length=15)
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
            related_name=_('logs'))
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
