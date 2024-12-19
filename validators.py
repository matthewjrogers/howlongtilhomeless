# cerberus validator for scenarios
# id, name, description, created_at, updated_at

from cerberus import Validator

scenario_schema = {
    # "id": {
    #     "type": "integer",
    #     "required": True
    # },
    "name": {
        "type": "string",
        "required": True
    },
    "description": {
        "type": "string",
        "required": False
    },
    "created_at": {
        "type": "datetime",
        "required": True
    },
    "updated_at": {
        "type": "datetime",
        "required": True
    }
}