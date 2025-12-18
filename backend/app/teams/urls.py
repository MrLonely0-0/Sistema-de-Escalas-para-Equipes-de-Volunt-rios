"""
URLs for teams app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, RoleViewSet, VolunteerRoleViewSet, AvailabilityViewSet

router = DefaultRouter()
router.register(r'', TeamViewSet, basename='teams')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'volunteer-roles', VolunteerRoleViewSet, basename='volunteer-roles')
router.register(r'availability', AvailabilityViewSet, basename='availability')

urlpatterns = [
    path('', include(router.urls)),
]
