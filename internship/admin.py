from django.contrib import admin
# from .models import Internship
from .models import InternshipDetails, AssignmentIntern, HoursReport, Priority, InternshipAndMentor, InternshipAndIntern

# from .models import Internship, HoursReport, AssignmentIntern, Priority

# class InternshipsAdmin(admin.ModelAdmin):
    # list_display = ('program', 'internshipName', 'companyName', 'internshipName', 'about', 'requirements')


# Register your models here.

admin.site.register(InternshipDetails)
admin.site.register(AssignmentIntern)
admin.site.register(HoursReport)
admin.site.register(Priority)
admin.site.register(InternshipAndMentor)
admin.site.register(InternshipAndIntern)

