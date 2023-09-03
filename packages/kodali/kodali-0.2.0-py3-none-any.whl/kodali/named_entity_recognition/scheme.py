from strenum import StrEnum


class NerTags(StrEnum):
    BEGIN = "B"
    END = "E"
    INSIDE = "I"
    OUTSIDE = "O"
    SINGLE = "S"
