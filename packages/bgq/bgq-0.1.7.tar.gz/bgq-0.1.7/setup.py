# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_jobs', 'webint_jobs.templates']

package_data = \
{'': ['*']}

modules = \
['bgq']
install_requires = \
['sqlyte>=0.1.1,<0.2.0',
 'txtint>=0.1.2,<0.2.0',
 'webagt>=0.1.2,<0.2.0',
 'webint>=0.1.59,<0.2.0']

entry_points = \
{'console_scripts': ['bgq = bgq:main'], 'webapps': ['jobs = webint_jobs:app']}

setup_kwargs = {
    'name': 'bgq',
    'version': '0.1.7',
    'description': 'a simple asynchronous background job queue',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/bgq',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
