from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    full_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "full_name", "phone_number")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password dan konfirmasi tidak sama."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            role='USER'  # Default role adalah USER
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk response user info (tanpa password)"""
    class Meta:
        model = User
        fields = ("id", "username", "email", "full_name", "phone_number", "role", "date_joined")
        read_only_fields = ("id", "role", "date_joined")


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer lengkap untuk admin view - include semua info user"""
    total_calculations = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            "id", "username", "email", "full_name", "phone_number", 
            "role", "is_active", "date_joined", "last_login", "total_calculations"
        )
        read_only_fields = fields
    
    def get_total_calculations(self, obj):
        """Hitung total perhitungan dari semua kalkulator"""
        total = 0
        # Count dari semua related calculations
        if hasattr(obj, 'emergency_fund_calculations'):
            total += obj.emergency_fund_calculations.count()
        if hasattr(obj, 'pension_calculations'):
            total += obj.pension_calculations.count()
        if hasattr(obj, 'goldcalculation_set'):
            total += obj.goldcalculation_set.count()
        return total


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer untuk change password.
    User harus provide old password untuk security.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, 
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password baru tidak sama."}
            )
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password lama salah.")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer untuk update profile user.
    Username tidak bisa diubah (read-only).
    """
    username = serializers.CharField(read_only=True)  # Username immutable
    role = serializers.CharField(read_only=True)  # Role tidak bisa diubah sendiri
    
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'phone_number', 'role')
        read_only_fields = ('username', 'role')


# ============================
# Kalkulator Finansial
# ============================

class DanaDaruratSerializer(serializers.Serializer):
    pengeluaran_wajib_bulanan = serializers.FloatField()
    bulan_mengumpulkan = serializers.IntegerField(min_value=1)
    dana_darurat_saat_ini = serializers.FloatField()
    target_investasi_bulanan = serializers.FloatField()
    return_tahunan = serializers.FloatField(help_text="dalam persen, misal 10 untuk 10% per tahun")


class PendidikanAnakSerializer(serializers.Serializer):
    usia_anak_sekarang = serializers.IntegerField(min_value=0)
    usia_anak_masuk_kuliah = serializers.IntegerField(min_value=1)
    biaya_kuliah_saat_ini_per_tahun = serializers.FloatField()
    lama_kuliah_tahun = serializers.IntegerField(min_value=1)
    inflasi_pendidikan = serializers.FloatField(help_text="dalam persen/tahun")
    return_investasi = serializers.FloatField(help_text="dalam persen/tahun")
    dana_saat_ini = serializers.FloatField()
    investasi_bulanan = serializers.FloatField()


class MenikahSerializer(serializers.Serializer):
    target_biaya_menikah = serializers.FloatField()
    dana_saat_ini = serializers.FloatField()
    investasi_bulanan = serializers.FloatField()
    return_tahunan = serializers.FloatField(help_text="dalam persen/tahun")
    tahun_menuju_menikah = serializers.IntegerField(min_value=1)


class KendaraanSerializer(serializers.Serializer):
    harga_kendaraan = serializers.FloatField()
    dp_persen = serializers.FloatField(help_text="misal 20 untuk 20%")
    dana_saat_ini = serializers.FloatField()
    investasi_bulanan = serializers.FloatField()
    return_tahunan = serializers.FloatField(help_text="dalam persen/tahun")
    lama_investasi_bulan = serializers.IntegerField(min_value=1)


class SimulasiKPRSerializer(serializers.Serializer):
    harga_properti = serializers.FloatField()
    penghasilan_bulanan = serializers.FloatField()
    dp_persen = serializers.FloatField()
    tenor_bulan = serializers.IntegerField(min_value=1)
    bunga_fix = serializers.FloatField(help_text="persen/tahun")
    periode_fix_bulan = serializers.IntegerField(min_value=0)
    bunga_floating = serializers.FloatField(help_text="persen/tahun")


class DanaPensiunSerializer(serializers.Serializer):
    usia_sekarang = serializers.IntegerField(min_value=0)
    usia_pensiun = serializers.IntegerField(min_value=1)
    lama_pensiun_tahun = serializers.IntegerField(min_value=1)
    pengeluaran_bulanan_saat_ini = serializers.FloatField()
    inflasi_tahunan = serializers.FloatField(help_text="persen/tahun")
    return_investasi = serializers.FloatField(help_text="persen/tahun")
    dana_saat_ini = serializers.FloatField()
    investasi_bulanan = serializers.FloatField()


class KalkulatorEmasSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=["emas_ke_rupiah", "rupiah_ke_emas"])
    harga_emas_per_gram = serializers.FloatField()
    jumlah_gram = serializers.FloatField(required=False)
    jumlah_rupiah = serializers.FloatField(required=False)

    def validate(self, attrs):
        mode = attrs.get("mode")
        if mode == "emas_ke_rupiah" and attrs.get("jumlah_gram") is None:
            raise serializers.ValidationError("Untuk mode emas_ke_rupiah, 'jumlah_gram' wajib diisi.")
        if mode == "rupiah_ke_emas" and attrs.get("jumlah_rupiah") is None:
            raise serializers.ValidationError("Untuk mode rupiah_ke_emas, 'jumlah_rupiah' wajib diisi.")
        return attrs
