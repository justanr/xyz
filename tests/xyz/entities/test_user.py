from xyz.entities.user import User
from datetime import datetime


class TestUser:

    def test_initialize_user(self):
        assert User(name='fred', email='fred@fred.com',
                    password='fred', registered_at=datetime(2015, 10, 11))

    def test_register_user(self, clock):
        user = User.register(name='fred', email='fred@fred.com',
                             password='fred', registered_at=clock.now())

        assert user.registered_at == datetime(2015, 10, 11)
        assert user.name == 'fred'
        assert user.email == 'fred@fred.com'
