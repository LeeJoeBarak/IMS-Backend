# IMS-Backend
Internship Management System Backend 


![erd](https://user-images.githubusercontent.com/48882261/155854175-66d127ca-5930-4a86-8ae3-fe41b52f7413.png)


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
