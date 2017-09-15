class Error(Exception):
    pass


class PasswordError(Exception):
    pass


class NoStorageError(Exception):
    pass


class WrongSerialsNumber(Exception):
    pass


class ErrorMessage(Exception):
    did_not_return_battery = "还未归还电池"
    battery_already_rented = "电池已被租用"
    pass


class VirtualCardErrorMessage(Exception):
    no_enough_deposit = "押金不足"
    no_enough_balance = "余额不足"
    abnormal_situation = "账户异常"
    virtual_card_no_exist = "虚拟消费卡未开通"

