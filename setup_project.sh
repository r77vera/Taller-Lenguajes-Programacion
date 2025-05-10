#!/bin/bash

# Activar el entorno virtual
source ../env_rivera/bin/activate

# Migraciones de la base de datos
echo "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar el servidor de desarrollo
echo "Iniciando el servidor en http://127.0.0.1:8000/"
python manage.py runserver