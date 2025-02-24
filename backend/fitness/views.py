from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Workout, Goal, DailyActivity, Progress, Meal, WaterIntake, SleepRecord
from .serializers import WorkoutSerializer, GoalSerializer, DailyActivitySerializer, ProgressSerializer,MealSerializer,WaterIntakeSerializer,SleepRecordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import CustomUser

User = get_user_model()

class SignupView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        
        try:
            # Check if user exists
            username = request.data.get('username')
            email = request.data.get('email')
            
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                # Check if CustomUser exists for this user
                try:
                    custom_user = existing_user.customuser
                    return Response({
                        "message": "User already exists",
                        "user_details": {
                            "username": existing_user.username,
                            "email": existing_user.email,
                            "date_of_birth": custom_user.date_of_birth,
                            "height": custom_user.height,
                            "weight": custom_user.weight,
                        }
                    }, status=status.HTTP_200_OK)
                except CustomUser.DoesNotExist:
                    # If CustomUser doesn't exist, create one
                    CustomUser.objects.create(
                        user=existing_user,
                        date_of_birth=request.data.get('date_of_birth'),
                        height=request.data.get('height'),
                        weight=request.data.get('weight')
                    )
                    return Response({
                        "message": "CustomUser profile created for existing user",
                        "user_details": {
                            "username": existing_user.username,
                            "email": existing_user.email,
                            "date_of_birth": request.data.get('date_of_birth'),
                            "height": request.data.get('height'),
                            "weight": request.data.get('weight'),
                        }
                    }, status=status.HTTP_200_OK)

            existing_email = User.objects.filter(email=email).first()
            if existing_email:
                return Response({
                    "error": "Email already registered"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate and save
            if serializer.is_valid(raise_exception=True):
                custom_user = serializer.save()
                
                return Response({
                    "message": "User registered successfully",
                    "user": {
                        "username": custom_user.user.username,
                        "email": custom_user.user.email,
                        "date_of_birth": custom_user.date_of_birth,
                        "height": custom_user.height,
                        "weight": custom_user.weight,
                    }
                }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "An unexpected error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user = request.user
    custom_user = user.customuser
    data = {
        "username": user.username,
        "email": user.email,
        "age": user.custom_user.age,
        "height": user.custom_user.height,
        "weight": user.custom_user.weight,
        "goals": list(custom_user.goal_set.values()),  # Fetch user's goals
        "workouts": list(user.workout_set.values()),  # Fetch user's workouts
    }
    return Response(data, status=status.HTTP_200_OK)


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user.customuser)  
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)


# Goal ViewSet
class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user.customuser) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)

# Daily Activity ViewSet
class DailyActivityViewSet(viewsets.ModelViewSet):
    serializer_class = DailyActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyActivity.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)

# Progress Tracking ViewSet
class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)

class WaterIntakeViewSet(viewsets.ModelViewSet):
    serializer_class = WaterIntakeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WaterIntake.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)

class SleepRecordViewSet(viewsets.ModelViewSet):
    serializer_class = SleepRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SleepRecord.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)