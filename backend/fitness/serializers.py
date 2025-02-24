from rest_framework import serializers
from .models import CustomUser, Workout, Goal, DailyActivity, Progress, Meal, WaterIntake, SleepRecord
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'date_of_birth', 'height', 'weight']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth'),
            height=validated_data.get('height'),
            weight=validated_data.get('weight'),
        )
        return user


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'user', 'name', 'duration', 'calories_burned', 'date']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'goal_name', 'target_value', 'current_value', 'unit', 'deadline', 'completed']

class DailyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyActivity
        fields = ['id', 'user', 'steps', 'distance', 'calories_burned', 'date']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'user', 'weight', 'body_fat_percentage', 'muscle_mass', 'date']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'user', 'name', 'calories', 'protein', 'carbs', 'fat', 'date']

class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = ['id', 'user', 'amount', 'date']

class SleepRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepRecord
        fields = ['id', 'user', 'sleep_start', 'sleep_end', 'quality_score', 'duration']
        read_only_fields = ['duration']