from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Details, WorkoutRoutine, Attendance
from django.utils import timezone
from datetime import timedelta
from .forms import UserForm, WorkoutRoutineForm,BMICalculatorForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'admin@123' and password == 'Pass@123':
           
            try:
                user = User.objects.get(username=username)
    
                if not user.is_superuser:
                    messages.error(request, "User is not an admin.")
                    return redirect('admin_login')
            except User.DoesNotExist:
                messages.error(request, "admin account not found")
                # User.objects.create_superuser(username=username, password=password)
                # user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid admin credentials")
        else:
            messages.error(request, "Invalid admin credentials")
    
    return render(request, 'admin_login.html')


@login_required
def admin_dashboard(request):
    today = timezone.now().date()
    users = Details.objects.all()
    
    for user in users:
        user.days_left = (user.end_date - today).days
    
    return render(request, 'admin_dashboard.html', {'users': users, 'today': today})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully!")
            return redirect('admin_dashboard')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

@login_required
def edit_user(request, id):
    user = get_object_or_404(Details, id=id)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "User details updated successfully!")
        return redirect('admin_dashboard')
    return render(request, 'edit_user.html', {'form': form})

@login_required
def delete_user(request, id):
    user = get_object_or_404(Details, id=id)
    user.delete()
    return redirect('admin_dashboard')

@login_required
def user_details(request, id):
    user = get_object_or_404(Details, id=id)
    workouts = WorkoutRoutine.objects.filter(user=user)
    today = timezone.now().date()
    days_left = (user.end_date - today).days
    context = {
        'user': user,
        'workouts': workouts,
        'days_left': days_left,
    }
    return render(request, 'user_details.html', context)


def add_workout(request, user_id):
    if request.method == "POST":
        form = WorkoutRoutineForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user_id = user_id
            workout.save()

            if request.user.is_superuser:
                return redirect('user_details', id=user_id)
            else:
                return redirect('user_profile', id=user_id)
    else:
        form = WorkoutRoutineForm()
    return render(request, 'add_workout.html', {'form': form})


def edit_workout(request, id):
    workout = get_object_or_404(WorkoutRoutine, id=id)
    form = WorkoutRoutineForm(request.POST or None, instance=workout)
    if form.is_valid():
        form.save()
        messages.success(request, "Workout updated successfully!")
       
        if request.user.is_superuser:
            return redirect('user_details', id=workout.user.id)
        else:
            return redirect('user_profile', id=workout.user.id)
    return render(request, 'edit_workout.html', {'form': form})

def delete_workout(request, id):
    workout = get_object_or_404(WorkoutRoutine, id=id)
    user_id = workout.user.id
    workout.delete()
   
    if request.user.is_superuser:
        return redirect('user_details', id=user_id)
    else:
        return redirect('user_profile', id=user_id)

def check_in(request, id):
    user = get_object_or_404(Details, id=id)
    
    time_varation = timedelta(hours=5, minutes=30)
    
    attendance = Attendance.objects.create(user=user, check_in_time=timezone.now() + time_varation)
    
    return redirect('user_profile', id=user.id)

def check_out(request, id):
    user = get_object_or_404(Details, id=id)
    
    time_varation = timedelta(hours=5, minutes=30)
    
    attendance = Attendance.objects.filter(user=user, check_in_time__isnull=False, check_out_time__isnull=True).first()
    
    if attendance:
        attendance.check_out_time = timezone.now() + time_varation
        attendance.save()
        messages.success(request, "Checked out successfully!")
        print(f"Checked out at: {attendance.check_out_time}")  
    else:
        messages.error(request, "You haven't checked in yet!")
        print("Check out failed: No check-in record found") 

    if request.user.is_superuser:
        return redirect('user_details', id=user.id)
    else:
        return redirect('user_profile', id=user.id)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = get_object_or_404(Details, user_name=username)
        return redirect('user_profile', id=user.id)
    return render(request, 'user_login.html')

def user_profile(request, id):
    user_obj = get_object_or_404(Details, id=id)
    today = timezone.now().date()
    days_left = (user_obj.end_date - today).days
    
    workouts = WorkoutRoutine.objects.filter(user=user_obj)
    user_attendance = Attendance.objects.filter(user=user_obj).order_by('-check_in_time') #descending order.
    
    can_check_in = True
    if user_attendance.exists():
        last_attendance = user_attendance.first()
        if not last_attendance.check_out_time:
            can_check_in = False
    
    context = {
        'user': user_obj,
        'days_left': days_left,
        'workouts': workouts,
        'user_attendance': user_attendance,
        'can_check_in': can_check_in,
    }
    
    return render(request, 'user_profile.html', context)


def home (request):
    return render(request, 'home.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def calculate_bmi(request):
    result = None
    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height_cm = form.cleaned_data['height']
            
            height_m = height_cm / 100
            
            if height_m > 0:
                bmi = weight / (height_m ** 2)
                
                if bmi < 18.5:
                    category = 'Underweight'
                    advice = 'Do bulking and muscle gaining.'
                elif 18.5 <= bmi < 24.9:
                    category = 'Normal weight'
                    advice = 'Do strength training.'
                elif 25 <= bmi < 29.9:
                    category = 'Overweight'
                    advice = 'Do more cardio, abs, and maintain a diet plan.'
                else:
                    category = 'Obesity'
                    advice = 'Start your weight loss journey with a diet and fat-burning workout sessions.'
                
                result = (bmi, category, advice)
            else:
                form.add_error(None, "Height must be greater than zero.")
    else:
        form = BMICalculatorForm()

    return render(request, 'calculate_bmi.html', {
        'form': form,
        'result': result,
    })
