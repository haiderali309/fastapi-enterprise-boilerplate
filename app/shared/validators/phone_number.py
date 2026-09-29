import phonenumbers


def phone_number_validator(value: str):

    try:
        phone = phonenumbers.parse(value, None)

    except phonenumbers.NumberParseException:
            raise ValueError(
                "Invalid phone number format"
        )


    if not phonenumbers.is_valid_number(phone):
        raise ValueError(
                "Invalid phone number"
        )

        
    return phonenumbers.format_number(
        phone,
        phonenumbers.PhoneNumberFormat.E164)