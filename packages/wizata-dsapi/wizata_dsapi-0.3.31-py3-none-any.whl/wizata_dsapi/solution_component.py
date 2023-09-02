import uuid
from .api_dto import ApiDto
from enum import Enum
import json


class SolutionType(Enum):
    GRAFANA_DASHBOARD = "grafana_dashboard"


class SolutionComponent(ApiDto):
    """
    A solution components handle an element giving to end-users to interact with solution.
    Currently supporting:
        - Grafana Dashboard
    """

    def __init__(self, solution_component_id: None):
        if solution_component_id is None:
            self.solution_component_id = uuid.uuid4()
        else:
            self.solution_component_id = solution_component_id
        self.category = None
        self.sub_category = None
        self.solution_type = None
        self.content = None

    def api_id(self) -> str:
        return str(self.solution_component_id).upper()

    def endpoint(self) -> str:
        return "SolutionComponents"

    def to_json(self):
        obj = {
            "id": str(self.solution_component_id)
        }
        if self.category is not None:
            obj["category"] = self.category
        if self.sub_category is not None:
            obj["subCategory"] = str(self.sub_category)
        if self.content is not None:
            obj["content"] = self.content
        if self.solution_type is not None and isinstance(self.solution_type, SolutionType):
            obj["type"] = self.solution_type.value
        return obj

    def from_json(self, obj):
        if "id" in obj.keys():
            self.solution_component_id = uuid.UUID(obj["id"])
        if "category" in obj.keys() and obj["category"] is not None:
            self.category = obj["category"]
        if "subCategory" in obj.keys() and obj["subCategory"] is not None:
            self.sub_category = obj["subCategory"]
        if "content" in obj.keys() and obj["content"] is not None:
            self.content = obj["content"]
        if "type" in obj.keys():
            self.solution_type = SolutionType(str(obj["type"]))
