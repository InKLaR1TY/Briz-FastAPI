from enum import Enum


class EntityName(str, Enum):
    user = "Пользователь"
    category = "Категория"
    procedure = "Услуга"
    staff = "Сотрудник"
