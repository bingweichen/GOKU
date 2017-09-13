from playhouse.migrate import *
from server.database.db import database

my_db = database
migrator = MySQLMigrator(my_db)


def migrate_script():
    with my_db.transaction():
        out_trade_no = CharField(default=None, null=True)

        migrate(
            # migrator.drop_column('consumerecord', 'out_trade_no')
            migrator.add_column('virtualcard', 'out_trade_no', out_trade_no),
        )

if __name__ == '__main__':
    migrate_script()