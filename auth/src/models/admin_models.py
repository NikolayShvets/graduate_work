from sqladmin import ModelView

from models.models import Role, User, UserRole


class RoleAdmin(ModelView, model=Role):
    name = "Роль"
    name_plural = "Роли"
    column_list = [Role.id, Role.name]
    form_excluded_columns = [Role.users, Role.created_at, Role.updated_at]
    can_view_details = False


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [User.id, User.email, User.is_active, User.is_superuser, User.is_verified]
    form_excluded_columns = [User.roles, User.sessions, User.oauth_accounts, User.created_at, User.updated_at]
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False
    can_view_details = False


class UserRoleAdmin(ModelView, model=UserRole):
    name = "Роль пользователя"
    name_plural = "Роли пользователей"
    column_list = [UserRole.user_id, UserRole.role_id]
    form_excluded_columns = [UserRole.created_at, UserRole.updated_at]
    can_view_details = False
