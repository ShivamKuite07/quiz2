
from rest_framework import viewsets
from .models import Employee, Attendance, Performance, Department
from .serializers import EmployeeSerializer, AttendanceSerializer, PerformanceSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
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






