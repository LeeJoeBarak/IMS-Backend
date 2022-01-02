from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# example for  function that is triggered by route '' (landing page of the website)

############# Need to implement until Jan 6th, 2022 ##############
def home(request):
    return HttpResponse('home')


def register_student(request):
    return NotImplemented


def create_internship(request):
    return NotImplemented

def assign_intern(request):
    return NotImplemented


def pick_internships(request):
    return NotImplemented


###################################################################
def login(request):
    return NotImplemented

def logout(request):
    return NotImplemented

def register_program_mngr(request):
    return NotImplemented
