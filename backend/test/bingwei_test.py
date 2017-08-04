import sys
# sys.path.insert(0, '..')
sys.path.append("../")

from server.service import user_service
# from server.database import create_table

from server.database.user import initialize

if __name__ == '__main__':
    pass
    # initialize()
    # user_service.add_user("bingwei11", 123456, {"student_id": "1111", "phone": "1111"})
    user_service.get_users_list()
    pass