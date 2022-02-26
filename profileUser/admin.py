from django.contrib import admin

# Register your models here.
from profileUser.models import StudentProfile, CompanyProfile

admin.site.register(StudentProfile)
admin.site.register(CompanyProfile)
