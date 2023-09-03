# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autograder',
 'autograder.plagiarism_detection',
 'autograder.plagiarism_detection.lexers',
 'autograder.testcase_types.cpython',
 'autograder.testcase_types.cpython.helpers',
 'autograder.testcase_types.cpython.templates',
 'autograder.testcase_types.cpython.templates.tests.testcases',
 'autograder.testcase_types.gcc',
 'autograder.testcase_types.javac',
 'autograder.testcase_utils']

package_data = \
{'': ['*'],
 'autograder.testcase_types.cpython.templates': ['tests/output/*'],
 'autograder.testcase_types.gcc': ['c++_templates/*',
                                   'c++_templates/tests/output/*',
                                   'c++_templates/tests/testcases/*',
                                   'c_templates/*',
                                   'c_templates/tests/output/*',
                                   'c_templates/tests/testcases/*',
                                   'helpers/*',
                                   'memleak/*'],
 'autograder.testcase_types.javac': ['extra/*',
                                     'helpers/*',
                                     'templates/*',
                                     'templates/tests/output/*',
                                     'templates/tests/testcases/*']}

install_requires = \
['antlr4-python3-runtime==4.9.2',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.22.4,<2.0.0',
 'tomlkit>=0.11.4,<0.12.0']

entry_points = \
{'console_scripts': ['autograder = autograder.__main__:main']}

setup_kwargs = {
    'name': 'autograder',
    'version': '3.7.6',
    'description': 'A simple, secure, and versatile way to automatically grade programming assignments',
    'long_description': '<p align="center">\n  <a href="https://ovsyanka83.github.io/autograder/"><img src="https://raw.githubusercontent.com/Ovsyanka83/autograder/main/docs/_media/logo_with_text.svg" alt="AutoGrader"></a>\n</p>\n<p align="center">\n  <b>A simple, secure, and versatile way to automatically grade programming assignments</b>\n</p>\n\n---\n\n<p align="center">\n<a href="https://github.com/ovsyanka83/autograder/actions?query=workflow%3ATests+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/Ovsyanka83/autograder/actions/workflows/test.yaml/badge.svg?branch=main&event=push" alt="Test">\n</a>\n<a href="https://codecov.io/gh/ovsyanka83/autograder" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/ovsyanka83/autograder?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/autograder/" target="_blank">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/autograder?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/autograder/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/autograder?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n## Features\n\n* Blazingly fast (can grade hundreads of submissions using dozens of testcases in a few minutes. Seconds if grading python)\n* [Easy to grade](https://ovsyanka83.github.io/autograder/#/?id=usage)\n* [Easy-to-write testcases](https://ovsyanka83.github.io/autograder/#/?id=writing-testcases)  \n* Testcase grade can be based on [student\'s stdout](https://ovsyanka83.github.io/autograder/#/?id=helper-functions)\n* Can grade C, C++, Java, and Python code in regular mode\n* Can grade any programming language in stdout-only mode\n* A file with testcase grades and details can be generated for each student\n* You can customize the total points for the assignment, maximum running time of student\'s program, file names to be considered for grading, formatters for checking student stdout, and [so much more](https://github.com/Ovsyanka83/autograder/blob/master/autograder/default_config.toml).\n* [Anti Cheating capabilities](https://ovsyanka83.github.io/autograder/#/?id=anti-cheating) that make it nearly impossible for students to cheat\n* Grading submissions in multiple programming languages at once\n* JSON result output supported if autograder needs to be integrated as a part of a larger utility\n* Can check submissions for similarity (plagiarism)\n* Can detect and report memory leaks in C/C++ code\n\n## Installation\n\n* Run `pip install autograder`\n* To grade various programming languages, you\'d need to install:\n  * `gcc`/`clang` for C/C++ support\n  * `Java JDK` for java support\n  * `make` for compiled stdout-only testcase support\n  * Any interpreter/compiler necessary to run stdout-only testcases. For example, testcases with ruby in their shebang lines will require the ruby interpreter\n\n### Updates\n\n`pip install -U --no-cache-dir autograder`\n\n## Quickstart\n\n* Run `autograder guide path/to/directory/you\'d/like/to/grade`. The guide will create all of the necessary configurations and directories for grading and will explain how to grade.\n* Read the [usage](https://ovsyanka83.github.io/autograder/#/?id=usage) section of the docs\n\n## Supported Platforms\n\n* Linux is fully supported\n* OS X is fully supported\n* Windows is partially supported:\n  * Stdout-testcases that require shebang lines are not and cannot be supported\n\n## Supported Programming Languages\n\n* Java\n* C\n* C++\n* CPython (3.8-3.11)\n* Any programming language if stdout-only grading is used\n',
    'author': 'Stanislav Zmiev',
    'author_email': 'zmievsa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ovsyanka83/autograder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
