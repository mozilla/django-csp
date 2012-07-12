from django.dispatch import Signal


group_created = Signal(providing_args=['report', 'site'])
