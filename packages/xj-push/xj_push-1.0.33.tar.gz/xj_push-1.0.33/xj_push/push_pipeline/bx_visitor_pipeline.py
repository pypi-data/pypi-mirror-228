# encoding: utf-8
"""
@project: djangoModel->push_pipeline
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 推送管道
@created_time: 2023/7/18 13:08
"""
import time

from config.config import JConfig
from .pipline_base import PipelineBase
from ..services.push_template_main_service import PushTemplateMainService
from ..utils.custom_tool import write_to_log, force_transform_type

config = JConfig()


class BXVisitorPipeline(PipelineBase):

    @staticmethod
    def process(*args, params: dict = None, **kwargs):
        """流程参数进入管道"""
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        params["push_current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

        user_id = params.get("user_id", None)
        if user_id:
            data, err = BXVisitorPipeline._get_user_info(user_id=user_id, prefix="")
            BXVisitorPipeline._setdefault(params=params, update_params=data)

        if not user_id:
            write_to_log(prefix="推送管道警告", content="没有用户ID无法进行推送")
            return None, "没有用户ID无法进行推送"

        # 开始推送
        push_type = params.get("push_type")
        push_template_value = params.get("push_template_value")
        if push_type and push_template_value and params:
            try:
                data, err = PushTemplateMainService.template_send(
                    type=push_type,
                    value=push_template_value,
                    replacements=params,
                    user_id=user_id
                )
                # TODO 推送人数加一
            except Exception as e:
                # TODO 推送失败人数加一
                write_to_log(prefix="推送管道调用推送服务失败：PushTemplateMainService", err_obj=e)
        return params, None
