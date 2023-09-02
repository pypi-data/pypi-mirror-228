.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/collective/collective.linkconsentinfo/workflows/Plone%20package/badge.svg
    :target: https://github.com/collective/collective.linkconsentinfo/actions

.. image:: https://coveralls.io/repos/github/collective/collective.linkconsentinfo/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.linkconsentinfo?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/collective.linkconsentinfo.svg
    :target: https://pypi.python.org/pypi/collective.linkconsentinfo/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.linkconsentinfo.svg
    :target: https://pypi.python.org/pypi/collective.linkconsentinfo
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.linkconsentinfo.svg?style=plastic   :alt: supported - Python versions


==========================
collective.linkconsentinfo
==========================

A consent info page for Plone Links, which allows you to show a custom info message before the user open's the link.

Features
--------

- LinkConsentInfo behavior, add's a checkbox to enable a consent info page for a link object
- Prevent redirection when link consent info is enabled
- Control panel to define a custom html text to show to the user, before she follows the link

.. image:: https://github.com/collective/collective.linkconsentinfo/raw/main/docs/link-consent-info.gif

.. image:: https://github.com/collective/collective.linkconsentinfo/raw/main/docs/link_consent_info_controlpanel.png


Translations
------------

This product has been translated into

- English
- German


Installation
------------

Install collective.linkconsentinfo by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.linkconsentinfo


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.linkconsentinfo/issues
- Source Code: https://github.com/collective/collective.linkconsentinfo

Author
------

Maik Derstappen [MrTango] - `Derico <https://derico.de>`_


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
