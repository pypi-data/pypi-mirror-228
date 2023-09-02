#! /usr/bin/env python3
# coding: utf-8

"""
REMINDER:
1- build
./setup.py sdist bdist_wheel
2- basic verifications
twine check dist/*
2.5- Deploy on testpypi (optionnal, site here : https://test.pypi.org/):
twine upload --repository testpypi dist/*
3- upload to PyPi
twine upload dist/*
"""

from django_silly_adminplus import __version__, __home_page__
import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-silly-adminplus",
    version=f"{__version__}",
    description=(
        "Add quickly a new page to your admin site"
        ),
    long_description=README,
    long_description_content_type="text/markdown",
    url=__home_page__,
    author="Vincent Fabre",
    author_email="peigne.plume@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    packages=[
        "django_silly_adminplus",
        "django_silly_adminplus.management",
        "django_silly_adminplus.management.commands",
        "django_silly_adminplus.plop",
        "django_silly_adminplus.plop.adminplus",
        "django_silly_adminplus.plop.adminplus._adminplus",
        "django_silly_adminplus.plop.adminplus._adminplus.templates",
        "django_silly_adminplus.plop.adminplus._adminplus.templates._adminplus",
        "django_silly_adminplus.plop.adminplus._adminplus.templates.admin",
        "django_silly_adminplus.plop.adminplus_plus",
        "django_silly_adminplus.plop.adminplus_plus._adminplus",
        "django_silly_adminplus.plop.adminplus_plus._adminplus.management",
        "django_silly_adminplus.plop.adminplus_plus._adminplus.management.commands",
        "django_silly_adminplus.plop.adminplus_plus._adminplus.templates",
        "django_silly_adminplus.plop.adminplus_plus._adminplus.templates._adminplus",
        "django_silly_adminplus.plop.adminplus_plus._adminplus.templates.admin",
        ],
    # include_package_data=True,
    package_data={'': ['*.txt', '*.html', '*.po', '*.mo', '*.pot']},
    python_requires='>=3.7',
    # install_requires=[],
    keywords='django adminplus admin',
    # entry_points={
    #     "console_scripts": [
    #     ]
    # },
    setup_requires=['wheel'],
)
