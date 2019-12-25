# Django SMS

基于Django的短信模块

## Platforms

- [x] [253](https://zz.253.com/v5.html#/api_doc)
- [ ] [阿里云](https://help.aliyun.com/product/44282.html)

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
