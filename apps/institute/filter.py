from rest_framework.filters import BaseFilterBackend


class CustomSchema(BaseFilterBackend):
    def get_schema_operation_parameters(self, view):
        return [{
            "name": "foo",
            "in": "query",
            "required": True,
            "description": "What foo does...",
            "schema": {"type": "string"}
        }]