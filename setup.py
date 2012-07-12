from setuptools import setup, find_packages

import csp

setup(
    name='django_csp',
    version=csp.__version__,
    description='Django Content Security Policy support.',
    author='James Socol',
    author_email='james@mozilla.com',
    url='http://github.com/mozilla/django-csp',
    license='BSD',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
