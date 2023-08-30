# encoding: utf-8
"""
@project: djangoModel->push_pipeline
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 推送管道
@created_time: 2023/7/18 13:08
"""
import time

from orator import DatabaseManager

from config.config import JConfig
from .pipline_base import PipelineBase
from ..services.push_template_main_service import PushTemplateMainService
from ..utils.custom_tool import force_transform_type, write_to_log

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}
db = DatabaseManager(db_config)


class BXCustomPipeline(PipelineBase):

    @staticmethod
    def process(*args, params: dict = None, **kwargs):
        """流程参数进入管道"""
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        params["push_current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # # 获取报名相关的信息
        enroll_id = params.get("enroll_id", None)
        if enroll_id:
            data, err = BXCustomPipeline._get_enroll_info(enroll_id=enroll_id, prefix="enroll_")
            BXCustomPipeline._setdefault(params=params, update_params=data)

        category_id = params.get("category_id", None)
        if category_id:
            category_obj = db.table("thread_category").select_raw("""
                value as category_value,
                name as category_name,
                need_auth,
                platform_code,
                parent_id  as category_parent_id
            """).where("id", '=', category_id).first()
            BXCustomPipeline._setdefault(params=params, update_params=category_obj)

        classify_id = params.get("classify_id", None)
        if classify_id:
            classify_obj = db.table("thread_classify").select_raw("""
                value as classify_value,
                name as classify_name,
                category_id as classify_category_id,
                parent_id  as classify_parent_id
            """).where("id", '=', classify_id).first()
            BXCustomPipeline._setdefault(params=params, update_params=classify_obj)

        enroll_user_id = params.get("enroll_user_id", None)
        if enroll_user_id:
            data, err = BXCustomPipeline._get_user_info(user_id=enroll_user_id, prefix="enroll_user_")
            BXCustomPipeline._setdefault(params=params, update_params=data)

        # # 获取开票相关的信息
        invoice_id = params.get("invoice_id", None)
        if invoice_id:
            data, err = BXCustomPipeline.__get_invoice_info(invoice_id=invoice_id)
            BXCustomPipeline._setdefault(params=params, update_params=data)

        # 获取财务相关的信息
        finance_id = params.get("finance_id", None)
        order_no = params.get("order_no", None)
        transact_no = params.get("transact_no", None)
        if finance_id or transact_no or order_no:
            data, err = BXCustomPipeline._get_finance_info(finance_id=finance_id, order_no=order_no, transact_no=transact_no)
            BXCustomPipeline._setdefault(params=params, update_params=data)

        push_type = params.get("push_type")
        push_template_value = params.get("push_template_value")
        # print("BXCustomPipeline.process params:", params)
        if push_type and push_template_value and params:
            try:
                data, err = PushTemplateMainService.template_send(
                    type=push_type,
                    value=push_template_value,
                    replacements=params,
                    user_id=params.get("enroll_user_id")
                )
            except Exception as e:
                write_to_log(prefix="推送管道调用推送服务失败：PushTemplateMainService", err_obj=e)

        return None, None
