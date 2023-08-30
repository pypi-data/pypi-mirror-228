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
from .bx_custom_pipeline import BXCustomPipeline
from .pipline_base import PipelineBase
from ..services.push_template_main_service import PushTemplateMainService
from ..utils.custom_tool import force_transform_type, write_to_log, dynamic_load_class

config = JConfig()


class BXWorkerPipeline(PipelineBase):

    @staticmethod
    def get_record(enroll_id, prefix="record"):
        record_info = {}
        enroll_id, err = force_transform_type(variable=enroll_id, var_type="int")
        EnrollRecordServices, import_err = dynamic_load_class(import_path="xj_enroll.service.enroll_record_serivce", class_name="EnrollRecordServices")
        if enroll_id and not import_err:
            data, err = EnrollRecordServices.record_detail(
                search_params={"enroll_id": enroll_id, "exclude_code": 124},
            )
            if not err and isinstance(data, dict):
                record_info = data

        return {prefix + k: v for k, v in record_info.items()}, None

    @staticmethod
    def process(*args, params: dict = None, **kwargs):
        """流程参数进入管道"""
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        params["push_current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # 获取报名相关的信息
        enroll_id = params.get("enroll_id", None)
        if enroll_id:
            # 报名主表和项目信息
            data, err = BXWorkerPipeline._get_enroll_info(enroll_id=enroll_id, prefix="enroll_")
            BXCustomPipeline._setdefault(params=params, update_params=data)
            # 报名记录信息
            data, err = BXWorkerPipeline.get_record(enroll_id=enroll_id, prefix="record_")
            BXCustomPipeline._setdefault(params=params, update_params=data)

        # 获取开票相关的信息
        invoice_id = params.get("invoice_id", None)
        if invoice_id:
            data, err = BXWorkerPipeline.__get_invoice_info(invoice_id=invoice_id)
            BXWorkerPipeline._setdefault(params=params, update_params=data)

        # 获取财务相关的信息
        finance_id = params.get("finance_id", None)
        order_no = params.get("order_no", None)
        transact_no = params.get("transact_no", None)
        if finance_id or transact_no or order_no:
            data, err = BXCustomPipeline._get_finance_info(finance_id=finance_id, order_no=order_no, transact_no=transact_no)
            BXCustomPipeline._setdefault(params=params, update_params=data)

        # 开始推送
        push_type = params.get("push_type")
        push_template_value = params.get("push_template_value")
        if not params.get("record_user_id"):
            write_to_log(prefix="推送管道警告", content="该项目还没有镖师承接订单，enroll_id为" + str(enroll_id or "None"))
            return None, None
        if push_type and push_template_value and params:
            try:
                write_to_log(
                    prefix="发起推送",
                    content="push_type:" + str(push_type) + " push_template_value:" + str(push_template_value) + " user_id:" + str(params.get("record_user_id", ""))
                )
                data, err = PushTemplateMainService.template_send(
                    type=push_type,
                    value=push_template_value,
                    replacements=params,
                    user_id=params.get("record_user_id", 0)
                )
                write_to_log(prefix="推送结果", content="data:" + str(data) + " ; err" + str(err or ""))
                return None, None
                # TODO 推送人数加一
            except Exception as e:
                # TODO 推送失败人数加一
                write_to_log(prefix="推送管道调用推送服务失败：PushTemplateMainService", err_obj=e)
        return params, None
