# encoding: utf-8
"""
@project: djangoModel->push_plan
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 推送计划
@created_time: 2023/8/10 8:59
"""
from .base_model import BaseModel


class PushPlan(BaseModel):
    __table__ = 'push_plan'
    __guarded__ = ['id', 'created_time']
