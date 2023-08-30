# encoding: utf-8
"""
@project: djangoModel->single_push_pipline
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 单挑推送管道
@created_time: 2023/8/23 13:13
"""
import datetime

from django.db.models import F

from xj_enroll.models import EnrollSubitemRecord
from xj_push.push_pipeline.pipline_base import PipelineBase
from xj_push.services.push_single_service import PushSingleService
from ..utils.custom_tool import force_transform_type, dynamic_load_class, write_to_log


class SinglePushPipeline(PipelineBase):
    worker_notice_title = {
        "enroll": {
            "title": "报名成功",
            "content": "该项目您已成功报名",
        },
        "appoint": {
            "title": "抢单成功",
            "content": "恭喜您成功抢到订单，快去制作吧",
        },
        "appoint_fail": {
            "title": "报名失败",
            "content": "客户未派单给您，继续努力~",
        },
        "upload": {
            "title": "资料审核中",
            "content": "您已提交应标资料，平台审核中",
        },
        "check_success": {
            "title": "待客户验收",
            "content": "您上传的资料平台已审核通过",
        },
        "check_fail": {
            "title": "平台审核不通过",
            "content": "请修改后重新上传",
        },
        "accept_success": {
            "title": "订单完成",
            "content": "恭喜您，订单已完成验收",
        },
        "accept_fail": {
            "title": "客户验收不通过",
            "content": "您上传的资料被客户驳回，请及时确认",
        },
        "cancel_publish": {
            "title": "订单关闭",
            "content": "客户已取消订单",
        },
        "cancel_enroll": {
            "title": "取消报名成功",
            "content": "您已取消报名",
        },
    }

    custom_notice_title = {
        "publish": {
            "title": "订单报名中",
            "content": "您发布的新订单正在报名中",
        },
        "enroll": {
            "title": "订单待派单",
            "content": "您的订单有新的镖师报名",
        },
        "appoint": {
            "title": "已派单，等待付款",
            "content": "付款后镖师将收到通知，开始制作",
        },
        "payed": {
            "title": "等待镖师上传标书",
            "content": "订单已完成付款，待镖师提交标书",
        },
        "upload": {
            "title": "平台审核资料",
            "content": "镖师已上传项目标书，平台审核中",
        },
        "check_success": {
            "title": "标书待验收",
            "content": "平台已完成标书审核",
        },
        "check_fail": {
            "title": "审核驳回，待镖师修改",
            "content": "项目标书已驳回，等待修改",
        },
        "accept_success": {
            "title": "订单完成",
            "content": "项目标书已完成验收",
        },
        "accept_fail": {
            "title": "验收驳回，待镖师修改",
            "content": "项目标书已驳回，等待修改",
        },
        "cancel_publish": {
            "title": "订单关闭",
            "content": "您已取消该订单",
        },
    }

    @staticmethod
    def process(*args, params: dict = None, **kwargs):
        # 获取报名相关的信息
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        enroll_id = params.get("enroll_id", None)
        if not enroll_id:
            return None, "报名ID错误"

        # 导入依赖
        Enroll, enroll_import_err = dynamic_load_class(import_path="xj_enroll.models", class_name="Enroll")
        EnrollRecord, record_import_err = dynamic_load_class(import_path="xj_enroll.models", class_name="EnrollRecord")
        if enroll_import_err or record_import_err:
            write_to_log(prefix="站内推送管道异常", content="请安装报名模块")
            return None, None

        # write_to_log(prefix="站内推送管道入参", content=params)
        # 获取相关信息
        enroll_info = Enroll.objects.filter(id=enroll_id).values().first()
        thread_id = enroll_info.get("thread_id")
        enroll_user_id = enroll_info.get("user_id")
        # 重置已读状态，默认跳转链接
        add_params = {
            "thread_id": thread_id,
            "source_code": "订单动态",
            "snapshot": params, "is_jump_link": True,
            "is_read": 0,
            "created_time": str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        }
        # ------------------------- section 管道挂油，管道分流 start ------------------------
        # 发布的订单后通知客户
        if params.get("push_action") == "publish":
            add_params["title"] = SinglePushPipeline.custom_notice_title["publish"]["title"]
            add_params["content"] = SinglePushPipeline.custom_notice_title["publish"]["content"]
            add_params["to_user_id"] = enroll_user_id
            data, err = PushSingleService.add(params=add_params)

        # 镖师报名相互通知
        elif params.get("push_action") == "enroll":
            # 提醒客户有人报名
            add_params["content"] = SinglePushPipeline.custom_notice_title["enroll"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["enroll"]["title"]
            add_params["to_user_id"] = enroll_user_id
            data, err = PushSingleService.add(params=add_params)

            # 体校镖师报名成功
            record_info = EnrollRecord.objects.filter(id=params.get("record_id")).values().first()
            if record_info:
                add_params["content"] = SinglePushPipeline.worker_notice_title["enroll"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["enroll"]["title"]
                add_params["snapshot"]["record_id"] = record_info.get("id")
                add_params["to_user_id"] = record_info.get("user_id")
                data, err = PushSingleService.add(params=add_params)

        # 镖师取消报名
        elif params.get("push_action") == "cancel":
            # # 提醒客户有人报名
            # add_params["content"] = SinglePushPipeline.custom_notice_title["cancel"]["content"]
            # add_params["title"] = SinglePushPipeline.custom_notice_title["cancel"]["title"]
            # add_params["to_user_id"] = enroll_user_id
            # data, err = PushSingleService.add(params=add_params)

            # 提醒镖师客户取消了订单
            record_info = EnrollRecord.objects.filter(id=params.get("record_id")).values().first()
            if record_info:
                add_params["content"] = SinglePushPipeline.worker_notice_title["cancel_enroll"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["cancel_enroll"]["title"]
                add_params["snapshot"]["record_id"] = record_info.get("id")
                add_params["is_jump_link"] = False
                add_params["to_user_id"] = record_info.get("user_id")
                data, err = PushSingleService.add(params=add_params)

        # 用户取消订单通知所有的报名用户
        elif params.get("push_action") == "cancel_publish":
            # 通知所有报名的镖师
            add_params["content"] = SinglePushPipeline.worker_notice_title["cancel_publish"]["content"]
            add_params["title"] = SinglePushPipeline.worker_notice_title["cancel_publish"]["title"]
            record_infos = list(EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values())
            for i in record_infos:
                if not i.get("user_id"):
                    continue
                add_params["snapshot"]["record_id"] = i.get("id")
                add_params["to_user_id"] = i.get("user_id")
                PushSingleService.add(params=add_params)

            # 通知客户取消成功
            add_params["content"] = SinglePushPipeline.custom_notice_title["cancel_publish"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["cancel_publish"]["title"]
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

        # 指派通知
        elif params.get("push_action") == "appoint":
            # 通知客户指派成功
            add_params["content"] = SinglePushPipeline.custom_notice_title["appoint"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["appoint"]["title"]
            add_params["to_user_id"] = enroll_user_id
            data, err = PushSingleService.add(params=add_params)

            # # 通知镖师您已被指派
            # record_info = EnrollRecord.objects.filter(id=params.get("record_id")).values().first()
            # if record_info:
            #     add_params["content"] = SinglePushPipeline.worker_notice_title["appoint"]["content"]
            #     add_params["title"] = SinglePushPipeline.worker_notice_title["appoint"]["title"]
            #     add_params["to_user_id"] = record_info.get("user_id")
            #     data, err = PushSingleService.add(params=add_params)
            #
            # # 没有指派的镖师给予提示
            # un_appoint_records = list(EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(id=params.get("record_id")).values())
            # for i in un_appoint_records:
            #     add_params["is_jump_link"] = False
            #     add_params["content"] = SinglePushPipeline.worker_notice_title["appoint_fail"]["content"]
            #     add_params["title"] = SinglePushPipeline.worker_notice_title["appoint_fail"]["title"]
            #     add_params["to_user_id"] = i.get("user_id")
            #     data, err = PushSingleService.add(params=add_params)

        # 已支付通知客户
        elif params.get("push_action") == "payed":
            add_params["content"] = SinglePushPipeline.custom_notice_title["payed"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["payed"]["title"]
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 产品沟通过，在支付后通知是否报名成功
            # 通知镖师您已被指派
            record_info = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if record_info:
                add_params["content"] = SinglePushPipeline.worker_notice_title["appoint"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["appoint"]["title"]
                add_params["snapshot"]["record_id"] = record_info.get("id")
                add_params["to_user_id"] = record_info.get("user_id")
                data, err = PushSingleService.add(params=add_params)

            # 没有指派的镖师给予提示
            un_appoint_records = list(EnrollRecord.objects.filter(enroll_id=enroll_id, enroll_status_code=124).values())
            for i in un_appoint_records:
                add_params["is_jump_link"] = False
                add_params["content"] = SinglePushPipeline.worker_notice_title["appoint_fail"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["appoint_fail"]["title"]
                add_params["snapshot"]["record_id"] = i.get("id")
                add_params["to_user_id"] = i.get("user_id")
                data, err = PushSingleService.add(params=add_params)

        # 镖师上传
        elif params.get("push_action") == "upload":
            # 通知客户
            add_params["content"] = SinglePushPipeline.custom_notice_title["upload"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["upload"]["title"]
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            subitem_record = EnrollSubitemRecord.objects.annotate(
                record_user_id=F("enroll_record__user_id")
            ).filter(id=params.get("id")).values("record_user_id", "enroll_record_id", "id").first()
            if subitem_record:
                add_params["content"] = SinglePushPipeline.worker_notice_title["upload"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["upload"]["title"]
                add_params["to_user_id"] = subitem_record.get("record_user_id")
                add_params["snapshot"]["record_id"] = subitem_record.get("enroll_record_id")
                PushSingleService.add(params=add_params)

        # 标书初审通过
        elif params.get("push_action") == "check_success":
            # 通知客户
            add_params["content"] = SinglePushPipeline.custom_notice_title["check_success"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["check_success"]["title"]
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["content"] = SinglePushPipeline.worker_notice_title["check_success"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["check_success"]["title"]
                add_params["to_user_id"] = bx_worker.get("user_id")
                add_params["snapshot"]["record_id"] = bx_worker.get("id")
                PushSingleService.add(params=add_params)

        # 标书初审失败
        elif params.get("push_action") == "check_fail":
            # 通知客户
            add_params["content"] = SinglePushPipeline.custom_notice_title["check_fail"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["check_fail"]["title"]
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["content"] = SinglePushPipeline.worker_notice_title["check_fail"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["check_fail"]["title"]
                add_params["to_user_id"] = bx_worker.get("user_id")
                add_params["snapshot"]["record_id"] = bx_worker.get("id")
                PushSingleService.add(params=add_params)

        # 标书初审通过
        elif params.get("push_action") == "accept_success":
            add_params["content"] = SinglePushPipeline.custom_notice_title["accept_success"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["accept_success"]["title"]
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["content"] = SinglePushPipeline.worker_notice_title["accept_success"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["accept_success"]["title"]
                add_params["snapshot"]["record_id"] = bx_worker.get("id")
                add_params["to_user_id"] = bx_worker.get("user_id")
                PushSingleService.add(params=add_params)

        # 标书验收失败
        elif params.get("push_action") == "accept_fail":
            add_params["content"] = SinglePushPipeline.custom_notice_title["accept_fail"]["content"]
            add_params["title"] = SinglePushPipeline.custom_notice_title["accept_fail"]["title"]
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["content"] = SinglePushPipeline.worker_notice_title["accept_fail"]["content"]
                add_params["title"] = SinglePushPipeline.worker_notice_title["accept_fail"]["title"]
                add_params["to_user_id"] = bx_worker.get("user_id")
                add_params["snapshot"]["record_id"] = bx_worker.get("id")
                PushSingleService.add(params=add_params)

        # ------------------------- section 管道挂油 end  ------------------------
        return None, None
