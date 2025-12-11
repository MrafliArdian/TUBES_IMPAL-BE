# kendaraan/serializers.py
from rest_framework import serializers
from .models import VehicleCalculation


class VehicleCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCalculation
        fields = [
            'id',
            'user',
            # Input fields
            'vehicle_price',
            'down_payment',
            'current_saving',
            'monthly_invest',
            'expected_return_pct',
            'investment_period_months',
            # Output fields
            'needed_amount',
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
            'needed_amount',
            'future_value',
            'gap_amount',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]

    def validate_vehicle_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Harga kendaraan harus lebih dari 0")
        return value

    def validate_down_payment(self, value):
        if value < 0:
            raise serializers.ValidationError("DP tidak boleh negatif")
        return value

    def validate_current_saving(self, value):
        if value < 0:
            raise serializers.ValidationError("Tabungan tidak boleh negatif")
        return value

    def validate_monthly_invest(self, value):
        if value < 0:
            raise serializers.ValidationError("Investasi bulanan tidak boleh negatif")
        return value

    def validate_expected_return_pct(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Return ekspektasi harus antara 0-100%")
        return value

    def validate_investment_period_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("Periode investasi harus lebih dari 0 bulan")
        return value
