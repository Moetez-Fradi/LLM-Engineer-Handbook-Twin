def split_user_name(full_name: str) -> tuple[str, str]:
    """Splits a full name into first and last name.

    Args:
        full_name (str): The full name of the user.
    Returns:
        tuple[str, str]: A tuple containing the first name and last name.
    """
    parts = full_name.strip().split()
    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        return parts[0], ""
    else:
        first_name = parts[0]
        last_name = " ".join(parts[1:])
        return first_name, last_name