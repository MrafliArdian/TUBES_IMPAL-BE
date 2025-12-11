# simulasi_kpr/serializers.py
from rest_framework import serializers
from .models import SimulasiKPR


class SimulasiKPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulasiKPR
        fields = [
            'id',
            'user',
            # Input fields
            'property_price',
            'monthly_income',
            'dp_percentage',
            'loan_term_months',
            'fixed_interest_rate',
            'fixed_period_months',
            'floating_interest_rate',
            # Output fields
            'dp_amount',
            'loan_amount',
            'monthly_installment_fixed',
            'monthly_installment_floating',
            'income_to_installment_ratio',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'dp_amount',
            'loan_amount',
            'monthly_installment_fixed',
            'monthly_installment_floating',
            'income_to_installment_ratio',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]

    def validate_property_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Harga properti harus lebih dari 0")
        return value

    def validate_monthly_income(self, value):
        if value <= 0:
            raise serializers.ValidationError("Pendapatan bulanan harus lebih dari 0")
        return value

    def validate_dp_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Persentase DP harus antara 0-100%")
        return value

    def validate_loan_term_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("Tenor KPR harus lebih dari 0 bulan")
        return value

    def validate_fixed_interest_rate(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Suku bunga fixed harus antara 0-100%")
        return value

    def validate_fixed_period_months(self, value):
        if value < 0:
            raise serializers.ValidationError("Periode bunga fixed tidak boleh negatif")
        return value

    def validate_floating_interest_rate(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Suku bunga floating harus antara 0-100%")
        return value

    def validate(self, data):
        # Validasi periode fixed tidak boleh lebih lama dari tenor
        if data.get('fixed_period_months') and data.get('loan_term_months'):
            if data['fixed_period_months'] > data['loan_term_months']:
                raise serializers.ValidationError(
                    "Periode bunga fixed tidak boleh lebih lama dari tenor KPR"
                )
        return data
