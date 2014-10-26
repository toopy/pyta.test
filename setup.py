# -*- coding: utf-8 -*-
"""Python packaging."""
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

NAME = u'pyta.test'
DESCRIPTION = u'Funky functional test tool for UIX team.'
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(os.path.dirname(here), 'VERSION')).read().strip()
PACKAGES = ['pyta_test']
REQUIREMENTS = [
    'pytest-xdist',
    'pytest-splinter'
]
ENTRY_POINTS = {}
AUTHOR = u'Florent Pigout'
EMAIL = u'florent@toopy.org'
URL = u'https://github.com/toopy/pyta_test'
CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Programming Language :: Python :: 2.7']
KEYWORDS = []


if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=README,
        classifiers=CLASSIFIERS,
        keywords=' '.join(KEYWORDS),
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license = 'MIT',
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        install_requires=REQUIREMENTS,
        entry_points=ENTRY_POINTS
    )
