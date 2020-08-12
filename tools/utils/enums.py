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


class TrainingStatus(Enum):
    STARTED = "Started"
    READING = "Reading"
    WORKSHEET = "Worksheet"
    TRAINING = "Training"
    TEST_PIECE = "Test Piece"
    COMPLETE = "Complete"
