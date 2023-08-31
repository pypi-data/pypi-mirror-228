# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anno3d',
 'anno3d.annofab',
 'anno3d.annofab.specifiers',
 'anno3d.kitti',
 'anno3d.model',
 'anno3d.util']

package_data = \
{'': ['*']}

install_requires = \
['annofabapi>=0.65.0',
 'boto3>=1.17.20,<2.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'fire>=0.3.1,<0.4.0',
 'more-itertools>=8.5.0,<9.0.0',
 'numpy>=1.23.0,<2.0.0',
 'scipy>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['anno3d = anno3d.app:main']}

setup_kwargs = {
    'name': 'annofab-3dpc-editor-cli',
    'version': '0.2.1',
    'description': 'Annofabの3次元プロジェクトを操作するためのCLIです。',
    'long_description': '# annofab-3dpc-editor-cli\nAnnofabの3次元プロジェクトを操作するためのCLIです。\n\n[![Build Status](https://app.travis-ci.com/kurusugawa-computer/annofab-3dpc-editor-cli.svg?branch=master)](https://app.travis-ci.com/kurusugawa-computer/annofab-3dpc-editor-cli)\n[![PyPI version](https://badge.fury.io/py/annofab-3dpc-editor-cli.svg)](https://badge.fury.io/py/annofab-3dpc-editor-cli)\n[![Python Versions](https://img.shields.io/pypi/pyversions/annofab-3dpc-editor-cli.svg)](https://pypi.org/project/annofab-3dpc-editor-cli)\n[![Documentation Status](https://readthedocs.org/projects/annofab-3dpc-editor-cli/badge/?version=latest)](https://annofab-3dpc-editor-cli.readthedocs.io/ja/latest/?badge=latest)\n\n\n\n## Install\n\n```\n$ pip install annofab-3dpc-editor-cli\n```\n\n## コマンドサンプル\nhttps://annofab-3dpc-editor-cli.readthedocs.io/ja/latest/user_guide/command_sample.html 参照\n\n\n### バージョンの確認方法\n\n```\n$ anno3d version\nannofab-3dpc-editor-cli 0.2.1\n```\n\n--------------\n## 開発環境\n\n * poetry\n     * Poetry version 1.0.5\n * python 3.8\n \n \n### 開発環境初期化\n\npoetryのインストール手順は、このファイル下部の`poetryのインストール手順`を参照\n\n```\npoetry install\n```\n\n\n\n## poetryのインストール手順\n\n\npoetryのインストール手順一例を以下に示す  \n2020/05/21 ubuntu 18.04 にて確認\n\nローカルの環境に以下の手順でインストールする以外に，\npython 3.8 および poetry の導入がなされた `docker/Dockerfile` を用いても良い．\n\n### pyenv\n\nシステムにpython 3.8を直接インストールして使うなら`pyenv`は要らない\n\n```\nsudo apt-get update\n\nsudo apt-get install build-essential libssl-dev zlib1g-dev libbz2-dev \\\nlibreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \\\nxz-utils tk-dev libffi-dev liblzma-dev python-openssl git\n```\n\n```\ncurl https://pyenv.run | bash\n``` \n\nコンソールに、以下のような設定すべき内容が出力されるので`.bashrc`などに設定\n\n```\nexport PATH="/home/vagrant/.pyenv/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)"\n```\n\n```\npyenv install 3.8.3\npyenv global 3.8.3\n```\n\n### pipx\n\n直接 poetry をインストールするなら要らない\n\n```\npython -m pip install --user pipx\npython -m pipx ensurepath\n```\n\ncompletionを効かせたいときは、`pipx completions` の実行結果に従って設定する\n\n```\n$ pipx completions\n\nAdd the appropriate command to your shell\'s config file\nso that it is run on startup. You will likely have to restart\nor re-login for the autocompletion to start working.\n\nbash:\n    eval "$(register-python-argcomplete pipx)"\n\nzsh:\n    To activate completions for zsh you need to have\n    bashcompinit enabled in zsh:\n\n    autoload -U bashcompinit\n    bashcompinit\n\n    Afterwards you can enable completion for pipx:\n\n    eval "$(register-python-argcomplete pipx)"\n\ntcsh:\n    eval `register-python-argcomplete --shell tcsh pipx`\n\nfish:\n    register-python-argcomplete --shell fish pipx | .\n```\n\n### poetry\n\n```\npipx install poetry\npoetry completions bash | sudo tee /etc/bash_completion.d/poetry.bash-completion\n```\n\n## PyPIへの公開\n\n```\n$ make publish\n```\n\n\n',
    'author': 'Kurusugawa Computer Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kurusugawa-computer/annofab-3dpc-editor-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
