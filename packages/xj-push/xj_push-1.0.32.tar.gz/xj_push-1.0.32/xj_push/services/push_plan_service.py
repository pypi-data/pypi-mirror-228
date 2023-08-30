from django.core.paginator import Paginator, EmptyPage
from django.forms import model_to_dict

from ..models import *
from ..utils.custom_tool import format_params_handle, force_transform_type


class PushPlanService:

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
                    "role_id|int",
                    "group_id|int",
                    "user_id_list|list_int",
                    "template_id|int",
                    "node_to_action_id|int",
                    "plan_push_circle|int",
                    "plan_push_time|date",
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
            push = PushPlan.objects.create(**main_form_data)
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
                    "id|int", "id_list|list_int"
                ],
                alias_dict={"id_list": "id__in"}
            )
        # 修改内容检查处理
        try:
            main_form_data = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                is_remove_empty=True,
                filter_filed_list=[
                    "role_id|int",
                    "group_id|int",
                    "user_id_list|list_int",
                    "template_id|int",
                    "node_to_action_id|int",
                    "plan_push_circle|int",
                    "plan_push_time|date"
                ],
            )
        except ValueError as e:
            return None, str(e)
        # 构建ORM，检查是否存在可修改项目
        push_obj = PushPlan.objects
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

        # 搜索参数
        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "id_list|list_int", "template_id_list|list_int",
                "created_time_start|date", "created_time_end|date",
                "plan_push_time_start|date", "plan_push_time_end|date"
            ],
            split_list=["template_id_list", "id_list"],
            alias_dict={
                "created_time_start": "created_time__gte", "created_time_end": "created_time__lte", "id_list": "id__in",
                "plan_push_time_start": "plan_push_time__gte", "plan_push_time_end": "plan_push_time__lte",
            }
        )

        # 构建orm
        push = PushPlan.objects.order_by('-id').extra(
            select={'created_time': 'DATE_FORMAT(send_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
        ).filter(**params).values()
        total = push.count()

        # 分页查询
        paginator = Paginator(push, size)
        try:
            res_list = paginator.page(page)
        except EmptyPage:
            return {'total': total, "page": page, "size": size, 'list': []}, None
        except Exception as e:
            return None, f'{str(e)}'

        return {'size': int(size), 'page': page, 'total': total, 'list': res_list}, None

    @staticmethod
    def detail(push_id: int):
        if not push_id:
            return None, "推送id不能为空"
        push = PushPlan.objects.filter(id=push_id).extra(
            select={'created_time': 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
        ).first()
        if not push:
            return None, "无法找到要查询的数据，请检查参数"
        data = model_to_dict(push)
        return data, None
