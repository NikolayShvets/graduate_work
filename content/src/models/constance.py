from enum import Enum


NAME_STR_LEN = 128
EMAIL_STR_LEN = 128
PASSWORD_STR_LEN = 128
SALT_STR_LEN = 32
USER_AGENT_STR_LEN = 256
REFRESH_TOKEN_STR_LEN = 512


class VideoType(Enum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"


class Role(Enum):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"
