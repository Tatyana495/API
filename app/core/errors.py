class AppError(Exception):
    """Базовая ошибка приложения."""


class ConflictError(AppError):
    """Конфликт состояния, например объект уже существует."""


class UnauthorizedError(AppError):
    """Ошибка аутентификации, например неверный логин или пароль."""


class ForbiddenError(AppError):
    """Недостаточно прав для выполнения действия."""


class NotFoundError(AppError):
    """Сущность не найдена."""


class ExternalServiceError(AppError):
    """Ошибка при обращении к внешнему сервису."""