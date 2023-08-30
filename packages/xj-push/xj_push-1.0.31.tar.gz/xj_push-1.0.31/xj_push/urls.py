# 应用名称
from django.urls import re_path

app_name = 'push'
from .service_register import register
from .apis.push_apis import PushApis
from .apis.push_single_apis import PushSingleApi

register()
urlpatterns = [
    re_path(r'^single_batch_edit/?$', PushSingleApi.batch_dit, name="站内推送批量修改"),
    re_path(r'^wechat/?$', PushApis.template_send, name="模板推送"),
    re_path(r'^single_push_list/?$', PushSingleApi.list, name="模板推送列表"),
    re_path(r'^single_push_add/?$', PushSingleApi.add, name="模板推送添加"),
    re_path(r'^single_push_del/?$', PushSingleApi.delete, name="模板删除"),
    re_path(r'^single_push_edit/?$', PushSingleApi.edit, name="模板编辑"),
    re_path(r'^single_group_list/?$', PushSingleApi.group_list, name="单挑分组列表"),
]
