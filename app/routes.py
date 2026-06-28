# TAMBAHKAN session DAN flash:
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.logic.scoring import calculate_score
from app.logic.ranking import rank_data # Tetap import jika dibutuhkan di fungsi lain
import csv
from extensions import mail
from app.models import Admin, Kolam, Review, User # Pastikan Review diimport kalau dipakai di submit_rating
from extensions import db
import pandas as pd
import urllib.parse
import os
import re
from io import TextIOWrapper
from werkzeug.security import generate_password_hash, check_password_hash
from scipy.stats import spearmanr
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# =========================
# LOAD CSV
# =========================
def load_csv():
    data = []
    try:
        with open('dataset-kolam.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("Error: File dataset-kolam.csv tidak ditemukan!")
    return data

def to_float(val):
    try:
        return float(str(val).replace(',', '.'))
    except:
        return 0

def to_int(val):
    try:
        return int(val)
    except:
        return 0


@main.route('/admin/import_csv', methods=['POST'])
def import_csv():
    file = request.files.get('file_csv')

    if not file:
        flash('File tidak ditemukan!', 'danger')
        return redirect(url_for('main.admin_kolam'))

    csv_file = TextIOWrapper(file.stream, encoding='utf-8')
    reader = csv.DictReader(csv_file)

    count = 0

    try:
        for row in reader:
            # 🔥 WAJIB DI DALAM LOOP
            row = {k.strip().lower(): v for k, v in row.items()}

            new_kolam = Kolam(
                nama=row.get('nama kolam'),
                alamat_lengkap=row.get('alamat lengkap'),
                kecamatan=row.get('kecamatan'),
                panjang=to_float(row.get('panjang')),
                kedalaman=row.get('kedalaman'),
                jalur=to_int(row.get('jalur')),
                papan_start=row.get('papan start'),
                pace_clock=row.get('pace clock'),
                harga=to_float(row.get('harga')),
                fasilitas=row.get('fasilitas'),
                lokasi=row.get('lokasi'),
                kebersihan=row.get('kebersihan'),
                rating=to_float(row.get('rating'))
            )

            db.session.add(new_kolam)
            count += 1  # 🔥 HARUS SEJAJAR dengan add()

        db.session.commit()
        print(f"✅ BERHASIL IMPORT {count} DATA")
        flash(f'{count} data berhasil diimport!', 'success')

    except Exception as e:
        db.session.rollback()
        print("❌ ERROR:", e)
        flash(f'Gagal import: {str(e)}', 'danger')

    return redirect(url_for('main.admin_kolam'))





@main.route('/')
def index():
    return render_template('user/index.html')

# =========================
# USER
# =========================
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['email'] = user.email

            return redirect(url_for('main.beranda'))
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('user/login.html')



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # validasi sederhana
        if not username:
            return "Username tidak boleh kosong"

        # hash password
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('user/register.html')




@auth.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))




# =========================
# BERANDA
# =========================
@main.route('/beranda')
def beranda():

    return render_template('user/beranda.html')

