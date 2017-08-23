"""

@author: Bingwei Chen

@time: 8/4/17

@desc: models

每个field 生效是要重新删表，建表

"""
import json

from peewee import *

from server.database.db import database
from server.utility.constant.basic_constant import DELIVERY, APPOINTMENT_STATUS


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class BaseModel(Model):
    class Meta:
        database = database


class Const(BaseModel):
    key = CharField(primary_key=True)
    value = JSONField()


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
    school = ForeignKeyField(School, related_name='users')
    student_id = CharField(db_column='student_id')  # 学号
    phone = BigIntegerField(unique=True, null=True)
    identify_number = CharField(unique=True)  # 身份证号

    we_chat_id = CharField()  # 微信号
    account = CharField()  # 退款账号
    account_type = CharField()  # 账号类型

    status = CharField(default="empty")  # 租用状态

    # 什么效果？
    def __unicode__(self):
        return self.username


class VirtualCard(BaseModel):
    card_no = ForeignKeyField(
        User, primary_key=True, related_name="virtual_cards")
    deposit = FloatField(default=0.0)
    balance = FloatField(default=0.0)
    situation = CharField(default="正常")  # 冻结


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

    category = CharField()  # 电动车类别：小龟，酷车，闪车，MINI租
    type = CharField()  # 电动车类型：买车，租车
    price = JSONField()  # 价格
    colors = JSONField()  # [红，蓝，绿。。。]
    distance = CharField()  # 续航
    configure = CharField()  # 配置
    battery = CharField()  # 电池规格

    image_urls = JSONField(default=None, null=True)  # 轮播图
    introduction_image_urls = JSONField(default=None, null=True)  # 介绍图
    introduction = CharField(default="物品简介")  # 文字介绍

    num_sold = IntegerField(default=0)  # 销售量
    num_view = IntegerField(default=0)  # 浏览量


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
    category = CharField()  # 电动车类别：小龟，酷车，闪车，MINI租
    type = CharField()  # 电动车类型：买车，租车

    note = CharField(null=True)  # 备注
    date = DateTimeField()  # 生成日期
    expired_date_time = DateTimeField()  # 有效期限
    serial_number = CharField(null=True)  # 车序列号

    rent_time_period = CharField()  # 租期：学期，年
    end_time = DateTimeField()  # 租用结束日期

    price = FloatField()  # 最终价格

    reduced_price = FloatField(null=True)  # 优惠价格

    appointment_fee = FloatField(default=0)  # 预约金
    rent_deposit = FloatField(default=0)  # 租车押金

    appointment_fee_needed = \
        FloatField(default=Const.get(
                key="DEFAULT_APPOINTMENT_FEE").value)  # 需要的预约金

    rent_deposit_needed = \
        FloatField(default=Const.get(
            key="RENT_DEPOSIT").value)  # 需要的押金

    delivery = CharField(default=DELIVERY["0"])
    status = CharField(default=APPOINTMENT_STATUS["0"])


# 闪充电池 出租
class Battery(BaseModel):
    serial_number = CharField(primary_key=True)
    # 电池信息，比如电压、电流
    desc = CharField(null=True)
    # 是否被租
    on_loan = BooleanField(default=False)
    # 租用人
    user = ForeignKeyField(User, related_name='battery', null=True)


# 闪充电池租用记录
class BatteryRecord(BaseModel):
    user = ForeignKeyField(User)
    battery = ForeignKeyField(Battery, related_name="battery_records")
    rent_date = DateTimeField()
    return_date = DateTimeField()
    price = FloatField(default=0)
    situation = CharField(default="借用中")  # 借用中，已归还


# 闪充电池报修记录
class BatteryReport(BaseModel):
    # 电池id
    battery = ForeignKeyField(
        Battery, related_name='battery_report', null=True)
    # 当前使用人
    current_owner = ForeignKeyField(
        User, related_name='battery_report', null=True)
    report_time = DateTimeField()  # 保修单生成时间
    # reporter = ForeignKeyField(User, related_name=)


# 优惠券模版
class CouponTemplate(BaseModel):
    # 优惠劵描述
    desc = CharField()
    # 使用条件
    situation = FloatField(null=True, default=0)
    # 面值
    value = FloatField()
    # 有效期
    duration = IntegerField(null=True)


# 优惠券
class Coupon(BaseModel):
    # 优惠劵描述
    desc = CharField()
    # 用户
    user = ForeignKeyField(User, related_name='coupon', null=True)
    # 使用条件
    situation = FloatField(null=True, default=0)
    # 面值
    value = FloatField()
    # 到期日期
    expired = DateTimeField(null=True)
    # 状态: 可用，已使用，过期
    status = CharField(default="可用")
    # 模版编号
    template_no = ForeignKeyField(CouponTemplate, related_name='coupon',
                                  null=True)


# 编号
class SerialNumber(BaseModel):
    code = CharField(primary_key=True)
    store = ForeignKeyField(Store)
    store_code = CharField()
    category_code = CharField()
    available = BooleanField(default=True)
    appointment = ForeignKeyField(Appointment, null=True)
    battery = ForeignKeyField(Battery, null=True)


# 退款表格
class RefundTable(BaseModel):
    user = ForeignKeyField(User)
    account = CharField()  # 退款账号
    account_type = CharField()  # 账号类型
    type = CharField()  # 退款类型：退预约金，退虚拟卡押金
    value = FloatField()  # 退款金额
    date = DateTimeField()  # 日期
    comment = CharField(null=True)  # 备注
    status = CharField(default="未处理")  # 状态：已退款


# 报修表格 电动车点击报修
class ReportTable(BaseModel):
    appointment = ForeignKeyField(Appointment)
    user = ForeignKeyField(User)
    address = CharField()  # 报修地址
    comment = CharField()
    phone = BigIntegerField(null=True)
    date = DateTimeField()


table_list = [User, School, Store, VirtualCard, EBikeModel,
              Storage, EBike, Appointment, BatteryReport, Battery, SerialNumber]

table_temp = [SerialNumber]


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
