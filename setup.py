"""
Setup.py for django-vega-admin
"""
import os
import sys

from setuptools import find_packages, setup

import vega_admin

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

if sys.argv[-1] == "publish":
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/* --skip-existing")
    print("You probably want to also tag the version now:")
    print(
        f"  git tag -a {vega_admin.__version__} -m 'version {vega_admin.__version__}'"
    )
    print("  git push --tags")
    sys.exit()

setup(
    name="django-vega-admin",
    version=vega_admin.__version__,
    description="Simple and fast automated CRUD for any Django model",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Kelvin Jayanoris",
    author_email="kelvin@jayanoris.com",
    url="https://github.com/moshthepitt/django-vega-admin",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=[
        "Django >=2.1.10",
        "django-crispy-forms",
        "django-braces",
        "django-filter",
        "django-tables2",
        "tablib",
        "pyyaml>=4.2b1",  # fixes security vulnerability
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
    ],
    include_package_data=True,
)
