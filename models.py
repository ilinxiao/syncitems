from enum import IntEnum

from tortoise import fields, Model

from choices_decorator import choices
from tests.testchoices import CarCategory


@choices
class JobStatus(IntEnum):
    Working = (0,)  # 工作中
    Leave = (1,)  # 离职
    # 暴力中文 = 0


class Choice(Model):
    name = fields.CharField(max_length=50)
    status = fields.IntEnumField(JobStatus, description="TEST Description.")
    # car_category = fields.IntEnumField(CarCategory)
