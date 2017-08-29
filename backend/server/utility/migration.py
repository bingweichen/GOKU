from playhouse.migrate import *
from server.database.db import database

my_db = database
migrator = MySQLMigrator(my_db)


def migrate_script():
    with my_db.transaction():
        admin_field = BooleanField(default=False)
        migrate(
            migrator.add_column('user', 'admin', admin_field),
        )

if __name__ == '__main__':
    migrate_script()