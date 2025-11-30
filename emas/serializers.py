from decimal import Decimal
from rest_framework import serializers
from .models import GoldCalculation


class GoldCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldCalculation
        fields = [
            'id',
            'mode',
            'price_choice',
            'grams_input',
            'rupiah_input',
            'price_per_gram',
            'result_rupiah',
            'result_grams',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'result_rupiah',
            'result_grams',
            'created_at',
        ]

    def validate(self, attrs):
        """
        Validasi:
        - mode wajib
        - price_per_gram > 0
        - emas_to_rupiah → butuh grams_input
        - rupiah_to_emas → butuh rupiah_input
        """
        mode = attrs.get('mode') or (self.instance.mode if self.instance else None)
        price_per_gram = attrs.get('price_per_gram') or (
            self.instance.price_per_gram if self.instance else None
        )
        grams_input = attrs.get('grams_input', getattr(self.instance, 'grams_input', None))
        rupiah_input = attrs.get('rupiah_input', getattr(self.instance, 'rupiah_input', None))

        if not mode:
            raise serializers.ValidationError("mode wajib diisi.")

        if not price_per_gram or price_per_gram <= 0:
            raise serializers.ValidationError("price_per_gram harus lebih dari 0.")

        if mode == 'emas_to_rupiah':
            if grams_input is None:
                raise serializers.ValidationError(
                    "Untuk mode emas_to_rupiah, field grams_input wajib diisi."
                )
        elif mode == 'rupiah_to_emas':
            if rupiah_input is None:
                raise serializers.ValidationError(
                    "Untuk mode rupiah_to_emas, field rupiah_input wajib diisi."
                )
        else:
            raise serializers.ValidationError(
                "mode harus 'emas_to_rupiah' atau 'rupiah_to_emas'."
            )

        return attrs

    def _apply_calculation(self, instance):
        """
        Hitung result_rupiah / result_grams berdasarkan mode.
        """
        price = Decimal(instance.price_per_gram)

        if instance.mode == 'emas_to_rupiah':
            grams = Decimal(instance.grams_input or 0)
            rupiah = grams * price
            instance.result_rupiah = rupiah
            instance.result_grams = None
        else:  # rupiah_to_emas
            rupiah = Decimal(instance.rupiah_input or 0)
            if price == 0:
                instance.result_grams = Decimal('0')
            else:
                grams = rupiah / price
                instance.result_grams = grams
            instance.result_rupiah = None

    def create(self, validated_data):
        instance = GoldCalculation(**validated_data)
        self._apply_calculation(instance)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for field in [
            'mode',
            'price_choice',
            'grams_input',
            'rupiah_input',
            'price_per_gram',
        ]:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        self._apply_calculation(instance)
        instance.save()
        return instance
