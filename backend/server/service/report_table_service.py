"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for school

"""
from datetime import datetime
from server.database.model import ReportTable, User


def add(**kwargs):
    return ReportTable.create(
        date=datetime.utcnow(),
        **kwargs
    )


def get_all(user):
    report_table = ReportTable.select().where(
        ReportTable.user == user
    )
    return report_table


def manager_get_all():
    report_table = ReportTable.select().order_by(ReportTable.date.desc())
    return report_table
