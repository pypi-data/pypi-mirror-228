# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['craterslab']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.13.1,<3.0.0',
 'matplotlib>=3.7.2,<4.0.0',
 'numpy>=1.24.0,<2.0.0',
 'opencv-python>=4.8.0,<5.0.0',
 'scikit-learn>=1.3.0,<2.0.0',
 'scipy>=1.11.1,<2.0.0',
 'tensorflow>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'craterslab',
    'version': '0.2.4',
    'description': '',
    'long_description': '# Craters Morphology Analysis Tool\n\nA library to simplify the analysis of crater data from depth maps.\n\n## Installation\n\nCraterslab requires Python 3.10+ for functioning. Make sure you have a compliant version of [python](https://www.python.org/downloads/) installed in your system.\n\n### Installing craterslab from pypi using pip (Recommended)\n\n\nCraterslab is also available from pypi. You can install it by running:\n\n```\n$ pip install craterslab\n```\n\nWe strongly encourage users using this method to create a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) before installing the library.\n\n### Installing craterslab from the repository using poetry \nMake sure you have [poetry](https://python-poetry.org/docs/) in your system and then run:\n\n```\n$ git clone https://github.com/gvieralopez/craterslab.git\n$ cd craterslab\n$ poetry install\n$ poetry shell\n```\n\nThese will create and activate an isolated virtual environment with craterslab installed on it. \n\n## Usage\n\nYou can find some examples on how to use the library in this repository:\n\n```\n$ git clone https://github.com/gvieralopez/craterslab.git\n$ cd craterslab/examples\n```\n\nBefore executing any example, you will need to download data from actual craters using the provided scripts:\n\n```\n$ python download_data.py\n```\n\nThen, you can execute any given example as:\n\n```\n$ python example1.py\n```\n\nSee [software documentation](https://craterslab.readthedocs.io/en/latest/) for more details.\n\n',
    'author': 'Gustavo Viera López',
    'author_email': 'gvieralopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gvieralopez/craters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
