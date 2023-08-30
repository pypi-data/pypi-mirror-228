import json
from decimal import Decimal

from django.db.models import F
from django.forms import model_to_dict
from ..models import *
from utils.custom_tool import filter_result_field
from ..utils.custom_tool import format_params_handle, force_transform_type, dynamic_load_class, \
    write_to_log


# 自定义序列化函数
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # 将 Decimal 对象转换为字符串
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


class PushService:

    @staticmethod
    def add(params: dict = None, **kwargs):
        """
        推送添加
        :param params: 添加参数子字典
        :param kwargs:
        :return:
        """
        # 参数整合与空值验证
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)
        # 过滤主表修改字段
        try:
            main_form_data = format_params_handle(
                param_dict=params.copy(),
                is_remove_empty=True,
                filter_filed_list=[
                    "template_id|int",
                    "plan_id|int",
                    "title",
                    "content",
                    "files",
                    "push_total",
                    "send_success",
                    "send_time",
                    "created_time"
                ],
                alias_dict={},
                is_validate_type=True
            )
        except ValueError as e:
            # 模型字段验证
            return None, str(e)
        # IO操作
        try:
            # 主表插入数据
            push = PushPush.objects.create(**main_form_data)
        except Exception as e:
            return None, f'''{str(e)} in "{str(e.__traceback__.tb_frame.f_globals["__file__"])}" : Line {str(
                e.__traceback__.tb_lineno)}'''

        return {"id": push.id}, None

    @staticmethod
    def edit(params: dict = None, push_id=None, search_param: dict = None, **kwargs):
        """
        推送编辑
        :param params: 修改的参数
        :param push_id: 需要修改的推送主键
        :param search_param: 搜索参数, 服务层根据信息等其他搜索字段检索到需要修改的数据
        :return: data, err
        """
        # 空值检查
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        push_id, is_pass = force_transform_type(variable=push_id, var_type="int")
        search_param, is_pass = force_transform_type(variable=search_param, var_type="dict", default={})
        if not push_id and not search_param:
            return None, "无法找到要修改数据，请检查参数"

        # 搜索字段过滤
        if search_param:
            search_param = format_params_handle(
                param_dict=search_param,
                filter_filed_list=[
                    "templet_id|int", "templet_id_list|list", "plan_id|int", "plan_id_list|list",
                ],
                alias_dict={"templet_id_list": "id__in", "[": "templet_id__in"}
            )
        # 修改内容检查处理
        try:
            main_form_data = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                is_remove_empty=True,
                filter_filed_list=[
                    "templet_id|int",
                    "plan_id|int",
                    "title",
                    "content",
                    "files",
                    "push_total",
                    "send_success",
                    "send_time",
                    "created_time"
                ],
            )
        except ValueError as e:
            return None, str(e)
        # 构建ORM，检查是否存在可修改项目
        push_obj = PushPush.objects
        if push_id:
            push_obj = push_obj.filter(id=push_id)
        elif search_param:
            push_obj = push_obj.filter(**search_param)

        update_total = push_obj.count()
        if update_total == 0:
            return None, "没有找到可修改项目"

        # IO 操作
        try:
            push_obj.update(**main_form_data)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return push_obj.first().to_json(), None

    @staticmethod
    def list(params):

        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10
        push = PushPush.objects
        # invoice = invoice.order_by('-send_time')
        push = push.order_by('-id')

        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "id_list|list", "templet_id|int", "plan_id|int", "templet_id_list|list",
                "send_time_start|date", "send_time_end|date"
            ],
            split_list=["templet_id_list", "id_list"],
            alias_dict={
                "send_time_start": "send_time__gte", "send_time_end": "send_time__lte",
                "templet_id_list": "templet_id__in", "id_list": "id__in"
            },
        )
        push = push.extra(select={'send_time': 'DATE_FORMAT(send_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        push = push.filter(**params).values()
        total = push.count()
        #
        current_page_set = push[page * size: page * size + size] if page >= 0 and size > 0 else push
        res_list = []
        for i, it in enumerate(current_page_set):
            it['order'] = page * size + i + 1
            it['send_time'] = it['send_time'].strftime("%Y-%m-%d %H:%M:%S") if it['send_time'] else it[
                'send_time']
            it['created_time'] = it['created_time'].strftime("%Y-%m-%d %H:%M:%S") if it['created_time'] else it[
                'created_time']

            res_list.append(it)

        data = res_list

        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': data, }, None

    @staticmethod
    def detail(push_id):
        if not push_id:
            return None, "推送id不能为空"
        push = PushPush.objects.filter(id=push_id)
        push = push.extra(select={'send_time': 'DATE_FORMAT(send_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                  'created_time': 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})

        push = push.first()
        if not push:
            return None, "无法找到要查询的数据，请检查参数"
        data = model_to_dict(push)
        return data, None
