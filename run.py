from flask import Flask
from extensions import db, mail # Ambil db dari extensions
from app.models import Admin, Kolam # Import models sekarang aman
from app.routes import main, auth
from flask_mail import Mail
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__, 
            template_folder="app/templates", 
            static_folder="app/static")

# Konfigurasi MySQL
import os

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'skripsi_aquatic_malang_2026'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adminkolam@gmail.com'
app.config['MAIL_PASSWORD'] = 'hrfhlrjfpntbzoyo'
app.config['MAIL_DEFAULT_SENDER'] = 'adminkolam@gmail.com'

mail.init_app(app)
# Hubungkan db ke app
db.init_app(app)

app.register_blueprint(main)
app.register_blueprint(auth)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Logika buat admin default tetap di sini...
        if not Admin.query.filter_by(username='admin_pool').first():
            admin_baru = Admin(username='admin_pool', password='password123')
            db.session.add(admin_baru)
            db.session.commit()
            print("✅ Database Sinkron & Admin Ready!")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))