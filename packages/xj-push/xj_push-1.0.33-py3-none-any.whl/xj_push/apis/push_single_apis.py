# encoding: utf-8
"""
@project: djangoModel->push_single
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 单人推送
@created_time: 2023/8/10 10:13
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.push_single_service import PushSingleService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_wrapper


class PushSingleApi(APIView):

    @api_view(["GET"])
    @request_params_wrapper
    def list(self, *args, request_params, **kwargs):
        filter_fields = request_params.get("filter_fields")
        only_first = request_params.get("only_first", False)
        need_pagination = request_params.get("need_pagination", True)
        data, err = PushSingleService.list(
            params=request_params,
            filter_fields=filter_fields,
            only_first=only_first,
            need_pagination=need_pagination
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["POST"])
    @request_params_wrapper
    def add(self, *args, request_params, **kwargs):
        data, err = PushSingleService.add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["PUT"])
    @request_params_wrapper
    def edit(self, *args, request_params, **kwargs):
        data, err = PushSingleService.edit(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["PUT"])
    @request_params_wrapper
    def batch_dit(self, *args, request_params, **kwargs):
        data, err = PushSingleService.batch_edit(
            params=request_params
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["DELETE"])
    @request_params_wrapper
    def delete(self, *args, request_params, **kwargs):
        data, err = PushSingleService.delete(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    @user_authentication_wrapper
    def group_list(self, *args, request_params, user_info, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = PushSingleService.group_list(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
