from django.urls import path
from . import views

urlpatterns = [
    # Web Dashboard Reports
    path('reports/', views.staff_report_view, name='staff_reports'),
    
    # REST API Endpoints (v1)
    path('api/v1/members/', views.StaffListAPIView.as_view(), name='api_staff_list'),
    path('api/v1/members/<int:pk>/', views.StaffDetailAPIView.as_view(), name='api_staff_detail'),
    path('api/v1/departments/', views.DepartmentListAPIView.as_view(), name='api_department_list'),
    path('api/v1/analytics/', views.StaffAnalyticsAPIView.as_view(), name='api_staff_analytics'),

    # Report Export Endpoints
    path('api/v1/export/csv/', views.StaffExportCSVAPIView.as_view(), name='api_staff_export_csv'),
    path('api/v1/export/excel/', views.StaffExportExcelAPIView.as_view(), name='api_staff_export_excel'),
    path('api/v1/auth/register/', views.RegisterAPIView.as_view(), name='api_register'),
]