from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import date


class AutomobileType(Enum):
    sedan = "Sedan"
    couple = "Coupe"
    convertible = "Convertible"
    suv = "SUV"
    truck = "Truck"


class Automobile(BaseModel):
    """
    This is a pydantic model that represents an automobile.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    manufacturer: str
    series_name: str
    type_: AutomobileType
    is_electric: bool = False
    manufactured_date: date
    base_msrp_usd: float
    vin: str
    number_of_doors: int = 4
    registration_country: str | None = None
    license_plate: str | None = None
