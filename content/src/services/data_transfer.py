class DataTransform:
    def __init__(self):
        pass
        # self.logger = logging.getLogger("content")

    @staticmethod
    async def transform_movies_pgdata(raw_data: list[dict]) -> list[dict]:
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
