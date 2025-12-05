from rest_framework import serializers

class SimulasiKPRInputSerializer(serializers.Serializer):
    harga_properti = serializers.FloatField()
    penghasilan = serializers.FloatField()
    dp_percent = serializers.FloatField()
    tenor_bulan = serializers.IntegerField()
    bunga_fix = serializers.FloatField()
    periode_fix = serializers.IntegerField()
    bunga_floating = serializers.FloatField()