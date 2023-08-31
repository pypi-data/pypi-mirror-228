def handle_fields_special_chars(field: str) -> str:
    """
    Handle special characters in field names.

    Having, for example, a hyphen in a field name is not allowed in Python.

    Parameters
    ----------
    field : str
        Original Name of the field

    Returns
    -------
    str
        Name of the field with special characters replaced
    """
    special_characters_map = {"-": "_"}
    if any(special_char in field for special_char in special_characters_map.keys()):
        # the name that the field has in the filesystem
        for special_char in special_characters_map.keys():
            field = field.replace(special_char, special_characters_map[special_char])
    return field
