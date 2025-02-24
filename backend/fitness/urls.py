from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    WorkoutViewSet, GoalViewSet, DailyActivityViewSet, ProgressViewSet,
    SignupView, user_dashboard
)

# Create a router and register ViewSets
router = SimpleRouter()
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'daily-activities', DailyActivityViewSet, basename='daily-activity')
router.register(r'progress', ProgressViewSet, basename='progress')

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Authentication Endpoints
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
