
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from decimal import Decimal
import math

from .serializers import (
    DanaDaruratSerializer,
    PendidikanAnakSerializer,
    MenikahSerializer,
    KendaraanSerializer,
    SimulasiKPRSerializer,
    DanaPensiunSerializer,
    KalkulatorEmasSerializer
)




def validate_emergency_fund(self, data):
        """Validasi strategi Dana Darurat"""
        serializer = DanaDaruratSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        # Hitung target dana darurat (3-6x pengeluaran bulanan adalah standar)
        target_minimum = d['pengeluaran_wajib_bulanan'] * 3
        target_ideal = d['pengeluaran_wajib_bulanan'] * 6
        target_user = d['pengeluaran_wajib_bulanan'] * d['bulan_mengumpulkan']
        
        # Simulasi future value dengan investasi bulanan
        r_monthly = (d['return_tahunan'] / 100) / 12
        n = d['bulan_mengumpulkan']
        
        # FV = dana_saat_ini * (1 + r)^n + investasi_bulanan * [((1 + r)^n - 1) / r]
        fv_dana_saat_ini = d['dana_darurat_saat_ini'] * math.pow(1 + r_monthly, n)
        if r_monthly > 0:
            fv_investasi = d['target_investasi_bulanan'] * ((math.pow(1 + r_monthly, n) - 1) / r_monthly)
        else:
            fv_investasi = d['target_investasi_bulanan'] * n
            
        total_dana_akhir = fv_dana_saat_ini + fv_investasi
        
        # Evaluasi strategi
        is_valid = True
        recommendations = []
        warnings = []
        
        # Cek apakah target bulan cukup realistis
        if d['bulan_mengumpulkan'] < 3:
            warnings.append("Target waktu terlalu singkat (< 3 bulan). Pertimbangkan waktu lebih lama untuk hasil optimal.")
            is_valid = False
        elif d['bulan_mengumpulkan'] > 12:
            recommendations.append("Target waktu cukup baik (> 12 bulan), memberikan buffer untuk kondisi tak terduga.")
        
        # Cek apakah target dana sesuai standar
        if target_user < target_minimum:
            warnings.append(f"Target dana darurat Anda (Rp {target_user:,.0f}) di bawah minimum yang direkomendasikan (Rp {target_minimum:,.0f}).")
            recommendations.append(f"Tingkatkan target minimal {d['bulan_mengumpulkan']} bulan menjadi 3-6 bulan pengeluaran.")
            is_valid = False
        elif target_user >= target_ideal:
            recommendations.append("Target dana darurat Anda sudah sangat baik (≥ 6 bulan pengeluaran).")
        
        # Cek apakah investasi bulanan cukup
        if total_dana_akhir < target_user:
            kekurangan = target_user - total_dana_akhir
            investasi_tambahan = kekurangan / n
            warnings.append(f"Dengan investasi saat ini, Anda akan kekurangan Rp {kekurangan:,.0f}")
            recommendations.append(f"Tambahkan investasi bulanan sebesar Rp {investasi_tambahan:,.0f} untuk mencapai target.")
            is_valid = False
        else:
            kelebihan = total_dana_akhir - target_user
            recommendations.append(f"Strategi Anda akan menghasilkan surplus Rp {kelebihan:,.0f}. Bagus!")
        
        # Cek return investasi
        if d['return_tahunan'] < 3:
            warnings.append("Return investasi terlalu rendah (< 3%). Pertimbangkan instrumen dengan return lebih tinggi.")
        elif d['return_tahunan'] > 15:
            warnings.append("Return investasi sangat tinggi (> 15%). Pastikan risiko sesuai dengan profil risiko Anda.")
        elif 3 <= d['return_tahunan'] <= 8:
            recommendations.append("Return investasi dalam range konservatif (3-8%), cocok untuk dana darurat.")
        
        return Response({
            "is_valid": is_valid,
            "calculator_type": "emergency_fund",
            "summary": {
                "target_dana": target_user,
                "target_minimum_rekomendasi": target_minimum,
                "target_ideal_rekomendasi": target_ideal,
                "proyeksi_dana_akhir": round(total_dana_akhir, 2),
                "status": "Sesuai Strategi" if is_valid else "Perlu Penyesuaian"
            },
            "warnings": warnings,
            "recommendations": recommendations
        })

