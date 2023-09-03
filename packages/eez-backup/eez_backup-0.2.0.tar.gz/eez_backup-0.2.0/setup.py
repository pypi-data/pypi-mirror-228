# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eez_backup']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'frozendict>=2.3.4,<3.0.0',
 'pydantic>=2.3.0,<3.0.0',
 'rich>=13.5.2,<14.0.0']

entry_points = \
{'console_scripts': ['backup = eez_backup.__main__:cli']}

setup_kwargs = {
    'name': 'eez-backup',
    'version': '0.2.0',
    'description': 'Another convenience wrapper for _restic_',
    'long_description': "# eez-backup\n\nAnother convenience wrapper for [_restic_](https://restic.net/).\n\n## Install\n\nYou can simply install `eez-backup` from PyPI via\n\n```bash\npython -m pip install eez-backup\n```\n\n## Setup\n\n`eez-backup` assumes `backup.yml` to be present in your home directory, thus create it.\nYou can use [`tests/demo/config.yml`](./tests/demo/config.yml) as a template.\n\nNow, you can initialize the _restic_ repositories by running\n\n```bash\nbackup repo-map init\n```\n\n... and then back up your data by running\n\n```bash\nbackup run\n```\n\nThat's it!\n\n## CLI interface\n\n```text\nusage: backup [-h] [-v] [-c] [-r] [-p] {run,repo-map,profile-map} ...\n\nAnother convenience wrapper for restic\n\npositional arguments:\n  {run,repo-map,profile-map}\n                        commands\n    run                 run backup and forget for all profiles\n    repo-map            run any restic command for all given repositories\n    profile-map         run any restic command for all given profiles\n\noptions:\n  -h, --help            show this help message and exit\n  -v, --verbose         log level (disables progress bars if set)\n  -c , --config         config file to use, default is ~/.backup.yml\n  -r , --repository     repository to use, use all repositories by default, can be used multiple times\n  -p , --profile        profile to use, use all profiles by default, can be used multiple times\n```\n\n(`backup --help`)\n\n### Glossary\n\n- **Repositories:** refer to a target locations for your backups and map 1:1 to [_restic_ repositories](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html).\n- **Profiles:** define a set of directories/files to be in-/excluded from a backup among other options. Per profile and\n  backup a [snapshot](https://restic.readthedocs.io/en/stable/040_backup.html) is created.\n\n",
    'author': '0b11001111',
    'author_email': '19192307+0b11001111@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/0b11001111/eez-backup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
