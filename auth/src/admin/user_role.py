from sqladmin import ModelView

from models.models import UserRole


class UserRoleAdmin(ModelView, model=UserRole):
    name = "Роль пользователя"
    name_plural = "Роли пользователей"
    column_list = [UserRole.user_id, UserRole.role_id]
    form_excluded_columns = [UserRole.created_at, UserRole.updated_at]
    can_view_details = False
