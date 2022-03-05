from django.contrib import admin
from .models import Internship
from .models import Internship
# from .models import Internship, HoursReport, AssignmentIntern, Priority

# class InternshipsAdmin(admin.ModelAdmin):
    # list_display = ('program', 'internshipName', 'companyName', 'internshipName', 'about', 'requirements')


# Register your models here.

admin.site.register(Internship)
# admin.site.register(AssignmentIntern)
# admin.site.register(HoursReport)
# admin.site.register(Priority)

