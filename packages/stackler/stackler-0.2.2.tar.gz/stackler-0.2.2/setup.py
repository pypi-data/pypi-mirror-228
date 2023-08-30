# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stackler']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.27',
 'ansiwrap>=0.8.4,<0.9.0',
 'click==8.1.3',
 'humanize>=4.3.0,<5.0.0',
 'phabricator==0.9.1',
 'pyperclip>=1.8.2,<2.0.0',
 'termcolor==1.1.0',
 'typer==0.6.1',
 'wcwidth>=0.2.5,<0.3.0']

entry_points = \
{'console_scripts': ['stackler = stackler.main:app']}

setup_kwargs = {
    'name': 'stackler',
    'version': '0.2.2',
    'description': '',
    'long_description': '# Stackler\n\nWorking with Phabricator Stack has never been so easy.\n\n```\n$ stackler submit -m "rebase msg"\nBy continuing, this script will:\nUpdate D157389 with [24a42cd9 1/3 Add Framework], message: rebase msg.\nUpdate D157390 with [67cfa09f 2/3 Add UI], message: rebase msg.\nSubmit [7bc9760d 3/3 Add API] based on [67cfa09f 2/3 Add the UI framework fo...].\n```\n\n* Display the working stack\n* Submit/Update all the commits into a Phabricator Stack\n* Wrap around `git rebase <sha>^` to allow easy mid-stack edit\n\n# Install\n\n## With [`pipx`](https://pypa.github.io/pipx/)\n```\n# get pipx, which runs a pip command easily\nbrew install pipx\npipx ensurepath\n\n# use pipx to install stackler\npipx install stackler\n```\n\n## Manual Install\n```\n# install from pip\npip3 install --user stackler\n```\n\nIf your path isn\'t setup to work with pip already, as in if you see \n> WARNING: The script stackler is installed in `<pip-path>` which is not on PATH.\n\nYou need to add the pip executable path to your `$PATH`. Here are some examples:\n\n* bash\n  \n  ```\n  echo -n \'PATH="$(python3 -m site --user-base)/bin:${PATH}"\' >> ~/.bash_profile\n  ```\n\n* zsh\n  \n  ```\n  echo -n \'PATH="$(python3 -m site --user-base)/bin:${PATH}"\' >> ~/.zshrc\n  ```\n\n# Develop\n\n## Roadmap\n\n- [ ] Arc land Improvements\n  - [x] Add the ability to `arc diff --create`\n  - [x] Landing on custom base / target `arc land --onto`\n- [ ] Complex Repo Support\n  - [x] Exit gracefully when `.arcconfig` is not found\n  - [ ] Support config file to point to `.arcconfig`\n- [ ] Environment Precheck\n  - [ ] Have a setup / doctor command to check environment setup\n- [x] Test and make sure the branches created by `arc work` work\n  - [x] Submission by multiple people on custom base\n- [x] Edit the stack (wrap around `git rebase -i`)\n  - [x] Wrap around `git rebase -i <target>^` to start the work of editing one commit\n  - [x] Wrap around `git rebase --continue` to complete the edit action\n- [x] Basic functionality (submit the stack and chain the diffs)\n- [x] Print the stack\n- [x] Gracefully land \n  - [x] Pull and rebase before landing\n  - [x] Wrap around `arc land`\n  - [x] reset head after calling land\n\n## Setup Enviornment\n```\npoetry install\npoetry config virtualenvs.in-project true\npoetry shell\n```\n Make sure you use the Python in the virtual environment setup by `poetry`. In\n VS Code, use ⌘⇧P and enter Select Interpreter, then pick the one with python.\n\n## Linter and Formatter\n\nAs specified in the [VS Code setting file\n(`.vscode/settings.json`)](.vscode/settings.json), this project uses\n[pylint](https://pypi.org/project/pylint/) for linting and\n[autopep8](https://pypi.org/project/autopep8/) for auto formatting.\n\n\n# Publish\n\n> This is mostly an excerpt from [Typer CLI\'s publish documentataion](https://typer.tiangolo.com/tutorial/package/).\n\n## Add PyPI API Token (Once)\n* Gain access to the PyPI project.\n* Generate a token from https://pypi.org/manage/account/token/.\n* Add the token to poetry.\n```\npoetry config pypi-token.pypi <pypi api token>\n```\n\n## Publish to PyPI\n* Make sure you bump the version.\n* Publish.\n```\npoetry publish --build\n```',
    'author': 'Modun',
    'author_email': 'modun@xiaohongshu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
