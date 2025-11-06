from fastapi import HTTPException, status


class CatalogExceptions:
    category_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена!'
    )
    procedure_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Услуга не найдена!'
    )
    incorrect_id_procedures = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Некорректные ID процедур!',
    )


class UsersExceptions:
    incorrect_id_masters = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Некорректные ID мастеров!',
    )
    user_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден!'
    )


class DBExceptions:
    @staticmethod
    def conflict(entity: str):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{entity} уже существует или нарушает ограничения!',
        )

    @staticmethod
    def not_found(entity: str):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{entity} не найден(а)!',
        )


class AuthExceptions:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные!',
    )
    bad_request_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Ошибка запроса!',
    )
    missing_data_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Обязательные данные не указаны!',
    )
    invalid_confirmation_code = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Неверный код верификации!',
    )
    forbidden = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Доступ запрещен!',
    )


class ValidatorExceptions:
    staff_is_required = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Поле "staff" обязательно, если is_staff=True!',
    )
    is_staff_must_be_true = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Поле "is_staff" должно быть True, если staff заполнено!',
    )
    impossible_recognize_phone_numbe = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail='Невозможно распознать номер телефона!',
    )
    incorrect_phone_number = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Некорректный номер телефона!',
    )
