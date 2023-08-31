# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['razorbill', 'razorbill.connectors']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.28.0,<0.29.0',
 'asyncpgsa>=0.27.1,<0.28.0',
 'fastapi-filter>=0.6.1,<0.7.0',
 'fastapi>=0.98.0,<0.99.0',
 'greenlet>=2.0.2,<3.0.0',
 'loguru>=0.7.0,<0.8.0',
 'psycopg2>=2.9.7,<3.0.0',
 'pytest-asyncio>=0.21.1,<0.22.0',
 'pytest>=7.4.0,<8.0.0',
 'sqlalchemy>=2.0.17,<3.0.0',
 'uvicorn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'razorbill',
    'version': '0.1.2',
    'description': 'Razorbill is a framework for quickly creating API applications using only the description of the data model.',
    'long_description': 'Razorbill is a framework for quickly creating API applications using only the description of the data model.',
    'author': 'Nikita Irgashev',
    'author_email': 'nik.irg@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
