#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import SSInstance

class SSInstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('u','d')

admin.site.register(SSInstance, SSInstanceAdmin)
