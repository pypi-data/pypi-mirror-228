# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tum_esm_lowcost_metadata']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['deepdiff>=6.3.0,<7.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'tum-esm-utils>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'tum-esm-lowcost-metadata',
    'version': '0.4.0',
    'description': "Single source of truth for ESM's lowcost measurement logistics",
    'long_description': '# Lowcost Metadata\n\nThis repository handles the metadata around the lowcost sensor network in Munich.<br/>\nWe selected this format over putting it in a database due to various reasons:\n\n-   Easy to read, modify and extend by selective group members using GitHub permissions\n-   Changes to this are more obvious here than in database logs\n-   Versioning (easy to revert mistakes)\n-   Automatic testing of the files integrities\n-   Easy import as a statically typed Python library\n\n<br/>\n\n## What does this data look like?\n\nThere is a set of **`JSON`** files in the data folder holding the follwing information:\n\n- **`SENSORS.json`**<br/>\nThis files contains basic information about the sensors in use in the monitoring network.\n```json\n{\n    "13077": {\n        "sensor_type": "LP8",\n        "sensor_make": "Decentlab",\n        "sensor_model": "DL-LP8",\n        "start_up_date": "2022-08-01T08:00:00+00:00",\n        "shut_down_date": null,\n        "comment": ""\n    },\n}\n```\n- **`SITES.json`**<br/>\nThis file contains basic information about the sites/locations where sensors have been installed.\n\n```json\n{\n    "FREV": {\n        "site_type": "individual",\n        "site_lat": 48.1615591,\n        "site_lon": 11.5860387,\n        "elevation": 514,\n        "comment": "Lamp post ids:55.0"\n    },\n}\n```\n- **`SAMPLING.json`**<br/>\nThis file contains basic information on which site, at which time, which sensors measured at which configuration.\n\n```json\n[\n    {\n        "site_id": "HANV",\n        "sensor_ids": [\n            13171,\n            13147\n        ],\n        "sampling_start": "2023-05-02T12:30+02:00",\n        "sampling_end": null,\n        "orientation": 0,\n        "elevation_ag": 3,\n        "comment": ""\n    },\n]\n```\n\n<br/>\n\n## How to add new measurement days?\n\n1. Possibly add new sensor in `data/SENSORS.json`\n2. Possibly add new site in `data/SITES.json`\n2. Add a new sampling event to `data/SAMPLING.json`\n\n<br/>\n\n## How can I know whether my changes were correct?\n\nWhenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed [here](https://github.com/tum-esm/lowcost-metadata/actions).\n\nA list of all integrity checks can be found in [`tests/README.md`](https://github.com/tum-esm/lowcost-metadata//tree/main/tests).\n\n<br/>\n\n## How to use it in your codebase?\n\n1. Install python library\n\n```bash\npoetry add tum_esm_lowcost_metadata\n# or\npip install tum_esm_lowcost_metadata\n```\n\n2. Create a personal access token for a GitHub account that has read access to the metadata repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\n\n3. Use the metadata anywhere\n\n```python\nimport tum_esm_lowcost_metadata\n\nlowcost_metadata_interface = tum_esm_lowcost_metadata.load_from_github(\n    github_repository = "org-name/repo-name",\n    access_token = "ghp_..."\n)\n\nmetadata = lowcost_metadata_interface.get(\n    sensor_id = "13077", date = pendulum.datetime(2023, 6, 6)\n)  # is of type list[tum_esm_lowcost_metadata.types.SensorDataContext]\n\nmetadata = interface.get(sensor_id = \'13155\', timestamp=pendulum.datetime(2023, 6, 6))\ninterfaces.print_beautiful(metadata))\n```\n\n... prints out:\n\n```\nMetadata for Sensor 13155, located at MOSV.\n---\nSensor type:            Decentlab DL-LP8\nSite coordinates:       48.1870436 lat\n                        11.5622708 lon\n                        508.0 m a.s.l.\nOrientation             0.0°\nElevation above ground: 3.0 m\nComment:                Lamp post ids:32.0\n\n---\n```\n\n<br/>\n\n## For Developers: Publish the Package to PyPI\n\n```bash\npoetry build\npoetry publish\n```\n',
    'author': 'Moritz Makowski',
    'author_email': 'moritz.makowski@tum.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tum-esm/lowcost-metadata',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
