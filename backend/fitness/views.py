from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Workout, Goal, DailyActivity, Progress
from .serializers import WorkoutSerializer, GoalSerializer, DailyActivitySerializer, ProgressSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()
class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if user already exists
        user = User.objects.filter(username=username, email=email).first()
        if user:
            return Response({
                "message": "User already exists",
                "user_details": {
                    "username": user.username,
                    "email": user.email,
                    "date_of_birth": user.customuser.date_of_birth,
                    "height": user.customuser.height,
                    "weight": user.customuser.weight,
                }
            }, status=status.HTTP_200_OK)

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create CustomUser linked to User
        custom_user = CustomUser.objects.create(
            user=user,
            date_of_birth=request.data.get('date_of_birth'),
            height=request.data.get('height'),
            weight=request.data.get('weight')
        )

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)




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
        return DailyActivity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)

# Progress Tracking ViewSet
class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Progress.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.customuser)
