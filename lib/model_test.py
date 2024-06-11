import pytest
from datetime import date

from pydantic import ValidationError

from lib.model import Automobile, AutomobileType

data = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": "Convertible",
    "is_electric": False,
    "manufactured_date": "2023-01-01",
    "base_msrp_usd": 93_300,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB",
}

data_expected_serialization = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": AutomobileType.convertible,
    "is_electric": False,
    "manufactured_date": date(2023, 1, 1),
    "base_msrp_usd": 93_300.0,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB",
}

# The extra whitespace in the JSON string is intentional.
data_json = """
{
    "manufacturer": " BMW ",
    "series_name": " M4 ",
    "type_": "Convertible",
    "manufactured_date": "2023-01-01",
    "base_msrp_usd": 93300,
    "vin": " 1234567890 "
}
"""

data_json_missing_manufacturer = """
{
    "series_name": "M4",
    "type_": "Convertible",
    "manufactured_date": "2023-01-01",
    "base_msrp_usd": 93300,
    "vin": "1234567890"
}
"""

data_json_invalid_type = """
{
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": "HappyFunCar",
    "manufactured_date": "2023-01-01",
    "base_msrp_usd": 93300,
    "vin": "1234567890",
}
"""

data_json_expected_serialization = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": AutomobileType.convertible,
    "is_electric": False,
    "manufactured_date": date(2023, 1, 1),
    "base_msrp_usd": 93_300.0,
    "vin": "1234567890",
    "number_of_doors": 4,
    "registration_country": None,
    "license_plate": None,
}


def test_automobile_data_serialization():
    automobile = Automobile.model_validate(data)
    assert automobile is not None
    assert automobile.model_dump() == data_expected_serialization


def test_auto_data_json_serialization():
    automobile = Automobile.model_validate_json(data_json)
    assert automobile is not None
    assert automobile.model_dump() == data_json_expected_serialization


def test_missing_json_manufacturer_raises_validation_error():
    with pytest.raises(ValidationError):
        Automobile.model_validate_json(data_json_missing_manufacturer)


def test_invalid_json_type_raises_validation_error():
    with pytest.raises(ValidationError):
        Automobile.model_validate_json(data_json_invalid_type)
