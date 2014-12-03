# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class SSInstance(models.Model):
    email = models.CharField('Email', max_length=32)
    servicepwd = models.CharField('AdminPWD', db_column='pass', max_length=16, default='000000', editable=False) # Field renamed because it was a Python reserved word.
    passwd = models.CharField('ServicePWD', max_length=16)
    t = models.IntegerField('LastAlive', default=0, editable=False)
    u = models.BigIntegerField('Upload', default=0)
    d = models.BigIntegerField('Download', default=0)
    transfer_enable = models.BigIntegerField('Threshold', default=settings.DEFAULT_THRESHOLD)
    port = models.IntegerField('ServicePort', unique=True)
    switch = models.IntegerField(default=1, editable=False)
    enable = models.BooleanField('Enable', default=1)
    type = models.IntegerField('Type', default=7, editable=False)
    last_get_gitf_time = models.IntegerField(default=1, editable=False)
    last_rest_pass_time = models.IntegerField(default=1, editable=False)
    # class Meta:
    #     managed = False
    #     db_table = 'user'

    def __unicode__(self):
        return "%s:%s U:%sM(%s) D:%sM(%s) Lmt:%sM(%s)" % (self.enable, self.port, "%.2f" % (float(self.u)/(1024*1024)), self.u, "%.2f" % (float(self.d)/(1024*1024)), self.d, "%.2f" % (float(self.transfer_enable)/(1024*1024)), self.transfer_enable)
    