def validate_child_education(self, data):
        """Validasi strategi Pendidikan Anak"""
        serializer = PendidikanAnakSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        tahun_sampai_kuliah = d['usia_anak_masuk_kuliah'] - d['usia_anak_sekarang']
        
        # Hitung biaya kuliah di masa depan dengan inflasi
        r_inflasi = d['inflasi_pendidikan'] / 100
        biaya_per_tahun_future = d['biaya_kuliah_saat_ini_per_tahun'] * math.pow(1 + r_inflasi, tahun_sampai_kuliah)
        total_biaya_kuliah = biaya_per_tahun_future * d['lama_kuliah_tahun']
        
        # Proyeksi dana dengan investasi
        r_monthly = (d['return_investasi'] / 100) / 12
        n_months = tahun_sampai_kuliah * 12
        
        fv_dana = d['dana_saat_ini'] * math.pow(1 + r_monthly, n_months)
        if r_monthly > 0:
            fv_investasi = d['investasi_bulanan'] * ((math.pow(1 + r_monthly, n_months) - 1) / r_monthly)
        else:
            fv_investasi = d['investasi_bulanan'] * n_months
            
        total_dana_akhir = fv_dana + fv_investasi
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Validasi waktu persiapan
        if tahun_sampai_kuliah < 1:
            warnings.append("Waktu persiapan terlalu singkat (< 1 tahun). Strategi investasi agresif diperlukan.")
            is_valid = False
        elif tahun_sampai_kuliah < 5:
            recommendations.append("Waktu persiapan cukup singkat. Pertimbangkan alokasi di instrumen rendah risiko.")
        else:
            recommendations.append("Waktu persiapan cukup panjang. Anda bisa memanfaatkan compound interest dengan baik.")
        
        # Validasi inflasi pendidikan
        if d['inflasi_pendidikan'] < 5:
            warnings.append("Inflasi pendidikan yang Anda masukkan terlalu rendah. Rata-rata inflasi pendidikan 10-15% per tahun.")
            recommendations.append("Pertimbangkan inflasi pendidikan 10-15% untuk proyeksi lebih realistis.")
        
        # Validasi kecukupan dana
        if total_dana_akhir < total_biaya_kuliah:
            kekurangan = total_biaya_kuliah - total_dana_akhir
            tambahan_per_bulan = kekurangan / n_months if n_months > 0 else kekurangan
            warnings.append(f"Proyeksi dana Anda kurang Rp {kekurangan:,.0f} dari target.")
            recommendations.append(f"Tambahkan investasi bulanan sebesar Rp {tambahan_per_bulan:,.0f}")
            is_valid = False
        else:
            surplus = total_dana_akhir - total_biaya_kuliah
            recommendations.append(f"Proyeksi dana mencukupi dengan surplus Rp {surplus:,.0f}. Excellent!")
        
        # Validasi return investasi
        if d['return_investasi'] < 8:
            warnings.append("Return investasi rendah untuk tujuan jangka panjang. Pertimbangkan instrumen ekuitas/reksadana saham.")
        elif d['return_investasi'] > 20:
            warnings.append("Return investasi sangat tinggi. Pastikan Anda memahami risikonya.")
        
        return Response({
            "is_valid": is_valid,
            "calculator_type": "child_education",
            "summary": {
                "tahun_sampai_kuliah": tahun_sampai_kuliah,
                "total_biaya_kuliah_future": round(total_biaya_kuliah, 2),
                "biaya_per_tahun_future": round(biaya_per_tahun_future, 2),
                "proyeksi_dana_akhir": round(total_dana_akhir, 2),
                "gap": round(total_biaya_kuliah - total_dana_akhir, 2),
                "status": "Sesuai Strategi" if is_valid else "Perlu Penyesuaian"
            },
            "warnings": warnings,
            "recommendations": recommendations
        })

