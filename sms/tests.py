from django.test import TestCase

from .models import *


class SmsTestCase(TestCase):
    def setUp(self):
        Template.objects.create(label='test', code='test', content='【漫点科技】验证码%s，用于注册登录，请勿泄露')

    def test_send_sms(self):
        result = Sms.objects.send_sms('15550001234', 'test', '1234')
        self.assertTrue(result)
