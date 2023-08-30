# encoding: utf-8
"""
@project: djangoModel->service_register
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 对外开放服务调用注册白名单
@created_time: 2023/1/12 14:29
"""

import xj_push
from .push_pipeline import bx_custom_pipeline, bx_worker_pipeline, bx_visitor_pipeline,single_push_pipeline
from .utils.service_manager import ServiceManager

# 对外服务白名单
register_list = [
    {
        "name": "镖行用户通知管道",
        "service_name": "bx_custom_pipeline",
        "pointer": bx_custom_pipeline.BXCustomPipeline.process
    },
    {
        "name": "镖行镖师通知管道",
        "service_name": "bx_worker_pipeline",
        "pointer": bx_worker_pipeline.BXWorkerPipeline.process
    },
    {
        "name": "镖行游客通知管道",
        "service_name": "bx_visitor_pipeline",
        "pointer": bx_visitor_pipeline.BXVisitorPipeline.process
    },
    {
        "name": "镖行站内推送管道",
        "service_name": "bx_single_pipeline",
        "pointer": single_push_pipeline.SinglePushPipeline.process
    }
]

server_manager = ServiceManager()


# 遍历注册
def register():
    for i in register_list:
        setattr(xj_push, i["service_name"], i["pointer"])
        server_manager.put_service(route=i["service_name"], method=i["pointer"])


if __name__ == '__main__':
    register()