# =========================
# PROCESS (SOLUSI FINAL FIXED)
# =========================
@main.route('/process', methods=['POST'])
def process():
    user_profile = request.form.get('pool_category', 'basic').strip().lower()

    pools = Kolam.query.all()
    alternatives = []

    def clean_to_float(value):
        if value is None or value == '':
            return 0.0
        try:
            match = re.search(r"[-+]?\d*\.\d+|\d+", str(value))
            return float(match.group()) if match else 0.0
        except:
            return 0.0

    def safe_int(value, default=0):
        try:
            return int(value)
        except:
            return default

    def safe_float(value, default=0.0):
        try:
            return float(value)
        except:
            return default

    # =========================
    # BUILD DATA
    # =========================
    for p in pools:
        alternatives.append({
            "name": p.nama,

            "harga": clean_to_float(p.harga),
            "panjang": clean_to_float(p.panjang),
            "kedalaman": clean_to_float(p.kedalaman),
            "jalur": clean_to_float(p.jalur),

            "papan_start": (p.papan_start or '-').lower(),
            "pace_clock": (p.pace_clock or '-').lower(),
            "kebersihan": p.kebersihan or '-',
            "fasilitas": p.fasilitas or '-',
            "air_hangat": p.air_hangat or '-',
            "rating": clean_to_float(p.rating),
            "kecamatan": p.kecamatan,
            "link_google_maps": p.link_google_maps, 
        })

    # =========================
    # IMPORTANT FIX: user_input HARUS SELALU FRESH
    # =========================
    def normalize(val):
        try:
            val = float(val)
            return float(val) / 5.0
        except:
            return 0.0
    if user_profile == "basic":
        user_input = {
            "harga": safe_float(request.form.get("harga_basic")),
            "kebersihan": safe_float(request.form.get("kebersihan")),
            "fasilitas": safe_float(request.form.get("fasilitas")),
            "air_hangat": safe_float(request.form.get("suhu")),
            "rating": safe_float(request.form.get("rating_basic")),
        }
    else:
        user_input = {
            "harga": safe_float(request.form.get("harga")),
            "kedalaman": safe_float(request.form.get("kedalaman")),
            "panjang": safe_float(request.form.get("panjang")),
            "jalur": safe_int(request.form.get("jalur")),
            "papan_start": safe_int(request.form.get("start")),
            "pace_clock": safe_int(request.form.get("pace")),
            "rating": safe_float(request.form.get("rating")),
        }

    # =========================
    # DEBUG (WAJIB UNTUK CEK BUG)
    # =========================
    print("PROFILE:", user_profile)
    print("USER INPUT:", user_input)

    scores_dict = calculate_score(
        alternatives,
        user_input=user_input,
        preference_profile=user_profile
    )

    ranking_result = sorted(
        [
            {**alt, "score": scores_dict.get(alt["name"], 0)}
            for alt in alternatives
        ],
        key=lambda x: x["score"],
        reverse=True
    )

    return render_template(
        "result.html",
        ranking=ranking_result,
        profile=user_profile
    )


# =========================
# HALAMAN DAFTAR SEMUA KOLAM
# =========================
@main.route('/daftar-kolam')
def daftar_kolam():
    pools = Kolam.query.all()
    reviews = Review.query.all()

    # mapping review ke kolam
    review_map = {}
    for r in reviews:
        if r.kolam_id not in review_map:
            review_map[r.kolam_id] = []
        review_map[r.kolam_id].append(r)

    # jumlah review
    review_count = {k: len(v) for k, v in review_map.items()}

    return render_template(
        'user/daftar_kolam.html',
        pools=pools,
        review_map=review_map,
        review_count=review_count
    )



# =========================
# RATING
# =========================

@main.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.get_json()

    try:
        pool_id = int(data.get('pool_id'))
        rating_value = float(data.get('rating'))
        isi_komentar = data.get('komentar', '')

        pool = Kolam.query.get(pool_id)
        if not pool:
            return jsonify({"success": False, "message": "Kolam tidak ditemukan"}), 404

        # =========================
        # HITUNG JUMLAH REVIEW LAMA
        # =========================
        review_count = Review.query.filter_by(kolam_id=pool_id).count()

        rating_lama = pool.rating or 0.0

        # =========================
        # HITUNG RATING BARU (INCREMENTAL)
        # =========================
        new_avg = ((rating_lama * review_count) + rating_value) / (review_count + 1)

        # =========================
        # SIMPAN KE KOLOM rating
        # =========================
        pool.rating = round(new_avg, 1)

        # =========================
        # SIMPAN REVIEW
        # =========================
        new_review = Review(
            kolam_id=pool_id,
            rating=rating_value,
            komentar=isi_komentar
        )

        db.session.add(new_review)
        db.session.commit()

        return jsonify({
            "success": True,
            "new_rating": pool.rating
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})




@main.route('/tentang', methods=['GET', 'POST'])
def tentang():
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        pesan = request.form.get('pesan')

        # Format pesan WhatsApp
        text = f"""
Halo Aquatic Malang 👋

Nama: {nama}
Email: {email}

Pesan:
{pesan}
        """

        # Encode URL
        encoded_text = urllib.parse.quote(text)

        # Ganti nomor WA kamu
        wa_number = "6282338758794"

        # Redirect ke WhatsApp
        wa_url = f"https://wa.me/{wa_number}?text={encoded_text}"
        return redirect(wa_url)

    return render_template('user/tentang.html')

#------------------------------ ADMIN -----------------------------------

