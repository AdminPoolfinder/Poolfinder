from run import app
from extensions import db
from app.models import Kolam
import csv

def to_float(val):
    try:
        return float(str(val).replace(',', '.'))
    except:
        return 0

# ✅ khusus harga range: 10000-15000 → jadi rata-rata
def parse_harga(val):
    try:
        val = str(val).replace(' ', '')
        if '-' in val:
            low, high = val.split('-')
            return (float(low) + float(high)) / 2
        return float(val)
    except:
        return 0

with app.app_context():
    with open('dataset kolam malang_final.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        total = 0

        for row in reader:
            # normalize key
            row = {k.strip().lower(): v for k, v in row.items()}

            data = Kolam(
                # ✅ IDENTITAS
                nama=row.get('nama kolam'),
                jenis=row.get('jenis'),

                # ✅ LOKASI
                alamat_lengkap=row.get('alamat lengkap'),
                kecamatan=row.get('kecamatan'),
                lokasi=row.get('lokasi'),

                # ✅ SPESIFIKASI
                panjang=row.get('panjang'),  # tetap string
                kedalaman=row.get('kedalaman'),
                jalur=row.get('jalur'),      # string sesuai DB
                papan_start=row.get('papan start'),
                pace_clock=row.get('pace clock'),

                # ✅ HARGA & RATING
                harga=parse_harga(row.get('harga tiket')),
                rating=to_float(row.get('rating')),

                # ✅ FITUR
                fasilitas=row.get('fasilitas'),
                kebersihan=row.get('kebersihan'),

                # ✅ TAMBAHAN (BARU)
                air_hangat=row.get('air hangat'),
                link_google_maps=row.get('link gogle maps'),

                # ✅ DEFAULT (biar aman)
                skor_harga=0,
                skor_rating=0
            )

            db.session.add(data)
            total += 1

        db.session.commit()

        print(f"✅ IMPORT BERHASIL: {total} data")