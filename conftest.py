import pytest
from django.core.management import call_command
from django.conf import settings


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):

    settings.DATABASES['default']

    with django_db_blocker.unblock():
        call_command('loaddata', 'fixtures/groups.json')
        call_command('loaddata', 'fixtures/departments.json')
        call_command('loaddata', 'fixtures/cities.json')