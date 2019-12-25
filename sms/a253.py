import datetime
import json
import logging
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


class A253:

    def __init__(self):
        self.appid = settings.SMS.get('appid', None)
        self.secret = settings.SMS.get('secret', None)

    def send_sms(self, mobile, data):
        """
        发送短信

        """
        now = datetime.datetime.now()
        sendtime = now.strftime('%Y%m%d%H%M')
        data = {
            'account': self.appid,
            'password': self.secret,
            'msg': data,
            'phone': mobile,
            'sendtime': sendtime
        }
        data = json.dumps(data).encode('utf8')
        url = 'http://smssh1.253.com/msg/send/json'
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(url=req, data=data) as f:
            res = f.read().decode('utf8')

        return res
