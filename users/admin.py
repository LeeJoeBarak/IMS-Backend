from django.contrib import admin

# Register your models here.
from users.models import Student, Company, ProgramManager,ProgramCoordinator, Company_companyRepresentative, Company_mentor

admin.site.register(Student)
admin.site.register(Company)
admin.site.register(ProgramManager)
admin.site.register(ProgramCoordinator)
admin.site.register(Company_companyRepresentative)
admin.site.register(Company_mentor)