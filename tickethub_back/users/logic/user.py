
from typing import Dict

from tickethub_back.users.models.users import User


class UserLogic:

    @classmethod
    def create_user(cls, data: Dict) -> User:
        groups_data = data.pop('groups')
        user_permissions_data = data.pop('user_permissions', [])
        data['password'] = str(data.get('password'))

        user = User.objects.create(**data)
        user.set_password(data['password'])
        user.save()

        if not isinstance(groups_data, list):
            groups_data = [groups_data]
        user.groups.set(groups_data)
        user.user_permissions.set(user_permissions_data)
        return user
