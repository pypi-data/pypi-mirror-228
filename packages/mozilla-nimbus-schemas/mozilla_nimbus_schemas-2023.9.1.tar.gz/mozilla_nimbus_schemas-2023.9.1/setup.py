# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozilla_nimbus_schemas',
 'mozilla_nimbus_schemas.jetstream',
 'mozilla_nimbus_schemas.tests.jetstream']

package_data = \
{'': ['*']}

install_requires = \
['polyfactory>=2.7.2,<3.0.0', 'pydantic>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'mozilla-nimbus-schemas',
    'version': '2023.9.1',
    'description': 'Schemas used by Mozilla Nimbus and related projects.',
    'long_description': '# Nimbus Schemas\n\nThis directory contains a package of schemas published to various repositories for use by different parts of the Mozilla Nimbus experimentation ecosystem.\n\n\n## Installation/Usage\n### Prerequisites\n- python ^3.10\n- poetry ^1.2.2\n- node ^16\n- yarn ^1.22\n\n#### Common Operations\nFrom project root (i.e., parent to this directory)\n- Install: `make schemas_install`\n- Run linting and tests: `make schemas_check`\n- Code formatting: `make schemas_code_format`\n\n#### Building Python Schemas Package\n`make schemas_build`\n\n#### Building Typescript Schemas Package\n`make schemas_build_npm`\n\n## Schemas\n### Jetstream\n\nContains schemas describing analysis results, metadata, and errors from [Jetstream](https://github.com/mozilla/jetstream).\n\n\n## Deployment\nThe build and deployment occurs automatically through CI. A deployment is triggered on merges into the `main` branch when the version number changes. Schemas are published to various repos for access in different languages.\n\n#### Versioning\n`mozilla-nimbus-schemas` uses a date-based versioning scheme (`CalVer`). The format is `yyyy.m.MINOR`, where `m` is the non-zero-padded month, and `MINOR` is an incrementing number starting from 1 for each month. Notably, this `MINOR` number does NOT correspond to the day of the month. For example, the second release in June of 2023 would have a version of `2023.6.2`.\n\n#### Version Updates\n1. To update the published package versions, update the `VERSION` file in this directory.\n  - From the project root, you can run the helper script:\n    - `./scripts/set_schemas_version.sh <version>`\n  - Or write to the file:\n    - `echo <version> > ./schemas/VERSION`\n  - Or simply edit the file in any text editor.\n2. Update the package versions with the new VERSION file:\n  - `make schemas_version`\n\n### Python\nPublished to PyPI as `mozilla-nimbus-schemas`\n\n### Typescript\nPublished to NPM as `@mozilla/nimbus-schemas`\n\n### Rust\nNot yet implemented.\n',
    'author': 'mikewilli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
