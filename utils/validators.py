def is_digit_input(value: str, action_type: str) -> bool:
    """Validate that input is digits only when inserting (Tk validatecommand helper)."""
    if action_type == '1':  # insert
        return value.isdigit() if value else True
    return True
