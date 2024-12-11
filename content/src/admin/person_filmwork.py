from sqladmin import ModelView

from models.models import PersonFilmWork


class PersonFilmWorkAdmin(ModelView, model=PersonFilmWork):
    name = "Персона фильма"
    name_plural = "Персоны фильмов"
    column_list = [
        PersonFilmWork.person_id,
        PersonFilmWork.film_work_id,
        PersonFilmWork.role,
    ]
    form_excluded_columns = [PersonFilmWork.updated_at, PersonFilmWork.created_at]
    can_view_details = False
