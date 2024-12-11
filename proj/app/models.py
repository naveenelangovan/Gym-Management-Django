from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Details(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.BigIntegerField(
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    payment_status = models.BooleanField(default=False) 

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"User Name: {self.user_name}\n"
            f"Email: {self.email}\n"
            f"Phone Number: {self.phone_number}\n"
            f"Start Date [YYYY-MM-DD]: {self.start_date}\n"
            f"End Date [YYYY-MM-DD]: {self.end_date}\n"
            f"Payment Status: {self.payment_status}"
        )

class WorkoutRoutine(models.Model):
    user = models.ForeignKey(Details, on_delete=models.CASCADE)# Django's ORM (Object-Relational Mapping) -all objects that reference it will also be deleted.
    workout_name = models.CharField(max_length=100)
    monday_exercises = models.TextField(blank=True, null=True) #db,frm vld
    tuesday_exercises = models.TextField(blank=True, null=True)
    wednesday_exercises = models.TextField(blank=True, null=True)
    thursday_exercises = models.TextField(blank=True, null=True)
    friday_exercises = models.TextField(blank=True, null=True)
    saturday_exercises = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"Workout Name: {self.workout_name}\n"
            f"Monday: {self.monday_exercises}\n"
            f"Tuesday: {self.tuesday_exercises}\n"
            f"Wednesday: {self.wednesday_exercises}\n"
            f"Thursday: {self.thursday_exercises}\n"
            f"Friday: {self.friday_exercises}\n"
            f"Saturday: {self.saturday_exercises}"
        )

class Attendance(models.Model):
    user = models.ForeignKey(Details, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - Check in: {self.check_in_time} - Check out: {self.check_out_time}"
