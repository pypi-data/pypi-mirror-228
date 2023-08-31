# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auxiliary', 'auxiliary.nifti', 'auxiliary.normalization']

package_data = \
{'': ['*']}

install_requires = \
['nibabel>=3.2,<4.0', 'numpy>=1.25,<2.0', 'pathlib>=1.0,<2.0']

setup_kwargs = {
    'name': 'auxiliary',
    'version': '0.0.20',
    'description': 'TODO.',
    'long_description': None,
    'author': 'Florian Kofler',
    'author_email': 'florian.kofler@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
