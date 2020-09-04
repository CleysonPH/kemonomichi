[![time tracker](https://wakatime.com/badge/github/CleysonPH/kemonomichi.svg)](https://wakatime.com/badge/github/CleysonPH/kemonomichi)
[![codecov](https://codecov.io/gh/CleysonPH/kemonomichi/branch/master/graph/badge.svg)](https://codecov.io/gh/CleysonPH/kemonomichi)

# KemonoMICHI

Projeto feito para fins de estudo, esse projeto é um gerenciador para clínicas veterinárias que permite com que os usuários possam cadastrar clientes, pets e consultas.

## Dependências de Produção

- Django
- django-adminlte2
- django-localflavor-br
- python-decouple
- dj-database-url

## Dependências de Desenvolvimento

- poetry
- black
- pytest
- pytest-django
- pytest-cov
- model_bakery

## Requisitos

- Python 3.6 ou superior

## Como testar esse projeto na minha máquina?

Clone este repositório e ente na pasta do projeto

```bash
git clone https://github.com/CleysonPH/kemonomichi.git
cd kemonomichi
```

Crie um novo ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente virtual
```bash
source .venv/bin/activate
```

Instale as dependências do projeto

```sh
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com as informações do banco de dados, use o arquivo `contrib/.env_sample` como base.

Crie o banco de dados e um usuario para acessar o sistema

```sh
python manage.py migrate
python manage.py createsuperuser
```

Execute o servidor de desenvolvimento do Django

```sh
python manage.py runserver
```

E então acessar a aplicação em http://localhost:8000/

## Como contribuir com o projeto?

Para contribuir com o projeto, faça um clone, crie um ambiente virtual com o poetry e instale as dependências de desenvolvimento

```bash
git clone https://github.com/CleysonPH/kemonomichi.git
cd kemonomichi
poetry use env 3.8
poetry shell
poetry install
```