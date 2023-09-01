# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metagene', 'metagene.data']

package_data = \
{'': ['*']}

install_requires = \
['Click>=8.0.0,<9.0.0',
 'asciichartpy>=1.5.25,<2.0.0',
 'gtfparse>=2.0.1,<3.0.0',
 'matplotlib>=3.0.0,<4.0.0',
 'pandas>=2.0.2,<3.0.0',
 'polars<0.16.14',
 'pyarrow>=13.0.0,<14.0.0',
 'pyranges>=0.0.117,<0.0.118',
 'ray>=2.6.3,<3.0.0',
 'rich-click>=1.6.1,<2.0.0',
 'rich>=13.5.2,<14.0.0']

entry_points = \
{'console_scripts': ['metagene = metagene.cli:cli']}

setup_kwargs = {
    'name': 'metagene',
    'version': '0.0.0.dev48',
    'description': 'Metagene Profiling Analysis and Visualization',
    'long_description': '# Metagene\n\n[![Pypi Releases](https://img.shields.io/pypi/v/metagene.svg)](https://pypi.python.org/pypi/metagene)\n[![Downloads](https://static.pepy.tech/badge/metagene)](https://pepy.tech/project/metagene)\n\n**Metagene Profiling Analysis and Visualization**\n\n(WIP)\n\n## DEMO\n\n![demo](docs/fig_metagene.svg)\n\n- example\n\n```bash\nmetagene -i metagene/data/input.bed.gz -t 10 -w 7,8,9 -n a,xxx,new -F GRCh38 -b 100 -o /dev/null -s test.tsv -p test.pdf\n```\n',
    'author': 'Ye Chang',
    'author_email': 'yech1990@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/y9c/metagene',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
