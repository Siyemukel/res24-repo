from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, AdminRegistrationForm, StudentDetailsForm, FacultyResidenceForm, FacultySelectionForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Student, StudentDetails, Residence, FacultyResidence
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import forms


def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('student_login')  # Redirect to login after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()

    return render(request, 'studentcreateacc.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def student_login(request):
    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=student_number, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('student_dashboard')  # Redirect after login
        else:
            messages.error(request, 'Invalid student number or password.')
    return render(request, 'studentlogin.html')


def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created successfully. Please log in.')
            return redirect('admin_login')  # Redirect to the admin login page
        else:
            messages.error(request, 'There was an error creating the account. Please try again.')
    else:
        form = AdminRegistrationForm()
    
    return render(request, 'admincreateacc.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)  # Log the user in
            return redirect('admin_dashboard')  # Redirect to a home page after successful login
        else:
            messages.error(request, 'Invalid admin username or password.')

    return render(request, 'adminlogin.html')


@login_required
def student_dashboard(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        context = {
            'student_number': request.user.student_number  # Assuming 'student_number' is the field name
        }
        return render(request, 'studentdashboard.html', context)
    else:
        return redirect('student_login')  # Redirect to login if not authenticated



@login_required
def student_details(request):
    student = request.user  # Get the logged-in student

    try:
        details = StudentDetails.objects.get(student=student)
    except StudentDetails.DoesNotExist:
        details = None

    if request.method == 'POST':
        # Bind the data to both forms
        form = StudentDetailsForm(request.POST, instance=details)
        faculty_form = FacultySelectionForm(request.POST)

        # Validate both forms
        if form.is_valid() and faculty_form.is_valid():
            # Save student details
            student_details = form.save(commit=False)
            student_details.student = student
            student_details.save()

            # Get the selected faculty from the faculty form
            selected_faculty = faculty_form.cleaned_data['faculty']
           
            # Redirect to the success page, passing the faculty as a parameter
            return redirect('available_residences', faculty=selected_faculty)
        else:
            print(form.errors)
            print(faculty_form.errors)
            print(request.POST.get('faculty'))  # This will show the submitted value for faculty
  
    else:
        # Initialize the forms with existing data or empty fields
        form = StudentDetailsForm(instance=details)
        faculty_form = FacultySelectionForm()

    # Render the template with both forms and the student number
    return render(request, 'studentdetails.html', {
        'form': form,
        'faculty_form': faculty_form,
        'student_number': student.student_number
    })

@login_required
def select_residences(request, faculty):
    # Ensure the selected faculty is passed correctly and the form is filtered by it
    if request.method == 'POST':
        form = FacultyResidenceForm(request.POST, selected_faculty=faculty)
        
        if form.is_valid():
            selected_residences = form.cleaned_data['residences']
            
            # Save the selected residences for the student
            student_details = get_object_or_404(StudentDetails, student=request.user)
            student_details.residences.set(selected_residences)
            student_details.save()
            
            return redirect('success')  # Redirect after saving
    else:
        form = FacultyResidenceForm(selected_faculty=faculty)

    return render(request, 'residencesorting.html', {'form': form, 'faculty': faculty})

def available_residences(request):
    faculty = request.GET.get('faculty')  # Fetch the selected faculty from the URL
    residences = Residence.objects.none()  # Default to no residences

    if faculty:
        # Filter residences by the selected faculty
        residences = Residence.objects.filter(facultyresidence__faculty=faculty)

    return render(request, 'available_residences.html', {
        'residences': residences,
        'selected_faculty': faculty
    })

def success(request):
    return render(request, 'success.html')


def custom_logout(request):
    logout(request)
    return redirect(reverse('home'))  # Replace 'home' with your desired home URL name


def admin_dashboard(request):
    return render(request, 'admindashboard.html')

