from django.contrib import admin
from .models import EmployeeProfile, Attendance, Announcement

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'position']
    search_fields = ['user__username', 'employee_id']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'check_in', 'check_out', 'hours_worked']  # CHANGED: employee → user
    list_filter = ['date', 'user']  # CHANGED: employee → user

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_active']