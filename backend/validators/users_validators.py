from typing import Any

import phonenumbers

from constants.exceptions import ValidatorExceptions


def validate_staff_required(values: Any) -> Any:
    is_staff = values.is_staff
    staff = values.staff
    if is_staff and not staff:
        raise ValidatorExceptions.staff_is_required
    elif not is_staff and staff:
        raise ValidatorExceptions.is_staff_must_be_true
    return values


def validate_phone_number(cls, v: str) -> str:
    try:
        parsed = phonenumbers.parse(v, None)
    except phonenumbers.NumberParseException:
        raise ValidatorExceptions.impossible_recognize_phone_numbe

    if not phonenumbers.is_valid_number(parsed):
        raise ValidatorExceptions.incorrect_phone_number

    return phonenumbers.format_number(
        parsed, phonenumbers.PhoneNumberFormat.E164
    )
