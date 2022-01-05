from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import FileResponse
import utils
import traceback

# Create your views here.

# example for  function that is triggered by route '' (landing page of the website)
def home(request):
    return HttpResponse('home !!! :)')


def register_student(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')

        data = {
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'password': password,
            'email': email
        }
        #todo Validate username doesn't exist. If wrong username -> return 400 A user with the same username already exists

        #todo validate that the student is a BGU student
        db, client = utils.get_db_handle()
        studentColl = utils.get_collection_handle(db, "students")
        res = studentColl.insert_one(data)
        print("successful insert")
        print(res.inserted_id)
        return HttpResponse(201)
    return HttpResponse("request method wasn't POST")

 
def create_internship(request):
    """company representative creates an internship offered by his company"""
    #todo validate that the internship doesn't exist in system already
    if request.method == "POST":
        username = request.POST.get('username')
        companyName = request.POST.get('companyName')
        internshipName = request.POST.get('internshipName')
        about = request.POST.get('about')
        requirments = request.POST.get('requirments') #DON'T fix the typo (i.e. don't add 'e' after 'r')
        mentor = request.POST.get('mentor')

        #todo Validate username. If wrong username -> return 401 invalid username

        data = {
            'username': username,
            'companyName': companyName,
            'internshipName': internshipName,
            'about': about,
            'requirments': requirments,
            'mentor': mentor
        }

        db, client = utils.get_db_handle()
        internshipsColl = utils.get_collection_handle(db, "Internships")
        res = internshipsColl.insert_one(data)
        print("successful insert")
        print(res.inserted_id)
        return HttpResponse(200, 'internship created successfully')
    return HttpResponse("request method wasn't POST")


def assign_intern(request):
    return NotImplemented


# the below 2 routes serve UC22
def get_internships(request):
    """ return all existing Internships that are associated with the specific Program the Student belongs to"""
    programDoc = None
    internshipsArr = None
    if request.method == "GET":
        try:
            programName = request.GET.get('program', '')
            print(f"Program Name = {programName}")
            if programName == '':
                return HttpResponse(404,'program not found')
            elif not isinstance(programName, str):
                programName = str(programName)

            db, client = utils.get_db_handle()
            programsColl = utils.get_collection_handle(db, "Programs")
            internshipsColl = utils.get_collection_handle(db, "Internships")

            programDoc = programsColl.find_one({"prog_name" : programName}) # try to get the req. program
            print(programDoc)
            internshipsArr = programDoc['internships']
            print(internshipsArr)
            if internshipsArr is not None:
                return JsonResponse(internshipsArr, safe=False)
            return HttpResponse('Something went wrong.. probably retrieving the program doc from DB')
        except Exception:
            print("please take this exception and change the code's exception clause to be specific!")
            traceback.print_exc()
    return HttpResponse("request method wasn't GET")

# internship_obj = {
#     "companyName": "string",
#     "internshipName": "string",
#     "about": "string",
#     "requirments": "string"
#   }

# program_obj = {
    # _id: ObjectID('AAA'),
    # prog_name: '2021A',
    # prog_mngr: 'some mngr',
    # ... ,
    # internships: [
#                {
#                 ObjectID('ABB')
#                 internshipName: '#1 Wix'
#                 },
#                  {
#                  ObjectID('DC778hljkH6')
#                  internshipName: '#1 coolStartup'
#                  },
#                  {
#                  ObjectID('fjhkYG789RGFDS5SL')
#                  internshipName: '#2 Wix'
#                  },......
#     ]
# }
def save_student_priorities(request):
    """save the Student internship priorities in the DB """
    return NotImplemented


###################################################################


def login(request):
    return NotImplemented

def logout(request):
    return NotImplemented

def register_program_mngr(request):
    return NotImplemented

