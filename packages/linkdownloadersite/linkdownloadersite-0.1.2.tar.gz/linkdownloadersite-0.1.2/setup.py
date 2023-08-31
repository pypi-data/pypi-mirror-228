# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkdownloadersite']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.3.3,<3.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'linkdownloadersite',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'asaunde78',
    'author_email': 'saundersasher78@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
