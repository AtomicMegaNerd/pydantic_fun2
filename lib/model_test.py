import pytest
from uuid import UUID
from datetime import date

from pydantic import ValidationError

from lib.model import Automobile, AutomobileType


data = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

expected_serialized_by_alias = {
    "id": UUID("c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7"),
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": AutomobileType.convertible,
    "isElectric": False,
    "manufacturedDate": date(2023, 1, 1),
    "baseMSRPUSD": 93300.0,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "numberOfDoors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

str_too_small_in_top_features = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

date_before_1980 = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "1979-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

manufacturer_too_small = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "B",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

vin_too_long = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "123456789012345678900000000000000000000000000000000000000000000000000",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}


def test_serialization_with_id():
    automobile = Automobile.model_validate(data)
    assert automobile
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict == expected_serialized_by_alias


def test_str_too_small_in_top_features_should_fail_validation():
    with pytest.raises(ValidationError):
        Automobile.model_validate(str_too_small_in_top_features)


def test_date_before_1980_should_fail_validation():
    with pytest.raises(ValidationError):
        Automobile.model_validate(date_before_1980)


def test_manufacturer_too_small_should_fail_validation():
    with pytest.raises(ValidationError):
        Automobile.model_validate(manufacturer_too_small)


def test_vin_too_long_should_fail_validation():
    with pytest.raises(ValidationError):
        Automobile.model_validate(vin_too_long)
