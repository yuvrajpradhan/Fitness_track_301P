from rest_framework import serializers
from .models import CustomUser, Workout, Goal, DailyActivity, Progress, Meal, WaterIntake, SleepRecord
from django.contrib.auth.models import User

class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')  # ✅ Get from User model
    email = serializers.EmailField(source='user.email')  # ✅ Get from User model
    password = serializers.CharField(write_only=True)  # ✅ Ensure password is write-only

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'date_of_birth', 'height', 'weight']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract user-related data
        user_data = validated_data.pop('user', {})
        
        # Create User first
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email']
        )
        user.set_password(validated_data.pop('password'))  # ✅ Hash password
        user.save()

        # Create CustomUser linked to User
        custom_user = CustomUser.objects.create(
            user=user,
            date_of_birth=validated_data.get('date_of_birth'),
            height=validated_data.get('height'),
            weight=validated_data.get('weight'),
        )
        return custom_user


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