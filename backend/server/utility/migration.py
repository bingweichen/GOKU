from playhouse.migrate import *
from server.database.db import database
from server.database.model import Appointment
my_db = database
migrator = MySQLMigrator(my_db)


def migrate_script():
    with my_db.transaction():
        # out_trade_no = CharField(default=None, null=True)

        real_name_authentication = CharField(
            default="未认证", choices=["已认证", "未认证"])

        migrate(
            # migrator.drop_column('consumerecord', 'out_trade_no')
            migrator.add_column('virtualcard', 'real_name_authentication', real_name_authentication),
        )

if __name__ == '__main__':
    migrate_script()