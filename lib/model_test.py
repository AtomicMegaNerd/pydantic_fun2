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
    "vin": "1234567890",
    "numberOfDoors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

data_3_doors = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "vin": "1234567890",
    "doors": 3,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

data_6_doors = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "vin": "1234567890",
    "doors": 6,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

data_no_id = {
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}


def test_serialization_with_id():
    automobile = Automobile.model_validate(data)
    assert automobile
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict == expected_serialized_by_alias


def test_3_doors_should_fail_validation():
    with pytest.raises(ValidationError):
        Automobile.model_validate(data_3_doors)


def test_6_doors_should_fail_validation():
    with pytest.raises(ValidationError):
        Automobile.model_validate(data_6_doors)


def test_no_id_generates_valid_uuid():
    automobile = Automobile.model_validate(data_no_id)
    assert automobile
    assert isinstance(automobile.id_, UUID)
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict
