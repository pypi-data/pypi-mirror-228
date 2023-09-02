# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betternot']

package_data = \
{'': ['*']}

install_requires = \
['astroplan>=0.9',
 'astropy>=5.0,<6.0',
 'backoff>=1.10.0,<2.0.0',
 'importlib-metadata>=6.7.0',
 'keyring>=23.7.0,<24.0.0',
 'matplotlib>=3.5.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.2.5',
 'pypeit>=1.13.0,<2.0.0',
 'requests>=2.23.0',
 'ztfquery>=1.20.0']

entry_points = \
{'console_scripts': ['not = main:run']}

setup_kwargs = {
    'name': 'betternot',
    'version': '0.1.0',
    'description': 'Toolset for interacting with the Nordic Optical Telescope (NOT)',
    'long_description': '# betterNOT\nToolset for preparing observations with the Nordic Optical Telescope (NOT). Currently only set up to work with ZTF transients. You need [Fritz](https://fritz.science) credentials.\n\nThe observability code is largely based on the [`NOT Observing Tools`](https://github.com/steveschulze/NOT_Observing_Tools) by Steve Schulze.\n\nNote the [observation guidelines](https://notes.simeonreusch.com/s/dHt_0XzwQ#)\n\n## Installation\nSimply run `pip install betternot`.\n\nIf you want to make local changes, clone the repository, `cd` into it and issue `poetry install`.\n\n## Usage\n### Prepare observations\nThe observation planning can be run with a command line interface. Simply issue\n```\nnot ZTF23changeit ZTF23thistoo ...\n```\nThis will generate a standard star observability plot, create an observability plot for all ZTF objects, download the finding charts for them from Fritz and print the coordinates as well as the last observed magnitude. They will all end up in the `betternot/DATE` directory. \n\nOptionally, you can specify a desired date with `-date YYYY-MM-DD` (the default is today). You can also specify a telescope site with `-site SITE` (available sites are listed [here](https://github.com/astropy/astropy-data/blob/gh-pages/coordinates/sites.json)). Default is the NOT site (Roque de los Muchachos).\n\n### Uploading spectra to WISeREP\nYou will need a [TNS](https://www.wis-tns.org) and [WISeREP](https://www.wiserep.org) bot token for this. Uploading spectra can be done as follows:\n\n```python\nimport logging\nfrom betternot.wiserep import Wiserep\n\nlogging.basicConfig()\nlogger = logging.getLogger()\nlogger.setLevel(logging.DEBUG)\n\nWiserep(\n    ztf_id="ZTF23aaawbsc",\n    spec_path="ZTF23aaawbsc_combined_3850.ascii",\n    sandbox=True,\n    quality="high", # "low", "medium" or "high". Default: "medium"\n)\n```\nThis will check TNS if an IAU object exists at the ZTF transient location, open the spectrum, extract the metadata, and upload the file to WISeREP as well as a report containing the extracted metadata.\n\nAfter checking with the [WISeREP sandbox](https://sandbox.wiserep.org) that everything works fine, use `sandbox=False`',
    'author': 'simeonreusch',
    'author_email': 'simeon.reusch@desy.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
