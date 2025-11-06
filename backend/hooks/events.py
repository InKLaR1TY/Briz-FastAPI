import sqlalchemy
from sqlalchemy import event

from models import Category, Procedure, User
from utils.slugify import translit_text


@event.listens_for(User, 'before_insert')
def create_username_before_insert(mapper, connection, target: User):
    if not target.username:
        target.username = translit_text(target.get_fullname)


@event.listens_for(User, 'before_update')
def update_procedure_slug_before_update(mapper, connection, target: User):
    state = sqlalchemy.inspect(target)
    history_first_name = state.attrs.first_name.history
    history_last_name = state.attrs.last_name.history
    history_surname = state.attrs.surname.history
    if (
        history_first_name.has_changes()
        or history_last_name.has_changes()
        or history_surname.has_changes()
    ):
        target.username = translit_text(target.get_fullname)


@event.listens_for(Category, 'before_insert')
def create_category_slug_before_insert(mapper, connection, target: Category):
    if not target.slug:
        target.slug = translit_text(target.title)


@event.listens_for(Category, 'before_update')
def update_category_slug_before_update(mapper, connection, target: Category):
    state = sqlalchemy.inspect(target)
    history = state.attrs.title.history
    if history.has_changes():
        target.slug = translit_text(target.title)


@event.listens_for(Procedure, 'before_insert')
def create_procedure_slug_before_insert(mapper, connection, target: Procedure):
    if not target.slug:
        target.slug = translit_text(target.title)


@event.listens_for(Procedure, 'before_update')
def update_procedure_slug_before_update(mapper, connection, target: Procedure):
    state = sqlalchemy.inspect(target)
    history = state.attrs.title.history
    if history.has_changes():
        target.slug = translit_text(target.title)
