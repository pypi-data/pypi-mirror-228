# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['delta_sync']

package_data = \
{'': ['*']}

extras_require = \
{'spark': ['pyspark>=3.1.2,<3.3.0']}

entry_points = \
{'console_scripts': ['pydantic-spark = pydantic_spark.__main__:root_main']}

setup_kwargs = {
    'name': 'delta-sync',
    'version': '0.0.0',
    'description': 'Syncing delta tables',
    'long_description': '',
    'author': "Peter van 't Hof'",
    'author_email': 'pjrvanthof@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/godatadriven/pydantic-spark',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
