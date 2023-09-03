# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newapi']

package_data = \
{'': ['*']}

install_requires = \
['pydantic==2.3']

setup_kwargs = {
    'name': 'newapi',
    'version': '0.1.0',
    'description': 'Api framework from scratch',
    'long_description': None,
    'author': 'Johannes',
    'author_email': 'joh@nnes.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
