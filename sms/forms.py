from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Sms


class CaptchaForm(forms.Form):
    mobile = forms.CharField(label=_('mobile'), max_length=20)
    captcha = forms.CharField(label=_('captcha'), max_length=6)

    def clean(self):
        cleaned_data = super().clean()
        captcha = cleaned_data.get('captcha')
        mobile = cleaned_data.get('mobile')

        if not Sms.objects.valid_captcha(mobile, captcha):
            raise forms.ValidationError('验证码不正确')
