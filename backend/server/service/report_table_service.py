"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for school

"""
from datetime import datetime
from server.database.model import ReportTable


def add(**kwargs):
    return ReportTable.create(
        date=datetime.now(),
        **kwargs
    )


def get_all():
    report_table = ReportTable.select(
        ReportTable.user,
        ReportTable.id,
        ReportTable.comment,
        ReportTable.address,
        ReportTable.phone,
        ReportTable.date,
    )
    return report_table
