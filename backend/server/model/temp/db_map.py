from peewee import *

database = MySQLDatabase('Goku', **{'host': '127.0.0.1', 'password': '123456', 'port': 3306, 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class BikeModel(BaseModel):
    category = CharField()
    color = CharField(null=True)
    id = CharField(primary_key=True)
    introduction = CharField(null=True)
    left = IntegerField()
    num_sold = IntegerField()
    num_view = IntegerField()
    pics = CharField(null=True)
    price = FloatField()
    type = CharField()

    class Meta:
        db_table = 'bike_model'

class Store(BaseModel):
    address = CharField(unique=True)
    id = CharField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        db_table = 'store'

class School(BaseModel):
    address = CharField(unique=True)
    id = CharField(primary_key=True)
    name = CharField(unique=True)
    store = ForeignKeyField(db_column='store_id', rel_model=Store, to_field='id')

    class Meta:
        db_table = 'school'

class VirtualCard(BaseModel):
    deposit = FloatField(null=True)
    id = CharField(primary_key=True)
    security = IntegerField()

    class Meta:
        db_table = 'virtual_card'

class User(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    password = CharField()
    phone = IntegerField(null=True)
    school = ForeignKeyField(db_column='school_id', rel_model=School, to_field='id')
    status = CharField()
    student = CharField(db_column='student_id')
    username = CharField(unique=True)
    vc = ForeignKeyField(db_column='vc_id', null=True, rel_model=VirtualCard, to_field='id')

    class Meta:
        db_table = 'user'

class Appointment(BaseModel):
    date = DateTimeField()
    id = CharField(primary_key=True)
    model = ForeignKeyField(db_column='model_id', null=True, rel_model=BikeModel, to_field='id')
    note = CharField(null=True)
    type = CharField(null=True)
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=User, to_field='id')

    class Meta:
        db_table = 'appointment'

class Battery(BaseModel):
    date = DateTimeField()
    id = CharField(primary_key=True)
    status = CharField()

    class Meta:
        db_table = 'battery'

class Coupon(BaseModel):
    date = DateTimeField()
    description = CharField(null=True)
    id = CharField(primary_key=True)
    money = FloatField(null=True)
    name = CharField()
    type = CharField()

    class Meta:
        db_table = 'coupon'

class CustomerService(BaseModel):
    email = CharField(null=True)
    id = CharField(primary_key=True)
    name = CharField()
    phone = IntegerField(null=True)
    wechat = CharField(db_column='wechat_id', null=True)

    class Meta:
        db_table = 'customer_service'

class Ebike(BaseModel):
    id = CharField(primary_key=True)
    model = ForeignKeyField(db_column='model_id', rel_model=BikeModel, to_field='id')
    state = CharField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=User, to_field='id')

    class Meta:
        db_table = 'ebike'

class FlashCharge(BaseModel):
    battery = ForeignKeyField(db_column='battery_id', null=True, rel_model=Battery, to_field='id')
    date = DateTimeField()
    id = CharField(primary_key=True)
    status = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'flash_charge'

class History(BaseModel):
    battery = ForeignKeyField(db_column='battery_id', null=True, rel_model=Battery, to_field='id')
    bike_model = ForeignKeyField(db_column='bike_model_id', null=True, rel_model=BikeModel, to_field='id')
    ebike = ForeignKeyField(db_column='ebike_id', null=True, rel_model=Ebike, to_field='id')
    id = CharField(primary_key=True)
    operation = CharField()
    time = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=User, to_field='id')

    class Meta:
        db_table = 'history'

class MakeAppointment(BaseModel):
    a = ForeignKeyField(db_column='a_id', rel_model=Appointment, to_field='id')
    date = DateTimeField()
    u = ForeignKeyField(db_column='u_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'make_appointment'
        indexes = (
            (('a', 'u'), True),
        )
        primary_key = CompositeKey('a', 'u')

class UserCoupon(BaseModel):
    coupon = ForeignKeyField(db_column='coupon_id', rel_model=Coupon, to_field='id')
    date = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'user_coupon'
        indexes = (
            (('user', 'coupon'), True),
        )
        primary_key = CompositeKey('coupon', 'user')

