# ourapp/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import Student, Admin  # Import your models

# Custom backend for students
class StudentBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = Student.objects.get(student_number=username)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            return None

# Custom backend for admins
class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(username=username)
            if admin.check_password(password):
                return admin
        except Admin.DoesNotExist:
            return None