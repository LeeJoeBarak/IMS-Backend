from django.urls import path
from . import views

urlpatterns = [
    path('', views.home), # Home page data
    path('users/register/student', views.register_student), # UC2

    path('assignIntern', views.assign_intern), # UC26

    path('companyRep/createInternship', views.create_internship), # UC15 -> uc17: do we implement a different route for when IM (Internship Manager) accesses this functionality???

    path('student/pickInternships', views.pick_internships), # UC22 - student picks top internships she wants to be interviewed to
# 2 נתיבים:
    # 1. לשלוף את ההתמחויות הקיימות בתוכנית שהסטודנט משוייך אליה
    # 2. לאחר בחירת ההעדפות של הסטודנט לשלוח לשרת את מה שהוא בחר


    # path('/users/register/program', views.register_program_mngr),
    # path('/users/login', views.login),
    # path('/users/logout', views.logout),

]
