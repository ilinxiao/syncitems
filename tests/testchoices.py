from enum import IntEnum

from choices_decorator import choices


@choices
class CarCategory(IntEnum):
    Car = 0
    Freight = 1
