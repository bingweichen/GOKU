"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for school

"""
from datetime import datetime
from server.database.model import ReportTable, User


def add(**kwargs):
    return ReportTable.create(
        date=datetime.now(),
        **kwargs
    )


def get_all(user):
    report_table = ReportTable.select().where(
        user=user
    )
    return report_table


def manager_get_all():
    report_table = ReportTable.select()
    return report_table
