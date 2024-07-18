from uuid import UUID
from datetime import date


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
    "registrationCountry": "us",
    "registrationDate": "2023-06-01",
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
    "registrationCountry": "United States of America",
    "registrationCountryCode": "USA",
    "registrationDate": date(2023, 6, 1),
    "licensePlate": "AAA-BBB",
}


def test_serialization_with_id():
    automobile = Automobile.model_validate(data)
    assert automobile
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict == expected_serialized_by_alias
