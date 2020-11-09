# encoding: utf-8

from setuptools import setup, find_packages
import os.path

# Package data
# ------------

_name        = 'jplestd.theme'
_version     = '1.0.1'
_description = 'Look and feel for the intranet of Section 873 at JPL'
_url         = 'http://pypi.python.org/pypi/jplestd.theme'
_downloadURL = 'http://oodt.jpl.nasa.gov/dist/jplestd'
_author      = 'Sean Kelly'
_authorEmail = 'sean.kelly@jpl.nasa.gov'
_license     = 'Proprietary'
_namespaces  = ['jplestd']
_zipSafe     = False
_keywords    = 'web zope plone theme nasa caltech jpl 873'
_extras = {
    'test': ['plone.app.testing'],
}
_entryPoints = {
    'z3c.autoinclude.plugin': ['target=plone'],
}
_requirements = [
    'setuptools',
    'jpl.ngtheme',
    'z3c.jbot',
    'Plone',
]
_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Plone',
    'Intended Audience :: Science/Research',
    'License :: Other/Proprietary License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Setup Metadata
# --------------

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = _header + '\n\n' + _read('README.txt') + '\n\n' + _read('docs', 'INSTALL.txt') + '\n\n' \
    + _read('docs', 'HISTORY.txt') + '\n\n' + _read('docs', 'LICENSE.txt')
open('doc.txt', 'w').write(_longDescription)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    download_url=_downloadURL,
    entry_points=_entryPoints,
    extras_require=_extras,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages(exclude=['ez_setup']),
    url=_url,
    version=_version,
    zip_safe=_zipSafe,
)
