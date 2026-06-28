from datetime import datetime
from extensions import db


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # email
    password = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'



class Kolam(db.Model):
    __tablename__ = 'kolam'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    jenis = db.Column(db.String(100))
    harga = db.Column(db.Float)
    kebersihan = db.Column(db.String(100))
    fasilitas = db.Column(db.String(255))
    kedalaman = db.Column(db.String(50))
    skor_harga = db.Column(db.Float, default=0)
    skor_rating = db.Column(db.Float, default=0)
    alamat_lengkap = db.Column(db.Text)
    kecamatan = db.Column(db.String(100))
    panjang = db.Column(db.String(50))
    jalur = db.Column(db.String(50))
    papan_start = db.Column(db.String(50))
    pace_clock = db.Column(db.String(50))
    lokasi = db.Column(db.String(100))
    rating = db.Column(db.Float)

    # ✅ TAMBAHAN
    air_hangat = db.Column(db.String(20))
    link_google_maps = db.Column(db.Text)
    def to_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "jenis": self.jenis,
            "harga": self.harga,
            "kebersihan": self.kebersihan,
            "fasilitas": self.fasilitas,
            "kedalaman": self.kedalaman,
            "skor_harga": self.skor_harga,
            "skor_rating": self.skor_rating,
            "alamat_lengkap": self.alamat_lengkap,
            "kecamatan": self.kecamatan,
            "panjang": self.panjang,
            "jalur": self.jalur,
            "papan_start": self.papan_start,
            "pace_clock": self.pace_clock,
            "lokasi": self.lokasi,
            "rating": self.rating,
            "air_hangat": self.air_hangat,
            "link_google_maps": self.link_google_maps
        }
    
    def __repr__(self):
        return f"<Kolam {self.nama}>"
    
    

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    kolam_id = db.Column(db.Integer, db.ForeignKey('kolam.id'))
    username = db.Column(db.String(50), default='Anonymous')
    rating = db.Column(db.Float)
    komentar = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)