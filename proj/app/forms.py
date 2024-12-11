from django import forms
from .models import Details, WorkoutRoutine

class UserForm(forms.ModelForm):
    class Meta:
        model = Details
        fields = ['name', 'user_name', 'email', 'phone_number', 'start_date', 'end_date', 'payment_status']
        labels = {
            'start_date': 'Start Date [YYYY-MM-DD]',
            'end_date': 'End Date [YYYY-MM-DD]',
        }

class WorkoutRoutineForm(forms.ModelForm):
    class Meta:
        model = WorkoutRoutine
        fields = ['workout_name', 'monday_exercises', 'tuesday_exercises', 'wednesday_exercises', 'thursday_exercises', 'friday_exercises', 'saturday_exercises']

class BMICalculatorForm(forms.Form):
    weight = forms.DecimalField(label='Weight (kg)', decimal_places=2, max_digits=5, min_value=0)
    height = forms.DecimalField(label='Height (m)', decimal_places=2, max_digits=5, min_value=0)

