import csv
from io import StringIO
from typing import Any

from fastapi import Depends

from .operations import OperationsService
from ..models.operations import (
    Operation,
    OperationCreate,
)


class ReportsService:
    def __init__(self, operations_service: OperationsService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: Any) -> None:
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=[
                'date',
                'kind',
                'amount',
                'description',
            ],
        )

        operations = []
        next(reader)
        for row in reader:
            operation_data = OperationCreate.model_validate(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operations_service.create_many(
            user_id,
            operations,
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'date',
                'kind',
                'amount',
                'description',
            ],
            extrasaction='ignore',
        )

        operations = self.operations_service.get_list(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = Operation.model_validate(operation)
            writer.writerow(operation_data.model_dump())

        output.seek(0)
        return output
