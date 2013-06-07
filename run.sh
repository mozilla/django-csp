#!/bin/bash

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_settings"

usage() {
    echo "USAGE: $0 [command]"
    echo "  test - run the django-csp tests"
    echo "  shell - open the Django shell"
    exit 1
}

case "$1" in
    "test" )
        django-admin.py test csp ;;
    "shell" )
        django-admin.py shell ;;
    * )
        usage ;;
esac
