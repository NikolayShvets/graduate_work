import pprint
from src.api.v1.schemas.film import FilmResponseSchema


class DataTransform:
    """
    данные преобразуются из формата Postgres в формат, пригодный для Elasticsearch.
    тот этап можно пропустить, если преобразования не требуется.
    """

    def __init__(self):
        pass
        # self.logger = logging.getLogger("data_transform")

    async def transform_movies_pgdata(self, raw_data: list[dict]) -> list:
        """Данные преобразуются из формата Postgres в формат, пригодный для Elasticsearch"""
        data_to_transfer = []

        for dict_ in raw_data:
            schema = {}
            schema.setdefault("id", dict_["fw_id"])
            schema.setdefault("title", dict_["title"])
            schema.setdefault("description", dict_["description"])
            schema.setdefault("imdb_rating", dict_["rating"])
            schema.setdefault("type", dict_["type"])
            schema.setdefault("creation_date", dict_["creation_date"])
            schema.setdefault("genres", dict_["name"])
            schema.setdefault("directors", [])
            schema.setdefault("actors", [])
            schema.setdefault("writers", [])

            value = {"id": dict_["person_id"], "name": dict_["full_name"]}

            if dict_["role"] == "director":
                schema.update({"directors": [value]})
            elif dict_["role"] == "actor":
                schema.update({"actors": [value]})
            else:
                schema.update({"writers": [value]})

            data_to_transfer.append(schema)

        return data_to_transfer

        # try:
        #     data_to_transfer.append(FilmResponseSchema(**schema))
        # except ValidationError as err:
        #     self.logger.exception(err)
        # return data_to_transfer

    # def transform_persons_pgdata_to_esdata(self, raw_data: list[dict]):
    #     """
    #     Данные преобразуются из формата Postgres в формат, пригодный для Elasticsearch
    #
    #     person_schema: {id: 22, full_name: George Lucas, films: [{id: 123, roles: 'actor', 'writer'}, ...]}
    #     film_schema: {id: 123, roles: 'actor', 'writer'}
    #     """
    #     data_to_transfer = []
    #     person_schema = {}
    #     film_schema = {}
    #     role_set = set()
    #
    #     for dict_ in raw_data:
    #         person_schema.setdefault("full_name", dict_["full_name"])
    #         person_id = person_schema.setdefault("id", str(dict_["person_id"]))
    #
    #         if person_id == str(dict_["person_id"]):
    #             films_list = person_schema.setdefault("films", [])
    #
    #             film_id = film_schema.setdefault("id", str(dict_["film_id"]))
    #             if film_id == str(dict_["film_id"]):
    #                 role_set.add(dict_["role"])
    #                 film_schema.update({"roles": [role for role in role_set]})
    #             else:
    #                 if film_schema not in films_list:
    #                     films_list.append(film_schema)
    #                 role_set = set()
    #                 film_schema = {}
    #                 film_schema.setdefault("id", str(dict_["film_id"]))
    #                 role_set.add(dict_["role"])
    #                 film_schema.update({"roles": [role for role in role_set]})
    #         else:
    #             if film_schema not in films_list:
    #                 films_list.append(film_schema)
    #             person_schema.update({"films": films_list})
    #             data_to_transfer.append(Person(**person_schema))
    #             person_schema = {}
    #             film_schema = {}
    #             role_set = set()
    #
    #             film_id = film_schema.setdefault("id", str(dict_["film_id"]))
    #
    #             if film_id == str(dict_["film_id"]):
    #                 role_set.add(dict_["role"])
    #                 film_schema.update({"roles": [role for role in role_set]})
    #     return data_to_transfer

    @staticmethod
    def transform_raw_dict_for_movies(schema: dict, role: str, raw_dict: dict) -> None:
        schema.setdefault("id", str(raw_dict["fw_id"]))
        schema.setdefault("imdb_rating", raw_dict["rating"])
        schema.setdefault("title", raw_dict["title"])
        schema.setdefault("creation_date", raw_dict["creation_date"])
        schema.setdefault("description", raw_dict["description"])
        schema.setdefault("genres", [])
        schema.setdefault("directors_names", [])
        schema.setdefault("actors_names", [])
        schema.setdefault("writers_names", [])
        schema.setdefault("directors", [])
        schema.setdefault("actors", [])
        schema.setdefault("writers", [])

        value = {"id": str(raw_dict["id"]), "name": raw_dict["full_name"]}
        value_name = value["name"]

        if role == "director":
            directors_list = schema.setdefault("directors", [value])
            directors_names_list = schema.setdefault("directors_names", [value_name])
            if value not in directors_list:
                directors_list.append(value)
                directors_names_list.append(value_name)
                schema.update({"directors": directors_list})
                schema.update({"directors_names": directors_names_list})

        if role == "actor":
            actors_list = schema.setdefault("actors", [value])
            actors_names_list = schema.setdefault("actors_names", [value_name])
            if value not in actors_list:
                actors_list.append(value)
                actors_names_list.append(value_name)
                schema.update({"actors": actors_list})
                schema.update({"actors_names": actors_names_list})

        if role == "writer":
            writers_list = schema.setdefault("writers", [value])
            writers_names_list = schema.setdefault("writers_names", [value_name])
            if value not in writers_list:
                writers_list.append(value)
                writers_names_list.append(value_name)
                schema.update({"writers": writers_list})
                schema.update({"writers_names": writers_names_list})

    # @staticmethod
    # def transform_raw_dict_for_persons(
    #     schema: dict, schema_film: dict, raw_dict: dict
    # ) -> None:
    #     schema.setdefault("id", str(raw_dict["person_id"]))
    #     schema.setdefault("full_name", raw_dict["full_name"])
    #     schema.setdefault("films", [])
    #
    #     value = {"id": str(raw_dict["id"]), "name": raw_dict["full_name"]}
    #     genre_value = {
    #         "id": str(raw_dict["g_id"]),
    #         "name": raw_dict["name"],
    #         "description": raw_dict["g_description"],
    #     }
    #
    #     films_value = {"id": str(raw_dict["film_id"]), "roles": []}
    #
    #     films_list = schema.setdefault("films", [films_value])
    #     if films_value not in films_list:
    #         films_list.append(genre_value)
    #         schema.update({"films": films_list})
