from sqladmin import ModelView

from models.models import Genre


class GenreAdmin(ModelView, model=Genre):
    name = "Жанр"
    name_plural = "Жанры"
    column_list = [Genre.id, Genre.name]
    form_excluded_columns = [Genre.films, Genre.created_at, Genre.updated_at]
    can_view_details = False
