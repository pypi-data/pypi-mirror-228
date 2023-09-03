from strenum import StrEnum


class SrlTags(StrEnum):
    BEGIN = "B"
    END = "E"
    INSIDE = "I"
    OUTSIDE = "O"
    SINGLE = "S"
