from django.core.management import call_command


def poblar_datos_bd():
    call_command('loaddata', 'fixtures/departments.json')
    call_command('loaddata', 'fixtures/cities.json')
    call_command('loaddata', 'fixtures/groups.json')

def run():
    print(">>> Inició creacion de datos en la BD...")
    poblar_datos_bd()
    print(">>> Finalizó creación de datos en la BD.")