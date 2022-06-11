import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

student_status = ['סטודנט', 'מועמד מתקדם', 'מתמחה']
# student_status = ['student', 'advancedCandidate', 'intern']

student_status_for_internship = {
    0: 'false',
    1: 'true'
}

intern_status_approved_hours_by_mentor = {
    0: 'false',
    1: 'true'
}


def remove_info_from_serializer(list_of_obg, serializer):
    for obj in serializer.data:
        for i in list_of_obg:
            obj.pop(i)
    return serializer


saves_paths = {
    "photo": 'data\images',
    "cv": 'data\cv',
    "gradesSheet": 'data\gradesSheet',
    "reportByStudent": 'data/reportByStudent',
    "reportByMentor": 'data/reportByMentor'
}

cv_storage = FileSystemStorage(location='./data/')
photo_storage = FileSystemStorage(location='./data/')
gradesSheet_storage = FileSystemStorage(location='./data/')
reportByStudent_storage = FileSystemStorage(location='./data/')
reportByMentor_storage = FileSystemStorage(location='./data/')


# companies_list = Company.objects.values_list('companyName', flat=True).order_by('companyName')

def save_to_path(path):
    return os.path.join(settings.LOCAL_FILE_DIR, path)


# def get_program_id_by_student(username):
#     users = User.objects.all()
#     user = users.filter(username=username)
#     # print("1. user: ", user)
#     user_serializer = UserDetailsSerializer(user, many=True)
#     user_serializer = list(user_serializer.data)
#     user_serializer = user_serializer[0]
#     Student_id = user_serializer['id']
#     # print('2. Student_id: ', Student_id)
#     program = StudentAndProgram.objects.filter(student_id=Student_id)
#     program_serializer = StudentAndProgramSerializers(program, many=True)
#     program_serializer = list(program_serializer.data)
#     program_serializer = program_serializer[0]
#     program_id = program_serializer['program_id']
#     # print('3. program_id: ', program_id)
#     return program_id


# def get_internship_id(internshipName, program_id, companyName):
#     internship_obj = InternshipDetails.objects.filter(internshipName=internshipName,
#                                                       program_id=program_id,
#                                                       companyName_id=companyName)
#     # print('4. internship_obj: ', internship_obj)
#     internship_serializer = InternshipIdSerializer(internship_obj, many=True)
#     # print('5. internship_serializer: ', internship_serializer.data)
#     internship_serializer = list(internship_serializer.data)
#     # print('6. internship_serializer: ', internship_serializer)
#     internship_serializer = internship_serializer[0]
#     # print('7. internship_serializer: ', internship_serializer)
#     internship_id = internship_serializer['id']
#     return internship_id


# def cv_path():
#     return os.path.join(settings.LOCAL_FILE_DIR, 'data\cv')


# content = ContentType.objects.filter(app_label='api', model='electrics').first()

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
