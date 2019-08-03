from django.contrib import admin

from .models import *


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('label', 'code', 'content')


class SmsAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'content', 'is_success', 'created')
    list_per_page = 12
    list_filter = ('is_success', 'created')
    search_fields = ('mobile',)


admin.site.register(Template, TemplateAdmin)
admin.site.register(Sms, SmsAdmin)
