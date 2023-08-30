from pathlib import Path

from django.forms.models import model_to_dict

from main.settings import BASE_DIR
from utils.custom_tool import write_to_log, format_params_handle
from xj_user.services.login_service import LoginService
from xj_user.utils.wechat_sign import applet_subscribe_message, subscribe_message
from ..models import PushTemplate
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.utility_method import replace_values

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

payment_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
payment_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = payment_main_config_dict.wechat_merchant_app_id or payment_module_config_dict.wechat_merchant_app_id or ""
sub_app_secret = payment_main_config_dict.wechat_merchant_app_secret or payment_module_config_dict.wechat_merchant_app_secret or ""
wechat_merchant_name = payment_main_config_dict.wechat_merchant_name or payment_module_config_dict.wechat_merchant_name or ""

subscription_app_id = payment_main_config_dict.wechat_subscription_app_id or payment_module_config_dict.wechat_subscription_app_id or ""
subscription_app_secret = payment_main_config_dict.wechat_subscription_app_secret or payment_module_config_dict.wechat_subscription_app_secret or ""

app_app_id = payment_main_config_dict.wechat_app_app_id or payment_module_config_dict.wechat_app_app_id or ""
app_app_secret = payment_main_config_dict.wechat_app_app_secret or payment_module_config_dict.wechat_app_app_secret or ""


class PushTemplateMainService:

    # 微信模板发送
    @staticmethod
    def template_send(type, value, user_id, replacements=None):
        """
        微信模板发送
        :param touser: 要推送的人 openid
        :param replacements: 要替换的模板参数
        :param type: 模板类型
        :return: param_dict
        """
        new_data = {}
        template_set = PushTemplate.objects.filter(value=value).first()
        if not template_set:
            write_to_log(
                prefix="模板记录",
                content="模板关键词:" + str(value) + "不存在",
            )
            return None, "模板记录不存在"

        template_set = model_to_dict(template_set)
        data = format_params_handle(
            param_dict=format_params_handle(
                param_dict=replacements,
                alias_dict=template_set.get("alias_params"),
            ),
            filter_filed_list=list(template_set.get("alias_params").values()),
        )
        write_to_log(prefix="推送记录收录：", content="模板变量:" + str(data or {}) + " 推送用户：" + str(user_id) + "推送模板:" + str(value))

        template = template_set.get("template")
        if type in ['subscribe', 'applet']:
            new_data = replace_values(data, template)
        if type == "sms":
            wechat_user_info = subscribe_message(new_data)
        elif type == "subscribe":
            sso, err = LoginService.sso_record(user_id, subscription_app_id)
            if err:
                write_to_log(
                    prefix="公众号获取单点登录信息",
                    content="单点登录信息:" + str(user_id) + "不存在",
                    err_obj=err
                )
            new_data['touser'] = sso.get("sso_unicode", "")
            # wechat_user_info = subscribe_message(new_data)
        elif type == "applet":
            sso, err = LoginService.sso_record(user_id, sub_appid)
            if err:
                write_to_log(
                    prefix="小程序获取单点登录信息",
                    content="单点登录信息:" + str(user_id) + ";" + str(sub_appid) + "不存在",
                    err_obj=err
                )
                return None, err
            new_data['touser'] = sso.get("sso_unicode", "")
            wechat_user_info = applet_subscribe_message(new_data)
            write_to_log(prefix="微信推送结果日志", content=wechat_user_info)

        # TODO 推送成功人数加一
        # print(new_data)
        return None, None
