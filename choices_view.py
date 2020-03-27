import importlib

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from choices_decorator import ENUM_CHOICES

bp = Blueprint("choices", "/choices")


@bp.route("/<enum_name>", methods=["GET"])
def choices_list(request: Request, enum_name, *args):
    """提供给前端访问的选项列表

    Example:

    @choices
    class Status(IntEnum):
        Opening = 0
        Closed = 1

    访问链接：/choices/status
    result:
        {"Opening":0,"Closed":1}

    :param request: 请求
    :param enum_name: 枚举类名称
    :param args:
    :return: dict
    """
    cls_path = ENUM_CHOICES.get(enum_name, None)
    if cls_path is None:
        return json({})
    dot_index = cls_path.rindex(".")
    mod_str = cls_path[:dot_index]
    cls_str = cls_path[dot_index + 1:]
    # print(f"mod={mod_str}, cls={cls_str}")
    mod = importlib.import_module(mod_str)
    cls = getattr(mod, cls_str)
    data = {}
    for item in cls.__members__:
        enum_item = cls.__getattr__(item)
        if isinstance(enum_item, cls):
            data.update({enum_item.name: enum_item.value})
    return json(data)
