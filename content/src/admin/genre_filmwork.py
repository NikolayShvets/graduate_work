from sqladmin import ModelView

from models.models import GenreFilmWork


class GenreFilmWorkAdmin(ModelView, model=GenreFilmWork):
    name = "Жанр фильма"
    name_plural = "Жанры фильмов"
    column_list = [GenreFilmWork.genre_id, GenreFilmWork.film_work_id]
    form_excluded_columns = [GenreFilmWork.updated_at, GenreFilmWork.created_at]
    can_view_details = False
