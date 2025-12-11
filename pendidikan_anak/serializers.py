# pendidikan_anak/serializers.py
from rest_framework import serializers
from .models import ChildEducationCalculation


class ChildEducationCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildEducationCalculation
        fields = [
            'id',
            'user',
            # Input fields
            'child_age_years',
            'college_entry_age',
            'current_tuition_per_year',
            'college_duration_years',
            'education_inflation_pct',
            'current_saving',
            'monthly_invest',
            'expected_return_pct',
            # Output fields
            'years_until_college',
            'future_tuition_per_year',
            'total_education_need',
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
            'years_until_college',
            'future_tuition_per_year',
            'total_education_need',
            'future_value',
            'gap_amount',
            'status',
            'is_suitable',
            'recommendation',
            'created_at',
        ]

    def validate_child_age_years(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Usia anak harus antara 0-100 tahun")
        return value

    def validate_college_entry_age(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Usia masuk kuliah harus antara 0-100 tahun")
        return value

    def validate(self, data):
        # Validasi usia anak harus lebih kecil dari usia masuk kuliah
        if data.get('child_age_years') and data.get('college_entry_age'):
            if data['child_age_years'] >= data['college_entry_age']:
                raise serializers.ValidationError(
                    "Usia anak saat ini harus lebih kecil dari usia masuk kuliah"
                )
        return data

    def validate_current_tuition_per_year(self, value):
        if value <= 0:
            raise serializers.ValidationError("Biaya kuliah per tahun harus lebih dari 0")
        return value

    def validate_college_duration_years(self, value):
        if value <= 0:
            raise serializers.ValidationError("Durasi kuliah harus lebih dari 0 tahun")
        return value

    def validate_education_inflation_pct(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Inflasi pendidikan harus antara 0-100%")
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
