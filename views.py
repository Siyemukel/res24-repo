from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, AdminRegistrationForm, StudentDetailsForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Student, StudentDetails, Residence, FacultyResidence
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('student_login')  # Redirect to login after registration
        else:
            # If the form is not valid, we can provide error messages to the user
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
    # Render login form with messages, if any
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
            return redirect('admin_dashboard')  # Redirect to a home page after successful login (adjust 'home' as needed)
        else:
            messages.error(request, 'Invalid admin username or password.')

    return render(request, 'adminlogin.html')  # Ensure the template file name is correct (lowercase)

def student_dashboard(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Pass the student number to the template
        context = {
            'student_number': request.user.student_number  # Assuming 'student_number' is the field name
        }
        return render(request, 'studentdashboard.html', context)
    else:
        return redirect('student_login')  # Redirect to login if not authenticated
    
def student_details(request):
    if request.user.is_authenticated:
        context = {
            'student_number' : request.user.student_number
        }
        return render(request, 'studentdetails.html', context)
    else:
        return render(request, 'studentdetails.html')
    

@login_required
def student_details(request):
    student = request.user  # Get the logged-in student
    
    # Check if the student already has details, or create new ones
    try:
        details = StudentDetails.objects.get(student=student)
    except StudentDetails.DoesNotExist:
        details = None

    if request.method == 'POST':
        form = StudentDetailsForm(request.POST, instance=details)
        if form.is_valid():
            student_details = form.save(commit=False)
            student_details.student = student  # Link the details to the student
            student_details.save()
            return redirect('success')  # Redirect after successful submission
    else:
        form = StudentDetailsForm(instance=details)

    return render(request, 'studentdetails.html', {'form': form, 'student_number': student.student_number})

def success(request):
    return render(request, 'success.html')

# yourapp/views.py


def custom_logout(request):
    logout(request)
    return redirect(reverse('home'))  # Replace 'home' with your desired home URL name


def admin_dashboard(request):
    return render(request, 'admindashboard.html')

def residence_sorting(request):
    return render(request, 'residencesorting.html')


def available_residences(request):
    faculty = request.GET.get('faculty')
    residences = Residence.objects.none()

    if faculty:
        residences = Residence.objects.filter(facultyresidence__faculty=faculty)

    return render(request, 'available_residences.html', {'residences': residences})

def select_residences(request):
    faculties = ['accounting', 'health', 'arts', 'engineering', 'applied', 'management', 'other']

    if request.method == 'POST':
        for faculty in faculties:
            selected_residences = request.POST.getlist(f'{faculty}[]')
            for residence_name in selected_residences:
                residence, created = Residence.objects.get_or_create(name=residence_name)
                FacultyResidence.objects.get_or_create(faculty=faculty, residence=residence)
        return redirect('success')  # Replace with your actual success page URL

    return render(request, 'select_residences.html')