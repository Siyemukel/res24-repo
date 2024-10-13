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
    # Assuming the student_number comes from the related Student model
    student_number = forms.CharField(required=False, label='Student Number', widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))

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
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cellphone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'area_code': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentDetailsForm, self).__init__(*args, **kwargs)
        
        # Make the student_number read-only if it exists
        if self.instance and self.instance.student:
            self.fields['student_number'].initial = self.instance.student.student_number
            self.fields['student_number'].widget.attrs['readonly'] = True