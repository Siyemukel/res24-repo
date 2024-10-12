from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, AdminRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Student

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
        user = authenticate(request, username=student_number, password=password)#chaned username to student number
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to a home page after successful login
        else:
            messages.error(request, 'Invalid student number or password.')

    return render(request, 'studentlogin.html')  # Render the login template

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
            return redirect('home')  # Redirect to a home page after successful login (adjust 'home' as needed)
        else:
            messages.error(request, 'Invalid admin username or password.')

    return render(request, 'adminlogin.html')  # Ensure the template file name is correct (lowercase)