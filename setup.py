from setuptools import setup

setup(
    name='django_csp',
    version='1.0.2',
    description='Django Content Security Policy support.',
    author='James Socol',
    author_email='james@mozilla.com',
    url='http://github.com/mozilla/django-csp',
    license='BSD',
    packages=['csp'],
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
