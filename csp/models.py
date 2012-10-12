from datetime import datetime
import hashlib
import json

from django.db import models

from csp.exceptions import BadReportError
from csp.signals import group_created
from csp.utils import send_new_mail


__all__ = ['Group', 'Report']


class Group(models.Model):
    """A group of similar violation reports."""
    name = models.CharField(max_length=200, verbose_name='Report Group',
                            help_text='A human-readable name for a group.')
    identifier = models.CharField(max_length=40, verbose_name='Group Hash',
                                  help_text='A unique identifier for a group.',
                                  unique=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_or_create(cls, report):
        """Given a CSP report, find an existing group or create a new one."""
        ident = report.get_identifier()
        try:
            return (cls.objects.get(identifier=ident), False)
        except cls.DoesNotExist as e:
            # We're going to have to create a new group.
            pass
        name = u'%s - %s' % (report.document_uri, report.violated_directive)
        group = cls(name=name, identifier=ident)
        group.save()
        return (group, True)

    def count(self):
        if not hasattr(self, '_count'):
            self._count = self.report_set.count()
        return self._count


class Report(models.Model):
    """A representation of one report."""
    group = models.ForeignKey(Group, null=True, blank=True)
    document_uri = models.URLField(max_length=400, db_index=True)
    blocked_uri = models.CharField(max_length=400, null=True, blank=True,
                                  db_index=True)
    referrer = models.URLField(max_length=400, null=True, blank=True)
    violated_directive = models.CharField(max_length=1000, null=True,
                                          blank=True, db_index=True)
    original_policy = models.TextField(null=True, blank=True)
    reported = models.DateTimeField(default=datetime.now, db_index=True)

    @classmethod
    def create(cls, report):
        """If passed a JSON blob in the report kwarg, use it."""
        try:
            report = json.loads(report)['csp-report']
        except ValueError:
            raise BadReportError()
        kw = dict((k.replace('-', '_'), v) for k, v in report.items())
        return cls(**kw)

    def __unicode__(self):
        return self.get_identifier()

    def get_identifier(self):
        if not hasattr(self, '_ident'):
            ident = u'%s %s %s' % (self.document_uri, self.blocked_uri,
                                   self.violated_directive)
            self._ident = hashlib.sha1(ident).hexdigest()
        return self._ident

    def save(self, site=None, *a, **kw):
        if not self.group:
            self.group, created = Group.get_or_create(self)
        super(Report, self).save(*a, **kw)
        if created:
            ret = group_created.send_robust(sender=self.group, report=self,
                                            site=site)


group_created.connect(send_new_mail, dispatch_uid='group-created-email')
