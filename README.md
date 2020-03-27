# Syncitems
前后端可选项同步Sanic实现。Optional synchronous sanic implementation.
#### 提出问题：
在前后端分离的开发协作中，后端的可选项或者某种状态列表通常需要前端保持同步。比如前端需要按照用户的离职在职状态来进行筛选，前端首先需要知道能够传递哪些值和什么类型的值，然后后端针对不同的状态返回相应的结果。这些值就是一个可选项列表或者说是状态列表。
#### 解决方案：
这个问题是我个人在开发过程中遇到的一个实际问题，我设计的解决方案如下，以下代码基于Sanic框架：
1. 后端定义枚举。

```python

class JobStatus(IntEnum):
    Working = (0,)  # 工作中
    Leave = (1,)  # 离职 本人现在离职中，欢迎骚扰
    # 暴力中文 = 2
```

2. 通过choices装饰器把枚举类型收录到供前端访问的可选项列表。

```python

@choices
class JobStatus(IntEnum):
    Working = (0,)  # 工作中
    Leave = (1,)  # 离职
    # 暴力中文 = 2

```

* choices装饰器实现choices_view：

```python
from enum import EnumMeta

ENUM_CHOICES = {}


def choices(enum_type: EnumMeta):
    """以装饰器的形式收录作为选项的枚举类型"""

    if not isinstance(enum_type, EnumMeta):
        raise TypeError(f"{enum_type} 不是枚举类型。")

    cls_path = enum_type.__module__ + "." + enum_type.__name__
    ENUM_CHOICES.update({enum_type.__name__.lower(): cls_path})
    return enum_type
```

* 开启供前端访问的选项路由：

```python

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
    :return: response(json)
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
```
* 别忘记在Sanic中添加蓝图：
```python
from choices_view import bp

app = Sanic("sync_items")
app.blueprint(bp)
```
* 访问结果：
```
{"Working":0,"Leave":1}
```

#### 使用方式：

1. 确保已安装pipenv.
```Shell
pip install pipenv
```
2. 安装依赖包。
```python
pipenv install
```
3. 进入环境并运行。
```
pipenv shell
```
4. 运行。
```
python  main.py
```

#### 方案的好处：
最低成本的解决了选项同步的问题。

#### 注意事项：
如果定义了一个枚举类型，也加上了choices装饰器，但是该枚举类型在实际代码并没有被用到，该选项并不会被前端访问到。这是python的代码加载机制决定的。
为了解决这个问题，最好在choices_view里面显式的导入一次需要供前端访问的枚举类型。

