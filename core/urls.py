from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, AttendanceViewSet, PerformanceViewSet, DepartmentViewSet



router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'performance', PerformanceViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


# core/urls.py
from .views import attendance_summary_chart, attendance_chart_page

urlpatterns += [
    path('charts/attendance-summary/', attendance_summary_chart, name='attendance-summary-chart'),
    path('charts/attendance/', attendance_chart_page, name='attendance-chart-page'),
]







