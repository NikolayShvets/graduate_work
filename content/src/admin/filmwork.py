from sqladmin import ModelView

from models.models import FilmWork


class FilmAdmin(ModelView, model=FilmWork):
    name = "Фильм"
    name_plural = "Фильмы"
    column_list = [FilmWork.id, FilmWork.title, FilmWork.rating, FilmWork.creation_date, FilmWork.type]
    form_excluded_columns = [FilmWork.genres, FilmWork.persons, FilmWork.created_at, FilmWork.updated_at]
    can_view_details = False
