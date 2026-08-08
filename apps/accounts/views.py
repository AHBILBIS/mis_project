from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg

# Django REST Framework Imports
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.decorators import role_required
from apps.departments.models import Department
from .models import Staff
from .serializers import StaffSerializer, DepartmentSerializer, RegisterSerializer
from .permissions import IsAdminOrReadOnly
from .exports import export_staff_csv, export_staff_excel


# ==========================================
# 1. HTML Authentication & User Views
# ==========================================

def user_login(request):
    """
    Standard HTML login view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """
    Renders the primary dashboard for the logged-in user.
    """
    user = request.user
    staff_profile = getattr(user, 'staff_profile', None)

    context = {
        'user': user,
        'staff_profile': staff_profile,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
@role_required(['ADMIN', 'MANAGER'])
def manager_only_view(request):
    """
    Restricted manager panel view.
    """
    return render(request, 'accounts/manager_panel.html')


# ==========================================
# 2. HTML Management Dashboard View
# ==========================================

@login_required
@role_required(['ADMIN', 'MANAGER'])
def staff_report_view(request):
    """
    Management report generating aggregated staff statistics and department analytics.
    """
    total_staff = Staff.objects.count()
    total_departments = Department.objects.filter(is_active=True).count()
    total_payroll = Staff.objects.aggregate(total=Sum('salary'))['total'] or 0.00
    avg_salary = Staff.objects.aggregate(avg=Avg('salary'))['avg'] or 0.00

    selected_dept_id = request.GET.get('department')
    staff_list = Staff.objects.select_related('user', 'department').all()
    
    if selected_dept_id:
        staff_list = staff_list.filter(department_id=selected_dept_id)

    department_stats = Department.objects.annotate(
        member_count=Count('staff_members'),
        dept_payroll=Sum('staff_members__salary')
    )

    context = {
        'total_staff': total_staff,
        'total_departments': total_departments,
        'total_payroll': total_payroll,
        'avg_salary': avg_salary,
        'staff_list': staff_list,
        'departments': Department.objects.all(),
        'department_stats': department_stats,
        'selected_dept': selected_dept_id,
    }
    return render(request, 'staff/reports.html', context)


# ==========================================
# 3. Authentication & Self-Registration View
# ==========================================

class RegisterAPIView(generics.CreateAPIView):
    """
    Public API endpoint for new members to self-register via a link.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Registration successful.",
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)


# ==========================================
# 4. REST API Views
# ==========================================

class StaffListAPIView(generics.ListCreateAPIView):
    """
    API endpoint returning staff members with role-based restrictions.
    """
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'employment_type']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'job_title']
    ordering_fields = ['date_joined', 'salary']
    ordering = ['-date_joined']

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or getattr(user, 'role', '') in ['ADMIN', 'MANAGER']:
            return Staff.objects.select_related('user', 'department').all()
            
        return Staff.objects.select_related('user', 'department').filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StaffDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific staff member by ID.
    """
    queryset = Staff.objects.select_related('user', 'department').all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


class DepartmentListAPIView(APIView):
    """
    API endpoint returning active departments in JSON format.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        departments = Department.objects.filter(is_active=True)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffAnalyticsAPIView(APIView):
    """
    API endpoint returning aggregated staff and payroll metrics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "total_staff": Staff.objects.count(),
            "total_payroll": Staff.objects.aggregate(total=Sum('salary'))['total'] or 0.00,
            "avg_salary": Staff.objects.aggregate(avg=Avg('salary'))['avg'] or 0.00,
            "department_counts": list(
                Department.objects.annotate(member_count=Count('staff_members')).values('name', 'member_count')
            )
        }
        return Response(data, status=status.HTTP_200_OK)


# ==========================================
# 5. Report Export API Views
# ==========================================

class StaffExportCSVAPIView(APIView):
    """
    Export staff list as a CSV document.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Staff.objects.select_related('user', 'department').all()
        
        dept_id = request.GET.get('department')
        emp_type = request.GET.get('employment_type')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        if emp_type:
            queryset = queryset.filter(employment_type=emp_type)

        return export_staff_csv(queryset)


class StaffExportExcelAPIView(APIView):
    """
    Export staff list as a formatted Excel (.xlsx) document.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Staff.objects.select_related('user', 'department').all()
        
        dept_id = request.GET.get('department')
        emp_type = request.GET.get('employment_type')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        if emp_type:
            queryset = queryset.filter(employment_type=emp_type)

        return export_staff_excel(queryset)