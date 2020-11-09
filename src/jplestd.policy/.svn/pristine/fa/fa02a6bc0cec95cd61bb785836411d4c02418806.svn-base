This is the policy package for the home website of the JPL_ Data System and
Technology Office (section 873).

The purpose of this policy is to turn an ordinary Plone_ website into the
section 873 website.

To release to pypi.jpl.nasa.gov::

    bin/buildout setup . egg_info -Rb '' sdist upload -r jpl -v

with the following in ~/.pypirc::

    [distutils]
    index-servers =
        jpl
    [jpl]
    username = jpl-username
    password = jpl-password
    repository = https://pypi.jpl.nasa.gov/simple/


.. References:
.. _JPL: http://www.jpl.nasa.gov/
.. _Plone: http://plone.org/

