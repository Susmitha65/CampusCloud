from django.contrib import admin
from .models import CustomUser, StudentProfile
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'email', 'role', 'department')
    search_fields = ('username', 'name', 'email')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'role', 'department')}),
    )

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'prn', 'admin_number', 'phone_number', 'email')
    search_fields = ('user__username', 'prn', 'admin_number')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
