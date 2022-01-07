from django.urls import path
from . import views

urlpatterns = [
    path('', views.home), # Home page data
    path('users/register/student', views.register_student), # UC2
    # path("react", views.react, name="react"),
    # path("/react", views.react, name="react"),
    path('assignIntern', views.assign_intern), # UC26

    path('companyRep/createInternship', views.create_internship), # UC15 -> uc17: do we implement a different route for when IM (Internship Manager) accesses this functionality???

   # UC22 - student picks top internships she wants to be interviewed to
    path('internships/{program}', views.get_internships),
    path('candidate/internshipsPriorities', views.save_student_priorities)


    # path('/users/register/program', views.register_program_mngr),
    # path('/users/login', views.login),
    # path('/users/logout', views.logout),

]
