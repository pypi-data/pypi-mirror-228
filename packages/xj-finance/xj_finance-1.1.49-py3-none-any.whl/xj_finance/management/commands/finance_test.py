# encoding: utf-8
"""
@project: djangoModel->sync_table_structure
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 更新表结构
@created_time: 2023/8/22 9:09
"""
from django.core.management import BaseCommand

from xj_push.push_pipeline.single_push_pipeline import SinglePushPipeline


class Command(BaseCommand):
    # 帮助文本, 一般备注命令的用途及如何使用。
    help = "测试调试结构"

    # 给命令添加一个名为name的参数
    def add_arguments(self, parser):
        pass

    # 核心业务逻辑，通过options字典接收name参数值，拼接字符串后输出
    def handle(self, *args, **options):
        data, err = SinglePushPipeline.process(
            params={
                "enroll_id": 727,
                # "record_id":447,
                # "id":207,
                # "push_action": "cancel_publish",
                "push_action": "publish"
            }
        )
        print("err", err)
