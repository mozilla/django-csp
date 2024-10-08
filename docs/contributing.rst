.. _contributing-chapter:

============
Contributing
============

Patches are more than welcome! You can find the issue tracker `on GitHub
<https://github.com/mozilla/django-csp/issues>`_ and we'd love pull
requests.

Setup
=====
To install all the requirements (probably into a virtualenv_):

.. code-block:: bash

    pip install -e .
    pip install -e ".[dev]"

This installs:

* All the text requirements
* All the typing requirements
* pre-commit_, for checking styles
* tox_, for running tests against multiple environments
* Sphinx_ and document building requirements

Style
=====

Patches should follow PEP8_ and should not introduce any new violations
as detected by the ruff_ tool.

To help stay on top of this, install pre-commit_, and then run ``pre-commit install-hooks``. Now you'll be set up
to auto-format your code according to our style and check for errors for every commit.

Tests
=====

Patches fixing bugs should include regression tests (ideally tests that
fail without the rest of the patch). Patches adding new features should
test those features thoroughly.

To run the tests, install the requirements (probably into a virtualenv_):

.. code-block:: bash

    pip install -e .
    pip install -e ".[tests]"

Then just `pytest`_ to run the tests:

.. code-block:: bash

    pytest

To run the tests with coverage and get a report, use the following command:

.. code-block:: bash

    pytest --cov=csp --cov-config=.coveragerc

To run the tests like Github Actions does, you'll need pyenv_:

.. code-block:: bash

    pyenv install 3.9 3.10 3.11 3.12 pypy3.9 pypy3.10
    pyenv local 3.9 3.10. 3.11 3.12 pypy3.9 pypy3.10
    pip install -e ".[dev]"  # installs tox
    tox                # run sequentially
    tox run-parallel   # run in parallel, may cause issues on coverage step
    tox -e 3.12-4.2.x  # run tests on Python 3.12 and Django 4.x
    tox --listenvs     # list all the environments

Type Checking
=============

New code should have type annotations and pass mypy_ in strict mode. Use the
typing syntax available in the earliest supported Python version 3.9.

To check types:

.. code-block:: bash

    pip install -e ".[typing]"
    mypy .

If you make a lot of changes, it can help to clear the mypy cache:

.. code-block:: bash

    mypy --no-incremental .

Updating Documentation
======================

To rebuild documentation locally:

.. code-block:: bash

    pip install -e ".[dev]"
    cd docs
    make html
    open _build/html/index.html  # On macOS

.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _mypy: https://mypy.readthedocs.io/en/stable/
.. _pre-commit: https://pre-commit.com/#install
.. _pyenv: https://github.com/pyenv/pyenv
.. _pytest: https://pytest.org/latest/usage.html
.. _ruff: https://pypi.org/project/ruff/
.. _tox: https://tox.wiki/en/stable/
.. _virtualenv: http://www.virtualenv.org/
