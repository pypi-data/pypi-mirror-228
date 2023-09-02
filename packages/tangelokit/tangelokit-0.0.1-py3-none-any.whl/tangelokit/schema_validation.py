import jsonschema


def credit_line_validator(credit_lines):
    credit_lines_schema = {
        "type": "object",
        "properties": {
            "uid": {"type": "string"},
            "created_at": {"type": "string", "format": "date"},
            "balance": {"type": "number"},
            "todayToPay": {
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "total": {"type": "number"},
                    "date": {"type": "string", "format": "date"},
                    "last_quota": {"type": "number"}
                },
                "required": ["value", "total", "date", "last_quota"]
            }
        },
        "required": ["uid", "created_at", "balance", "todayToPay"]
    }
    validator = jsonschema.Draft7Validator(credit_lines_schema)
    errors = []
    for error in validator.iter_errors(credit_lines):
        errors.append(error.message)

    return errors


def disbursement_validator(disbursements):
    disbursements_schema = {
        "type": "list",
        "properties": {
            "uid": {"type": "string"},
            "uuid": {"type": "string"},
            "start_date": {"type": "string", "format": "date"},
            "created_at": {"type": "string", "format": "date"},
            "principal": {"type": "number"},
            "days_late": {"type": "number"},
            "status": {"type": "string"},

            "quotas": {
                "type": "list",
                "properties": {
                    "uuid": {"type": "string"},
                    "quota_number": {"type": "string"},
                    "start_date": {"type": "string", "format": "date"},
                    "payment_date": {"type": "string", "format": "date"},
                    "expire_date": {"type": "string", "format": "date"},
                    "is_late": {"type": "boolean"}
                },
                "required": ["value", "total", "date", "last_quota"]
            },
            "resumen": {
                "type": "object",
                "properties": {
                    "last_quota": {"type": "number"},
                    "total": {"type": "number"},
                    "value": {"type": "number"}
                }
            }
        },
        "required": ["uid", "created_at", "balance", "todayToPay"]
    }
    validator = jsonschema.Draft7Validator(disbursements_schema)
    errors = []
    for error in validator.iter_errors(disbursements):
        errors.append(error.message)

    return errors
