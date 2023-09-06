from typing import Type

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from ..database import get_session
from ..models.operations import (
    OperationCreate,
    OperationKind,
    OperationUpdate,
)
from ..tables import Operation


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, user_id: int, operation_id) -> Type[Operation]:
        operation = (
            self.session
            .query(Operation)
            .filter_by(
                id=operation_id,
                user_id=user_id,
            )
            .first()
        )
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, user_id: int, kind: OperationKind = None) -> list[Type[Operation]]:
        query = (
            self.session
            .query(Operation)
            .filter_by(user_id=user_id)
        )
        if kind:
            query = query.filter_by(kind=kind)
        operations = query.all()
        return operations

    def get(self, user_id: int, operation_id: int) -> Type[Operation]:
        return self._get(user_id, operation_id)

    def create_many(self, user_id: int, operations_data: list[OperationCreate]) -> list[Operation]:
        operations = [
            Operation(
                **operation_data.model_dump(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()
        return operations

    def create(self, user_id: int, operation_data: OperationCreate) -> Operation:
        operation = Operation(
            **operation_data.model_dump(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self,
               user_id: int,
               operation_id: int,
               operation_data: OperationUpdate,
               ) -> Type[Operation]:
        operation = self._get(user_id, operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(self, user_id: int, operation_id: int) -> None:
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()
