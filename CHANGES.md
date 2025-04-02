CHANGES
=======

4.0
===

This release contains several breaking changes. For a complete migration guide, see:
https://django-csp.readthedocs.io/en/latest/migration-guide.html

## Breaking Changes

- **Configuration Format**: Moved to dict-based configuration which allows for setting policies for
both enforced and report-only. Instead of using individual settings with `CSP_` prefixes, you now
use dictionaries called `CONTENT_SECURITY_POLICY` and/or `CONTENT_SECURITY_POLICY_REPORT_ONLY`.
([#219](https://github.com/mozilla/django-csp/pull/219))

  You can use Django's check command to automatically identify existing CSP settings and generate a
  template for the new configuration format:

  ```
  python manage.py check
  ```

  This will detect your old `CSP_` prefixed settings and output a draft of the new dict-based
  configuration, giving you a starting point for migration.

  **Example:**

  Change from:
  ```python
  CSP_DEFAULT_SRC = ["'self'", "*.example.com"]
  CSP_SCRIPT_SRC = ["'self'", "js.cdn.com/example/"]
  CSP_IMG_SRC = ["'self'", "data:", "example.com"]
  CSP_EXCLUDE_URL_PREFIXES = ["/admin"]
  ```

  to:
  ```python
  from csp.constants import SELF

  CONTENT_SECURITY_POLICY = {
      "DIRECTIVES": {
          "default-src": [SELF, "*.example.com"],
          "script-src": [SELF, "js.cdn.com/example/"],
          "img-src": [SELF, "data:", "example.com"],
      },
      "EXCLUDE_URL_PREFIXES": ["/admin"],
  }
  ```

- **Nonce Configuration**: Switched from specifying directives that should contain nonces as a
separate list to using a sentinel `NONCE` value in the directive itself.
([#223](https://github.com/mozilla/django-csp/pull/223))

  **Example:**

  Change from:
  ```python
  CSP_INCLUDE_NONCE_IN = ['script-src', 'style-src']
  ```

  to:
  ```python
  from csp.constants import NONCE, SELF

  CONTENT_SECURITY_POLICY = {
      "DIRECTIVES": {
          "script-src": [SELF, NONCE],
          "style-src": [SELF, NONCE],
      }
  }
  ```

- **Nonce Behavior**: Changed how `request.csp_nonce` works - it is now Falsy
(`bool(request.csp_nonce)`) until it is read as a string (e.g., used in a template or with
`str(request.csp_nonce)`). Previously, it always tested as `True`, and testing generated the nonce.
([#270](https://github.com/mozilla/django-csp/pull/270))

  **Before:**
  ```python
  # The nonce was generated when this was evaluated
  if request.csp_nonce:
      # Do something with nonce
  ```

  **After:**
  ```python
  # This won't generate the nonce, and will evaluate to False until nonce is read as a string
  if request.csp_nonce:
      # This code won't run until nonce is used as a string

  # To generate and use the nonce
  nonce_value = str(request.csp_nonce)
  ```

- Dropped support for Django ≤3.2.
- Dropped support for Python 3.8.

## New Features and Improvements

- **Dual Policy Support**: Added support for enforced and report-only policies simultaneously using
the separate `CONTENT_SECURITY_POLICY` and `CONTENT_SECURITY_POLICY_REPORT_ONLY` settings.

  **Example:**
  ```python
  from csp.constants import NONE, SELF

  # Enforced policy
  CONTENT_SECURITY_POLICY = {
      "DIRECTIVES": {
          "default-src": [SELF, "cdn.example.net"],
          "frame-ancestors": [SELF],
      },
  }

  # Report-only policy (stricter for testing)
  CONTENT_SECURITY_POLICY_REPORT_ONLY = {
      "DIRECTIVES": {
          "default-src": [NONE],
          "script-src": [SELF],
          "style-src": [SELF],
          "report-uri": "https://example.com/csp-report/",
      },
  }
  ```

- **CSP Constants**: Added CSP keyword constants in `csp.constants` (e.g., `SELF` instead of
`"'self'"`) to minimize quoting mistakes and typos.
([#222](https://github.com/mozilla/django-csp/pull/222))

  **Example:**

  Change from:
  ```python
  CSP_DEFAULT_SRC = ["'self'", "'none'"]
  ```

  to:
  ```python
  from csp.constants import SELF, NONE

  CONTENT_SECURITY_POLICY = {
      "DIRECTIVES": {
          "default-src": [SELF, NONE],  # No need to worry about quoting
      }
  }
  ```

- Added comprehensive type hints. ([#228](https://github.com/mozilla/django-csp/pull/228))
- Added `EXCLUDE_URL_PREFIXES` check not a string. ([#252](https://github.com/mozilla/django-csp/pull/252))
- Added support for CSP configuration as sets. ([#251](https://github.com/mozilla/django-csp/pull/251))
- Changed `REPORT_PERCENTAGE` to be a float between `0.0` and `100.0` and improved behavior for 100%
report percentage to always send CSP reports.
- Added ability to read the nonce after response if it was included in the header. This will raise
an error when nonce is accessed after response if not already generated.
([#269](https://github.com/mozilla/django-csp/pull/269))
- Made changes to simplify middleware logic and make `CSPMiddleware` easier to subclass. The updated
middleware returns a PolicyParts dataclass that can be modified before the policy is built.
([#237](https://github.com/mozilla/django-csp/pull/237))

## Other Changes

- Added Python 3.13 support.
- Added support for Django 5.1 and 5.2.
- Documentation improvements including fixed trusted_types links and clarification on NONE vs Python's None.
- Documentation note that reporting percentage needs rate limiting middleware.
- Expanded ruff configuration and moved into pyproject.toml.


4.0b7
=====
- Removed ``CSPMiddlewareAlwaysGenerateNonce`` middleware that forced nonce headers when not used in
  content encouraging better security practices ([#274](https://github.com/mozilla/django-csp/pull/274))

4.0b6
=====
- Fix ``CSPMiddlewareAlwaysGenerateNonce`` to always generate the nonce.
  ([#272](https://github.com/mozilla/django-csp/pull/272))

4.0b5
=====
BACKWARDS INCOMPATIBLE change:

- `request.csp_nonce` is now Falsy (`bool(request.csp_nonce)`) until it is read as a
  string (for example, used in a template, or `str(request.csp_nonce)`). Previously,
  it always tested as `True`, and testing generated the nonce.
  ([#270](https://github.com/mozilla/django-csp/pull/270))

Other changes:

- Upgrade ReadTheDocs environment ([#262](https://github.com/mozilla/django-csp/pull/262))
- Allow reading the nonce after response if it was included in the header. Add
  ``CSPMiddlewareAlwaysGenerateNonce`` to always generate a nonce.
  ([#269](https://github.com/mozilla/django-csp/pull/262))

4.0b4
=====
- Fix missing packaging dependency ([#266](https://github.com/mozilla/django-csp/pull/266))

4.0b3
=====
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
