import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

student_status = ['candidate', 'advanced_candidate', 'intern']

student_status_for_internship = {
    0: 'not accepted',
    1: 'accepted'
}

intern_status_approved_hours_by_mentor = {
    0: 'not approved',
    1: 'approved'
}

def remove_info_from_serializer(list_of_obg, serializer):
    for obj in serializer.data:
        for i in list_of_obg:
            obj.pop(i)
    return serializer


saves_paths = {
    "photo": 'data\images',
    "cv": 'data\cv',
    "gradesSheet": 'data\gradesSheet'
}

cv_storage = FileSystemStorage(location='./data/')
photo_storage = FileSystemStorage(location='./data/')
gradesSheet_storage = FileSystemStorage(location='./data/')


def save_to_path(path):
    return os.path.join(settings.LOCAL_FILE_DIR, path)
    # return os.path.join(settings.LOCAL_FILE_DIR, 'data\images')

# def cv_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, 'data\cv')

# How to create an app:
    # manage.py startapp <example>
    # <example> add to INSTALLED_APPS in settings
    # Add a class in the models of <example> like Student - crete a table with the name example_Student
    # Add admin.site.register(the name of the new class, like Student) in admin
    # manage.py makemigrations <example>
    # manage.py migrate <example>
    # python manage.py runserver
# If we want to add a table to existing app like users, we need to add a class in the models of users
    # manage.py makemigrations <example>
    # manage.py migrate <example>
    # python manage.py runserver


