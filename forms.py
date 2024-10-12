from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin, Student

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['student_number', 'email', 'password1', 'password2']

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password1', 'password2']