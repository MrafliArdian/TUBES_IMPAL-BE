from rest_framework import serializers
from .models import (
    User, 
    Role, 
    UserRole, 
    Calculation, 
    Article,
    ChildEducationCalculation, 
    KprCalculation, 
    EmergencyFundCalculation, 
    PensionCalculation, 
    MarriageCalculation,
    VehicleCalculation,
    GoldCalculation
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone', 'password_hash'] 
        
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']

class UserRoleSerializer(serializers.ModelSerializer):
    # Menggunakan ID dari User dan Role untuk POST
    user_id = serializers.IntegerField(write_only=True)
    role_id = serializers.IntegerField(write_only=True)
    
    # Field read-only untuk tampilan (opsional, tapi bagus)
    user_email = serializers.ReadOnlyField(source='user.email')
    role_name = serializers.ReadOnlyField(source='role.role_name')

    class Meta:
        model = UserRole
        fields = ['user_id', 'role_id', 'user_email', 'role_name']

class CalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Calculation
        fields = [
            'calc_id', 
            'user_id', 
            'calculator_type', 
            'title', 
            'input_data', 
            'result_data', 
            'created_at'
        ]
        read_only_fields = ['calc_id', 'created_at']

class ChildEducationCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ChildEducationCalculation
        fields = [
            'id', 
            'user_id', 
            'child_age_years', 
            'college_years_ahead', 
            'current_tuition', 
            'inflation_pct', 
            'monthly_invest', 
            'expected_return_pct', 
            'total_future_need',
            'monthly_needed',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class KprCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = KprCalculation
        fields = [
            'id', 
            'user_id', 
            'house_price', 
            'down_payment', 
            'tenor_months', 
            'fix_rate_pct', 
            'fix_period_months', 
            'floating_rate_pct',
            'monthly_installment',
            'total_interest_fix',
            'total_interest_floating',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class EmergencyFundCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = EmergencyFundCalculation
        fields = [
            'id', 
            'user_id', 
            'monthly_expense', 
            'target_months', 
            'current_fund', 
            'monthly_invest', 
            'expected_return_pct',
            'target_amount',
            'months_to_reach',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class PensionCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PensionCalculation
        fields = [
            'id', 
            'user_id', 
            'current_age', 
            'retire_age', 
            'monthly_expense_now', 
            'inflation_pct', 
            'expected_return_pct', 
            'pension_years',
            'monthly_invest',
            'total_need_at_retire',
            'estimated_portfolio',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class MarriageCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MarriageCalculation
        fields = [
            'id', 
            'user_id', 
            'target_cost', 
            'current_saving', 
            'months_to_event', 
            'monthly_invest', 
            'expected_return_pct',
            'gap_now',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class VehicleCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = VehicleCalculation
        fields = [
            'id', 
            'user_id', 
            'vehicle_price', 
            'down_payment', 
            'current_saving', 
            'monthly_invest', 
            'expected_return_pct',
            'needed_amount',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class GoldCalculationSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GoldCalculation
        fields = [
            'id', 
            'user_id', 
            'mode', 
            'price_choice', 
            'grams_input', 
            'rupiah_input', 
            'price_per_gram', 
            'result_rupiah',
            'result_grams',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class ArticleSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Article
        fields = [
            'article_id', 
            'author_id', 
            'title', 
            'content', 
            'image_url', 
            'created_at'
        ]
        read_only_fields = ['article_id', 'created_at']