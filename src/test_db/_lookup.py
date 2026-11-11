from sqlobject import SQLObjectNotFound


def get_key_value(key_values, key: str):
    try:
        return key_values.filter(key_values.sourceClass.q.key == key).getOne()
    except SQLObjectNotFound as exc:
        raise SQLObjectNotFound(f"key {key!r} does not exist") from exc
