import codecs
import os
import sys

from setuptools import find_packages, setup

version = "3.8rc"


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print(f'  git tag -a {version} -m "version {version}"')
    print("  git push --tags")
    sys.exit()


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


install_requires = [
    "Django>=3.2",
]

jinja2_requires = [
    "jinja2>=2.9.6",
]

test_requires = [
    "pytest",
    "pytest-cov",
    "pytest-django",
    "pytest-ruff",
]

test_requires += jinja2_requires


setup(
    name="django_csp",
    version=version,
    description="Django Content Security Policy support.",
    long_description=read("README.rst"),
    author="James Socol",
    author_email="me@jamessocol.com",
    maintainer="Mozilla MEAO team",
    maintainer_email="meao-backend@mozilla.com",
    url="http://github.com/mozilla/django-csp",
    license="BSD",
    packages=find_packages(),
    project_urls={
        "Documentation": "http://django-csp.readthedocs.org/",
        "Changelog": "https://github.com/mozilla/django-csp/blob/main/CHANGES",
        "Bug Tracker": "https://github.com/mozilla/django-csp/issues",
        "Source Code": "https://github.com/mozilla/django-csp",
    },
    install_requires=install_requires,
    extras_require={
        "tests": test_requires,
        "jinja2": jinja2_requires,
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: Web Environment :: Mozilla",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
    ],
)