def validate_marriage(self, data):
        """Validasi strategi Pernikahan"""
        serializer = MenikahSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        n_months = d['tahun_menuju_menikah'] * 12
        r_monthly = (d['return_tahunan'] / 100) / 12
        
        fv_dana = d['dana_saat_ini'] * math.pow(1 + r_monthly, n_months)
        if r_monthly > 0:
            fv_investasi = d['investasi_bulanan'] * ((math.pow(1 + r_monthly, n_months) - 1) / r_monthly)
        else:
            fv_investasi = d['investasi_bulanan'] * n_months
            
        total_dana_akhir = fv_dana + fv_investasi
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Validasi waktu persiapan
        if d['tahun_menuju_menikah'] < 1:
            warnings.append("Waktu persiapan sangat singkat (< 1 tahun). Fokus pada saving, bukan investasi berisiko.")
            is_valid = False
        elif d['tahun_menuju_menikah'] <= 2:
            recommendations.append("Waktu persiapan pendek. Gunakan instrumen low-risk seperti deposito atau money market.")
        
        # Validasi kecukupan dana
        if total_dana_akhir < d['target_biaya_menikah']:
            kekurangan = d['target_biaya_menikah'] - total_dana_akhir
            persentase_kekurangan = (kekurangan / d['target_biaya_menikah']) * 100
            warnings.append(f"Dana kurang Rp {kekurangan:,.0f} ({persentase_kekurangan:.1f}%)")
            
            if n_months > 0:
                tambahan_per_bulan = kekurangan / n_months
                recommendations.append(f"Tambahkan investasi Rp {tambahan_per_bulan:,.0f}/bulan atau kurangi target biaya.")
            is_valid = False
        else:
            surplus = total_dana_akhir - d['target_biaya_menikah']
            recommendations.append(f"Dana mencukupi dengan surplus Rp {surplus:,.0f} untuk biaya tak terduga.")
        
        # Validasi return investasi berdasarkan horizon
        if d['tahun_menuju_menikah'] <= 2 and d['return_tahunan'] > 10:
            warnings.append("Return terlalu tinggi untuk jangka pendek. Pertimbangkan instrumen lebih stabil.")
        
        return Response({
            "is_valid": is_valid,
            "calculator_type": "marriage",
            "summary": {
                "target_biaya": d['target_biaya_menikah'],
                "proyeksi_dana_akhir": round(total_dana_akhir, 2),
                "gap": round(d['target_biaya_menikah'] - total_dana_akhir, 2),
                "waktu_persiapan_bulan": n_months,
                "status": "Sesuai Strategi" if is_valid else "Perlu Penyesuaian"
            },
            "warnings": warnings,
            "recommendations": recommendations
        })

