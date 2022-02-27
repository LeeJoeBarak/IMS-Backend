from django.contrib import admin

# Register your models here.
# from users.models import Student
from user.models import Student, Company, ProgramManager, ProgramCoordinator, CompanyRepresentative, CompanyMentor

admin.site.register(Student)
admin.site.register(Company)
admin.site.register(ProgramManager)
admin.site.register(ProgramCoordinator)
admin.site.register(CompanyRepresentative)
admin.site.register(CompanyMentor)
