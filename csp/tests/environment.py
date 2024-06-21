from jinja2 import Environment
from typing import Any


def environment(**options: Any) -> Environment:
    env = Environment(**options)
    return env
