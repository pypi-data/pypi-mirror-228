from django.contrib import admin
# 引入用户平台
from .models import *


# #
#
class PushPushAdmin(admin.ModelAdmin):
    fields = (
        'id', 'templet_id', 'plan_id', 'title', 'content', 'files', 'push_total', 'send_success', 'send_time',
        'created_time')
    list_display = (
        'id', 'templet_id', 'plan_id', 'title', 'content', 'files', 'push_total', 'send_success', 'send_time',
        'created_time')
    search_fields = (
        'templet_id', 'plan_id', 'invoice_type', 'title')
    readonly_fields = ['id']


# #
#
class PushPlanAdmin(admin.ModelAdmin):
    fields = (
        'id', 'role_id', 'group_id', 'user_id_list', 'node_to_action_id', 'created_time')
    list_display = (
        'id', 'role_id', 'group_id', 'user_id_list', 'node_to_action_id', 'created_time')
    search_fields = (
        'role_id', 'plan_id', 'group_id')
    readonly_fields = ['id']


class PushRecordAdmin(admin.ModelAdmin):
    fields = (
        'id', 'push_id', 'to_user_id', 'is_receive', 'created_time')
    list_display = (
        'id', 'push_id', 'to_user_id', 'is_receive', 'created_time')
    search_fields = (
        'push_id',)
    readonly_fields = ['id']


class PushTemplateAdmin(admin.ModelAdmin):
    fields = (
        'id', 'value', 'template', 'default_params', 'alias_params', 'title', 'send_type', 'files', 'push_times',
        'push_success',
        'push_total', 'created_time')
    list_display = (
        'id', 'value', 'template', 'default_params', 'alias_params', 'title', 'send_type', 'files', 'push_times',
        'push_success',
        'push_total', 'created_time')
    search_fields = (
        'title',)
    readonly_fields = ['id']


#
# #
admin.site.register(PushPush, PushPushAdmin)
admin.site.register(PushPlan, PushPlanAdmin)
admin.site.register(PushRecord, PushRecordAdmin)
admin.site.register(PushTemplate, PushTemplateAdmin)