def validate_vehicle(self, data):
        """Validasi strategi Kendaraan"""
        serializer = KendaraanSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        dp_amount = d['harga_kendaraan'] * (d['dp_persen'] / 100)
        r_monthly = (d['return_tahunan'] / 100) / 12
        n = d['lama_investasi_bulan']
        
        fv_dana = d['dana_saat_ini'] * math.pow(1 + r_monthly, n)
        if r_monthly > 0:
            fv_investasi = d['investasi_bulanan'] * ((math.pow(1 + r_monthly, n) - 1) / r_monthly)
        else:
            fv_investasi = d['investasi_bulanan'] * n
            
        total_dana_akhir = fv_dana + fv_investasi
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Validasi DP
        if d['dp_persen'] < 20:
            warnings.append("DP terlalu rendah (< 20%). Cicilan bulanan akan tinggi dan bunga lebih besar.")
            recommendations.append("Usahakan DP minimal 30% untuk mengurangi beban cicilan.")
        elif d['dp_persen'] >= 30:
            recommendations.append("DP Anda sudah bagus (≥ 30%). Ini akan mengurangi beban bunga.")
        
        # Validasi kecukupan dana
        if total_dana_akhir < dp_amount:
            kekurangan = dp_amount - total_dana_akhir
            tambahan_per_bulan = kekurangan / n if n > 0 else kekurangan
            warnings.append(f"Dana kurang Rp {kekurangan:,.0f} untuk DP.")
            recommendations.append(f"Tambah investasi Rp {tambahan_per_bulan:,.0f}/bulan atau perpanjang waktu investasi.")
            is_valid = False
        else:
            surplus = total_dana_akhir - dp_amount
            recommendations.append(f"Dana DP tercapai dengan surplus Rp {surplus:,.0f}.")
        
        # Validasi waktu investasi
        if n < 6:
            warnings.append("Waktu investasi terlalu singkat (< 6 bulan). Gunakan instrumen liquid dan low-risk.")
        
        return Response({
            "is_valid": is_valid,
            "calculator_type": "vehicle",
            "summary": {
                "harga_kendaraan": d['harga_kendaraan'],
                "dp_amount": round(dp_amount, 2),
                "proyeksi_dana_akhir": round(total_dana_akhir, 2),
                "gap": round(dp_amount - total_dana_akhir, 2),
                "waktu_investasi_bulan": n,
                "status": "Sesuai Strategi" if is_valid else "Perlu Penyesuaian"
            },
            "warnings": warnings,
            "recommendations": recommendations
        })

