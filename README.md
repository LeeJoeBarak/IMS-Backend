# IMS-Backend
Internship Management System Backend 


![uml](https://user-images.githubusercontent.com/48882261/155864620-083f759a-b8a8-4ba5-993d-97117fdf490c.png)



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
