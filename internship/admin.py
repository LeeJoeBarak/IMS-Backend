from django.contrib import admin
# from .models import Internship
from .models import InternshipDetails, AssignmentIntern, HoursReport, Priority, InternshipAndMentor, InternshipAndIntern

admin.site.register(InternshipDetails)
admin.site.register(AssignmentIntern)
admin.site.register(HoursReport)
admin.site.register(Priority)
admin.site.register(InternshipAndMentor)
admin.site.register(InternshipAndIntern)

