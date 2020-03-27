from enum import EnumMeta

ENUM_CHOICES = {}


def choices(enum_type: EnumMeta):
    """以装饰器的形式收录作为选项的枚举类型"""

    if not isinstance(enum_type, EnumMeta):
        raise TypeError(f"{enum_type} 不是枚举类型。")

    cls_path = enum_type.__module__ + "." + enum_type.__name__
    ENUM_CHOICES.update({enum_type.__name__.lower(): cls_path})
    return enum_type
