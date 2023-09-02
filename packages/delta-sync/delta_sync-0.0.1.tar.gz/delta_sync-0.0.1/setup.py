# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['delta_sync']

package_data = \
{'': ['*']}

install_requires = \
['delta-spark>=2.4.0,<3.0.0']

extras_require = \
{'spark': ['pyspark>=3.4.0,<3.5.0']}

setup_kwargs = {
    'name': 'delta-sync',
    'version': '0.0.1',
    'description': 'Syncing delta tables',
    'long_description': '# Delta Sync\n\n**This package is not ready to use, still in development**\n\nThis package will contain methods to sync delta table. It will use\n\n\n### Example\n\n```python\nfrom delta import DeltaTable\n\nfrom delta_sync import sync_table\n\nsource_table = DeltaTable.forName("<source table name>")\noutput_table = DeltaTable.forName("<output table name>")\nstatus_table = DeltaTable.forName("<status table name>")\n\nsync_table(source_table, output_table, status_table)\n```\n\n\n### Install\n\n##### pip\n```shell\npip install delta-sync\n```\n\n##### poetry\n```shell\npoetry add delta-sync\n```\n',
    'author': "Peter van 't Hof'",
    'author_email': 'pjrvanthof@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffinfo/delta-sync',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
