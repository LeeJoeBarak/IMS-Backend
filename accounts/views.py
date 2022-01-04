from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import FileResponse
from manage import db, get_collection_handle

import datetime

# Create your views here.

# example for  function that is triggered by route '' (landing page of the website)

############# Need to implement until Jan 6th, 2022 ##############

def register_student(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')

        data = {'username': username,
                'firstName': firstName,
                'lastName': lastName,
                'password': password,
                'email': email}
        #todo validate that the student is a BGU student

        # create this student in the DB
        studentCol = db["students"]
        print(f"retrieved student collection:\n {studentCol}")

        res = studentCol.insert_one(data)
        print("successful insert")

        print(res.inserted_id)

        return JsonResponse(data, safe=False)
    return HttpResponse("request method wasn't POST")




def create_internship(request):
    return NotImplemented

def assign_intern(request):
    return NotImplemented


def pick_internships(request):
    return NotImplemented


###################################################################
def home(request):
    return HttpResponse('home !!! :)')


def login(request):
    return NotImplemented

def logout(request):
    return NotImplemented

def register_program_mngr(request):
    return NotImplemented
