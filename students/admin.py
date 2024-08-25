from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'admission_number', 'gender', 'date_of_birth', 'date_of_join', 'guardian', 'guardian_relation', 'address', 'religion', 'community', 'category', 'feeconcession', 'mobile', 'active', 'data_verified')
    search_fields = ('name', 'admission_number', 'mobile')

# Alternatively, if you prefer not to use the decorator:
# admin.site.register(Student, StudentAdmin)
