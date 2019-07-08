"""
Setup.py for django-vega-admin
"""
from setuptools import find_packages, setup

setup(
    name="django-vega-admin",
    version=__import__("vega_admin").__version__,
    description="Simple and fast automated CRUD for any Django model",
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
)
