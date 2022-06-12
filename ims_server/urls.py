from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from internship import views as internship_views
from profile_user import views as profile_views
from user import views as user_views
from program import views as program_views
from user.api import RegisterAPI, LoginAPI, LogoutAPI, RegisterCompanyRepAPI, \
    RegisterMentorAPI, RegisterProgramCoordinatorAPI, RegisterProgramManagerAPI, UpdatePassword
from knox import views as knox_views
from user.api import RegisterAPI, LoginAPI
from django.views.generic import TemplateView
import os
from pathlib import Path
from django.http import HttpResponse

BASE_DIR = Path(__file__).resolve().parent.parent
index_file_path = os.path.join(BASE_DIR, 'build', 'index.html')

def react(request):
    try:
        print(index_file_path)
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        print('error!!')

router = routers.DefaultRouter()
router.register(r'internships', internship_views.InternshipsView, 'internships')


urlpatterns = [
    # path('', react, name="react"),
    # path('', include(router.urls)),
    # path('admin/', admin.site.urls),
    path('companies', user_views.get_companies_list),
    path('students/<program>', user_views.get_details_about_students_by_program),
    path('mentors/<company>', user_views.get_mentors_by_company),
    path('users/details/<username>', user_views.get_details_about_user_by_username),
    path('programManagers', user_views.get_program_managers),
    path('internships/<program>', internship_views.get_internships_by_program),
    path('mentorsByCompanyRep/<companyRep>', user_views.get_mentors_by_companyRep),
    path('companyRep/createInternship', internship_views.PostCreateInternshipByCompanyRep.as_view()),
    path('programManager/createInternship', internship_views.PostCreateInternshipByProgramManager.as_view()),
    path('assignIntern', internship_views.UpdateStatusInternshipByManager.as_view()),
    path('setInterns', internship_views.SetInternsToInternship.as_view()),
    path('companyRep/setStatus', internship_views.SetStatusByCompanyRep.as_view()),
    path('mentor/setStatus', internship_views.SetStatusByMentor.as_view()),
    path('intern/hoursReport', internship_views.HoursReportByIntern.as_view()),
    path('mentor/hoursApproval', internship_views.HoursApprovalByMentor.as_view()),
    path('programManager/<program>/<companyName>/<internshipName>/nominees',
         internship_views.get_nominees_passed_company_interview),
    path('intern/getHours/<username>', internship_views.get_intern_hours),
    path('companies/<program>', internship_views.get_companies_by_program),
    path('companyRep/<username>/candidates/<program>', internship_views.get_candidates_by_program_by_companyRep),
    path('mentor/<username>/candidates/<program>', internship_views.get_candidates_by_program_by_mentor),
    path('mentor/getInterns/<username>', internship_views.get_interns_mentor),
    path('student/profile/<username>', profile_views.get_student_profile),
    path('company/<companyName>', profile_views.get_company_profile),
    path('student/createProfile', profile_views.PostCreateStudentProfile.as_view()),
    path('companyRep/createCompanyProfile', profile_views.PostCreateCompanyProfile.as_view()),
    path('prioritiesAmount/<program>', program_views.get_priorities_amount_by_program),
    path('admin/openProgram', program_views.PostCreateProgram.as_view()),
    path('admin/programs', program_views.get_programs),
    path('hoursRequired/<program>', program_views.get_hours_required_by_program),
    path('activePrograms', program_views.get_active_program),
    path('candidate/internshipsPriorities', internship_views.PostInternshipsPrioritiesByCandidate.as_view()),
    path('intern/uploadReport/<username>', internship_views.PostUploadReportByIntern.as_view()),
    path('mentor/<username>/uploadReport/<intern>', internship_views.PostUploadReportByMentor.as_view()),

    # register:
    path('users/register/student', RegisterAPI.as_view()),
    path('users/register/companyRep', RegisterCompanyRepAPI.as_view()),
    path('users/register/mentor', RegisterMentorAPI.as_view()),
    path('users/register/programCoordinator', RegisterProgramCoordinatorAPI.as_view()),
    path('users/register/programManager', RegisterProgramManagerAPI.as_view()),
    # login:
    path('users/login', LoginAPI.as_view()),
    # logout:
    path('users/logout', LogoutAPI.as_view()),
    path('users/changePsw', UpdatePassword.as_view()),


]