def validate_kpr(self, data):
        """Validasi strategi KPR"""
        serializer = SimulasiKPRSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        dp_amount = d['harga_properti'] * (d['dp_persen'] / 100)
        loan_amount = d['harga_properti'] - dp_amount
        
        # Hitung cicilan periode fix
        r_fix_monthly = (d['bunga_fix'] / 100) / 12
        if r_fix_monthly > 0:
            cicilan_fix = loan_amount * (r_fix_monthly * math.pow(1 + r_fix_monthly, d['tenor_bulan'])) / \
                        (math.pow(1 + r_fix_monthly, d['tenor_bulan']) - 1)
        else:
            cicilan_fix = loan_amount / d['tenor_bulan']
        
        # Hitung cicilan periode floating (estimasi)
        r_float_monthly = (d['bunga_floating'] / 100) / 12
        remaining_months = d['tenor_bulan'] - d['periode_fix_bulan']
        
        # Outstanding setelah periode fix
        outstanding = loan_amount
        for i in range(d['periode_fix_bulan']):
            interest = outstanding * r_fix_monthly
            principal = cicilan_fix - interest
            outstanding -= principal
        
        if r_float_monthly > 0 and remaining_months > 0:
            cicilan_floating = outstanding * (r_float_monthly * math.pow(1 + r_float_monthly, remaining_months)) / \
                        (math.pow(1 + r_float_monthly, remaining_months) - 1)
        else:
            cicilan_floating = outstanding / remaining_months if remaining_months > 0 else 0
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Validasi DP
        if d['dp_persen'] < 20:
            warnings.append("DP terlalu rendah (< 20%). Bank mungkin menolak atau bunga lebih tinggi.")
            is_valid = False
        elif d['dp_persen'] < 30:
            recommendations.append("DP sudah cukup, tapi idealnya 30% untuk bunga lebih rendah.")
        
        # Validasi rasio cicilan terhadap penghasilan
        rasio_cicilan_fix = (cicilan_fix / d['penghasilan_bulanan']) * 100
        rasio_cicilan_floating = (cicilan_floating / d['penghasilan_bulanan']) * 100
        
        if rasio_cicilan_fix > 30:
            warnings.append(f"Cicilan fix ({rasio_cicilan_fix:.1f}% penghasilan) melebihi 30%. Risiko finansial tinggi!")
            recommendations.append("Turunkan harga properti, tingkatkan DP, atau perpanjang tenor.")
            is_valid = False
        elif rasio_cicilan_fix > 25:
            warnings.append(f"Cicilan fix ({rasio_cicilan_fix:.1f}% penghasilan) cukup tinggi. Hati-hati dengan pengeluaran lain.")
        
        if rasio_cicilan_floating > 35:
            warnings.append(f"Cicilan floating ({rasio_cicilan_floating:.1f}% penghasilan) sangat tinggi! Siapkan dana cadangan.")
            is_valid = False
        
        # Validasi bunga
        if d['bunga_floating'] > d['bunga_fix'] + 2:
            warnings.append(f"Kenaikan bunga floating terlalu tinggi (+{d['bunga_floating'] - d['bunga_fix']:.1f}%). Pertimbangkan fixed rate lebih lama.")
        
        # Validasi tenor
        if d['tenor_bulan'] > 240:
            warnings.append("Tenor > 20 tahun berarti total bunga sangat besar. Pertimbangkan tenor lebih pendek jika mampu.")
        elif d['tenor_bulan'] < 60:
            recommendations.append("Tenor pendek berarti cicilan tinggi tapi total bunga lebih kecil. Bagus jika cash flow kuat.")
        
        return Response({
            "is_valid": is_valid,
            "calculator_type": "kpr",
            "summary": {
                "harga_properti": d['harga_properti'],
                "dp_amount": round(dp_amount, 2),
                "loan_amount": round(loan_amount, 2),
                "cicilan_fix": round(cicilan_fix, 2),
                "cicilan_floating": round(cicilan_floating, 2),
                "rasio_cicilan_fix_persen": round(rasio_cicilan_fix, 2),
                "rasio_cicilan_floating_persen": round(rasio_cicilan_floating, 2),
                "status": "Sesuai Strategi" if is_valid else "Perlu Penyesuaian"
            },
            "warnings": warnings,
            "recommendations": recommendations
        })

