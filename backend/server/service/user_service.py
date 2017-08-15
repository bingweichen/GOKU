"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for user

1. user Add/Get/Modify/Remove


"""
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from playhouse.shortcuts import model_to_dict

from server.utility.exception import PasswordError

from server.database.model import User
from server.service import virtual_card_service


def add(username, password, **kwargs):
    """

    eg = {
    "username": "bingwei",
    "password": "123456",
    "name": "bing",
    "phone": "11",
    "school": "123",
    "status": "1",
    "student_id": "11"
    }

    :param username:
    :type username:
    :param password:
    :type password:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    hashed_password = generate_password_hash(password)
    user = User.create(username=username, password=hashed_password, **kwargs)
    return model_to_dict(user)


def get(*query, **kwargs):
    user = User.get(*query, **kwargs)
    return model_to_dict(user)


def get_all():
    users = User.select()
    new_users = []
    for user in users:
        new_users.append(model_to_dict(user))
    return new_users


def get_by_username(username):
    return model_to_dict(User.get(User.username == username))


def login(username, password):
    user = User.get(User.username == username)
    if check_password_hash(user.password, password):
        return model_to_dict(user)
    raise PasswordError("error password")


def create_virtual_card(**kwargs):
    virtual_card = virtual_card_service.add(**kwargs)
    return virtual_card


# ***************************** test ***************************** #
def add_test():
    result = add(username="bingwei111", password="123456",
                 name='陈炳蔚', phone=15988731660,
                 school="2",
                 student_id="123434")
    print(result)


def add_test1():
    result = User.create(username="bingwei111", password="123456",
                         name='陈炳蔚', phone=15988731660,
                         school="2",
                         student_id="123434")
    print(result)


def remove_test():
    pass


def add_template():
    template_json = [
        # {
        #     "username": 'bingwei',
        #     "password": "123456",
        #     "name": "陈炳蔚",
        #     "phone": 15988731660,
        #     "school": "浙江大学",
        #     "student_id": "12358"
        # },
        {
            "username": 'Shuo_Ren',
            "password": "123456",
            "name": "Ren",
            "phone": 15701683747,
            "school": "浙江大学",
            "student_id": "00001"
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)

# ***************************** unit test ***************************** #
if __name__ == '__main__':
    pass
    # add_template()
    print(get_all())
