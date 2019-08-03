import logging
import random
import re

from django.core.cache import cache
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Sms

logger = logging.getLogger(__name__)

class SendCaptchaView(views.APIView):
    """
    发送短信验证码

    参数: mobile
    """
    permission_classes = (AllowAny,)
    throttle_scope = 'sms'

    def post(self, request, format=None):
        mobile = request.data.get('mobile', None)

        if not re.match('^1\d{10}$', mobile):
            return Response({'detail':'电话号码不正确'},
                    status=status.HTTP_400_BAD_REQUEST)
        code = ''.join(str(random.randint(0,9)) for _ in range(6))
        cache.set(mobile, code, 60*5)
        Sms.objects.send_sms(mobile, 'captcha', code)

        return Response({'detail':'短信发送成功'})
