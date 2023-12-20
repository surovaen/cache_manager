from bson import ObjectId


class OID(str):
    """Определение ID объекта модели с валидацией на ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(str(value)):
            return ValueError(
                'Получен некорректный id: {id}'.format(
                    id=value,
                ),
            )
        return str(value)
