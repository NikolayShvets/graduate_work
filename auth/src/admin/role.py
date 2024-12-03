from sqladmin import ModelView

from models.models import Role


class RoleAdmin(ModelView, model=Role):
    name = "Роль"
    name_plural = "Роли"
    column_list = [Role.id, Role.name]
    form_excluded_columns = [Role.users, Role.created_at, Role.updated_at]
    can_view_details = False
