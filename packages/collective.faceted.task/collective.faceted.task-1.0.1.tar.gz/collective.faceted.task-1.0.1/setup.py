# -*- coding: utf-8 -*-
"""Installer for the collective.faceted.task package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='collective.faceted.task',
    version='1.0.1',
    description="Faceted tools and view for tasks",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Zope Plone',
    author='Franck NGAHA',
    author_email='franck.o.ngaha@gmail.com',
    url='http://pypi.python.org/pypi/collective.faceted.task',
    license='GPL V2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.faceted'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.task',
        'collective.eeafaceted.z3ctable',
        'eea.facetednavigation>=10.0',
        'five.grok',
        'plone.api',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
