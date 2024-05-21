# Docker Compose


Construir proyecto

```
docker-compose build
```


Crear migraciones

```
docker-compose run --rm django python manage.py makemigrations

docker-compose run --rm django python manage.py migrate
```

Crear superusuario

```
docker-compose run --rm django python manage.py createsuperuser
```


Crear datos iniciales en la BD

```
docker-compose run --rm django python manage.py runscript poblar_bd
```

Ejecutar proyecto

```
docker-compose up
```

Ejecutar pruebas

```
docker-compose run --rm django pytest
```


# Entornos virtuales

Crear entorno vitual linux

```
python3 -m venv venv
source venv/bin/activate

```
Crear entorno vitual en Window

```
python3 -m venv venv
.\venv\Scripts\Activate
```

Instalar librerías desde un archivo

    pip install -r requirements/base.txt

Crear migraciones

    python3 manage.py makemigrations

    python3 manage.py migrate

Crear super usuario

    python3 manage.py createsuperuser

Crear datos iniciales en la BD

    python3 manage.py runscript poblar_bd

Ejecutar proyecto

    python3 manage.py runserver
