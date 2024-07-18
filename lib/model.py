from datetime import date
from enum import Enum
from functools import cached_property
from typing import Annotated, Tuple, TypeVar
from uuid import uuid4


from pydantic import (
    UUID4,
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    PlainSerializer,
    ValidationInfo,
    computed_field,
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


def validate_country(value: str) -> Tuple[str, str]:
    key: str = value.strip().casefold()
    try:
        return countries[key]
    except KeyError:
        raise ValueError(f"Invalid country: {value}")


def serialize_date(value: date) -> str:
    return value.strftime("%Y/%m/%d")


T = TypeVar("T")
BoundedList = Annotated[list[T], Field(min_length=1, max_length=5)]
BoundedString = Annotated[str, Field(min_length=2, max_length=50)]
Country = Annotated[str, AfterValidator(lambda name: validate_country(name)[0])]
CustomDate = Annotated[
    date, PlainSerializer(serialize_date, when_used="json-unless-none")
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

    # Model configuration
    # ------------------------------------------------------------

    model_config = ConfigDict(
        extra="forbid",
        validate_default=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        alias_generator=to_camel,
    )

    # Properties
    # ------------------------------------------------------------

    # These four properties show up in repr
    id_: UUID4 = Field(alias="id", default_factory=uuid4)
    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType = Field(alias="type", serialization_alias="type")

    # The rest of the properties are hidden from repr
    is_electric: bool = Field(default=False, repr=False)
    manufactured_date: CustomDate = Field(
        validation_alias="completionDate",
        ge=date(1980, 1, 1),  # type: ignore
        repr=False,
    )
    base_msrp_usd: float = Field(
        validation_alias="msrpUSD", serialization_alias="baseMSRPUSD", repr=False
    )
    top_features: BoundedList[BoundedString] | None = Field(
        default=None, alias="topFeatures", serialization_alias="topFeatures", repr=False
    )
    vin: BoundedString = Field(repr=False)
    number_of_doors: int = Field(
        ge=2, le=4, default=4, multiple_of=2, validation_alias="doors", repr=False
    )
    registration_country: Country = Field(repr=False)

    @computed_field(repr=False)
    @cached_property
    def registration_country_code(self) -> str:
        # This is a dictionary comprehension that creates a lookup table
        country_code_lookup = {name: code for (name, code) in countries.values()}
        return country_code_lookup[self.registration_country]

    registration_date: CustomDate | None = Field(default=None, repr=False)
    license_plate: BoundedString | None = Field(default=None, repr=False)

    # Validators
    # ------------------------------------------------------------

    @field_validator("registration_date")
    @classmethod
    def validate_registration_date(cls, value: date, values: ValidationInfo) -> date:
        data = values.data
        if "manufactured_date" in data and value < data["manufactured_date"]:
            raise ValueError("registration_date must be after manufactured_date")
        return value
