from enum import Enum


class Scope(Enum):
    BASE = "base"
    STUDENT = "student"
    NINJA = "ninja"
    FACULTY = "facultly"
    ADMIN = "admin"

    def to_str(self):
        return f"olin:{self.value}"

    def __str__(self):
        return self.to_str()
