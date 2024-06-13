from datetime import date
from enum import Enum

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
)
from pydantic.alias_generators import to_camel


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
        alias_generator=to_camel,
    )

    id_: UUID4 | None = Field(alias="id", default=None)

    manufacturer: str
    series_name: str
    type_: AutomobileType = Field(alias="type", serialization_alias="type")
    is_electric: bool = False
    manufactured_date: date = Field(validation_alias="completionDate")
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD", serialization_alias="baseMSRPUSD"
    )
    vin: str
    number_of_doors: int = Field(default=4, validation_alias="doors")
    registration_country: str | None = None
    license_plate: str | None = None

    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialze_manufactured_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")
