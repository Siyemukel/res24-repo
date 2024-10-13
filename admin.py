from django.contrib import admin
from .models import Admin, Residence, FacultyResidence

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff','is_superuser')


class FacultyResidenceInline(admin.TabularInline):
    model = FacultyResidence
    extra = 1

class ResidenceAdmin(admin.ModelAdmin):
    inlines = [FacultyResidenceInline]

admin.site.register(Residence, ResidenceAdmin)