# 1. Halaman Login
@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session['admin_logged_in'] = True
            session['admin_username'] = admin.username
            flash('Selamat datang kembali, Admin!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Username atau Password salah!', 'error')

    return render_template('admin/login.html')


@main.route('/admin/switch/<username>')
def switch_admin(username):
    session['admin_username'] = username
    return redirect(url_for('main.admin_dashboard'))



# =========================
# LUPA PASSWORD
# =========================

from datetime import datetime, timedelta
import secrets
from flask_mail import Message


@main.route('/admin/lupa-password', methods=['GET', 'POST'])
def lupa_password():
    if request.method == 'POST':
        email = request.form.get('username')

        admin = Admin.query.filter_by(username=email).first()

        if admin:
            token = secrets.token_urlsafe(32)

            admin.reset_token = token
            admin.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
            db.session.commit()

            reset_link = url_for('main.reset_password', token=token, _external=True)

            msg = Message(
                subject='Reset Password PoolFinder',
                recipients=[email],
                sender='PoolFinder <adminkolam@gmail.com>'  # ✅ FIX penting
            )

            msg.body = "Klik link berikut untuk reset password"
            msg.html = render_template(
                'email/reset_password.html',
                reset_link=reset_link
            )

            # ✅ DEBUG WAJIB
            try:
                mail.send(msg)
                print("✅ EMAIL TERKIRIM")
                flash('Link reset sudah dikirim ke email!', 'success')
            except Exception as e:
                print("❌ ERROR EMAIL:", e)
                flash(f'Gagal kirim email: {e}', 'error')

        else:
            flash('Email tidak ditemukan!', 'error')

    return render_template('admin/lupa_password.html')



from datetime import datetime

@main.route('/admin/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    admin = Admin.query.filter_by(reset_token=token).first()

    if not admin:
        flash('Token tidak valid!', 'error')
        return redirect(url_for('main.admin_login'))

    # 🔥 cek expiry
    if admin.reset_token_expiry and datetime.utcnow() > admin.reset_token_expiry:
        flash('Token sudah kadaluarsa!', 'error')
        return redirect(url_for('main.admin_login'))

    if request.method == 'POST':
        new_password = request.form.get('password')

        admin.password = generate_password_hash(new_password)
        admin.reset_token = None
        admin.reset_token_expiry = None
        db.session.commit()

        flash('Password berhasil direset!', 'success')
        return redirect(url_for('main.admin_login'))

    return render_template('admin/reset_password.html')



@main.route('/test-email')
def test_email():
    msg = Message(
        subject='TEST EMAIL',
        recipients=['EMAIL_KAMU_SENDIRI@gmail.com']
    )
    msg.body = 'INI TEST EMAIL'

    try:
        mail.send(msg)
        return "✅ BERHASIL"
    except Exception as e:
        return f"❌ ERROR: {e}"
    



# =========================
# GET HALAMAN KELOLA USER
# =========================
@main.route('/admin/users')
def admin_users():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))

    admins = Admin.query.all()
    return render_template('admin/user.html', admins=admins)


# =========================
# CREATE ADMIN
# =========================
@main.route('/admin/admin/create', methods=['POST'])
def create_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username & Password wajib diisi', 'error')
        return redirect(url_for('main.admin_users'))

    exist = Admin.query.filter_by(username=username).first()
    if exist:
        flash('Username sudah ada!', 'error')
        return redirect(url_for('main.admin_users'))

    new_admin = Admin(
        username=username,
        password=generate_password_hash(password)
    )

    db.session.add(new_admin)
    db.session.commit()

    flash('Admin berhasil ditambahkan!', 'success')
    return redirect(url_for('main.admin_users'))


# =========================
# UPDATE ADMIN
# =========================
@main.route('/admin/admin/update/<int:id>', methods=['POST'])
def update_admin_user(id):  # ✅ GANTI NAMA
    admin = Admin.query.get_or_404(id)

    username = request.form.get('username')
    password = request.form.get('password')

    admin.username = username

    if password:
        admin.password = generate_password_hash(password)

    db.session.commit()

    flash('Admin berhasil diupdate!', 'success')
    return redirect(url_for('main.admin_users'))


# =========================
# DELETE ADMIN
# =========================
@main.route('/admin/admin/delete/<int:id>', methods=['POST'])
def delete_admin_user(id):
    admin = Admin.query.get_or_404(id)

    db.session.delete(admin)
    db.session.commit()

    flash('Admin berhasil dihapus!', 'success')
    return redirect(url_for('main.admin_users'))




