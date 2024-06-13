from datetime import date
from enum import Enum
from typing import Annotated, TypeVar
from uuid import uuid4


from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
)
from pydantic.alias_generators import to_camel

T = TypeVar("T")
BoundedList = Annotated[list[T], Field(min_length=1, max_length=5)]
BoundedString = Annotated[str, Field(min_length=2, max_length=50)]


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

    id_: UUID4 = Field(alias="id", default_factory=uuid4)

    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType = Field(alias="type", serialization_alias="type")
    is_electric: bool = False
    manufactured_date: date = Field(
        validation_alias="completionDate",
        ge=date(1980, 1, 1),  # type: ignore
    )
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD", serialization_alias="baseMSRPUSD"
    )
    top_features: BoundedList[BoundedString] | None = Field(
        default=None, alias="topFeatures", serialization_alias="topFeatures"
    )
    vin: BoundedString
    number_of_doors: int = Field(
        ge=2, le=4, default=4, multiple_of=2, validation_alias="doors"
    )
    registration_country: BoundedString | None = None
    license_plate: BoundedString | None = None

    @field_serializer("manufactured_date", when_used="json-unless-none")
    def serialze_manufactured_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")
