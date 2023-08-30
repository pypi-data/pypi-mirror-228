# encoding: utf-8
"""
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.push_plan_service import PushPlanService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper, user_authentication_wrapper


class PushPlanApis(APIView):
    # 推送添加
    @api_view(['POST'])
    @request_params_wrapper
    def add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("user_id", user_id)  # 用户ID
        push_set, err = PushPlanService.add(params)
        if err is None:
            return util_response(data=push_set)
        return util_response(err=47767, msg=err)

    # 推送修改
    @api_view(['PUT'])
    @request_params_wrapper
    def edit(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        push_id = params.get("push_id", 0)
        push_set, err = PushPlanService.edit(params, push_id)
        if err is None:
            return util_response(data=push_set)
        return util_response(err=47767, msg=err)

    # 推送列表
    @api_view(['GET'])
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID

        push_set, err = PushPlanService.list(params)

        if err is None:
            return util_response(data=push_set)

        return util_response(err=47767, msg=err)
