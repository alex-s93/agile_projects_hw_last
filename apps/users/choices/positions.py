from enum import Enum


class Positions(Enum):
    CEO = "Ceo"
    CTO = "Cto"
    DESIGNER = "Designer"
    PROGRAMMER = "Programmer"
    PRODUCT_OWNER = "Product_owner"
    PROJECT_OWNER = "Project_owner"
    PROJECT_MANAGER = "Project_manager"
    QA = "QA"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]