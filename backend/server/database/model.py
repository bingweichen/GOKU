"""

@author: Bingwei Chen

@time: 8/4/17

@desc: models

每个field 生效是要重新删表，建表

"""
import json

from peewee import *

from server.database.db import database
from server.utility.constant import *


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class BaseModel(Model):
    class Meta:
        database = database


class Store(BaseModel):
    name = CharField(unique=True, primary_key=True)
    address = CharField(unique=True)


class School(BaseModel):
    name = CharField(unique=True, primary_key=True)
    address = CharField(unique=True)
    store = ForeignKeyField(Store, related_name="schools")


# status default empty, when the e_bike is used change to full
class User(BaseModel):
    username = CharField(primary_key=True)
    password = CharField()  # change
    name = CharField()
    phone = BigIntegerField(null=True)
    school = ForeignKeyField(School, related_name='users')
    student_id = CharField(db_column='student_id')

    status = CharField(default="empty")

    # 什么效果？
    def __unicode__(self):
        return self.username


class VirtualCard(BaseModel):
    card_no = ForeignKeyField(User, primary_key=True,
                              related_name="virtual_cards")
    deposit = FloatField(default=0.0)
    balance = FloatField(default=0.0)


class ConsumeRecord(BaseModel):
    card = ForeignKeyField(VirtualCard, related_name="consume_record")
    consume_event = CharField()
    consume_date_time = DateTimeField()
    consume_fee = FloatField()
    balance = FloatField(default=0.0)


# from playhouse.postgres_ext import ArrayField
# 颜色应该是数组
class EBikeModel(BaseModel):
    # 电动车型号 model string
    name = CharField(primary_key=True)
    # 电动车类型 小龟、酷车，租车
    category = CharField()
    price = CharField()

    colors = JSONField()  # [红，蓝，绿。。。]
    # 续航
    distance = CharField()
    configure = CharField()
    battery = CharField()
    introduction = CharField(default="物品简介")
    image_urls = JSONField(default=None, null=True)

    # introduction_image_url = CharField(default=None, null=True)
    # 销售量
    num_sold = IntegerField(default=0)
    # 浏览量
    num_view = IntegerField(default=0)


# 新增库存表
class Storage(BaseModel):
    # 属于什么型号
    model = ForeignKeyField(rel_model=EBikeModel,
                            related_name="storage")
    color = CharField(max_length=5)
    # 库存量
    num = IntegerField()

    class Meta:
        primary_key = CompositeKey('model', 'color', )


# TODO 思考完模式决定一下
# 1. 车不进行录入，当生成订单时生成
# 2. 录入车辆
# 不需要 primary key, 自动生成递增id
class EBike(BaseModel):
    # 车牌号
    plate_no = CharField(primary_key=True)
    # 属于什么型号
    model = ForeignKeyField(EBikeModel, related_name='e_bikes')
    # 属于哪个用户
    user = ForeignKeyField(User, related_name='e_bikes', null=True)
    color = CharField()
    # 电动车状态 空闲，被租用
    status = CharField(default="空闲")


# 订单针对车型和颜色
class Appointment(BaseModel):
    user = ForeignKeyField(User, related_name='appointments')
    e_bike_model = ForeignKeyField(EBikeModel, related_name='appointments')
    color = CharField(max_length=5)
    # 电动车类型 小龟、酷车，租车
    category = CharField(null=True)
    # 备注
    note = CharField(null=True)
    date = DateTimeField()
    expired_date_time = DateTimeField()
    serial_number = CharField(null=True)
    # 预约金
    appointment_fee = FloatField(default=0)
    delivery = CharField(default=DELIVERY["0"])
    status = CharField(default=APPOINTMENT_STATUS["0"])


# 闪充电池出租
class Battery(BaseModel):
    # 是否被租
    on_loan = BooleanField(default=False)
    # 电池信息，比如电压、电流
    desc = CharField(null=True)
    # 租用人
    user = ForeignKeyField(User, related_name='battery', null=True)


# 闪充电池报修记录
class BatteryReport(BaseModel):
    # 电池id
    battery = ForeignKeyField(
        Battery, related_name='battery_report', null=True)
    # 当前使用人
    current_owner = ForeignKeyField(
        User, related_name='battery_report', null=True)
    # 保修单生成时间
    report_time = DateTimeField()


# 优惠券
class Coupon(BaseModel):
    # 用户
    user = ForeignKeyField(User, related_name='coupon', null=True)
    # 使用条件
    situation = FloatField(null=True)
    # 面值
    value = FloatField(null=True)
    # 到期日期
    expired = DateTimeField(null=True)
    # 状态: 可用，已使用，过期
    status = CharField(default="可用")


# 编号
class SerialNumber(BaseModel):
    code = CharField(primary_key=True)
    store = ForeignKeyField(Store)
    store_code = CharField()
    category_code = CharField()
    available = BooleanField(default=True)
    appointment = ForeignKeyField(Appointment, null=True)


table_list = [User, School, Store, VirtualCard, EBikeModel,
              Storage, EBike, Appointment, BatteryReport, Battery]

table_temp = [Appointment]


#
# import uuid
# class Test(BaseModel):
#     uuid = UUIDField(primary_key=True, default=uuid.uuid4)


def create_tables():
    """

    :return: None
    :rtype:
    """
    return database.create_tables(table_temp, safe=True)


def drop_tables():
    """

    :return: None
    :rtype:
    """
    return database.drop_tables(table_temp, safe=True)


def create_table(model):
    """

    :param model:
    :type model:
    :return: <pymysql.cursors.Cursor object at 0x108d00828>
    :rtype:
    """
    return database.create_table(model)


def drop_table(model):
    """

    :param model:
    :type model:
    :return: the cursor of the drop model
    :rtype:
    """
    return database.drop_table(model)


def recreate_tables():
    drop_tables()
    create_tables()


if __name__ == '__main__':
    pass
    # create_table(Storage)
    print(recreate_tables())
    #
