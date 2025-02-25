from django.db import models  # Required for defining models
from django.contrib.auth.models import User  # Import Django's built-in User model

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # in cm 
    weight = models.FloatField(null=True, blank=True)  # in kg

    def __str__(self):
        return self.user.username

# Workout Model
class Workout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()  # In minutes
    calories_burned = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

# Goal Model
class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=255)
    target_value = models.FloatField()  # e.g., target weight, target calories burned
    current_value = models.FloatField(default=0.0)
    unit = models.CharField(max_length=50)  # Example: "kg", "kcal"
    deadline = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.goal_name} - {self.user.username}"

# Daily Activity Model
class DailyActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField(default=0)
    distance = models.FloatField(default=0.0)  # in km
    calories_burned = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Activity - {self.user.username} ({self.date})"

# Progress Tracking Model
class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, blank=True)  # in kg
    body_fat_percentage = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Progress - {self.user.username} ({self.date})"

class Meal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()  # in grams
    carbs = models.FloatField()  # in grams
    fat = models.FloatField()  # in grams
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class WaterIntake(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField()  # in liters
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}L - {self.user.username} ({self.date})"
class SleepRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sleep_start = models.DateTimeField()
    sleep_end = models.DateTimeField()
    quality_score = models.IntegerField()  # Scale: 1-10

    @property
    def duration(self):
        return (self.sleep_end - self.sleep_start).total_seconds() / 3600  # Returns hours

    def str(self):
        return f"Sleep - {self.user.username} ({self.sleep_start.date()})"