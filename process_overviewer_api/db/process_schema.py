import json
from jsonschema import validate

process_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "participants": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "purpose": {
            "type": "string"
        },
        "turnus": {
            "type": "string"
        }
    },
    "additionalProperties": False,
    "required": ["name", "participants", "purpose", "turnus"]
}

process1 = {
    "name": "spieleabend",
    "participants": ["it center"],
    "purpose": "socializing",
    "turnus": "monthly"
}

json_ser = json.dumps(process1)
json_data = json.loads(json_ser)
is_item = validate(instance=json_data, schema=process_schema)

test_process = '{"name": "spieleabend", "participants": ["it center"], "purpose": "socializing", "turnus": "weekly"}'

test_json_data = json.loads(test_process)
is_process = validate(test_json_data, process_schema)
print(is_process)
