from enum import StrEnum


class VideoType(StrEnum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"


class Role(StrEnum):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"
