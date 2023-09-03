# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['image_empty_space_cropper']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=10.0.0,<11.0.0', 'loguru>=0.7.0,<0.8.0', 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['iesc = image_empty_space_cropper.main:typer_main']}

setup_kwargs = {
    'name': 'image-empty-space-cropper',
    'version': '0.1.1',
    'description': 'contact me at @zalexit',
    'long_description': '# Image Empty Space Cropper\n\nRemove empty space from image',
    'author': 'Alexander Zakharov',
    'author_email': 'zah4job@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
