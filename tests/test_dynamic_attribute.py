from types import DynamicClassAttribute


class BaseClass:
    name = "linxiao"


if __name__ == "__main__":
    base = BaseClass()
    base.name = "linxiao-new"
    base.age = 30
    BaseClass.age = 30

    for c in BaseClass.mro():
        print(c)
        for k, v in c.__dict__.items():
            if isinstance(v, DynamicClassAttribute):
                print("dynamic value:")
                print(v)
