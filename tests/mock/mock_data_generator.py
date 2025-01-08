import decimal
from datetime import date, datetime
from enum import EnumMeta
from typing import List
from uuid import UUID

from faker import Faker


class FakerDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def types_converter(self, field_type):
        if field_type == str:
            return self.fake.pystr(4, 12)
        if field_type == UUID:
            return self.fake.uuid4()
        if field_type == date:
            return self.fake.date_object()
        if field_type == datetime:
            return self.fake.date_time()
        if field_type == bool:
            return self.fake.boolean()
        if field_type == int:
            return self.fake.pyint()
        if field_type == float:
            return self.fake.pyfloat()
        if field_type == decimal:
            return self.fake.pydecimal()
        if isinstance(field_type, EnumMeta):
            return self.fake.enum(field_type).value
        return field_type

    def get_fake_object(self, object_template: dict) -> dict:
        """
        object_template: шаблон объекта
        example input: object_template = {'name': str, 'year': int, 'is_live': bool}
        example output: {'name': 'test_name': 'year': 100, 'is_live': True}
        """
        return {key: self.types_converter(value) for key, value in object_template.items()}

    def get_fake_objects(self, object_template: dict, count: int) -> List[dict]:
        return [self.get_fake_object(object_template) for _ in range(count)]
