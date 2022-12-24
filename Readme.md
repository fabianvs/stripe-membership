# Django App

Project description

## Installation
Se recomienda usar un ambiente virtual de python como [venv](https://virtualenv.pypa.io/en/latest/) o [virtualenv](https://docs.python.org/3/library/venv.html)

Usar el gestor de paqutes [pip](https://pip.pypa.io/en/stable/) para instalar dependencias.

```bash
pip install -r requirements.txt
```

Crear migraciones de modelos de base de datos

```bash
python manage.py makemigrations
```

Crear migraciones de modelos de base de datos

```bash
python manage.py migrate
```

Cargar datos necesarios en base de datos

```bash
python manage.py loaddata db.json
```

## Usage

```python
python runserver 0.0.0.0:8000