# 2. Logout
@main.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('main.admin_login'))




from sqlalchemy import func
# 3. Dashboard (Statistik)
@main.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    admins = Admin.query.all()
    # Menghitung semua data di tabel Kolam
    total_kolam = Kolam.query.count()
    
    # Menghitung semua data di tabel Review
    total_review = Review.query.count()
    
    # Menghitung rata-rata rating dari tabel Review
    avg_rating_result = db.session.query(func.avg(Review.rating)).scalar() or 0

    return render_template('admin/dashboard.html', 
                        admins=admins,
                       total_kolam=total_kolam, 
                       total_review=total_review, 
                       rata_rata_rating=avg_rating_result)




# 4. Data Kolam
@main.route('/admin/kolam')
def admin_kolam():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    pools = Kolam.query.all() 
        
    return render_template('admin/kolam.html', pools=pools)


# =====================
# TAMBAH DATA
# =====================
@main.route('/admin/tambah_kolam', methods=['POST'])
def tambah_kolam():
    try:
        kolam = Kolam(
            nama=request.form.get('nama'),
            jenis=request.form.get('jenis'),
            harga=float(request.form.get('harga') or 0),
            kebersihan=request.form.get('kebersihan'),
            fasilitas=request.form.get('fasilitas'),
            kedalaman=request.form.get('kedalaman'),

            skor_harga=float(request.form.get('skor_harga') or 0),
            skor_rating=float(request.form.get('skor_rating') or 0),

            alamat_lengkap=request.form.get('alamat_lengkap'),
            kecamatan=request.form.get('kecamatan'),

            panjang=request.form.get('panjang'),
            jalur=request.form.get('jalur'),
            papan_start=request.form.get('papan_start'),
            pace_clock=request.form.get('pace_clock'),
            lokasi=request.form.get('lokasi'),

            rating=float(request.form.get('rating') or 0),

            # ✅ FIELD BARU
            air_hangat=request.form.get('air_hangat'),
            link_google_maps=request.form.get('link_google_maps')
        )

        db.session.add(kolam)
        db.session.commit()

        flash('Data berhasil ditambahkan', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('main.admin_kolam'))


