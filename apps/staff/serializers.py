from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.departments.models import Department
from .models import Staff

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'is_active']


class StaffSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.get_full_name')
    user_email = serializers.ReadOnlyField(source='user.email')
    department_name = serializers.ReadOnlyField(source='department.name')
    
    # Primary key field for POST/PUT requests
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=True
    )

    class Meta:
        model = Staff
        fields = [
            'id', 'user_name', 'user_email', 
            'department', 'department_name',
            'job_title', 'gender', 'employment_type', 
            'date_joined', 'salary'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for new user self-registration.
    Automatically creates a User and an associated Staff profile record.
    """
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # 1. Create the user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # 2. Check if user model supports role attribute
        if hasattr(user, 'role'):
            user.role = 'EMPLOYEE'
            user.save()

        # 3. Create initial staff profile linked to this user with current date
        Staff.objects.create(
            user=user,
            job_title="New Staff Member",
            employment_type="FT",
            salary=0.00,
            date_joined=timezone.now().date()
        )
        
        return user