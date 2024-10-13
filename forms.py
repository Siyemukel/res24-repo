from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin, Student, StudentDetails

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['student_number', 'email', 'password1', 'password2']

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password1', 'password2']


class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = [
            'name', 
            'surname', 
            'email', 
            'cellphone', 
            'address', 
            'area_code', 
            'course', 
            'faculty'
        ]
        widgets = {
            'faculty': forms.Select(choices=StudentDetails.faculty),
        }

        def __init__(self, *args, **kwargs):
             super(StudentDetailsForm, self).__init__(*args, **kwargs)
             # Make student_number readonly if you want to include it in the form
             self.fields['student_number'].widget.attrs['readonly'] = True