from pydantic import BaseModel, Field

from ..enums.operator_enum import Opertator_Enum


class ExprModel(BaseModel):
    """
    Represents an expression with a left operand, an operator, and a right operand.
    """

    Left: str = Field(default="")
    Operator: Opertator_Enum = Field(default=Opertator_Enum.Equals)
    Right: str = Field(default="")
