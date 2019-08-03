from django.urls import path

from .views import *

urlpatterns = [
    path('send_captcha/', SendCaptchaView.as_view())
]
