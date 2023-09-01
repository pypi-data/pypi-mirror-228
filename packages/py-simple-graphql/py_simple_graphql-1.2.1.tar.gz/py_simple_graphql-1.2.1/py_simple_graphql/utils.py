from .models import Errors, Error

def get_data(data: dict, method_name: str, field: str or list = None):
    if "data" in data:
        data = data["data"]
        if method_name in data:
            data = data[method_name]
            if not field:
                return data
            if isinstance(field, list):
                return [data[x] for x in field if x in data]
            if field in data:
                return data[field]
    return None

def check_errors(data: dict):
    if "errors" in data:
        errors = []
        for error in data["errors"]:
            errors.append(Error(**error))
        raise Errors(errors)