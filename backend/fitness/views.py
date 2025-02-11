views.py-
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

        # Check if user exists
        user = User.objects.filter(username=username, email=email).first()
        if user:
            return Response({
                "message": "User already exists",
                "user_details": {
                    "username": user.username,
                    "email": user.email,
                    "age": user.age,
                    "height": user.height,
                    "weight": user.weight,
                }
            }, status=status.HTTP_200_OK)

        # If user does not exist, collect all required details
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user = request.user
    data = {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "height": user.height,
        "weight": user.weight,
        "goals": list(user.goal_set.values()),  # Fetch user's goals
        "workouts": list(user.workout_set.values()),  # Fetch user's workouts
    }
    return Response(data, status=status.HTTP_200_OK)


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Goal ViewSet
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Daily Activity ViewSet
class DailyActivityViewSet(viewsets.ModelViewSet):
    queryset = DailyActivity.objects.all()
    serializer_class = DailyActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Progress Tracking ViewSet
class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
