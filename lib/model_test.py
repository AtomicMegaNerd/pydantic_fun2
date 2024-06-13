from uuid import UUID
from datetime import date

from lib.model import Automobile, AutomobileType


data = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4",
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
    "seriesName": "M4",
    "type": AutomobileType.convertible,
    "isElectric": False,
    "manufacturedDate": date(2023, 1, 1),
    "baseMSRPUSD": 93300.0,
    "vin": "1234567890",
    "numberOfDoors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

data_no_id = {
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}

expected_serialization_data_no_id_by_alias = {
    "id": None,
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": AutomobileType.convertible,
    "isElectric": False,
    "manufacturedDate": date(2023, 1, 1),
    "baseMSRPUSD": 93300.0,
    "vin": "1234567890",
    "numberOfDoors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB",
}


def test_serialization_with_id():
    automobile = Automobile.model_validate(data)
    assert automobile
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict == expected_serialized_by_alias


def test_serialization_no_id():
    automobile = Automobile.model_validate(data_no_id)
    assert automobile
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict == expected_serialization_data_no_id_by_alias
