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
from rest_framework.permissions import AllowAny

User = get_user_model()

class SignupView(APIView):
    permission_classes = [AllowAny]
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
    try:
        user = request.user
        custom_user = user.customuser  # Ensure this exists

        data = {
            "username": user.username,
            "email": user.email,
            "height": custom_user.height,
            "weight": custom_user.weight,
            "goals": list(custom_user.goal_set.values()),  # ✅ Corrected
            "workouts": list(custom_user.workout_set.values()),  # ✅ Corrected
        }
        return Response(data, status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist:
        return Response({"error": "Custom user profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class WorkoutViewSet(viewsets.ModelViewSet):
#     serializer_class = WorkoutSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Workout.objects.filter(user=self.request.user.customuser)  
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)


# # Goal ViewSet
# class GoalViewSet(viewsets.ModelViewSet):
#     serializer_class = GoalSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Goal.objects.filter(user=self.request.user.customuser) 

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)

# # Daily Activity ViewSet
# class DailyActivityViewSet(viewsets.ModelViewSet):
#     serializer_class = DailyActivitySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return DailyActivity.objects.filter(user=self.request.user.customuser)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)

# # Progress Tracking ViewSet
# class ProgressViewSet(viewsets.ModelViewSet):
#     serializer_class = ProgressSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Progress.objects.filter(user=self.request.user.customuser)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)

# class MealViewSet(viewsets.ModelViewSet):
#     serializer_class = MealSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Meal.objects.filter(user=self.request.user.customuser)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)

# class WaterIntakeViewSet(viewsets.ModelViewSet):
#     serializer_class = WaterIntakeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return WaterIntake.objects.filter(user=self.request.user.customuser)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)

# class SleepRecordViewSet(viewsets.ModelViewSet):
#     serializer_class = SleepRecordSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return SleepRecord.objects.filter(user=self.request.user.customuser)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user.customuser)

class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only workouts for the authenticated user
        return Workout.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a workout
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Goal ViewSet
class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only goals for the authenticated user
        return Goal.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a goal
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Daily Activity ViewSet
class DailyActivityViewSet(viewsets.ModelViewSet):
    serializer_class = DailyActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only daily activities for the authenticated user
        return DailyActivity.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a daily activity
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Progress ViewSet
class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only progress records for the authenticated user
        return Progress.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a progress record
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Meal ViewSet
class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only meals for the authenticated user
        return Meal.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a meal
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Water Intake ViewSet
class WaterIntakeViewSet(viewsets.ModelViewSet):
    serializer_class = WaterIntakeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only water intake records for the authenticated user
        return WaterIntake.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a water intake record
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Sleep Record ViewSet
class SleepRecordViewSet(viewsets.ModelViewSet):
    serializer_class = SleepRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only sleep records for the authenticated user
        return SleepRecord.objects.filter(user=self.request.user.customuser)

    def perform_create(self, serializer):
        # Automatically set the user to the current user when creating a sleep record
        serializer.save(user=self.request.user.customuser)

    def update(self, request, *args, **kwargs):
        # Handle PUT and PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)