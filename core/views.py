
from rest_framework import viewsets
from .models import Employee, Attendance, Performance, Department
from .serializers import EmployeeSerializer, AttendanceSerializer, PerformanceSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    # queryset = Employee.objects.all()
    queryset = Employee.objects.all().order_by('id')  # or any consistent field
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]







# core/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Attendance
from django.db.models import Count
import calendar

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_summary_chart(request):
    today = now().date()
    month_start = today.replace(day=1)
    month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    data = (
        Attendance.objects.filter(date__range=(month_start, month_end))
        .values('status')
        .annotate(count=Count('id'))
    )

    chart_data = {
        "labels": [entry["status"] for entry in data],
        "datasets": [{
            "label": "Attendance Status",
            "data": [entry["count"] for entry in data],
            "backgroundColor": [
                "#36A2EB",  # Present
                "#FF6384",  # Absent
                "#FFCE56",  # Leave
            ],
        }]
    }

    return Response(chart_data)

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

@login_required
def attendance_chart_page(request):
    return render(request, 'core/attendance_chart.html')



# core/views.py
from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employees_per_department(request):
    data = (
        Department.objects.annotate(count=Count('employee'))
        .values('name', 'count')
    )
    chart_data = {
        "labels": [d["name"] for d in data],
        "datasets": [{
            "label": "Employees",
            "data": [d["count"] for d in data],
            "backgroundColor": "#36A2EB",
        }]
    }
    return Response(chart_data)


from django.db.models import Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def avg_performance_by_department(request):
    data = (
        Department.objects
        .annotate(avg_rating=Avg('employee__performance__rating'))
        .values('name', 'avg_rating')
    )
    chart_data = {
        "labels": [d["name"] for d in data],
        "datasets": [{
            "label": "Avg Rating",
            "data": [round(d["avg_rating"] or 0, 2) for d in data],
            "backgroundColor": "#FF9F40",
        }]
    }
    return Response(chart_data)


