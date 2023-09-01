#! /usr/bin/env python3

from flamewok.cli import cli
from django_silly_adminplus import __version__, __home_page__

import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def plop_template():
    file = os.path.join(BASE_DIR, "plop/adminplus.html")
    cwd = os.getcwd()
    shutil.copy(file, cwd)
    print(f"template plopped in {cwd}")


def plop_adminplus():
    from_directory = os.path.join(BASE_DIR, "plop/adminplus/_adminplus")
    cwd = os.getcwd()
    shutil.copytree(
        from_directory, os.path.join(os.getcwd(), '_adminplus'))
    print(f"'_adminplus' plopped in {cwd}")


def plop_adminplus_plus():
    from_directory = os.path.join(BASE_DIR, "plop/adminplus_plus/_adminplus")
    print("=== directory :", from_directory)
    cwd = os.getcwd()
    shutil.copytree(
        from_directory, os.path.join(os.getcwd(), '_adminplus'))
    print(f"'_adminplus' (version with ConfigPlus) plopped in {cwd}")


def cmd():
    cli.route(
        "HELP",
        (["", "-h", "--help"], cli.help, "display this help"),
        "ACTIONS",
        ("plop template", plop_template, "provides a 'adminplus.html' template in the current directory"),
        ("plop adminplus", plop_adminplus, "provides the '_adminplus' django app in the current directory"),
        ("plop adminplus+", plop_adminplus_plus, "provides the '_adminplus' django app with ConfigPlus singleton in the current directory"),
        "ABOUT",
        "package: Django Silly Adminplus",
        f"version: {__version__}",
        f"home page : {__home_page__}",
    )


if __name__ == '__main__':
    cmd()
