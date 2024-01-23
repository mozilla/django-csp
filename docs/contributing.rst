.. _contributing-chapter:

============
Contributing
============

Patches are more than welcome! You can find the issue tracker `on GitHub
<https://github.com/mozilla/django-csp/issues>`_ and we'd love pull
requests.


Style
=====

Patches should follow PEP8_ and should not introduce any new violations
as detected by the ruff_ tool.


Tests
=====

Patches fixing bugs should include regression tests (ideally tests that
fail without the rest of the patch). Patches adding new features should
test those features thoroughly.

To run the tests, install the requirements (probably into a virtualenv_)::

    pip install -e .
    pip install -e .[tests]

Then just `pytest`_ to run the tests::

    pytest


.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _ruff: https://pypi.org/project/ruff/
.. _virtualenv: http://www.virtualenv.org/
.. _pytest: https://pytest.org/latest/usage.html
