from django.contrib import admin
from .models import Program, ProgramManagerAndProgram

# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('id', 'program', 'department', 'year', 'semester', 'programManager', 'programCoordinator',
#                     'prioritiesAmount', 'hoursRequired')


# Register your models here.

admin.site.register(Program)
admin.site.register(ProgramManagerAndProgram)

