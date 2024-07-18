from enum import Enum


class Statuses(Enum):
    NEW = "New"
    IN_PROGRESS = "In progress"
    PENDING = "Pending"
    BLOCKED = "Blocked"
    TESTING = "Testing"
    CLOSED = "Closed"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
