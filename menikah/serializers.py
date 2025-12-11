# menikah/serializers.py
from rest_framework import serializers
from .models import MarriageCalculation


class MarriageCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarriageCalculation
        fields = [
            'id',
            'user',
            # Input fields
            'target_cost',
            'current_saving',
            'months_to_event',
            'monthly_invest',
            'expected_return_pct',
            # Output fields
            'future_value',
            'gap_amount',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'future_value',
            'gap_amount',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]

    def validate_target_cost(self, value):
        if value <= 0:
            raise serializers.ValidationError("Biaya target pernikahan harus lebih dari 0")
        return value

    def validate_current_saving(self, value):
        if value < 0:
            raise serializers.ValidationError("Tabungan tidak boleh negatif")
        return value

    def validate_months_to_event(self, value):
        if value <= 0:
            raise serializers.ValidationError("Waktu ke pernikahan harus lebih dari 0 bulan")
        return value

    def validate_monthly_invest(self, value):
        if value < 0:
            raise serializers.ValidationError("Investasi bulanan tidak boleh negatif")
        return value

    def validate_expected_return_pct(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Return ekspektasi harus antara 0-100%")
        return value
