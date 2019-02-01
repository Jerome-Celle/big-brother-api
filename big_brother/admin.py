from django.contrib import admin

from . import models

admin.site.register(models.User)
admin.site.register(models.ActionToken)
admin.site.register(models.TemporaryToken)
admin.site.register(models.Application)
admin.site.register(models.Test)
admin.site.register(models.Execution)
admin.site.register(models.TestType)
