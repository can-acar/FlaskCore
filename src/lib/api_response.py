from typing import Any

from flask import json
from flask import Response


def create_response(data: Any, status: int):
    return Response(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )


class ApiResponse:
    def __init__(self, data=None, message=None, status=200):
        self.data = data
        self.status = status
        self.message = message

    def __str__(self):
        return f"ApiResponse(data={self.data}, message={self.message}, status={self.status})"

    def to_dict(self):
        return {
            "data": self.data,
            "message": self.message,
            "status": self.status
        }
