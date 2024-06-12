from datetime import date

from lib.model import Automobile, AutomobileType

data_json = """
{
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": "Convertible",
    "isElectric": false,
    "completionDate": "2023-01-01",
    "msrpUSD": 93300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}
"""

expected_serialized_dict = {
    "manufacturer": "BMW",
    "series_name": "M4",
    "type_": AutomobileType.convertible,
    "is_electric": False,
    "manufactured_date": date(2023, 1, 1),
    "base_msrp_usd": 93300.0,
    "vin": "1234567890",
    "number_of_doors": 2,
    "registration_country": "France",
    "license_plate": "AAA-BBB",
}

expected_serialized_dict_by_alias = {
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

expected_serialized_json_by_alias = (
    '{"manufacturer":"BMW","seriesName":"M4","type":"Convertible",'
    '"isElectric":false,"manufacturedDate":"2023/01/01","baseMSRPUSD":93300.0,'
    '"vin":"1234567890","numberOfDoors":2,"registrationCountry":"France",'
    '"licensePlate":"AAA-BBB"}'
)


def test_deserialization():
    automobile = Automobile.model_validate_json(data_json)
    assert automobile


def test_serialization():
    automobile = Automobile.model_validate_json(data_json)
    assert automobile
    serialized_dict = automobile.model_dump()
    assert serialized_dict == expected_serialized_dict


def test_serialization_by_alias():
    automobile = Automobile.model_validate_json(data_json)
    assert automobile
    serialized_dict = automobile.model_dump(by_alias=True)
    assert serialized_dict == expected_serialized_dict_by_alias


def test_serialization_json_by_alias():
    automobile = Automobile.model_validate_json(data_json)
    assert automobile
    serialized_json = automobile.model_dump_json(by_alias=True)
    assert serialized_json == expected_serialized_json_by_alias
