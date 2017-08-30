from peewee import *
import json

from server.database.db import database


class BaseModel(Model):
    class Meta:
        database = database


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class Const(BaseModel):
    key = CharField(primary_key=True)
    value = JSONField()
    label = CharField()


def script():
    database.drop_table(Const)
    database.create_table(Const)


if __name__ == "__main__":
    script()
    pass
