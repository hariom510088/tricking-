from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # THIS IS CORRECT: user NOT employee
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, default='Present')

    class Meta:
        unique_together = ('user', 'date')

    def calculate_hours(self):
        if self.check_out:
            duration = self.check_out - self.check_in
            self.hours_worked = round(duration.total_seconds() / 3600, 2)
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title