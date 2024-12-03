from sqladmin import ModelView

from models.models import User


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
