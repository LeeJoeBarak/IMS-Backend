from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from internship import views as internship_views
from program import views as program_views
from user.api import RegisterAPI, LoginAPI, LogoutAPI
from knox import views as knox_views
from user.api import RegisterAPI, LoginAPI
# from knox import views as knox_views
from django.views.generic import TemplateView
import os
from pathlib import Path
from django.http import HttpResponse

BASE_DIR = Path(__file__).resolve().parent.parent
index_file_path = os.path.join(BASE_DIR, 'build', 'index.html')

def react(request):
    # return render(request, index_file_path)
    try:
        print(index_file_path)
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        print('error!!')

router = routers.DefaultRouter()
router.register(r'internships', internship_views.InternshipsView, 'internships')
# router.register(r'internships/<program>', views.InternshipsView, '')
# router.register(r'internshipsList', views.internships_list(), 'internshipsList')

urlpatterns = [
    path('', react, name="react"),
    path('', include(router.urls)),
    path('internships/<program>', internship_views.get_internships_by_program),
    path('prioritiesAmount/<program>', program_views.get_priorities_amount_by_program),
    path('hoursRequired/<program>', program_views.get_hours_required_by_program),
    # path('candidate/internshipsPriorities', internship_views.set_internships_priorities_by_candidate),
    # path('hoursRequired/<program>', program_views.get_detail_about_program)
    # path('companyRep/createInternship', internships_views.create_internship)
    # path('api/auth/', include('knox.urls')),
    path('users/register/student', RegisterAPI.as_view()),
    path('users/login', LoginAPI.as_view()),
    # path('users/logout', LogoutAPI.as_view()),


]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
