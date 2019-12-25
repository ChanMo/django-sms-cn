# Django SMS


基于Django的短信模块

## Quick start

安装`django-sms`

```
$ pip install django-sms
```

在`settings.py`中修改INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'sms'
]
```

在`settings.py`底部加配置信息

```python
SMS = {
    'account': '',
    'password': ''
}
```

修改`urls.py`

```python
urlpatterns = [
    ...
    path('sms/', include('sms.urls'))
]
```

更新数据库

```bash
$ python manage.py migrate
```
