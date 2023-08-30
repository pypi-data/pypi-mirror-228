# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amdgpu_stats']

package_data = \
{'': ['*']}

install_requires = \
['humanfriendly>=10.0', 'textual>=0.32.0']

entry_points = \
{'console_scripts': ['amdgpu-stats = amdgpu_stats:textual_run']}

setup_kwargs = {
    'name': 'amdgpu-stats',
    'version': '0.1.21',
    'description': 'A module/TUI for AMD GPU statistics',
    'long_description': '# amdgpu_stats\n\nA Python module/TUI for AMD GPU statistics.\nTested _only_ on `RX6000` series cards and _(less so)_ with Ryzen CPU iGPUs.\n\nPlease [file an issue](https://git.init3.us/BraveTraveler/amdgpu_stats/issues)\nif finding incompatibility!\n\n## Screenshots\n\n<details open>\n  <summary>Main screen / stats</summary>\n\n  ![Screenshot of the main stats table](https://git.init3.us/BraveTraveler/amdgpu_stats/raw/branch/master/screens/main.svg "Main screen")\n</details>\n<details>\n  <summary>Usage graphs</summary>\n\n  ![Screenshot of the \'graphing\' scroll bars](https://git.init3.us/BraveTraveler/amdgpu_stats/raw/branch/master/screens/graphs.svg "Graphs")  \n</details>\n<details>\n  <summary>Logs</summary>\n\n  ![Screenshot of the \'Logs\' tab pane](https://git.init3.us/BraveTraveler/amdgpu_stats/raw/branch/master/screens/logs.svg "Logs")\n</details>\n\n## Installation\n```bash\npip install amdgpu-stats\n```\nTo use the _TUI_, run `amdgpu-stats` in your terminal of choice. For the _module_, see below!\n\n## Module\n\nIntroduction:\n```python\nIn [1]: import amdgpu_stats.utils\n\nIn [2]: amdgpu_stats.utils.AMDGPU_CARDS\nOut[2]: {\'card0\': \'/sys/class/drm/card0/device/hwmon/hwmon9\'}\n\nIn [3]: amdgpu_stats.utils.get_core_stats(\'card0\')\nOut[3]: {\'sclk\': 640000000, \'mclk\': 1000000000, \'voltage\': 0.79, \'util_pct\': 65}\n\nIn [4]: amdgpu_stats.utils.get_clock(\'core\', format_freq=True)\nOut[4]: \'659 MHz\' \n```\n\nFor more information on what the module provides, please see:\n - [ReadTheDocs](https://amdgpu-stats.readthedocs.io/en/latest/)\n - `help(\'amdgpu_stats.utils\')` in your interpreter\n - [The module source](https://git.init3.us/BraveTraveler/amdgpu_stats/src/branch/master/src/amdgpu_stats/utils.py)\n\nFeature requests [are encouraged](https://git.init3.us/BraveTraveler/amdgpu_stats/issues) 😀\n\n## Requirements\nOnly `Linux` is supported. Information is _completely_ sourced from interfaces in `sysfs`.\n\nIt _may_ be necessary to update the `amdgpu.ppfeaturemask` parameter to enable metrics.\n\nThis is assumed present for *control* over the elements being monitored. Untested without. \n\nSee [this Arch Wiki entry](https://wiki.archlinux.org/title/AMDGPU#Boot_parameter) for context.\n',
    'author': 'Josh Lay',
    'author_email': 'pypi@jlay.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.init3.us/BraveTraveler/amdgpu_stats',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