def validate_pension(self, data):
        """Validasi strategi Pensiun"""
        serializer = DanaPensiunSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        tahun_sampai_pensiun = d['usia_pensiun'] - d['usia_sekarang']
        
        # Hitung kebutuhan di masa pensiun dengan inflasi
        r_inflasi = d['inflasi_tahunan'] / 100
        pengeluaran_saat_pensiun = d['pengeluaran_bulanan_saat_ini'] * math.pow(1 + r_inflasi, tahun_sampai_pensiun)
        kebutuhan_per_tahun = pengeluaran_saat_pensiun * 12
        total_kebutuhan_pensiun = kebutuhan_per_tahun * d['lama_pensiun_tahun']
        
        # Proyeksi akumulasi dana
        r_monthly = (d['return_investasi'] / 100) / 12
        n_months = tahun_sampai_pensiun * 12
        
        fv_dana = d['dana_saat_ini'] * math.pow(1 + r_monthly, n_months)
        if r_monthly > 0:
            fv_investasi = d['investasi_bulanan'] * ((math.pow(1 + r_monthly, n_months) - 1) / r_monthly)
        else:
            fv_investasi = d['investasi_bulanan'] * n_months
            
        total_dana_akhir = fv_dana + fv_investasi
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Validasi waktu persiapan
        if tahun_sampai_pensiun < 5:
            warnings.append("Waktu persiapan sangat singkat (< 5 tahun). Perlu strategi agresif atau kurangi ekspektasi.")
            is_valid = False
        elif tahun_sampai_pensiun < 10:
            recommendations.append("Waktu persiapan cukup singkat. Maksimalkan investasi bulanan.")
        else:
            recommendations.append("Waktu persiapan cukup panjang. Manfaatkan compound interest dengan konsisten.")
        
        # Validasi inflasi
        if d['inflasi_tahunan'] < 4:
            warnings.append("Inflasi terlalu rendah. Rata-rata inflasi Indonesia 4-6% per tahun.")
            recommendations.append("Gunakan asumsi inflasi minimal 5% untuk proyeksi realistis.")
        
        # Validasi return investasi
        if d['return_investasi'] < 8:
            warnings.append("Return investasi rendah untuk tujuan jangka panjang. Pertimbangkan portofolio lebih agresif.")
        elif d['return_investasi'] > 15:
            warnings.append("Return investasi sangat tinggi. Pastikan sesuai dengan profil risiko Anda.")
        
        # Validasi kecukupan dana
        if total_dana_akhir < total_kebutuhan_pensiun:
            kekurangan = total_kebutuhan_pensiun - total_dana_akhir
            persentase_kekurangan = (kekurangan / total_kebutuhan_pensiun) * 100
            warnings.append(f"Dana pensiun kurang Rp {kekurangan:,.0f} ({persentase_kekurangan:.1f}%)")
            
            tambahan_per_bulan = kekurangan / n_months if n_months > 0 else kekurangan
            recommendations.append(f"Tambahkan investasi Rp {tambahan_per_bulan:,.0f}/bulan")
            recommendations.append("Atau pertimbangkan: pensiun lebih lambat, kurangi gaya hidup, atau cari sumber pendapatan pasif.")
            is_valid = False
        else:
            surplus = total_dana_akhir - total_kebutuhan_pensiun
            persentase_surplus = (surplus / total_kebutuhan_pensiun) * 100
            recommendations.append(f"Dana pensiun mencukupi dengan surplus Rp {surplus:,.0f} ({persentase_surplus:.1f}%). Excellent!")
        
        # Validasi lama pensiun
        if d['lama_pensiun_tahun'] < 15:
            warnings.append("Durasi pensiun terlalu pendek. Rata-rata orang hidup 20-30 tahun setelah pensiun.")
            recommendations.append("Pertimbangkan minimal 20 tahun untuk proyeksi lebih aman.")
        
        return Response({
            "is_valid": is_valid,
            "calculator_type": "pension",
            "summary": {
                "tahun_sampai_pensiun": tahun_sampai_pensiun,
                "pengeluaran_bulanan_saat_pensiun": round(pengeluaran_saat_pensiun, 2),
                "total_kebutuhan_pensiun": round(total_kebutuhan_pensiun, 2),
                "proyeksi_dana_akhir": round(total_dana_akhir, 2),
                "gap": round(total_kebutuhan_pensiun - total_dana_akhir, 2),
                "status": "Sesuai Strategi" if is_valid else "Perlu Penyesuaian"
            },
            "warnings": warnings,
            "recommendations": recommendations
        })

