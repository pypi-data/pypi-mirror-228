# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whereabouts']

package_data = \
{'': ['*'], 'whereabouts': ['queries/*']}

install_requires = \
['duckdb==0.8.1',
 'fastparquet>=2023.7.0,<2024.0.0',
 'lxml>=4.9.2,<5.0.0',
 'openpyxl>=3.1.1,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyarrow>=12.0.1,<13.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'scipy>=1.11.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'whereabouts',
    'version': '0.2.2',
    'description': '',
    'long_description': "# Whereabouts\nFast, scalable geocoding for Python using DuckDB. The geocoding algorithms are based on the following papers:\n- https://arxiv.org/abs/1708.01402\n- https://arxiv.org/abs/1712.09691\n\n## Description\nGeocode addresses and reverse geocode coordinates directly from Python in your own environment. \n- No additional database setup required. Uses DuckDB to run all queries\n- No need to send data to an external geocoding API\n- Fast (Geocode 1000s / sec and reverse geocode 200,000s / sec)\n- Robust to typographical errors\n\n\n## Requirements\n- Python 3.8+\n- Poetry (for package management)\n\n## Installation\nOnce Poetry is installed and you are in the project directory:\n\n```\npoetry shell\npoetry install\n```\n\nThe current process for using Australian data from the GNAF is as follows:\n1) Download the latest version of GNAF core from https://geoscape.com.au/data/g-naf-core/\n2) Update the `setup.yml` file to point to the location of the GNAF core file\n3) Finally, setup the geocoder. This creates the required reference tables\n\n```\npython setup_geocoder.py\n```\n\nTo use address data from another country, the file should have the following columns:\n\n| Column name | Description |\n| ----------- | ----------- |\n| ADDRESS_DETAIL_PID | Unique identifier for address |\n| ADDRESS_LABEL | The full address |\n| ADDRESS_SITE_NAME | Name of the site. This is usually null |\n| LOCALITY_NAME | Name of the suburb or locality |\n| POSTCODE | Postcode of address |\n| STATE | State \n| LATITUDE | Latitude of geocoded address |\n| LONGITUDE | Longitude of geocoded address |\n\nNote that by default the file should be pipe-separated, i.e., use '|' as the delimitor.\n\n## Examples\n\nGeocode a list of addresses \n```\nfrom whereabouts.Matcher import Matcher\n\nmatcher = Matcher(db_name='gnaf_au')\nmatcher.geocode(addresslist, how='standard')\n```\n\nFor more accurate geocoding you can use trigram phrases rather than token phrases (note that the trigram option has to have been specified in the setup.yml file as part of the setup)\n```\nmatcher.geocode(addresslist, how='trigram')\n```\n\nOnce a Matcher object is created, the KD-tree for fast geocoding will also be created. A list of latitude, longitude values can then be reverse geocoded as follows\n```\nmatcher.reverse_geocode(coordinates)\n```",
    'author': 'alex2718',
    'author_email': 'ajlee3141@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
