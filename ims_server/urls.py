from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from internship import views as internship_views
from program import views as program_views


router = routers.DefaultRouter()
router.register(r'internships', internship_views.InternshipsView, 'internships')
# router.register(r'internships/<program>', views.InternshipsView, '')
# router.register(r'internshipsList', views.internships_list(), 'internshipsList')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('internships/<program>', internship_views.get_internships_by_program),
    path('prioritiesAmount/<program>', program_views.get_priorities_amount_by_program),
    path('hoursRequired/<program>', program_views.get_hours_required_by_program),
    path('candidate/internshipsPriorities', internship_views.set_internships_priorities_by_candidate),
    # path('hoursRequired/<program>', program_views.get_detail_about_program)
    # path('companyRep/createInternship', internships_views.create_internship)


]