def validate_gold(self, data):
        """Validasi strategi Emas"""
        serializer = KalkulatorEmasSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Validasi harga emas (harga wajar emas saat ini sekitar 1-1.5 juta/gram)
        harga_wajar_min = 900000
        harga_wajar_max = 1600000
        
        if d['harga_emas_per_gram'] < harga_wajar_min:
            warnings.append(f"Harga emas terlalu rendah (< Rp {harga_wajar_min:,.0f}/gram). Pastikan data akurat.")
            is_valid = False
        elif d['harga_emas_per_gram'] > harga_wajar_max:
            warnings.append(f"Harga emas sangat tinggi (> Rp {harga_wajar_max:,.0f}/gram). Pertimbangkan timing pembelian.")
        
        # Kalkulasi berdasarkan mode
        if d['mode'] == 'emas_ke_rupiah':
            jumlah_gram = d.get('jumlah_gram', 0)
            hasil_rupiah = jumlah_gram * d['harga_emas_per_gram']
            
        def validate_gold(self, data):"""Validasi strategi Emas"""
        serializer = KalkulatorEmasSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        
        is_valid = True
        warnings = []
        recommendations = []
        
        # Asumsi range harga emas per gram yang "wajar" (boleh kamu adjust)
        harga_wajar_min = 900_000
        harga_wajar_max = 1_600_000
        
        # Validasi harga emas
        if d['harga_emas_per_gram'] < harga_wajar_min:
            warnings.append(
                f"Harga emas terlalu rendah (< Rp {harga_wajar_min:,.0f}/gram). "
                "Pastikan data harga emas yang digunakan sudah update dan akurat."
            )
            is_valid = False
        elif d['harga_emas_per_gram'] > harga_wajar_max:
            warnings.append(
                f"Harga emas sangat tinggi (> Rp {harga_wajar_max:,.0f}/gram). "
                "Pertimbangkan timing pembelian agar tidak di puncak harga."
            )

        summary = {
            "mode": d["mode"],
            "harga_emas_per_gram": d["harga_emas_per_gram"],
        }

        # Kalkulasi berdasarkan mode
        if d['mode'] == 'emas_ke_rupiah':
            jumlah_gram = d.get('jumlah_gram', 0)
            hasil_rupiah = jumlah_gram * d['harga_emas_per_gram']

            if jumlah_gram <= 0:
                warnings.append("Jumlah gram emas harus lebih dari 0.")
                is_valid = False
            elif jumlah_gram < 1:
                recommendations.append(
                    "Jumlah emas yang dimiliki masih relatif kecil (< 1 gram). "
                    "Untuk tujuan jangka panjang, pertimbangkan akumulasi rutin."
                )
            elif jumlah_gram >= 10:
                recommendations.append(
                    "Kepemilikan emas Anda sudah cukup signifikan (≥ 10 gram). "
                    "Pastikan juga ada diversifikasi ke instrumen lain."
                )

            summary.update({
                "jumlah_gram": jumlah_gram,
                "nilai_rupiah": round(hasil_rupiah, 2),
            })

        else:  # rupiah_ke_emas
            jumlah_rupiah = d.get('jumlah_rupiah', 0)
            if jumlah_rupiah <= 0:
                warnings.append("Jumlah rupiah untuk membeli emas harus lebih dari 0.")
                is_valid = False

            total_gram = (
                jumlah_rupiah / d['harga_emas_per_gram']
                if d['harga_emas_per_gram'] > 0 else 0
            )

            if jumlah_rupiah < 500_000:
                recommendations.append(
                    "Nominal pembelian emas relatif kecil. "
                    "Pertimbangkan pembelian rutin (dollar cost averaging) setiap bulan."
                )
            elif jumlah_rupiah >= 10_000_000:
                recommendations.append(
                    "Nominal pembelian emas cukup besar. "
                    "Pastikan penyimpanan aman (brankas, safe deposit box, atau emas digital terpercaya)."
                )

            summary.update({
                "jumlah_rupiah": jumlah_rupiah,
                "estimasi_gram": round(total_gram, 4),
            })

        # Beberapa rekomendasi umum soal emas (tanpa 'cukup/tidak cukup')
        recommendations.append(
            "Emas cocok untuk tujuan lindung nilai (hedging) dan jangka menengah–panjang, "
            "bukan untuk kebutuhan jangka sangat pendek."
        )
        recommendations.append(
            "Idealnya emas hanya sebagian dari portofolio (misal 10–20%), "
            "bukan 100% aset investasi."
        )

        return Response({
            "is_valid": is_valid,
            "calculator_type": "gold",
            "summary": summary,
            # sengaja tidak pakai 'Cukup/Tidak Cukup' di emas, hanya valid/need adjustment
            "status": "Strategi Layak" if is_valid else "Perlu Peninjauan Ulang",
            "warnings": warnings,
            "recommendations": recommendations,
        })
