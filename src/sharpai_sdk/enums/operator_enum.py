from enum import Enum


class Opertator_Enum(str, Enum):
    """
    Operator Enum
    """

    GreaterThan = "GreaterThan"
    LessThan = "LessThan"
    Equals = "Equals"
    Contains = "Contains"
    NotEquals = "NotEquals"
    GreaterThanOrEqual = "GreaterThanOrEqual"
    LessThanOrEqual = "LessThanOrEqual"
