from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OperationKind(str, Enum):
    """модель вида операции."""
    INCOME = 'income'
    OUTCOME = 'outcome'


class OperationBase(BaseModel):
    """базовая модель операции"""
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]


class Operation(OperationBase):
    """была создана отдельная модель с целью соблюдения
    принципов SOLID."""
    id: int

    class Config:
        from_attributes = True


class OperationCreate(OperationBase):
    """модель для создания опирации."""
    pass


class OperationUpdate(OperationBase):
    """модель для изменения операции"""
    pass
