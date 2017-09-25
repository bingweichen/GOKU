"""

"""
from datetime import datetime, timedelta
import time

import sys

sys.path.append("../../")

from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict
from server.database.model import create_tables
from server.database.model import BatteryRecord

from server.service import user_service
from server.service import battery_record_service
from server.service import virtual_card_service


def db_create():
    pass


def db_migrate():
    pass


def db_upgrade():
    pass


def db_downgrade():
    pass


def create_database_tables():
    return create_tables()


def check_battery_record_script():
    while 1:
        print("check time", datetime.utcnow())
        check_battery_record()
        time.sleep(600)


def check_battery_record():
    """
    实现还电池后2h未借电池, 冻结账户

    实现租用电池超过 一个月，冻结账户


    :return:
    :rtype:
    """
    # 获取所有用户
    users = user_service.get_all()
    for user in users:
        # 获取用户虚拟卡, 不存在或账号已冻结，跳过检查
        try:
            virtual_card = virtual_card_service.get(card_no=user.username)
            if virtual_card.situation == "冻结":
                continue
        except DoesNotExist:
            continue

        try:
            # 用户最近一条记录
            battery_record = BatteryRecord.select().where(
                BatteryRecord.user==user
            ).order_by(BatteryRecord.id.desc()).get()

            # 2h未借电池 TODO 暂时关闭
            if battery_record.situation == '已归还':
                now = datetime.utcnow()
                delta = now - battery_record.return_date
                if delta > timedelta(hours=2):
                    # 冻结账户
                    result = virtual_card_service.freeze(user, "2h未借电池")
                    print("result", result)

            # 租用电池超过一个月
            if battery_record.situation == '借用中':
                now = datetime.utcnow()
                delta = now - battery_record.rent_date
                if delta > timedelta(days=30):
                    # 冻结账户
                    result = virtual_card_service.freeze(user, "电池租用超一月")
                    print("result", result)

        except DoesNotExist:
            # print(DoesNotExist)
            pass

        # # 租用电池超过一个月
        # try:
        #     # 用户最近一条记录
        #     battery_record = BatteryRecord.select().where(
        #         BatteryRecord.user==user
        #     ).order_by(BatteryRecord.id.desc()).get()
        #
        #     if battery_record.situation == '借用中':
        #         now = datetime.utcnow()
        #         delta = now - battery_record.rent_date
        #         if delta > timedelta(days=30):
        #             # 冻结账户
        #             result = virtual_card_service.freeze(user, "电池租用超一月")
        #             print("result", result)
        # except DoesNotExist:
        #     pass


if __name__ == '__main__':
    # my_t()
    print(check_battery_record_script())
