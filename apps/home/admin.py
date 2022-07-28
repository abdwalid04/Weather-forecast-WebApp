# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(observation)
admin.site.register(nebulosite)
admin.site.register(prevision)
admin.site.register(validation)
