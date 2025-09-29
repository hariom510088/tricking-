from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from .models import Attendance, Announcement, EmployeeProfile
from .forms import SignUpForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create employee profile
            EmployeeProfile.objects.create(
                user=user,
                employee_id=form.cleaned_data.get('employee_id'),
                department=form.cleaned_data.get('department'),
                position=form.cleaned_data.get('position'),
                phone_number=form.cleaned_data.get('phone_number')
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    today = date.today()
    
    # Get today's attendance
    try:
        today_attendance = Attendance.objects.get(user=request.user, date=today)
    except Attendance.DoesNotExist:
        today_attendance = None

    # Get recent announcements
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Get attendance summary for the week
    week_start = today - timedelta(days=today.weekday())
    week_attendance = Attendance.objects.filter(
        user=request.user,
        date__gte=week_start
    )
    
    # Calculate total hours for the week
    total_hours = sum([att.hours_worked for att in week_attendance if att.hours_worked])
    
    context = {
        'today_attendance': today_attendance,
        'announcements': announcements,
        'week_attendance': week_attendance,
        'total_hours': total_hours,
    }
    return render(request, 'dashboard.html', context)

@login_required
def check_in(request):
    today = date.today()
    
    # Check if already checked in today
    if Attendance.objects.filter(user=request.user, date=today).exists():
        messages.warning(request, 'You have already checked in today!')
        return redirect('dashboard')
    
    # Create attendance record
    attendance = Attendance.objects.create(
        user=request.user,
        check_in=timezone.now(),
        date=today
    )
    messages.success(request, 'Check-in successful!')
    return redirect('dashboard')

@login_required
def check_out(request):
    today = date.today()
    
    try:
        attendance = Attendance.objects.get(user=request.user, date=today)
        if attendance.check_out:
            messages.warning(request, 'You have already checked out today!')
        else:
            attendance.check_out = timezone.now()
            attendance.calculate_hours()
            messages.success(request, 'Check-out successful!')
    except Attendance.DoesNotExist:
        messages.error(request, 'You need to check in first!')
    
    return redirect('dashboard')

@login_required
def attendance_history(request):
    attendance_records = Attendance.objects.filter(
        user=request.user
    ).order_by('-date')[:30]
    
    return render(request, 'attendance_history.html', {'attendance_records': attendance_records})