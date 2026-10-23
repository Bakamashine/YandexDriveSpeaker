def try_get_value(key: str):
    """Return the value for `key` from the .env file, or None if missing."""
    with open(".env", "r", encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, sep, value = line.partition("=")
            if sep and name.strip() == key:
                return value.strip()
    return None


def get_value(key: str) -> str:
    value = try_get_value(key)
    if value is None:
        raise Exception("No value found for this key")
    return value
