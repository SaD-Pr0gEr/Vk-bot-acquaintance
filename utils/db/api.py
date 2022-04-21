class BaseModelMixin:
    """Базовые методы моделей БД"""

    @classmethod
    def get_all(cls):
        return cls.query.all()
