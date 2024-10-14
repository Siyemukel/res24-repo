from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin, Student, StudentDetails,  Residence, FacultyResidence

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
        fields = ['name', 'surname', 'email', 'cellphone', 'address', 'area_code', 'course', 'faculty']
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



class FacultyResidenceForm(forms.Form):
    faculties = [
        ('accounting', 'Accounting and Informatics'),
        ('health', 'Health Sciences'),
        ('arts', 'Arts and Design'),
        ('engineering', 'Engineering and the Built Environment'),
        ('applied', 'Applied Sciences'),
        ('management', 'Management Sciences'),
        ('other', 'Other')
    ]

    # Faculty selection field
    faculty = forms.ChoiceField(choices=faculties, label="Select Faculty", required=True)

    # Residences will be dynamically populated based on selected faculty
    residences = forms.ModelMultipleChoiceField(
        queryset=Residence.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Residences"
    )

    def __init__(self, *args, **kwargs):
        # Get the selected faculty from the passed arguments
        selected_faculty = kwargs.pop('selected_faculty', None)
        super().__init__(*args, **kwargs)

        if selected_faculty:
            # If a faculty is selected, filter residences based on the selected faculty
            self.fields['residences'].queryset = Residence.objects.filter(facultyresidence__faculty=selected_faculty)

class FacultySelectionForm(forms.Form):
    FACULTY_CHOICES = [
        ('Engineering and the Built Environment', 'Engineering and the Built Environment'),
        ('Health Sciences', 'Health Sciences'),
        ('Arts and Design', 'Arts and Design'),
        ('Applied Sciences', 'Applied Sciences'),
        ('Accounting and Informatics', 'Accounting and Informatics'),
        ('Management Sciences', 'Management Sciences'),
        ('Law', 'Law'),
        ('Humanities', 'Humanities'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]
    
    faculty = forms.ChoiceField(choices=FACULTY_CHOICES, required=True)

class FacultyResidenceForm(forms.Form):
    residences = forms.ModelMultipleChoiceField(
        queryset=Residence.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Residences"
    )

    def __init__(self, *args, **kwargs):
        selected_faculty = kwargs.pop('selected_faculty', None)
        super(FacultyResidenceForm, self).__init__(*args, **kwargs)

        if selected_faculty:
            self.fields['residences'].queryset = Residence.objects.filter(faculty=selected_faculty)


