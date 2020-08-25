from enum import Enum


class Role(Enum):
    BASE = "base"
    STUDENT = "student"
    NINJA = "ninja"
    FACULTY = "faculty"
    ADMIN = "admin"

    def to_str(self):
        return f"olin:{self.value}"

    def __str__(self):
        return self.to_str()

    @classmethod
    def from_str(cls, string):
        role_name = string.split(":")[1]
        return cls(role_name)

    def full(self) -> tuple:
        """
        Returns the full list of roles, including
        less priveleged roles. So Role.NINJA.full()
        will be (Role.BASE, Role.STUDENT, Role.NINJA)
        """
        enum_list = tuple(Role)
        return enum_list[: enum_list.index(self) + 1]


class TrainingStatus(Enum):
    STARTED = "Started"
    READING = "Reading"
    WORKSHEET = "Worksheet"
    TRAINING = "Training"
    TEST_PIECE = "Test Piece"
    COMPLETE = "Complete"
