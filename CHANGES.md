CHANGES
=======

4.0b3
==========
- Add Python 3.13, drop EOL Python 3.8 ([#245](https://github.com/mozilla/django-csp/pull/245))
- docs: Fix trusted_types links ([#250](https://github.com/mozilla/django-csp/pull/250))
- Add `EXCLUDE_URL_PREFIXES` check ([#252](https://github.com/mozilla/django-csp/pull/252))
- Support CSP configuration as sets ([#251](https://github.com/mozilla/django-csp/pull/251))
- docs: Note that reporting percentage needs rate limiting middleware ([#256](https://github.com/mozilla/django-csp/pull/256))
* Document constant NONE vs Python's None ([#255](https://github.com/mozilla/django-csp/pull/255))
- Raise error when nonce accessed after response ([#258](https://github.com/mozilla/django-csp/pull/258))
- Test on Django 5.2 ([#261](https://github.com/mozilla/django-csp/pull/261))

4.0b2
=====
- Add type hints. ([#228](https://github.com/mozilla/django-csp/pull/228))
- Expand ruff configuration and move into pyproject.toml [[#234](https://github.com/mozilla/django-csp/pull/234)]
- Documentation fixes by jamesbeith and jcari-dev
- Simplify middleware logic ([#226](https://github.com/mozilla/django-csp/pull/226))
- Report percentage of 100% should always send CSP report ([#236](https://github.com/mozilla/django-csp/pull/236))
- Changes to make `CSPMiddleware` easier to subclass ([#237](https://github.com/mozilla/django-csp/pull/237))
- Change `REPORT_PERCENTAGE` to allow floats (e.g. for values < 1%) ([#242](https://github.com/mozilla/django-csp/pull/242))
- Add Django 5.1 support ([#243](https://github.com/mozilla/django-csp/pull/243))

4.0b1
=====
BACKWARDS INCOMPATIBLE changes:
- Move to dict-based configuration which allows for setting policies for both enforced and
  report-only. See the migration guide in the docs for migrating your settings.
- Switch from specifying which directives should contain the nonce as a separate list, and instead
  use a sentinel `NONCE` in the directive itself.

Other changes:
- Add pyproject-fmt to pre-commit, and update pre-commit versions
- Fixes #36: Add support for enforced and report-only policies simultaneously
- Drop support for Django <=3.2, end of extended support
- Add CSP keyword constants in `csp.constants`, e.g. to replace `"'self'"` with `SELF`

3.8
===

Please note: this release folds in a number of fixups, upgrades and documentation tweaks,
but is functionally the same as 3.7. New features will come with 3.9+

- Update Python syntax for modern versions with pyupgrade
- Drop support for EOL Python <3.8 and Django <2.2 version; add support up to Django 5 on Python 3.12
- Switch to ruff instead of pep8 and flake8
- Move from CircleCI to Github Actions for CI
- Add support for using pre-commit with the project
- Remove deprecation warning for child-src
- Fix capturing brackets in script template tags
- Update docs to clarify when nonce will not be added to headers
- Move from setup.py and setup.cfg to pyproject.toml (#209)

Note: identical other than release packaging to 3.8rc1

3.8rc1
======
- Move from setup.py and setup.cfg to pyproject.toml (#209)

3.8rc
=====

Please note: this release folds in a number of fixups, upgrades and documentation tweaks,
but is functionally the same as 3.7. New features will come with 3.9+

- Update Python syntax for modern versions with pyupgrade
- Drop support for EOL Python <3.8 and Django <2.2 version; add support up to Django 5 on Python 3.12
- Switch to ruff instead of pep8 and flake8
- Move from CircleCI to Github Actions for CI
- Add support for using pre-commit with the project
- Remove deprecation warning for child-src
- Fix capturing brackets in script template tags
- Update docs to clarify when nonce will not be added to headers

3.7
===

- Add support for Trusted Types
- Use 128 bits base64 encoded for nonce

3.6
===

- Add support/testing for Django 2.2 and 3.0
- Add support/testing for Python 3.7 and 3.8
- Disable CSP for Django NotFound debug view
- Add new headers used in CSP level 3
- Add support for the report-to directive

3.5
===

- New RateLimitedCSPMiddleware middleware (#97)
- Add support for csp nonce and "script" template tag. (#78)
- Various smaller fixes along the way

3.4
===

- Remove support for Django 1.6 and 1.7 as they're out of life
- Adds pypy3, Django 2.0.x and current Django master to our CI tests
- Allow removing directives using @csp_replace
- Add CSP nonce support

3.3
===

- Add support for Django 1.11
- Add support for Python 3.6

3.2
===

- Add manifest-src fetch directive - <https://w3c.github.io/webappsec-csp/#directive-manifest-src>
- Add worker-src fetch directive - <https://w3c.github.io/webappsec-csp/#directive-worker-src>
- Add plugin-types document directive - <https://w3c.github.io/webappsec-csp/#directive-plugin-types>
- Add require-sri-for <https://www.w3.org/TR/CSP/#directives-elsewhere> - <https://w3c.github.io/webappsec-subresource-integrity/#request-verification-algorithms>
- Add upgrade-insecure-requests - <https://w3c.github.io/webappsec-upgrade-insecure-requests/#delivery>
- Add block-all-mixed-content - <https://w3c.github.io/webappsec-mixed-content/>
- Add deprecation warning for child-src (#80)

3.1
===

- Add support for Django 1.10 middlewares
- Allow lazy objects to be assigned to CSP_REPORT_URI

v3.0
====

- Add support for Python 3 and PyPy
- Move to pytest for testing
- Add wheel build support
- Drops support for Django < 1.6, adds support for Django 1.6, 1.7, 1.8 and 1.9
- Remove leftover references to the old report processing feature (#64)
- Fix accidental mutation of config (#52)

Please note that this is a big release that touches quite a few parts so please
make sure you're testing thoroughly and report any issues to
<https://github.com/mozilla/django-csp/issues>

v2.0.3
======

- Disable CSP on built-in error pages.

v2.0.1 & v2.0.2
===============

No changes. I just can't package Python files.

v2.0
====

- Dropped report processing feature and code.
- Complies with CSP v1.0 and v1.1 (excluding experimental features).
- Dropped support for X-Content-Security-Policy and X-WebKit-CSP
  headers.
