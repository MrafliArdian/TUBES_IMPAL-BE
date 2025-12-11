# dana_pensiun/serializers.py
from rest_framework import serializers
from .models import PensionCalculation


class PensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PensionCalculation
        fields = [
            'id',
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
            'is_suitable',
            'recommendation',
            'created_at',
        ]
        # field hasil hitung + metadata dibaca saja
        read_only_fields = [
            'id',
            'total_need_at_retire',
            'estimated_portfolio',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]
