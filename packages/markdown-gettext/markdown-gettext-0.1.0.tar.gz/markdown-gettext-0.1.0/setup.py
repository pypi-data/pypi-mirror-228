# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_gettext',
 'markdown_gettext.extraction',
 'markdown_gettext.generation']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'Pygments>=2.16.1,<3.0.0',
 'markdown-it-py[plugins]>=3.0.0,<4.0.0',
 'polib>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['markdown-gettext = markdown_gettext.cli:main',
                     'md-gettext = markdown_gettext.cli:main']}

setup_kwargs = {
    'name': 'markdown-gettext',
    'version': '0.1.0',
    'description': 'Markdown i18n with gettext',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>\nSPDX-License-Identifier: CC-BY-SA-4.0\n-->\n\n# markdown-gettext\n\nMarkdown i18n with gettext.\n\nCommonMark compliant. All core Markdown elements are supported, as well as\nfront matter, table, and definition list.\n\nThe package can be used as a command line program to do i18n and l10n for\nindividual Markdown files, and as a library to make larger programs. \n\n## Install\n\n```bash\npip install markdown-gettext\n```\n\n## Usage as a command line program\n_("Usage as a library" in Development section)_\n\nYou can use either `md-gettext` or `markdown-gettext` command\n\n#### Extraction\n```\nmd-gettext extract [-p PACKAGE] [-r REPORT_ADDR] [-t TEAM_ADDR] md pot\n\npositional arguments:\n  md                    path of the Markdown file to extract messages from\n  pot                   path of the POT file to create\n\noptional arguments:\n  -p PACKAGE, --package PACKAGE\n                        the package name in POT metadata\n  -r REPORT_ADDR, --report-addr REPORT_ADDR\n                        the report address in POT metadata\n  -t TEAM_ADDR, --team-addr TEAM_ADDR\n                        the team address in POT metadata\n```\n\n#### Generation\n```\nmd-gettext generate [-l LANG] in-md po out-md\n\npositional arguments:\n  in-md                 path of the source Markdown file\n  po                    path of the PO file containing translations\n  out-md                path of the Markdown file to create\n\noptional arguments:\n  -l LANG, --lang LANG  language of translations\n```\n\n## Notes\n\nSome notes about how different elements are handled:\n- Inlines: newlines and consecutive spaces are not kept;\n- Content of each HTML block isn\'t parsed into finer tokens but processed\nas a whole;\n- Fenced code blocks: only `//` comments are processed;\n\n## Development\n\n### Environment\n\n- With Conda\n\n```bash\nconda env create -f environment.yml\nconda activate mg\npoetry install\n```\n\n### Usage as a library\n\n#### Extraction\n- Subclass `DomainExtractionProtocol`, implement\n`DomainExtractionProtocol.render_front_matter`\n- Subclass `RendererMarkdownI18N`\n\n#### Generation\n- Subclass `DomainGenerationProtocol`, implement\n`DomainGenerationProtocol.render_front_matter`\n- Subclass `RendererMarkdownL10N`',
    'author': 'Phu Hung Nguyen',
    'author_email': 'phuhnguyen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phunh/markdown-gettext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
