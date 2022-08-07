from pydantic import BaseModel

from pydantic_factories import ModelFactory


class AssertDict:
    random_float = "random_float"
    random_int = "random_int"
    random_str = "random_str"

    @staticmethod
    def assert_dict_expected_shape(expected_json, json):
        if type(expected_json) == list:
            assert len(expected_json) == len(json)
            for expected, actual in zip(expected_json, json):
                AssertDict.assert_dict_expected_shape(expected, actual)
        elif type(expected_json) == dict:
            for key, value in expected_json.items():
                assert key in json
                AssertDict.assert_dict_expected_shape(value, json[key])
        elif expected_json == AssertDict.random_float:
            assert type(json) == float
        elif expected_json == AssertDict.random_int:
            assert type(json) == int
        elif expected_json == AssertDict.random_str:
            assert type(json) == str
        else:
            assert expected_json == json


def test_factory_child_model_list():
    """
    Given a Pydantic model with a Pydantic model and a list of Pydantic models as attributes,
    When I create a model using the factory passing only part of the attributes of these attributes,
    Then I get the models with the attributes I passed and the other fields are randomly generated by the factory.
    """

    class Address(BaseModel):
        city: str
        country: str

    class Material(BaseModel):
        name: str
        origin: str

    class Toy(BaseModel):
        name: str
        weight: float
        materials: list[Material]

    class Pet(BaseModel):
        name: str
        age: int
        toys: list[Toy]

    class Person(BaseModel):
        name: str
        age: int
        pets: list[Pet]
        address: Address

    class PersonFactory(ModelFactory[Person]):
        __model__ = Person

    data = {
        "name": "Jean",
        "pets": [
            {
                "name": "dog",
                "toys": [
                    {
                        "name": "ball",
                        "materials": [{"name": "yarn"}, {"name": "plastic"}],
                    },
                    {
                        "name": "bone",
                    },
                ],
            },
            {
                "name": "cat",
            },
        ],
        "address": {
            "country": "France",
        },
    }

    person = PersonFactory.build(**data)
    expected_json = {
        "name": "Jean",
        "age": AssertDict.random_int,
        "pets": [
            {
                "name": "dog",
                "age": AssertDict.random_int,
                "toys": [
                    {
                        "name": "ball",
                        "weight": AssertDict.random_float,
                        "materials": [
                            {"name": "yarn", "origin": AssertDict.random_str},
                            {"name": "plastic", "origin": AssertDict.random_str},
                        ],
                    },
                    {
                        "name": "bone",
                        "weight": AssertDict.random_float,
                        "materials": [
                            {"name": AssertDict.random_str, "origin": AssertDict.random_str},
                        ],
                    },
                ],
            },
            {
                "name": "cat",
                "age": AssertDict.random_int,
                "toys": [
                    {
                        "name": AssertDict.random_str,
                        "weight": AssertDict.random_float,
                        "materials": [
                            {"name": AssertDict.random_str, "origin": AssertDict.random_str},
                        ],
                    }
                ],
            },
        ],
        "address": {"city": AssertDict.random_str, "country": "France"},
    }
    AssertDict.assert_dict_expected_shape(expected_json, person.dict())