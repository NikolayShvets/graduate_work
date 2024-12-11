from sqladmin import ModelView

from models.models import Person


class PersonAdmin(ModelView, model=Person):
    name = "Персона"
    name_plural = "Персоны"
    column_list = [Person.id, Person.full_name]
    form_excluded_columns = [Person.films, Person.created_at, Person.updated_at]
    can_view_details = False