# =====================
# UPDATE DATA
# =====================
@main.route('/admin/update_kolam/<int:id>', methods=['POST'])
def update_kolam(id):
    kolam = Kolam.query.get_or_404(id)

    try:
        kolam.nama = request.form.get('nama')
        kolam.jenis = request.form.get('jenis')
        kolam.harga = float(request.form.get('harga') or 0)
        kolam.kebersihan = request.form.get('kebersihan')
        kolam.rating = float(request.form.get('rating') or 0)

        kolam.kecamatan = request.form.get('kecamatan')
        kolam.alamat_lengkap = request.form.get('alamat_lengkap')

        kolam.fasilitas = request.form.get('fasilitas')
        kolam.kedalaman = request.form.get('kedalaman')

        kolam.panjang = request.form.get('panjang')
        kolam.jalur = request.form.get('jalur')
        kolam.papan_start = request.form.get('papan_start')
        kolam.pace_clock = request.form.get('pace_clock')
        kolam.lokasi = request.form.get('lokasi')

        kolam.skor_harga = float(request.form.get('skor_harga') or 0)
        kolam.skor_rating = float(request.form.get('skor_rating') or 0)

        # ✅ FIELD BARU
        kolam.air_hangat = request.form.get('air_hangat')
        kolam.link_google_maps = request.form.get('link_google_maps')

        db.session.commit()
        flash('Data berhasil diupdate', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error update: {str(e)}', 'error')

    return redirect(url_for('main.admin_kolam'))


# =====================
# HAPUS DATA
# =====================
@main.route('/admin/hapus_kolam/<int:id>', methods=['POST'])
def hapus_kolam(id):
    kolam = Kolam.query.get_or_404(id)

    try:
        db.session.delete(kolam)
        db.session.commit()
        flash('Data berhasil dihapus', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('main.admin_kolam'))

# 5. Rating Masuk
@main.route('/admin/rating')
def admin_rating():
    all_reviews = Review.query.all()
    return render_template('admin/rating.html', reviews=all_reviews)



@main.route('/admin/user')
def admin_user():
    users = User.query.all()
    admins = Admin.query.all()
    return render_template('admin/user.html', users=users, admins=admins)


@main.route('/admin/user/update/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    
    user.username = request.form['username']
    user.email = request.form['email']

    # cek jika password diisi
    if request.form['password']:
        user.password = generate_password_hash(request.form['password'])

    db.session.commit()
    flash('User berhasil diupdate', 'success')
    return redirect(url_for('main.admin_user'))


@main.route('/admin/admin/update/<int:id>', methods=['POST'])
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    
    admin.username = request.form['username']

    if request.form['password']:
        admin.password = generate_password_hash(request.form['password'])

    db.session.commit()
    flash('Admin berhasil diupdate', 'success')
    return redirect(url_for('main.admin_user'))








#--------------------- EVALUASI RANKING ---------------------
def precision_at_k(system_rank, ground_truth, k=5):
    if not system_rank or not ground_truth:
        return 0.0

    system_top_k = system_rank[:k]
    relevant = set(ground_truth)

    hit = 0
    for item in system_top_k:
        if item in relevant:
            hit += 1

    return (hit / k) * 100


# =========================
# CLEAN FLOAT (FIX GLOBAL ERROR)
# =========================
def clean_to_float(value):
    try:
        import re
        match = re.search(r"[-+]?\d*\.\d+|\d+", str(value))
        return float(match.group()) if match else 0.0
    except:
        return 0.0


@main.route('/admin/evaluasi', methods=['GET', 'POST'])
def evaluasi():

    result_atlet = []
    result_basic = []

    precision_atlet = None
    precision_basic = None

    pools = Kolam.query.all()

    alternatives = []

    for p in pools:
        alternatives.append({
            "name": p.nama,
            "harga": clean_to_float(p.harga),
            "panjang": clean_to_float(p.panjang),
            "kedalaman": clean_to_float(p.kedalaman),
            "jalur": clean_to_float(p.jalur),

            "papan_start": p.papan_start or '-',
            "pace_clock": p.pace_clock or '-',
            "kebersihan": p.kebersihan or '-',
            "fasilitas": p.fasilitas or '-',
            "air_hangat": p.air_hangat or '-',

            "rating": clean_to_float(p.rating),
        })

    # =========================
    # USER INPUT
    # =========================
    user_input = {
        "kedalaman": 2,
        "panjang": 25,
        "jalur": 6,
        "harga": 25000,
        "kebersihan": 4,
        "fasilitas": 4,
        "air_hangat": 1
    }

    # =========================
    # HITUNG SYSTEM SCORE
    # =========================
    system_scores_atlet = calculate_score(
        alternatives,
        user_input=user_input,
        preference_profile='atlet'
    )

    system_scores_basic = calculate_score(
        alternatives,
        user_input=user_input,
        preference_profile='basic'
    )

    # =========================
    # SORT HASIL
    # =========================
    result_atlet = sorted(
        system_scores_atlet.items(),
        key=lambda x: x[1],
        reverse=True
    )

    result_basic = sorted(
        system_scores_basic.items(),
        key=lambda x: x[1],
        reverse=True
    )

    system_rank_atlet = [x[0] for x in result_atlet]
    system_rank_basic = [x[0] for x in result_basic]

    # =========================
    # DEFAULT: AUTO GROUND TRUTH (GET)
    # =========================
    ground_truth = sorted(
        alternatives,
        key=lambda x: x['rating'],
        reverse=True
    )
    ground_truth_list = [x['name'] for x in ground_truth]

    # =========================
    # JIKA USER PILIH (POST)
    # =========================
    if request.method == 'POST':
        selected = request.form.getlist('ground_truth')

        # kalau user milih, override ground truth
        if selected:
            ground_truth_list = selected

    # =========================
    # HITUNG PRECISION
    # =========================
    precision_at_k_val = 5

    precision_atlet = precision_at_k(
        system_rank_atlet,
        ground_truth_list,
        k=precision_at_k_val
    )

    precision_basic = precision_at_k(
        system_rank_basic,
        ground_truth_list,
        k=precision_at_k_val
    )

    return render_template(
        'admin/evaluasi.html',
        result_atlet=result_atlet,
        result_basic=result_basic,
        precision_atlet=precision_atlet,
        precision_basic=precision_basic
    )