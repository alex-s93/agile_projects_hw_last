from enum import Enum

class Priorities(Enum):
    VERY_LOW = (1, "Very low")
    LOW = (2, "Low")
    MEDIUM = (3, "Medium")
    HIGH = (4, "High")
    CRITICAL = (5, "Critical")

    @classmethod
    def choices(cls):
        return [(attr.value[0], attr.value[1]) for attr in cls]

    def __getitem__(self, item):
        return self.value[item]
