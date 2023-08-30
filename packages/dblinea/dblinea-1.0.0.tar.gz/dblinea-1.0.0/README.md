# LIneA Database Library

---

[![Python package](https://github.com/linea-it/dblinea/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/linea-it/dblinea/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/dblinea/badge/?version=latest)](https://dblinea.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/linea-it/dblinea/badge.svg?branch=main)](https://coveralls.io/github/linea-it/dblinea?branch=main)



Python library to access LIneA's database from Python code.
Useful to retrieve data inside LIneA's JupyterHub platform.

## Authors

* [@glaubervila](https://github.com/glaubervila)
* [@gschwend](https://www.github.com/gschwend)

## Installation

Install **dblinea** with pip

```bash
  pip install dblinea
```

## Requirements

* sqlalchemy>=1.4.25
* psycopg2>=2.9.1
* numpy>=1.19.4
* pandas>=1.2.0
* astropy>=5.0.0

```bash
pip install sqlalchemy psycopg2 numpy pandas astropy
```

## Future plans

Sub-package to allow users to send user-generated data products to LIneA Science Server (e.g., a list of targets for visual inspection).

### Development

Python 3.8: <https://tecadmin.net/install-python-3-8-ubuntu/>

* Dependencias:

```bash
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev liblzma-dev
```

```bash
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

```bash
pip install wheel setuptools twine pytest pytest-runner pytest-cov black
```

Executar os testes:

```bash
python setup.py pytest --cov --cov-report term-missing --cov-report html
```

Fazer o Build: <https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f>

```bash
python setup.py sdist bdist_wheel
```

### Testando o pacote apos o build

```bash
python3.8 -m venv venv
source venv/bin/activate
```

```bash
pip install sqlalchemy psycopg2 numpy pandas astropy
```

Para instalar usando o pacote local

```bash
pip install --force-reinstall <path>/dist/wheelfile.whl
```

Abrir um terminal e importar a classe DBBase. ou utilizar o comando.

```bash
python -c 'from dblinea import DBBase'
```

Outro Teste

```bash
(env) glauber: ~ $ python
Python 3.8.12 (default, Jan 28 2022, 15:50:21)
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from dblinea import DBBase
>>> a = DBBase()
>>> a.get_engine()
Engine(postgresql+psycopg2://untrustedprod:***@desdb4.linea.gov.br:5432/prod_gavo)
>>>

```

### Publish in PyPi Test

Check if build is ok for publish

```bash
python -m twine check dist/*
```

```bash
python -m twine upload --verbose --repository testpypi dist/*
```

Check in <https://test.pypi.org/manage/project/dblinea/releases/>

### Publish in PyPi Oficial

<https://realpython.com/pypi-publish-python-package/>

```bash
twine upload dist/*
```

Executar o Lint em busca de errors de sintaxe ou formatação.

```bash
black . --check
```

Executar o Lint para corrigir automaticamente os errors encontrados.

```bash
black .
```

<!-- ```bash
flake8 . --count  --max-complexity=10 --max-line-length=127 --statistics
``` -->

### Documentation with sphinx

Generate Api Docs

```bash
cd docs
sphinx-apidoc -f -o ./source ../dblinea
```

Build html docs

```bash
make html
```

# TODO: Trocar Coveralls por codecov <https://about.codecov.io/>
