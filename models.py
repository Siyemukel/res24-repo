from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.conf import settings

# Custom Manager for Student
class StudentManager(BaseUserManager):
    def create_user(self, student_number, email, password=None, **extra_fields):
        if not student_number:
            raise ValueError('The student number is required')
        if not email:
            raise ValueError('The email is required')

        email = self.normalize_email(email)
        student = self.model(student_number=student_number, email=email, **extra_fields)
        student.set_password(password)
        student.save(using=self._db)
        return student

    def create_superuser(self, student_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(student_number, email, password, **extra_fields)

# Custom Student Model
class Student(AbstractBaseUser, PermissionsMixin):
    student_number = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{6,8}$', 'Student number must be numeric and 6-8 digits')]
    )
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'student_number'
    REQUIRED_FIELDS = ['email']

    objects = StudentManager()

    groups = models.ManyToManyField(Group, blank=True, related_name='student_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='student_permissions')

    def __str__(self):
        return self.student_number
    
    
    def check_password(self, raw_password):
        return super().check_password(raw_password)

# Custom Manager for Admin
class AdminManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The admin username is required')
        if not email:
            raise ValueError('The email is required')

        email = self.normalize_email(email)
        admin = self.model(username=username, email=email, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# Custom Admin Model
class Admin(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField(Group, related_name='admin_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_permissions')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AdminManager()

    def __str__(self):
        return self.username
    
    def check_password(self, raw_password):
        return super().check_password(raw_password)
    

class StudentDetails(models.Model):
    # Link to the Student model via a one-to-one relationship
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # This refers to the custom 'Student' model
        on_delete=models.CASCADE,  # When a student is deleted, delete the details too
        primary_key=True,
    )
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    cellphone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    area_code = models.CharField(max_length=10)
    course = models.CharField(max_length=255)
    
    faculty = models.CharField(
    max_length=50,
    choices=[
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
    ],
)


    def __str__(self):
        return f"{self.name} {self.surname} ({self.student.student_number})"
    

class Residence(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class FacultyResidence(models.Model):
    faculty = models.CharField(max_length=50, choices=[
        ('Accounting and Informatics', 'Accounting and Informatics'),
        ('Health Sciences', 'Health Sciences'),
        ('Arts and Design', 'Arts and Design'),
        ('Engineering and the Built Environment', 'Engineering and the Built Environment'),
        ('Applied Sciences', 'Applied Sciences'),
        ('Management Sciences', 'Management Sciences'),
        ('Other', 'Other'),
    ])
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('faculty', 'residence')

    def __str__(self):
        return f"{self.faculty} - {self.residence.name}"
    

from django.db import models

class StudentDetails(models.Model):
    FACULTY_CHOICES = [
        ('accounting', 'Accounting and Informatics'),
        ('health', 'Health Sciences'),
        ('arts', 'Arts and Design'),
        ('engineering', 'Engineering and the Built Environment'),
        ('applied', 'Applied Sciences'),
        ('management', 'Management Sciences'),
        ('other', 'Other')
    ]
    
