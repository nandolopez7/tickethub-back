import pytest
from tickethub_back.users.constants import UserConstant
from tickethub_back.users.logic.user import UserLogic
from tickethub_back.users.models.users import User


@pytest.mark.django_db
class TestUser:

    def test_user_create(self):
        count_ini = User.objects.all().count()
        data = {
            'first_name': 'Liseth',
            'last_name': 'Castillo',
            'email': 'otro@gmail.com',
            'phone_number': '3102541215',
            'identification_number': '11441234512',
            'groups': [UserConstant.ADMIN.value]
        }

        user = UserLogic.create_user(data)
        count_end = User.objects.all().count()

        assert (count_ini + 1) == count_end and isinstance(user, User)
