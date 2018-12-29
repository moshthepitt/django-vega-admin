"""
Setup.py for django-vega-admin
"""
from setuptools import setup, find_packages

setup(
    name='django-vega-admin',
    version=__import__('vega_admin').__version__,
    description='Simple and fast automated CRUD for any Django model',
    license='MIT',
    author='Kelvin Jayanoris',
    author_email='kelvin@jayanoris.com',
    url='https://github.com/moshthepitt/django-vega-admin',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'Django >= 2.0',
        'django-crispy-forms',
        'django-braces',
        'django-filter',
        'django-tables2',
        'tablib',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
