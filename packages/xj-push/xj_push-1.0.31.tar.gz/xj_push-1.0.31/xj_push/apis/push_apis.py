# encoding: utf-8
"""
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.push_template_main_service import PushTemplateMainService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class PushApis(APIView):
    # 推送添加
    @api_view(['POST'])
    @request_params_wrapper
    def template_send(self, *args, request_params, **kwargs, ):
        params = request_params
        type = params.get("type")
        value = params.get("value")
        user_id = params.get("user_id")
        replacements = params.get("replacements")
        push_set, err = PushTemplateMainService.template_send(type, value, user_id, replacements)
        if err is None:
            return util_response(data=push_set)
        return util_response(err=47767, msg=err)
