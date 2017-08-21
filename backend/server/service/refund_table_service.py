"""

@author: Bingwei Chen

@time: 8/17/17

@desc: 退款表格

"""
from server.database.model import RefundTable


def get_all(username=None):
    if username:
        refund_table = RefundTable.select().where(
            user=username
        )
        return refund_table
    refund_table = RefundTable.select()
    return refund_table


def modify_status(refund_table_id, status):
    refund_table = RefundTable.get(id=refund_table_id)
    refund_table.status = status
    return refund_table.save()


def add(**kwargs):
    return RefundTable.create(**kwargs)
