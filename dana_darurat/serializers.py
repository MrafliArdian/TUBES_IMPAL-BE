# dana_darurat/serializers.py
from rest_framework import serializers
from .models import EmergencyFundCalculation


class EmergencyFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyFundCalculation
        fields = [
            'id',
            'monthly_expense',
            'months_to_save',
            'current_emergency_fund',
            'monthly_invest',
            'expected_return_pct',
            'needed_fund',
            'future_value',
            'gap_amount',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]
        # field hasil perhitungan dibaca saja
        read_only_fields = [
            'id',
            'needed_fund',
            'future_value',
            'gap_amount',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]
