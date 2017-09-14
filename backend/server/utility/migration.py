from playhouse.migrate import *
from server.database.db import database
from server.database.model import Appointment
my_db = database
migrator = MySQLMigrator(my_db)


def migrate_script():
    with my_db.transaction():
        out_trade_no = CharField(default=None, null=True)

        # appointment = ForeignKeyField(Appointment,related_name="wx_payment",
        #                               null=True, to_field=Appointment.id)
        code = CharField(null=True)

        migrate(
            # migrator.drop_column('consumerecord', 'out_trade_no')
            migrator.add_column('wxpayment', 'code', code),
        )

if __name__ == '__main__':
    migrate_script()