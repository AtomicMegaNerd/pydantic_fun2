from datetime import date
from enum import Enum
from typing import Annotated, Tuple, TypeVar
from uuid import uuid4


from pydantic import (
    UUID4,
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_serializer,
    field_validator,
)
from pydantic.alias_generators import to_camel

countries: dict[str, Tuple[str, str]] = {
    "australia": ("Australia", "AUS"),
    "canada": ("Canada", "CAN"),
    "china": ("China", "CHN"),
    "france": ("France", "FRA"),
    "germany": ("Germany", "DEU"),
    "india": ("India", "IND"),
    "mexico": ("Mexico", "MEX"),
    "norway": ("Norway", "NOR"),
    "pakistan": ("Pakistan", "PAK"),
    "san marino": ("San Marino", "SMR"),
    "sanmarino": ("San Marino", "SMR"),
    "spain": ("Spain", "ESP"),
    "sweden": ("Sweden", "SWE"),
    "united kingdom": ("United Kingdom", "GBR"),
    "uk": ("United Kingdom", "GBR"),
    "great britain": ("United Kingdom", "GBR"),
    "britain": ("United Kingdom", "GBR"),
    "us": ("United States of America", "USA"),
    "united states": ("United States of America", "USA"),
    "usa": ("United States of America", "USA"),
}


def validate_registration_country(value: str) -> Tuple[str, str]:
    key: str = value.strip().casefold()
    try:
        return countries[key]
    except KeyError:
        raise ValueError(f"Invalid country: {value}")


T = TypeVar("T")
BoundedList = Annotated[list[T], Field(min_length=1, max_length=5)]
BoundedString = Annotated[str, Field(min_length=2, max_length=50)]

Country = Annotated[
    str, AfterValidator(lambda name: validate_registration_country(name)[0])
]


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
    registration_country: Country
    registration_date: date | None = None
    license_plate: BoundedString | None = None

    @field_validator("registration_date")
    @classmethod
    def validate_registration_date(cls, value: date, values: ValidationInfo) -> date:
        data = values.data
        if "manufactured_date" in data and value < data["manufactured_date"]:
            raise ValueError("registration_date must be after manufactured_date")
        return value

    # Note we can use the same function for multiple fields
    @field_serializer(
        "manufactured_date", "registration_date", when_used="json-unless-none"
    )
    def serialze_manufactured_date(self, value: date) -> str:
        return value.strftime("%Y/%m/%d")
