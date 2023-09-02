# -*- coding: utf-8 -*-

import os
from typing import Any
import orjson
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, UnknownType, ValidationError


def open_file(file):
    print()
    try:
        print("open", file, "...")

        json_data = None

        with open(file, "r") as f:
            json_data = orjson.loads(f.read())

        return json_data
    except Exception as e:
        print("open_file Exception:", e)


def save_file(file_name, data):
    try:
        with open(file_name, "wb") as f:
            f.write(orjson.dumps(data))

        print("Yep", file_name, "succesfully generated.")
    except Exception as e:
        print("save_file: Oops, definitely can not generate file...", e)


def check_file(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


def is_iterable(value: Any) -> bool:
    if value is None:
        return False

    return isinstance(value, (tuple, list))


def validate_json_schema(schema, body):
    try:
        validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
        errors: list[Any] = sorted(validator.iter_errors(body), key=str)

        if not is_iterable(errors):
            raise "error al validar la lista de errores"

        if len(errors) <= 0:
            print("JSON Schema Validator OK")
            return body

        missing: list[Any] = []

        for error in errors:
            obj_error: dict[str, Any] = {
                "absolute_path": list(error.absolute_path),
                "message": error.message,
                "validator": error.validator,
            }

            if "description" in error.schema:
                obj_error.update({"description": error.schema.get("description")})

            missing.append(obj_error)

        if len(missing) > 0:
            print("JSON Schema Validator errors:")
            print()
            print(missing)

    except (ValidationError, SchemaError, UnknownType) as ve:
        print("An instance was invalid under a provided schema...")
        print("ValidateSchema ValidationError: {}", ve)
    except Exception as e:
        print("ValidateSchema Exception:", e)
