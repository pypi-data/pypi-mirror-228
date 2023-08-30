# encoding: utf-8
"""
@project: djangoModel->push_template
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 推送模板模型
@created_time: 2023/8/10 9:05
"""
from .base_model import BaseModel


class PushTemplate(BaseModel):
    __table__ = 'push_template'
    __guarded__ = ['id', 'created_time']

