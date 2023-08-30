# encoding: utf-8
"""
@project: djangoModel->pipline_base
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 管道基础类
@created_time: 2023/7/20 11:09
"""
from abc import ABC, abstractmethod
import time

from config.config import JConfig
from ..utils.custom_tool import force_transform_type, dynamic_load_class, write_to_log

config = JConfig()


class PipelineBase(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def _setdefault(params: dict = None, update_params: dict = None):
        """
        合并字典，防止覆盖原有的值
        """
        # 强制类型转换
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        update_params, err = force_transform_type(variable=update_params, var_type="only_dict", default={})

        # 开始合并
        for k, v in update_params.items():
            params.setdefault(k, v)
        return params, None

    @staticmethod
    def _get_user_info(user_id: int = None, prefix=""):
        """
        获取用户信息
        :param user_id: 用户ID
        :return: 用户信息,err
        """
        user_info = {}
        try:
            app_id = config.get(section="xj_user", option="app_id", default="")

            user_id, err = force_transform_type(variable=user_id, var_type="int")
            if err:
                return user_info, err

            # 获取用户详细信息
            DetailInfoService, err = dynamic_load_class(import_path="xj_user.services.user_detail_info_service", class_name="DetailInfoService")
            if not err:
                user_detail, err = DetailInfoService.get_detail(user_id=user_id)
                user_detail, err = force_transform_type(variable=user_detail, var_type="only_dict", default={})
                if not err:
                    user_info.update(user_detail)

            # 获取用户的单点登录信息
            # UserSsoServeService, err = dynamic_load_class(import_path="xj_user.services.user_sso_serve_service", class_name="UserSsoServeService")
            # if not err:
            #     user_sso_info, err = UserSsoServeService.user_sso_to_user(user_id=user_id, app_id=app_id)
            #     user_sso_info, err = force_transform_type(variable=user_sso_info, var_type="only_dict", default={})
            #     if not err:
            #         user_info.update(user_sso_info)
        except Exception as e:
            write_to_log(prefix="推送管道异常", err_obj=e)
        return {prefix + k: v for k, v in user_info.items()}, None

    @staticmethod
    def _get_enroll_info(enroll_id: int = None, prefix=""):
        """
        获取报名信息，项目信息
        :param enroll_id: 报名ID
        :return: 报名信息，获取失败的错误信息
        """
        enroll_info = {}
        try:
            enroll_id, err = force_transform_type(variable=enroll_id, var_type="int")
            thread_id = None
            if err:
                return enroll_info, err

            # 获取信息标数据
            EnrollServices, err = dynamic_load_class(import_path="xj_enroll.service.enroll_services", class_name="EnrollServices")
            if not err:
                enroll_detail, err = EnrollServices.enroll_detail(enroll_id=enroll_id, simple_return=True)
                enroll_detail, err = force_transform_type(variable=enroll_detail, var_type="only_dict", default={})
                enroll_info.update(enroll_detail)
                thread_id = enroll_info.get("thread_id", None)

            # 获取项目信息
            ThreadItemService, err = dynamic_load_class(import_path="xj_thread.services.thread_item_service", class_name="ThreadItemService")
            if thread_id and not err:
                thread_info, err = ThreadItemService.detail(pk=thread_id)
                thread_info, err = force_transform_type(variable=thread_info, var_type="only_dict", default={})
                enroll_info.update(thread_info)
        except Exception as e:
            write_to_log(prefix="推送管道异常", err_obj=e)
        return {prefix + k: v for k, v in enroll_info.items()}, None

    @staticmethod
    def __get_invoice_info(invoice_id: int = None, prefix=""):
        """
        开票的获取服务
        :param invoice_id:
        """
        invoice_info = {}
        try:
            invoice_id, err = force_transform_type(variable=invoice_id, var_type="int")
            if err:
                return invoice_id, err

            InvoiceService, err = dynamic_load_class(import_path="xj_invoice.services.invoice_service", class_name="InvoiceService")
            if not err:
                invoice_detail_info, err = InvoiceService.detail(invoice_id)
                invoice_detail_info, err = force_transform_type(variable=invoice_detail_info, var_type="only_dict", default={})
                invoice_info.update(invoice_detail_info)
        except Exception as e:
            write_to_log(prefix="推送管道异常", err_obj=e)
        return {prefix + k: v for k, v in invoice_info.items()}, None, None

    @staticmethod
    def _get_finance_info(finance_id: int = None, order_no=None, transact_no=None, prefix=""):
        finance_info = {}
        # 强制类型转换
        try:
            finance_id, err = force_transform_type(variable=finance_id, var_type="int")
            order_no, err = force_transform_type(variable=order_no, var_type="str")
            transact_no, err = force_transform_type(variable=transact_no, var_type="str")
            if not finance_id and not transact_no and not order_no:
                return finance_info, err

            # 自动动态引入
            FinanceListService, err = dynamic_load_class(import_path="xj_finance.services.finance_list_service", class_name="FinanceListService")
            if not err:
                transact_detail, err = FinanceListService.detail(
                    pk=finance_id,
                    order_no=order_no,
                    transact_no=transact_no
                )
                transact_detail, err = force_transform_type(variable=transact_detail, var_type="only_dict", default={})
                finance_info.update(transact_detail)
        except Exception as e:
            write_to_log(prefix="推送管道异常", err_obj=e)
        return {prefix + k: v for k, v in finance_info.items()}, None, None

    def init_params(self, *args, params: dict = None, **kwargs):
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        params["push_current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

    @abstractmethod
    def process(*args, params: dict = None, **kwargs):
        # 当前的推送时间
        pass
